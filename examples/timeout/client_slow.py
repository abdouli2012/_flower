import time
import flwr as fl
import numpy as np


weights = [np.ones((3, 3))]

# Define Flower client
class TimeoutClient(fl.client.NumPyClient):
    def get_parameters(self):
        time.sleep(20)
        return weights

    def fit(self, parameters, config):
        time.sleep(40)
        return weights, 1, {}

    def evaluate(self, parameters, config):
        time.sleep(20)
        return 0.1, 1, {"accuracy": 1}


# Start Flower client
fl.client.start_numpy_client("[::]:8080", client=TimeoutClient())
