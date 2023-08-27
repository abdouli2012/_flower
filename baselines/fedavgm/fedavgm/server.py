"""Define the Flower Server and function to instantiate it."""

from omegaconf import DictConfig
from keras.utils import to_categorical


def get_on_fit_config(config: DictConfig):
    """Generate the function for config.
    
    The config dict is sent to the client fit() method.
    """

    def fit_config_fn(server_round: int):
        # option to use scheduling of learning rate based on round
        # if server_round > 50:
        #     lr = config.lr / 10
        return {
            "local_epochs": config.local_epochs,
            "batch_size": config.batch_size,
        }

    return fit_config_fn


def get_evaluate_fn(model, x_test, y_test, num_rounds, num_classes):
    """Generate the function for server global model evaluation.
    
    The method evaluate_fn runs after global model aggregation.
    """

    def evaluate_fn(server_round: int, parameters, config):
        # if server_round == num_rounds:
        #    return None

        # instantiate the model
        model.set_weights(parameters)

        y_test_cat = to_categorical(y_test, num_classes=num_classes)
        loss, accuracy = model.evaluate(x_test, y_test_cat)

        return loss, {"accuracy": accuracy}

    return evaluate_fn
