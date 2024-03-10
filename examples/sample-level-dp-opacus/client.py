import argparse
import warnings
from collections import OrderedDict

import flwr as fl
from flwr_datasets import FederatedDataset
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.transforms import Compose, Normalize, ToTensor
from tqdm import tqdm

from opacus import PrivacyEngine

warnings.filterwarnings("ignore", category=UserWarning)

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class Net(nn.Module):
    """Model (simple CNN adapted from 'PyTorch: A 60 Minute Blitz')"""

    def __init__(self) -> None:
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


def train(net, train_loader, privacy_engine, optimizer, epochs=1):
    criterion = torch.nn.CrossEntropyLoss()
    for _ in range(epochs):
        for batch in tqdm(train_loader, "Training"):
            images = batch["img"]
            labels = batch["label"]
            optimizer.zero_grad()
            criterion(net(images.to(DEVICE)), labels.to(DEVICE)).backward()
            optimizer.step()

    epsilon = privacy_engine.get_epsilon(delta=target_delta)
    return epsilon


def test(net, test_loader):
    criterion = torch.nn.CrossEntropyLoss()
    correct, loss = 0, 0.0
    with torch.no_grad():
        for batch in tqdm(test_loader, "Testing"):
            images = batch["img"].to(DEVICE)
            labels = batch["label"].to(DEVICE)
            outputs = net(images)
            loss += criterion(outputs, labels).item()
            correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
    accuracy = correct / len(test_loader.dataset)
    return loss, accuracy


def load_data(partition_id):
    fds = FederatedDataset(dataset="cifar10", partitioners={"train": 3})
    partition = fds.load_partition(partition_id)
    # Divide data on each node: 80% train, 20% test
    partition_train_test = partition.train_test_split(test_size=0.2)
    pytorch_transforms = Compose(
        [ToTensor(), Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    def apply_transforms(batch):
        batch["img"] = [pytorch_transforms(img) for img in batch["img"]]
        return batch

    partition_train_test = partition_train_test.with_transform(apply_transforms)
    train_loader = DataLoader(
        partition_train_test["train"], batch_size=32, shuffle=True
    )
    test_loader = DataLoader(partition_train_test["test"], batch_size=32)
    return train_loader, test_loader


class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model, train_loader, test_loader) -> None:
        super().__init__()
        self.test_loader = test_loader
        self.optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
        self.privacy_engine = PrivacyEngine(secure_mode=False)
        (
            self.model,
            self.optimizer,
            self.train_loader,
        ) = self.privacy_engine.make_private(
            module=model,
            optimizer=self.optimizer,
            data_loader=train_loader,
            noise_multiplier=noise_multiplier,
            max_grad_norm=max_grad_norm,
        )

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in net.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(net.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        net.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        epsilon = train(
            self.model,
            self.train_loader,
            self.privacy_engine,
            self.optimizer,
        )

        if epsilon is not None:
            print(f"Epsilon value for delta={target_delta} is {epsilon:.2f}")
        else:
            print("Epsilon value not available.")
        return (self.get_parameters(config={}), len(self.train_loader), {})

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = test(self.model, self.test_loader)
        return loss, len(test_loader.dataset), {"accuracy": accuracy}


parser = argparse.ArgumentParser(description="Flower")
parser.add_argument(
    "--partition-id",
    choices=[0, 1, 2],
    required=True,
    type=int,
    help="Partition of the dataset divided into 3 iid partitions created artificially.",
)
parser.add_argument(
    "--target-delta",
    default=1e-5,
    required=False,
    type=float,
)
parser.add_argument(
    "--noise-multiplier",
    default=1.3,
    required=False,
    type=float,
)
parser.add_argument(
    "--max-grad-norm",
    default=1.0,
    required=False,
    type=float,
)

partition_id = parser.parse_args().partition_id
target_delta = parser.parse_args().target_delta
noise_multiplier = parser.parse_args().noise_multiplier
max_grad_norm = parser.parse_args().max_grad_norm

net = Net().to(DEVICE)
train_loader, test_loader = load_data(partition_id=partition_id)
client = FlowerClient(net, train_loader, test_loader).to_client()

fl.client.start_client(
    server_address="127.0.0.1:8080",
    client=client,
)
