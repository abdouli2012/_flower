"""Define your client class and a function to construct such clients.

Please overwrite `flwr.client.NumPyClient` or `flwr.client.Client` and create a function
to instantiate your client.
"""

from typing import Callable, Dict
from power_of_choice.models import create_CNN_model
from power_of_choice.models import create_MLP_model
from power_of_choice.dataset import load_dataset
from flwr.common import Config, Scalar
import tensorflow as tf
import flwr as fl
import numpy as np
import math

class FlwrClient(fl.client.NumPyClient):
    def __init__(self, model, x_train, y_train) -> None:
        super().__init__()
        self.model = model
        split_idx = math.floor(len(x_train) * 0.9)  # Use 10% of x_train for validation
        self.x_train, self.y_train = x_train[:split_idx], y_train[:split_idx]
        self.x_val, self.y_val = x_train[split_idx:], y_train[split_idx:]

    def get_properties(self, config: Config) -> Dict[str, Scalar]:
        # Return the client's dataset size
        x_entire = np.concatenate((self.x_train, self.x_val))

        properties = {
            "data_size": len(x_entire),
        }

        return properties

    def get_parameters(self, config):
        return self.model.get_weights()

    def fit(self, parameters, config):
        epochs = config["local_epochs"]

        if epochs is None:
            epochs = 2

        batch_size = config["batch_size"]

        if batch_size is None:
            batch_size = 32
            
        fraction_samples = config["fraction_samples"]

        learning_rate = config["learning_rate"]

        x_train_selected = self.x_train
        y_train_selected = self.y_train

        # Randomly sample num_samples from the training set
        if fraction_samples is not None:
            num_samples = round(len(self.x_train) * fraction_samples)
            idx = np.random.choice(len(self.x_train), num_samples, replace=False)
            x_train_selected = self.x_train[idx]
            y_train_selected = self.y_train[idx]

        print(f"Client training on {len(x_train_selected)} samples, {epochs} epochs, batch size {batch_size}, learning rate {learning_rate}")

        # During training, update the learning rate as needed
        tf.keras.backend.set_value(self.model.optimizer.lr, learning_rate)

        self.model.set_weights(parameters)

        history = self.model.fit(x_train_selected, y_train_selected, batch_size=batch_size, epochs=epochs, verbose=2)
        return self.model.get_weights(), len(self.x_train), {"training_loss": history.history['loss'][-1]}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        if "first_phase" in config and config["first_phase"]:
            x_entire = np.concatenate((self.x_train, self.x_val))
            y_entire = np.concatenate((self.y_train, self.y_val))
            if config["is_cpow"] == False:
                # In the base variant, during the first phase we evaluate on the entire dataset
                loss, acc = self.model.evaluate(x_entire, y_entire, verbose=2)
            else:
                # In the cpow variant, during the first phase we evaluate on a mini-batch of b samples
                b = config["b"]
                idx = np.random.choice(len(x_entire), b, replace=False)
                x_entire_selected = x_entire[idx]
                y_entire_selected = y_entire[idx]
                loss, acc = self.model.evaluate(x_entire_selected, y_entire_selected, verbose=2)
        else:
            # In the normal evaluation phase, we evaluate on the validation set
            loss, acc = self.model.evaluate(self.x_val, self.y_val, verbose=2)

        return loss, len(self.x_val), {"accuracy": acc}


def gen_client_fn(is_cnn: bool = False) -> Callable[[str], fl.client.Client]:

    def client_fn(cid: str) -> fl.client.Client:
        # Load model
        if(is_cnn):
            model = create_CNN_model()
        else:
            model = create_MLP_model()
        
        model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

        # Load data partition (divide MNIST into NUM_CLIENTS distinct partitions)
        (x_train_cid, y_train_cid) = load_dataset(cid, is_cnn)

        # Create and return client
        return FlwrClient(model, x_train_cid, y_train_cid)
    
    return client_fn
