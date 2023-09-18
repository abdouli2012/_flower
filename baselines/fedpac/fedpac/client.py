# pylint: disable=too-many-arguments
"""Defines the Flower Client and a function to instantiate it."""


from collections import OrderedDict
from typing import Callable, Dict, List, Tuple

import flwr as fl
import numpy as np
import torch
from flwr.common.typing import NDArrays, Scalar
from hydra.utils import instantiate
from omegaconf import DictConfig
from torch.utils.data import DataLoader

from fedpac.dataset import load_datasets
from fedpac.models import test, train
from fedpac.utils import get_centroid



class FlowerClient(fl.client.NumPyClient):
    """Standard Flower client for CNN training."""

    def __init__(
        self,
        net: torch.nn.Module,
        trainloader: DataLoader,
        valloader: DataLoader,
        device: torch.device,
        num_epochs: int,
        learning_rate: float,
        lamda: float,

    ):
        self.net = net
        self.trainloader = trainloader
        self.valloader = valloader
        self.device = device
        self.num_epochs = num_epochs
        self.learning_rate = learning_rate
        self.lamda = lamda

    def get_parameters(self, config: Dict[str, Scalar]) -> NDArrays:
        """Returns the parameters of the current net."""
        return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

    def set_parameters(self, parameters: NDArrays) -> None:
        """Changes the parameters of the model using the given ones."""
        params_dict = zip(self.net.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
        self.net.load_state_dict(state_dict, strict=True)


    def get_class_sizes(self, num_classes):
        dataloader = self.trainloader
        sizes = torch.zeros(len(dataloader))
        for images, labels  in dataloader:
            for i in range(num_classes):
                sizes[i] = sizes[i] + (i == labels).sum()
        return sizes


    def get_feature_centroid(self):
        """function to extract feature extractor layers and get average of them"""
        feature_extractors = {}
        model=self.net
        train_data= self.trainloader

        for inputs, labels in train_data:
            inputs, labels = inputs.to(self.device), labels.to(self.device)
            features, outputs = model(inputs)
            feature_extractor = features.clone().detach()
            for i in range(len(labels)):
                if labels[i].item() not in feature_extractors.keys():
                    feature_extractors[labels[i].item()]=[]
                    feature_extractors[labels[i].item()].append(feature_extractor[i,:])
                else:
                    feature_extractors[labels[i].item()] = [feature_extractor[i,:]]

            feature_centroid = get_centroid(feature_extractors)

        return feature_centroid


    def fit(
        self, parameters: NDArrays, config: Dict[str, Scalar]
    ) -> Tuple[NDArrays, int, Dict]:
        """Implements distributed fit function for a given client."""
        self.set_parameters(parameters)
        self.feature_centroid = self.get_feature_centroid()
        self.class_sizes = self.get_class_sizes(self.net.num_classes)
        global_centroid = config["global_centroid"]
        feature_centroid = train(
            self.net,
            self.trainloader,
            self.valloader,
            self.num_epochs,
            self.learning_rate,
            self.device,
            global_centroid,
            self.feature_centroid,
            self.lamda
          )
        return self.get_parameters({}), len(self.trainloader), {'centroid': self.feature_centroid, 'class_sizes': self.class_sizes}

    def evaluate(
        self, parameters: NDArrays, config: Dict[str, Scalar]
    ) -> Tuple[float, int, Dict]:
        """Implements distributed evaluation for a given client."""
        self.set_parameters(parameters)
        loss, accuracy = test(self.net, self.valloader, self.device)
        return float(loss), len(self.valloader), {"accuracy": float(accuracy)}


def gen_client_fn(
    num_clients: int,
    num_rounds: int,
    num_epochs: int,
    trainloaders: List[DataLoader],
    valloaders: List[DataLoader],
    learning_rate: float,
    model: DictConfig,
    lamda: float
) -> Tuple[
    Callable[[str], FlowerClient], DataLoader
]:
    """Generates the client function that creates the Flower Clients.

    Parameters
    ----------
    device : torch.device
        The device on which the the client will train on and test on.
    iid : bool
        The way to partition the data for each client, i.e. whether the data
        should be independent and identically distributed between the clients
        or if the data should first be sorted by labels and distributed by chunks
        to each client (used to test the convergence in a worst case scenario)
    balance : bool
        Whether the dataset should contain an equal number of samples in each class,
        by default True
    num_clients : int
        The number of clients present in the setup
    num_epochs : int
        The number of local epochs each client should run the training for before
        sending it to the server.
    batch_size : int
        The size of the local batches each client trains on.
    learning_rate : float
        The learning rate for the SGD  optimizer of clients.

    Returns
    -------
    Tuple[Callable[[str], FlowerClient], DataLoader]
        A tuple containing the client function that creates Flower Clients and
        the DataLoader that will be used for testing
    """


    def client_fn(cid: str) -> FlowerClient:
        """Create a Flower client representing a single organization."""

        # Load model
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        net = instantiate(model).to(device)

        # Note: each client gets a different trainloader/valloader, so each client
        # will train and evaluate on their own unique data
        trainloader = trainloaders[int(cid)]
        valloader = valloaders[int(cid)]

        # Create a  single Flower client representing a single organization
        return FlowerClient(
            net, trainloader, valloader, device, num_epochs, learning_rate, lamda
        )

    return client_fn
