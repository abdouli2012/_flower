"""tfexample: A Flower / TensorFlow app."""

from typing import List, Tuple
from flwr.common import Context, ndarrays_to_parameters, Metrics
from flwr.server import ServerApp, ServerAppComponents, ServerConfig
from flwr.server.strategy import FedAvg

from tfexample.task import load_model


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


def server_fn(context: Context):
    """Construct components that set the ServerApp behaviour.

    You can use settings in `context.run_config` to parameterize the
    construction of all elements (e.g the strategy or the number of rounds)
    wrapped in the returned ServerAppComponents object.
    """

    # Let's define the global model and pass it to the strategy
    # Note this is optional.
    parameters = ndarrays_to_parameters(load_model().get_weights())

    # Define the strategy
    # We pass a callback to process the metrics returned by a client's
    # fit() method. Similarly, we set the fraction of clients to
    # sample for federated evaluation at run time based on the value
    # defined in the pyproject.toml (or overrided when calling `flwr run`.)
    strategy = strategy = FedAvg(
        fraction_fit=context.run_config["fraction-fit"],
        fraction_evaluate=1.0,
        min_available_clients=2,
        initial_parameters=parameters,
        evaluate_metrics_aggregation_fn=weighted_average,
    )
    # Read from config
    num_rounds = context.run_config["num-server-rounds"]
    config = ServerConfig(num_rounds=num_rounds)

    return ServerAppComponents(strategy=strategy, config=config)


# Create ServerApp
app = ServerApp(server_fn=server_fn)
