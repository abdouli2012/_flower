import pickle
import shutil
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

import numpy as np
import torch
from common import XY, create_lda_partitions
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.datasets import VisionDataset

from flwr.common.typing import NDArray, NDArrays


def get_dataset(path_to_data: Path, cid: str, partition: str):
    # generate path to cid's data
    path_to_data = path_to_data / cid / (partition + ".pt")

    return TorchVision_FL(path_to_data, transform=cifar10Transformation())


def get_dataloader(
    path_to_data: Path, cid: str, is_train: bool, batch_size: int, workers: int
) -> DataLoader:
    """Generates trainset/valset object and returns appropriate dataloader."""

    partition = "train" if is_train else "val"
    dataset = get_dataset(Path(path_to_data).absolute(), cid, partition)

    # we use as number of workers all the cpu cores assigned to this actor
    kwargs = {"num_workers": workers, "pin_memory": True, "drop_last": False}
    return DataLoader(dataset, batch_size=batch_size, **kwargs)


def get_random_id_splits(total: int, val_ratio: float, shuffle: bool = True):
    """splits a list of length `total` into two following a
    (1-val_ratio):val_ratio partitioning.

    By default the indices are shuffled before creating the split and
    returning.
    """

    if isinstance(total, int):
        indices = list(range(total))
    else:
        indices = total

    split = int(np.floor(val_ratio * len(indices)))
    # print(f"Users left out for validation (ratio={val_ratio}) = {split} ")
    if shuffle:
        np.random.shuffle(indices)
    return indices[split:], indices[:split]


def do_fl_partitioning(
    path_to_dataset: Path,
    pool_size: int,
    alpha: float,
    num_classes: int,
    val_ratio: float = 0.0,
):
    """Torchvision (e.g. CIFAR-10) datasets using LDA."""

    images, labels = torch.load(path_to_dataset)
    idx: NDArray = np.arange(len(images))
    dataset = (idx, labels)
    partitions, _ = create_lda_partitions(
        dataset, num_partitions=pool_size, concentration=alpha, accept_imbalanced=True
    )

    # Show label distribution for first partition (purely informative)
    partition_zero = partitions[0][1]
    hist, _ = np.histogram(partition_zero, bins=list(range(num_classes + 1)))
    print(
        f"Class histogram for 0-th partition (alpha={alpha}, {num_classes} classes): {hist}"
    )

    # now save partitioned dataset to disk
    # first delete dir containing splits (if exists), then create it
    splits_dir = path_to_dataset.parent / "federated"
    if splits_dir.exists():
        shutil.rmtree(splits_dir)
    Path.mkdir(splits_dir, parents=True)

    dataset_sizes = {"train": {}, "val": {}}

    for cid, p in enumerate(range(pool_size)):

        labels = partitions[p][1]
        image_idx = partitions[p][0]
        imgs = images[image_idx]

        # create dir
        Path.mkdir(splits_dir / str(p))
        if val_ratio > 0.0:
            # split data according to val_ratio
            train_idx, val_idx = get_random_id_splits(len(labels), val_ratio)
            val_imgs = imgs[val_idx]
            val_labels = labels[val_idx]

            with open(splits_dir / str(p) / "val.pt", "wb") as f:
                torch.save([val_imgs, val_labels], f)

            # remaining images for training
            imgs = imgs[train_idx]
            labels = labels[train_idx]
            dataset_sizes["val"][(cid)] = len(val_labels)

        with open(splits_dir / str(p) / "train.pt", "wb") as f:
            torch.save([imgs, labels], f)

        dataset_sizes["train"][str(cid)] = len(labels)

    # Save profile
    with open(splits_dir / "profiles.pickle", "wb") as f:
        pickle.dump(dataset_sizes, f)

    return splits_dir


def cifar10Transformation():
    return transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ]
    )


class TorchVision_FL(VisionDataset):
    """This is just a trimmed down version of torchvision.datasets.MNIST.

    Use this class by either passing a path to a torch file (.pt)
    containing (data, targets) or pass the data, targets directly
    instead.
    """

    def __init__(
        self,
        path_to_data: Path,
        data=None,
        targets=None,
        transform: Optional[Callable] = None,
    ) -> None:
        super(TorchVision_FL, self).__init__(
            str(path_to_data.absolute()), transform=transform
        )
        self.transform = transform

        if path_to_data:
            # load data and targets (path_to_data points to an specific .pt file)
            self.data, self.targets = torch.load(path_to_data)
        else:
            self.data = data
            self.targets = targets

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        img, target = self.data[index], int(self.targets[index])

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        if not isinstance(img, Image.Image):  # if not PIL image
            if not isinstance(img, np.ndarray):  # if torch tensor
                img = img.numpy()

            img = Image.fromarray(img)

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self) -> int:
        return len(self.data)


def get_cifar_10(path_to_data="./data"):
    """Downloads CIFAR10 dataset and generates a unified training set (it will
    be partitioned later using the LDA partitioning mechanism."""

    # download dataset and load train set
    train_set = datasets.CIFAR10(root=path_to_data, train=True, download=True)

    # fuse all data splits into a single "training.pt"
    data_loc = Path(path_to_data) / "cifar-10-batches-py"
    training_data = data_loc / "training.pt"
    print("Generating unified CIFAR dataset")
    torch.save([train_set.data, np.array(train_set.targets)], training_data)

    test_set = datasets.CIFAR10(
        root=path_to_data, train=False, transform=cifar10Transformation()
    )

    # returns path where training data is and testset
    return training_data, test_set
