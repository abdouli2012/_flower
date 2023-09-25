"""Define our models, and training and eval functions.

If your model is 100% off-the-shelf (e.g. directly from torchvision without requiring
modifications) you might be better off instantiating your  model directly from the Hydra
config. In this way, swapping your model for  another one can be done without changing
the python code at all
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from typing import Tuple, List
from torch.nn.parameter import Parameter
from torch.optim import Optimizer

class LogisticRegression(nn.Module):
    """Simple logistic regression."""

    def __init__(self, num_classes, input_dim=28*28):
        super().__init__()
        self.linear = nn.Linear(input_dim, num_classes)

    def forward(self, x):
        return self.linear(x)

class TwoLayerNet(nn.Module):
    """Simple two-layer MLP."""

    def __init__(self, num_classes, input_dim=28*28, hidden_dim=256):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# SimpleCNN(input_dim=(16 * 5 * 5), hidden_dims=[120, 84], output_dim=10)
class CNN(nn.Module):
    def __init__(self, input_dim, hidden_dims, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)

        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.fc3 = nn.Linear(hidden_dims[1], num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16*5*5)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


from torch.optim import SGD

class ScaffoldOptimizer(SGD):
    """
    Implements SGD optimizer step function as defined in the SCAFFOLD paper
    """

    def __init__(self, grads, step_size, momentum, weight_decay):
        super().__init__(grads, lr=step_size, momentum=momentum, weight_decay=weight_decay)
    
    def step_custom(self, server_cv, client_cv):
        # y_i = y_i - \eta * (g_i + c - c_i)  --> y_i = y_i - \eta*(g_i + \mu*b_{t}) - \eta*(c - c_i) 
        self.step()
        for group in self.param_groups:
            for p, s, c in zip(group["params"], server_cv, client_cv):
                p.data.add_(s - c, alpha=-group["lr"])

def train_scaffold(
    net: nn.Module,
    trainloader: DataLoader,
    device: torch.device,
    epochs: int,
    learning_rate: float,
    momentum: float,
    weight_decay: float,
    server_cv: torch.Tensor,
    client_cv: torch.Tensor,
) -> None:
    """Train the network on the training set using SCAFFOLD.

    Parameters
    ----------
    net : nn.Module
        The neural network to train.
    trainloader : DataLoader
        The training set dataloader object.
    device : torch.device
        The device on which to train the network.
    epochs : int
        The number of epochs to train the network.
    learning_rate : float
        The learning rate.
    momentum : float
        The momentum for SGD optimizer.
    weight_decay : float
        The weight decay for SGD optimizer.
    server_cv : torch.Tensor
        The server's control variate.
    client_cv : torch.Tensor
        The client's control variate.
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = ScaffoldOptimizer(net.parameters(), learning_rate, momentum, weight_decay)
    net.train()
    for _ in range(epochs):
        net = _train_one_epoch_scaffold(
            net, trainloader, device, criterion, optimizer, server_cv, client_cv
        )

def _train_one_epoch_scaffold(
    net: nn.Module,
    trainloader: DataLoader,
    device: torch.device,
    criterion: nn.Module,
    optimizer: ScaffoldOptimizer,
    server_cv: torch.Tensor,
    client_cv: torch.Tensor,
) -> nn.Module:
    """Train the network on the training set for one epoch."""
    for data, target in trainloader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step_custom(server_cv, client_cv) # type: ignore
    return net

def train_fedavg(
    net: nn.Module,
    trainloader: DataLoader,
    device: torch.device,
    epochs: int,
    learning_rate: float,
    momentum: float,
    weight_decay: float,
) -> None:
    """
    Train the network on the training set using FedAvg.
    
    Parameters
    ----------
    net : nn.Module
        The neural network to train.
    trainloader : DataLoader
        The training set dataloader object.
    device : torch.device
        The device on which to train the network.
    epochs : int
        The number of epochs to train the network.
    learning_rate : float
        The learning rate.
    momentum : float
        The momentum for SGD optimizer.
    weight_decay : float
        The weight decay for SGD optimizer.

    Returns
    -------
    None
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = SGD(net.parameters(), lr=learning_rate, momentum=momentum, weight_decay=weight_decay)
    net.train()
    for _ in range(epochs):
        net = _train_one_epoch(
            net, trainloader, device, criterion, optimizer
        )

def _train_one_epoch(
    net: nn.Module,
    trainloader: DataLoader,
    device: torch.device,
    criterion: nn.Module,
    optimizer: Optimizer,
) -> nn.Module:
    """Train the network on the training set for one epoch."""
    for data, target in trainloader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step() # type: ignore
    return net

def train_fedprox(
    net: nn.Module,
    trainloader: DataLoader,
    device: torch.device,
    epochs: int,
    mu: float,
    learning_rate: float,
    momentum: float,
    weight_decay: float,
) -> None:
    """
    Train the network on the training set using FedAvg.
    
    Parameters
    ----------
    net : nn.Module
        The neural network to train.
    trainloader : DataLoader
        The training set dataloader object.
    device : torch.device
        The device on which to train the network.
    epochs : int
        The number of epochs to train the network.
    mu : float
        The proximal mu parameter.
    learning_rate : float
        The learning rate.
    momentum : float
        The momentum for SGD optimizer.
    weight_decay : float
        The weight decay for SGD optimizer.

    Returns
    -------
    None
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = SGD(net.parameters(), lr=learning_rate, momentum=momentum, weight_decay=weight_decay)
    global_params = [param.detach().clone() for param in net.parameters()]
    net.train()
    for _ in range(epochs):
        net = _train_one_epoch_fedprox(
            net, global_params, trainloader, device, criterion, optimizer, mu
        )

def _train_one_epoch_fedprox(
    net: nn.Module,
    global_params: List[Parameter],
    trainloader: DataLoader,
    device: torch.device,
    criterion: nn.Module,
    optimizer: Optimizer,
    mu: float,
) -> nn.Module:
    """Train the network on the training set for one epoch."""
    for data, target in trainloader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output, target)
        proximal_term = 0.0
        for param, global_param in zip(net.parameters(), global_params):
            proximal_term += torch.norm(param - global_param)**2
        loss += (mu/2) * proximal_term
        loss.backward()
        optimizer.step() # type: ignore
    return net

def train_fednova(
    net: nn.Module,
    trainloader: DataLoader,
    device: torch.device,
    epochs: int,
    learning_rate: float,
    momentum: float,
    weight_decay: float,
) -> int:
    """
    Train the network on the training set using FedNova.

    Parameters
    ----------
    net : nn.Module
        The neural network to train.
    trainloader : DataLoader
        The training set dataloader object.
    device : torch.device
        The device on which to train the network.
    epochs : int
        The number of epochs to train the network.
    learning_rate : float
        The learning rate.
    momentum : float
        The momentum for SGD optimizer.
    weight_decay : float
        The weight decay for SGD optimizer.
    
    Returns
    -------
    int
        The number of local training steps.
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = SGD(net.parameters(), lr=learning_rate, momentum=momentum, weight_decay=weight_decay)
    net.train()
    local_steps = 0
    for _ in range(epochs):
        net, local_steps = _train_one_epoch_fednova(
            net, trainloader, device, criterion, optimizer, local_steps
        )
    return local_steps

def _train_one_epoch_fednova(
    net: nn.Module,
    trainloader: DataLoader,
    device: torch.device,
    criterion: nn.Module,
    optimizer: Optimizer,
    local_steps: int,
) -> Tuple[nn.Module, int]:
    """Train the network on the training set for one epoch."""
    for data, target in trainloader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step() # type: ignore
        local_steps += 1
    return net, local_steps

def test(
    net: nn.Module, testloader: DataLoader, device: torch.device
) -> Tuple[float, float]:
    """Evaluate the network on the test set.
    
    Parameters
    ----------
    net : nn.Module
        The neural network to evaluate.
    testloader : DataLoader
        The test set dataloader object.
    device : torch.device
        The device on which to evaluate the network.
    
    Returns
    -------
    Tuple[float, float]
        The loss and accuracy of the network on the test set.
    """

    criterion = nn.CrossEntropyLoss(reduction="sum")
    net.eval()
    correct, total, loss = 0, 0, 0.0
    with torch.no_grad():
        for data, target in testloader:
            data, target = data.to(device), target.to(device)
            output = net(data)
            loss += criterion(output, target).item()
            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
    loss = loss / total
    acc = correct / total
    return loss, acc