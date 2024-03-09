"""$project_name: A Flower / NumPy app."""

import flwr
import numpy as np


class FlowerClient(flwr.client.NumPyClient):
    def get_parameters(self, config):
        return [np.ones((1, 1))]

    def fit(self, parameters, config):
        return ([np.ones((1, 1))], 1, {})

    def evaluate(self, parameters, config):
        return float(0.0), 1, {"accuracy": float(1.0)}


def client_fn(cid: str):
    return FlowerClient().to_client()


# Flower ClientApp
app = flwr.client.ClientApp(
    client_fn=client_fn,
)
