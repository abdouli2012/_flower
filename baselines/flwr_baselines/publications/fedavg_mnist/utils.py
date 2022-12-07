"""Contains utility functions for CNN FL on MNIST."""
from collections import OrderedDict
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import torch
from flwr.common import Metrics
from flwr.common.typing import NDArrays, Scalar
from flwr.server.history import History
from torch.utils.data import DataLoader

from flwr_baselines.publications.fedavg_mnist import model


def plot_metric_from_history(
    hist: History, save_plot_path: Path, expected_maximum: float
) -> None:
    """Function to plot from Flower server History.

    Parameters
    ----------
    hist : History
        Object containing evaluation for all rounds.
    save_plot_path : Path
        Folder to save the plot to.
    expected_maximum : float
        The expected maximum accuracy from the original paper.
    """
    rounds, values = zip(*hist.metrics_distributed["accuracy"])
    plt.figure()
    plt.plot(rounds, np.asarray(values) * 100, label="FedAvg")  # Accuracy 0-100%
    # Set expected graph
    plt.axhline(y=expected_maximum, color="r", linestyle="--")
    plt.title("Distributed Validation - MNIST")
    plt.xlabel("Rounds")
    plt.ylabel("Accuracy")
    plt.legend(loc="upper left")
    plt.savefig(Path(save_plot_path) / Path("distributed_metrics.png"))
    plt.close()
    rounds, values = zip(*hist.metrics_centralized["accuracy"])
    plt.figure()
    plt.plot(rounds, np.asarray(values) * 100, label="FedAvg")  # Accuracy 0-100%
    # Set expected graph
    plt.axhline(y=expected_maximum, color="r", linestyle="--")
    plt.title("Centralized Validation - MNIST")
    plt.xlabel("Rounds")
    plt.ylabel("Accuracy")
    plt.legend(loc="upper left")
    plt.savefig(Path(save_plot_path) / Path("centralized_metrics.png"))
    plt.close()


def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    """Aggregation function for weighted average during evaluation.

    Parameters
    ----------
    metrics : List[Tuple[int, Metrics]]
        The list of metrics to aggregate.

    Returns
    -------
    Metrics
        The weighted average metric.
    """
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": int(sum(accuracies)) / int(sum(examples))}


def gen_evaluate_fn(
    testloader: DataLoader, device: torch.device
) -> Callable[
    [int, NDArrays, Dict[str, Scalar]], Optional[Tuple[float, Dict[str, Scalar]]]
]:
    """Generates the function for centralized evaluation.

    Parameters
    ----------
    testloader : DataLoader
        The dataloader to test the model with.
    device : torch.device
        The device to test the model on.

    Returns
    -------
    Callable[ [int, NDArrays, Dict[str, Scalar]], Optional[Tuple[float, Dict[str, Scalar]]] ]
        The centralized evaluation function.
    """

    def evaluate(
        server_round: int, parameters_ndarrays: NDArrays, config: Dict[str, Scalar]
    ) -> Optional[Tuple[float, Dict[str, Scalar]]]:
        # pylint: disable=unused-argument
        """Use the entire CIFAR-10 test set for evaluation."""
        # determine device
        net = model.Net()
        params_dict = zip(net.state_dict().keys(), parameters_ndarrays)
        state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
        net.load_state_dict(state_dict, strict=True)
        net.to(device)

        loss, accuracy = model.test(net, testloader, device=device)
        # return statistics
        return loss, {"accuracy": accuracy}

    return evaluate


def _test_cnn_size_mnist() -> None:
    """Test number of parameters with MNIST-sized inputs."""
    # Prepare
    net = model.Net()
    expected = 1_663_370

    # Execute
    actual = sum([p.numel() for p in net.parameters()])

    # Assert
    assert actual == expected


_test_cnn_size_mnist()
