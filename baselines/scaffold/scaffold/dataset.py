"""Handle basic dataset creation.

In case of PyTorch it should return dataloaders for your dataset (for both the clients
and the server). If you are using a custom dataset class, this module is the place to
define it. If your dataset requires to be downloaded (and this is not done
automatically -- e.g. as it is the case for many dataset in TorchVision) and
partitioned, please include all those functions and logic in the
`dataset_preparation.py` module. You can use all those functions from functions/methods
defined here of course.
"""

from typing import Optional, Tuple, List
from omegaconf import DictConfig
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets

from scaffold.dataset_preparation import _partition_data

def load_datasets(
    config: DictConfig,
    num_clients: int,
    val_ratio: float = 0.1,
    batch_size_ratio: Optional[int] = 0.2,
    seed: Optional[int] = 42,
) -> Tuple[List[DataLoader], List[DataLoader], DataLoader]:
    """Creates the dataloaders to be fed into the model.

    Parameters
    ----------
    config: DictConfig
        Parameterises the dataset partitioning process
    num_clients : int
        The number of clients that hold a part of the data
    similarity: float
        Parameter to sample similar data
    val_ratio : float, optional
        The ratio of training data that will be used for validation (between 0 and 1),
        by default 0.1
    batch_size : int, optional
        The size of the batches to be fed into the model, by default 32
    seed : int, optional
        Used to set a fix seed to replicate experiments, by default 42

    Returns
    -------
    Tuple[DataLoader, DataLoader, DataLoader]
        The DataLoader for training, the DataLoader for validation, the DataLoader for testing.
    """
    print(f"Dataset partitioning config: {config}")

    datasets, testset = _partition_data(
        num_clients,
        similarity=config.similarity,
        seed=seed,
    )
    # split each partition into train/val and create DataLoader
    trainloaders = []
    valloaders = []
    for dataset in datasets:
        len_val = int(len(dataset) / (1 / val_ratio))
        lengths = [len(dataset) - len_val, len_val]
        ds_train, ds_val = random_split(
            dataset, lengths, torch.Generator().manual_seed(seed)
        )
        batch_size = int(len(ds_train) * batch_size_ratio)
        trainloaders.append(DataLoader(ds_train, batch_size=batch_size, shuffle=True))
        valloaders.append(DataLoader(ds_val, batch_size=batch_size))
    return trainloaders, valloaders, DataLoader(testset, batch_size=len(testset))