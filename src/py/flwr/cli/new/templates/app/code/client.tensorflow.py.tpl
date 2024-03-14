"""$project_name: A Flower / TensorFlow app."""

import os

from flwr.cli.flower_toml import load_and_validate_with_defaults
from flwr.client import NumPyClient, ClientApp

from $project_name.task import load_data, load_model


# Make TensorFlow log less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Define Flower Client and client_fn
class FlowerClient(NumPyClient):
    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def get_parameters(self, config):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(self.x_train, self.y_train, epochs=1, batch_size=32, verbose=0)
        return self.model.get_weights(), len(self.x_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        return loss, len(self.x_test), {"accuracy": accuracy}

cfg, *_ = load_and_validate_with_defaults()

def client_fn(cid):
    # Load model and data
    net = load_model()
    engine = cfg["flower"]["engine"]
    num_partitions = 2
    if "simulation" in engine:
        num_partitions = engine["simulation"]["supernode"]["num"]
    x_train, y_train, x_test, y_test = load_data(cid, num_partitions)

    # Return Client instance
    return FlowerClient(net, x_train, y_train, x_test, y_test).to_client()


# Flower ClientApp
app = ClientApp(client_fn)
