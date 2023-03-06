from typing import Optional, Tuple

import torch
import torch.nn as nn
from torch.utils.data import DataLoader


class Net(nn.Module):
    """Implementation of the model used in the LEAF paper for training on
    FEMNIST data."""

    def __init__(self, num_classes):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=5, padding="same")
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, padding="same")
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(7 * 7 * 64, 2048)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(2048, num_classes)

    def forward(self, x):
        """Forward step in training."""
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = x.view(-1, 7 * 7 * 64)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        return x


def train(
    net: nn.Module,
    trainloader: DataLoader,
    valloader: DataLoader,
    epochs: int,
    learning_rate: float,
    device: torch.device,
    n_batches: int = None,
    verbose: bool = False,
):
    """Train a given model with CrossEntropy and SGD (or some version of it
    like batch-SGD).

    n_batches is an alternative way of specifying the training length
    (instead of epochs)
    """
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate)
    net.train()
    if epochs is not None:
        for epoch in range(epochs):
            correct, total, epoch_loss = 0, 0, 0.0
            for images, labels in trainloader:
                images = images.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()
                outputs = net(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                # Metrics
                epoch_loss += loss
                total += labels.size(0)
                correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
            epoch_loss /= len(trainloader.dataset)
            epoch_acc = correct / total

            if verbose:
                print(
                    f"Epoch {epoch + 1}: train loss {epoch_loss}, accuracy {epoch_acc}"
                )
        train_loss, train_acc = _validate(net, trainloader)
        val_loss, val_acc = _validate(net, valloader)
        return train_loss, train_acc, val_loss, val_acc
    else:
        # Training time given in number of batches not epochs
        correct, total, train_loss = 0, 0, 0.0
        for idx, (images, labels) in enumerate(trainloader):
            if idx == n_batches:
                break
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = net(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            # Metrics
            train_loss += loss
            total += labels.size(0)
            correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
        train_loss /= n_batches * images.size(0)
        train_acc = correct / total
        if verbose:
            print(
                f"Batch len based training: train loss {train_loss}, accuracy {train_acc}"
            )
        val_loss, val_acc = _validate(net, valloader)
        return train_loss, train_acc, val_loss, val_acc


def _validate(net, valloader) -> Tuple[float, float]:
    """Calculate metrics on the given valloader."""
    criterion = torch.nn.CrossEntropyLoss()
    if len(valloader) == 0:
        raise ValueError("Valloader can't be 0, exiting...")
    # Validation loop
    with torch.no_grad():
        val_loss = 0
        correct = 0
        total = 0
        for data, target in valloader:
            output = net(data)
            val_loss += criterion(output, target).item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

        accuracy = 100.0 * correct / total
        val_loss /= float(len(valloader))
    return accuracy, val_loss


def test(
    net: nn.Module, testloader: DataLoader, device: torch.device
) -> Tuple[float, float]:
    """Test network on the given testloader."""
    criterion = torch.nn.CrossEntropyLoss()
    correct, total, loss = 0, 0, 0.0
    net.eval()
    with torch.no_grad():
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            outputs = net(images)
            loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    loss /= len(testloader.dataset)
    accuracy = correct / total
    return loss, accuracy


if __name__ == "__main__":
    model = Net(num_classes=10)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)
