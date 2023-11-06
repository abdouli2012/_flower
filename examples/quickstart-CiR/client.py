import warnings
from collections import OrderedDict
from flwr.common import (
    Metrics,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
    bytes_to_ndarray,
)

import flwr as fl
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms import Compose, Normalize, ToTensor
from tqdm import tqdm
from models import AlexNet, Generator
import argparse
from utils_pacs import make_dataloaders

# #############################################################################
# 1. Regular PyTorch pipeline: nn.Module, train, test, and DataLoader
# #############################################################################

warnings.filterwarnings("ignore", category=UserWarning)
DEVICE = torch.device("cpu")
num_classes = 7

parser = argparse.ArgumentParser()
parser.add_argument("--client_idx", type=int, required=True, help="Client index")
args = parser.parse_args()


def train(net1, trainloader, config, epochs):
    """Train the model on the training set."""
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net1.parameters(), lr=0.001, momentum=0.9)
    lambda_reg = 0.5
    lambda_align = 5e-6
    all_labels = torch.arange(num_classes).to(DEVICE)

    z_g, mu_g, log_var_g = (
        torch.tensor(bytes_to_ndarray(config["z_g"])).to(DEVICE),
        torch.tensor(bytes_to_ndarray(config["mu_g"])).to(DEVICE),
        torch.tensor(bytes_to_ndarray(config["log_var_g"])).to(DEVICE),
    )
    for _ in range(epochs):
        for images, labels in tqdm(trainloader):
            optimizer.zero_grad()
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            pred, mu, log_var = net1(images)
            loss_fl = criterion(pred, labels)

            loss_reg = criterion(net1.clf(z_g), all_labels)

            # KL Div
            loss_align = 0.5 * (log_var_g[labels] - log_var - 1) + (
                log_var.exp() + (mu - mu_g[labels]).pow(2)
            ) / (2 * log_var_g[labels].exp())
            loss_align_reduced = loss_align.mean(dim=1).mean()
            loss = loss_fl + lambda_reg * loss_reg + lambda_align * loss_align_reduced
            loss.backward(retain_graph=True)
            optimizer.step()


def test(net1, testloader):
    """Validate the model on the test set."""
    criterion = torch.nn.CrossEntropyLoss()
    correct, loss = 0, 0.0
    with torch.no_grad():
        for images, labels in tqdm(testloader):
            outputs = net1(images.to(DEVICE))[0]
            labels = labels.to(DEVICE)
            loss += criterion(outputs, labels).item()
            correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
    accuracy = correct / len(testloader.dataset)
    return loss, accuracy


def load_data():
    """Load CIFAR-10 (training and test set)."""
    trf = Compose([ToTensor(), Normalize((0.5,), (0.5,))])
    trainset = MNIST("./data", train=True, download=True, transform=trf)
    testset = MNIST("./data", train=False, download=True, transform=trf)
    return DataLoader(trainset, batch_size=64, shuffle=True), DataLoader(testset)


# #############################################################################
# 2. Federation of the pipeline with Flower
# #############################################################################

# Load model and data (simple CNN, MNIST)
net1 = AlexNet(num_classes=num_classes, latent_dim=4096, other_dim=1000).to(DEVICE)
trainloaders, testloaders, valloader = make_dataloaders(batch_size=64)
trainloader = trainloaders[args.client_idx]
testloader = testloaders[args.client_idx]


# Define Flower client
class FlowerClient(fl.client.NumPyClient):
    def __init__(self) -> None:
        super().__init__()
        self.model_len = len(net1.state_dict())

    def get_parameters(self, config):
        n1 = [val.cpu().numpy() for _, val in net1.state_dict().items()]
        return n1

    def set_parameters(self, parameters):
        params_dict1 = zip(net1.state_dict().keys(), parameters)
        state_dict1 = OrderedDict({k: torch.tensor(v) for k, v in params_dict1})

        net1.load_state_dict(state_dict1, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)

        # print(parameters_to_ndarrays(config["dict"])[0].shape())
        train(net1, trainloader, config, epochs=5)
        return self.get_parameters(config={}), len(trainloader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = test(net1, testloader)
        return loss, len(testloader.dataset), {"accuracy": accuracy}


# Start Flower client
fl.client.start_client(
    server_address="127.0.0.1:8080",
    client=FlowerClient().to_client(),
)
