from sys import argv

import flwr as fl
import tensorflow as tf
from flwr.common import ndarrays_to_parameters
from flwr.server.strategy import FedMedian, FedTrimmedAvg, QFedAvg, FaultTolerantFedAvg, FedAvgM, FedAdam, FedAdagrad, FedYogi

from client import SUBSET_SIZE, FlowerClient

STRATEGY_LIST = [FedMedian, FedTrimmedAvg, QFedAvg, FaultTolerantFedAvg, FedAvgM, FedAdam, FedAdagrad, FedYogi]
OPT_IDX = 5

strat = argv[1]

def get_strat(name):
    return [(idx, strat) for idx, strat in enumerate(STRATEGY_LIST) if strat.__name__ == name][0]

init_model = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)
init_model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

def client_fn(cid):
    _ = cid
    return FlowerClient()

def evaluate(server_round, parameters, config):
    model = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    _, (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    x_test, y_test = x_test[:SUBSET_SIZE], y_test[:SUBSET_SIZE]

    model.set_weights(parameters)

    loss, accuracy = model.evaluate(x_test, y_test)

    # return statistics
    return loss, {"accuracy": accuracy}

strat_args = {
    "evaluate_fn": evaluate,
    "initial_parameters": ndarrays_to_parameters(init_model.get_weights())
}

start_idx, strategy = get_strat(strat)

if start_idx >= 4:
    strat_args["tau"] = 0.01

hist = fl.simulation.start_simulation(
    client_fn=client_fn,
    num_clients=2,
    config=fl.server.ServerConfig(num_rounds=3),
    strategy=strategy(**strat_args),
)

assert (hist.metrics_centralized['accuracy'][0][1] / hist.metrics_centralized['accuracy'][-1][1]) <= 1.04
