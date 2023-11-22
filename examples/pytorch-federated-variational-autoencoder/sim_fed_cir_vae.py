import argparse
from collections import OrderedDict
from typing import Dict, Tuple, List
from torch.utils.data import DataLoader

import torch

import flwr as fl
from flwr.common import Metrics, ndarrays_to_parameters
from flwr.common.logger import configure
from flwr.common.typing import Scalar

from utils_mnist import (
    test,
    visualize_gen_image,
    visualize_gmm_latent_representation,
    non_iid_train_iid_test,
    alignment_dataloader,
    train_align,
)
from utils_mnist import VAE
import os
import numpy as np

parser = argparse.ArgumentParser(description="Flower Simulation with PyTorch")

parser.add_argument(
    "--num_cpus",
    type=int,
    default=6,
    help="Number of CPUs to assign to a virtual client",
)
parser.add_argument(
    "--num_gpus",
    type=float,
    default=0.3,
    help="Ratio of GPU memory to assign to a virtual client",
)
parser.add_argument("--num_rounds", type=int, default=10, help="Number of FL rounds.")
parser.add_argument("--identifier", type=str, required=True, help="Name of experiment.")
args = parser.parse_args()

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
NUM_CLIENTS = 5
NUM_CLASSES = 7
IDENTIFIER = args.identifier
if not os.path.exists(IDENTIFIER):
    os.makedirs(IDENTIFIER)


# Flower client, adapted from Pytorch quickstart example
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, trainset, valset, cid):
        self.trainset = trainset
        self.valset = valset
        self.cid = cid

        # Instantiate model
        self.model = VAE()

        # Determine device
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)  # send model to device

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def fit(self, parameters, config):
        set_params(self.model, parameters)
        # Read from config
        batch, epochs = config["batch_size"], config["epochs"]

        # Construct dataloader
        trainloader = DataLoader(self.trainset, batch_size=batch, shuffle=True)

        # Define optimizer
        # optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        # Train
        train_align(
            self.model,
            trainloader,
            optimizer,
            config,
            epochs=epochs,
            device=self.device,
            num_classes=NUM_CLASSES,
        )

        visualize_gen_image(
            self.model,
            DataLoader(self.valset, batch_size=64),
            self.device,
            f'for_client_{self.cid}_train_at_round_{config.get("server_round")}',
            folder=IDENTIFIER,
        )
        visualize_gmm_latent_representation(
            self.model,
            DataLoader(self.valset, batch_size=64),
            self.device,
            f'for_client_{self.cid}_train_at_round_{config.get("server_round")}',
            folder=IDENTIFIER,
        )
        # Return local model and statistics
        return self.get_parameters({}), len(trainloader.dataset), {}

    def evaluate(self, parameters, config):
        set_params(self.model, parameters)

        # Construct dataloader
        valloader = DataLoader(self.valset, batch_size=64)

        # Evaluate
        loss, accuracy = test(self.model, valloader, device=self.device)

        # Return statistics
        return float(loss), len(valloader.dataset), {"accuracy": float(accuracy)}


def get_client_fn(train_partitions, val_partitions):
    """Return a function to construct a client.

    The VirtualClientEngine will exectue this function whenever a client is sampled by
    the strategy to participate.
    """

    def client_fn(cid: str) -> fl.client.Client:
        """Construct a FlowerClient with its own dataset partition."""

        # Extract partition for client with id = cid
        trainset, valset = train_partitions[int(cid)], val_partitions[int(cid)]

        # Create and return client
        return FlowerClient(trainset, valset, cid).to_client()

    return client_fn


def fit_config(server_round: int) -> Dict[str, Scalar]:
    """Return a configuration with static batch size and (local) epochs."""
    config = {
        "epochs": 10,  # Number of local epochs done by clients
        "batch_size": 64,  # Batch size to use by clients during fit()
        "server_round": server_round,
    }
    return config


def set_params(model: torch.nn.ModuleList, params: List[fl.common.NDArrays]):
    """Set model weights from a list of NumPy ndarrays."""
    params_dict = zip(model.state_dict().keys(), params)
    state_dict = OrderedDict({k: torch.from_numpy(v) for k, v in params_dict})
    model.load_state_dict(state_dict, strict=True)


def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    """Aggregation function for (federated) evaluation metrics, i.e. those returned by
    the client's evaluate() method."""
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


def get_evaluate_fn(
    testset,
):
    """Return an evaluation function for centralized evaluation."""

    def evaluate(
        server_round: int, parameters: fl.common.NDArrays, config: Dict[str, Scalar]
    ):
        """Use the entire test set for evaluation."""

        # Determine device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        model = VAE()
        set_params(model, parameters)
        if server_round == 0 or server_round == args.num_rounds:
            with open(f"{IDENTIFIER}/weights_cir_round_{server_round}.npy", "wb") as f:
                np.save(f, np.array(parameters, dtype=object))
        model.to(device)

        testloader = DataLoader(testset, batch_size=64)
        visualize_gen_image(
            model, testloader, device, f"server_eval_{server_round}", folder=IDENTIFIER
        )
        visualize_gmm_latent_representation(
            model, testloader, device, f"server_eval_{server_round}", folder=IDENTIFIER
        )

    return evaluate


def main():
    # Parse input arguments

    configure(identifier=IDENTIFIER, filename=f"logs_{IDENTIFIER}.log")

    # Download dataset and partition it
    trainsets, valsets = non_iid_train_iid_test()
    net = VAE().to(DEVICE)
    gen_net = VAE(encoder_only=True).to(DEVICE)

    n1 = [val.cpu().numpy() for _, val in net.state_dict().items()]
    initial_params = ndarrays_to_parameters(n1)
    n2 = [val.cpu().numpy() for _, val in gen_net.state_dict().items()]
    initial_gen_params = ndarrays_to_parameters(n2)
    samples_per_class = 100
    strategy = fl.server.strategy.FedCiR(
        initial_parameters=initial_params,
        initial_generator_params=initial_gen_params,
        gen_stats=initial_gen_params,
        min_fit_clients=NUM_CLIENTS,
        min_available_clients=NUM_CLIENTS,
        min_evaluate_clients=NUM_CLIENTS,
        on_fit_config_fn=fit_config,
        evaluate_metrics_aggregation_fn=weighted_average,  # Aggregate federated metrics
        evaluate_fn=get_evaluate_fn(valsets[-1]),  # Global evaluation function
        alignment_dataloader=alignment_dataloader(batch_size=samples_per_class * 10),
        lr_g=1e-3,
        steps_g=5,
    )

    # Resources to be assigned to each virtual client
    client_resources = {
        "num_cpus": args.num_cpus,
        "num_gpus": args.num_gpus,
    }

    # Start simulation
    fl.simulation.start_simulation(
        client_fn=get_client_fn(trainsets, valsets),
        num_clients=NUM_CLIENTS,
        client_resources=client_resources,
        config=fl.server.ServerConfig(num_rounds=args.num_rounds),
        strategy=strategy,
    )


if __name__ == "__main__":
    main()
