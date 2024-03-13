from task import DEVICE, Net, get_weights, load_data, set_weights, test, train

from flwr.client import ClientApp, NumPyClient
from flwr.client.mod import secaggplus_mod

from flwr.client.mod.centraldp_mods import fixedclipping_mod

# Load model and data (simple CNN, CIFAR-10)
net = Net().to(DEVICE)


# Define FlowerClient and client_fn
class FlowerClient(NumPyClient):
    
    def __init__(self, trainloader, testloader) -> None:
        self.trainloader = trainloader
        self.testloader = testloader

    def fit(self, parameters, config):
        set_weights(net, parameters)
        results = train(net, self.trainloader, self.testloader, epochs=1, device=DEVICE)
        return get_weights(net), len(self.trainloader.dataset), results

    def evaluate(self, parameters, config):
        set_weights(net, parameters)
        loss, accuracy = test(net, self.testloader)
        return loss, len(self.testloader.dataset), {"accuracy": accuracy}


def client_fn(cid: str):
    """Create and return an instance of Flower `Client`."""
    trainloader, testloader = load_data(partition_id=int(cid))
    return FlowerClient(trainloader, testloader).to_client()


# Flower ClientApp
app = ClientApp(
    client_fn=client_fn,
    mods=[
        secaggplus_mod,
        fixedclipping_mod,
    ],
)
