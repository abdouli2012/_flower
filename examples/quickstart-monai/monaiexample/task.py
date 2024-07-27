import torch

import os
import tarfile
from urllib import request


import numpy as np
from monai.data import DataLoader, Dataset
from monai.transforms import (
    Compose,
    EnsureChannelFirst,
    LoadImage,
    RandFlip,
    RandRotate,
    RandZoom,
    ScaleIntensity,
    ToTensor,
)

from datasets import Dataset
from flwr_datasets.partitioner import IidPartitioner


def train(model, train_loader, epoch_num, device):
    model.to(device)
    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), 1e-5)
    for _ in range(epoch_num):
        model.train()
        for batch in train_loader:
            images, labels = batch["img"], batch["label"]
            optimizer.zero_grad()
            loss_function(model(images.to(device)), labels.to(device)).backward()
            optimizer.step()


def test(model, test_loader, device):
    model.to(device)
    model.eval()
    loss = 0.0
    y_true = list()
    y_pred = list()
    loss_function = torch.nn.CrossEntropyLoss()
    with torch.no_grad():
        for batch in test_loader:
            images, labels = batch["img"], batch["label"]
            out = model(images.to(device))
            test_labels = test_labels.to(device)
            loss += loss_function(out, test_labels).item()
            pred = out.argmax(dim=1)
            for i in range(len(pred)):
                y_true.append(test_labels[i].item())
                y_pred.append(pred[i].item())
    accuracy = sum([1 if t == p else 0 for t, p in zip(y_true, y_pred)]) / len(
        test_loader.dataset
    )
    return loss, accuracy


def _get_transforms():
    train_transforms = Compose(
        [
            LoadImage(image_only=True),
            EnsureChannelFirst(),
            ScaleIntensity(),
            RandRotate(range_x=15, prob=0.5, keep_size=True),
            RandFlip(spatial_axis=0, prob=0.5),
            RandZoom(min_zoom=0.9, max_zoom=1.1, prob=0.5, keep_size=True),
            ToTensor(),
        ]
    )

    val_transforms = Compose(
        [LoadImage(image_only=True), EnsureChannelFirst(), ScaleIntensity(), ToTensor()]
    )

    return train_transforms, val_transforms


def get_apply_transforms_fn(transforms_to_apply):
    def apply_transforms(batch):
        """Apply transforms to the partition from FederatedDataset."""
        batch["img"] = [transforms_to_apply(img) for img in batch["img_file"]]
        return batch

    return apply_transforms


ds = None
partitioner = None


def load_data(num_partitions, partition_id):

    global ds, partitioner
    if ds is None:
        image_file_list, image_label_list = _download_data()

        # Construct HuggingFace dataset
        ds = Dataset.from_dict({"img_file": image_file_list, "label": image_label_list})
        # Set partitioner
        partitioner = IidPartitioner(num_partitions)
        partitioner.dataset = ds

    partition = partitioner.load_partition(partition_id)

    # Split train/validation
    partition_train_test = partition.train_test_split(test_size=0.2, seed=42)

    # Get transforms
    train_t, test_t = _get_transforms()

    # Apply transforms individually to each split
    train_partition = partition_train_test["train"]
    test_partition = partition_train_test["test"]

    partition_train = train_partition.with_transform(get_apply_transforms_fn(train_t))
    partition_val = test_partition.with_transform(get_apply_transforms_fn(test_t))

    # Create dataloaders
    train_loader = DataLoader(partition_train, batch_size=64, shuffle=True)
    val_loader = DataLoader(partition_val, batch_size=64)

    return train_loader, val_loader


def _download_data():
    data_dir = "./MedNIST/"
    _download_and_extract(
        "https://dl.dropboxusercontent.com/s/5wwskxctvcxiuea/MedNIST.tar.gz",
        os.path.join(data_dir),
    )

    class_names = sorted(
        [x for x in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, x))]
    )
    image_files = [
        [
            os.path.join(data_dir, class_name, x)
            for x in os.listdir(os.path.join(data_dir, class_name))
        ]
        for class_name in class_names
    ]
    image_file_list = []
    image_label_list = []
    for i, _ in enumerate(class_names):
        image_file_list.extend(image_files[i])
        image_label_list.extend([i] * len(image_files[i]))
    return image_file_list, image_label_list


def _download_and_extract(url, dest_folder):
    print(dest_folder)
    if not os.path.isdir(dest_folder):
        # Download the tar.gz file
        tar_gz_filename = url.split("/")[-1]
        if not os.path.isfile(tar_gz_filename):
            with request.urlopen(url) as response, open(
                tar_gz_filename, "wb"
            ) as out_file:
                out_file.write(response.read())

        # Extract the tar.gz file
        with tarfile.open(tar_gz_filename, "r:gz") as tar_ref:
            tar_ref.extractall()
