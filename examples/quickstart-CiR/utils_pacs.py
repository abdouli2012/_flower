import torch
from torchvision import transforms, datasets
from torch.utils.data import DataLoader, Subset, ConcatDataset
import os
from sklearn.model_selection import StratifiedKFold
from collections import Counter
from tqdm import tqdm

# Define the root directory where your dataset is located
dataset_root = "data/pacs_data/"
from flwr.common import (
    bytes_to_ndarray,
)

# List the subdirectories (folders) in the parent folder
data_kinds = [
    os.path.join(dataset_root, d)
    for d in os.listdir(dataset_root)
    if os.path.isdir(os.path.join(dataset_root, d))
]


def make_dataloaders(dataset_kinds=data_kinds, k=2, batch_size=32, verbose=False):
    # Define data transformations
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    trainloaders = []
    valloaders = []
    test_subsets = []
    for idx, data_kind in enumerate(dataset_kinds):
        dataset = datasets.ImageFolder(root=data_kind, transform=transform)
        for fold, (train_indices, val_indices) in enumerate(
            skf.split(range(len(dataset)), dataset.targets), start=1
        ):
            # Split the dataset into train and val subsets
            train_dataset = Subset(dataset, train_indices)
            val_dataset = Subset(dataset, val_indices)
            if fold == 1:
                # Create DataLoaders for train and val sets
                train_loader_tmp = DataLoader(
                    train_dataset, batch_size=batch_size, shuffle=True
                )
                val_loader_tmp = DataLoader(val_dataset, batch_size=batch_size)
                if verbose:
                    print(
                        f"Fold {fold}: Train samples: {len(train_dataset)}, val samples: {len(val_dataset)}"
                    )
                    val_labels = []

                    # Iterate through the val DataLoader to collect labels
                    for images, labels in val_loader_tmp:
                        val_labels.extend(labels.tolist())

                    # Calculate and print the class label frequency
                    label_counts = Counter(val_labels)

                    for label, count in label_counts.items():
                        print(f"Class {label}: {count} samples")

                trainloaders.append(train_loader_tmp)
                valloaders.append(val_loader_tmp)
            else:
                test_subsets.append(val_dataset)
    combined_test_dataset = ConcatDataset(test_subsets)
    testloader = DataLoader(combined_test_dataset, batch_size=batch_size, shuffle=True)

    return (trainloaders, valloaders, testloader)


def train(net1, trainloader, optim, config, epochs, device: str, num_classes=7):
    """Train the model on the training set."""
    criterion = torch.nn.CrossEntropyLoss()
    lambda_reg = 0.5
    lambda_align = 5e-6
    all_labels = torch.arange(num_classes).to(device)

    z_g, mu_g, log_var_g = (
        torch.tensor(bytes_to_ndarray(config["z_g"])).to(device),
        torch.tensor(bytes_to_ndarray(config["mu_g"])).to(device),
        torch.tensor(bytes_to_ndarray(config["log_var_g"])).to(device),
    )
    for _ in range(epochs):
        for images, labels in tqdm(trainloader):
            optim.zero_grad()
            images, labels = images.to(device), labels.to(device)
            pred, mu, log_var = net1(images)
            # loss_fl
            loss_fl = criterion(pred, labels)
            # loss_reg
            loss_reg = criterion(net1.clf(z_g), all_labels)

            # KL Div
            loss_align = 0.5 * (log_var_g[labels] - log_var - 1) + (
                log_var.exp() + (mu - mu_g[labels]).pow(2)
            ) / (2 * log_var_g[labels].exp())
            loss_align_reduced = loss_align.mean(dim=1).mean()
            loss = loss_fl + lambda_reg * loss_reg + lambda_align * loss_align_reduced
            loss.backward(retain_graph=True)
            optim.step()


def test(net1, testloader, device: str):
    """Validate the model on the test set."""
    criterion = torch.nn.CrossEntropyLoss()
    correct, loss = 0, 0.0
    with torch.no_grad():
        for images, labels in tqdm(testloader):
            outputs = net1(images.to(device))[0]
            labels = labels.to(device)
            loss += criterion(outputs, labels).item()
            correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
    accuracy = correct / len(testloader.dataset)
    return loss, accuracy


if __name__ == "__main__":
    aq, bq, cq = make_dataloaders(verbose=True)

    cc = 0
    for feat, label in cq:
        print(len(label))
        cc += len(label)
