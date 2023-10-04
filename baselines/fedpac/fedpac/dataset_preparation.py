from typing import List, Optional, Tuple

import numpy as np
import torch
import torchvision.transforms as transforms
from torch.utils.data import ConcatDataset, Dataset, Subset, random_split
from torchvision.datasets import EMNIST, CIFAR10
import timeit

def get_label_list(dataset, num_classes):
    label_counter = [0]*(num_classes+1)
    for feature, label  in dataset:
            label_counter[label+1] += 1
    return label_counter


def _download_data(dataset: str) -> Tuple[Dataset, Dataset]:
    """Downloads (if necessary) and returns the MNIST dataset.

    Returns
    -------
    Tuple[MNIST, MNIST]
        The dataset for training and the dataset for testing MNIST.
    """
    if dataset == 'emnist':

        transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        trainset = EMNIST("./dataset", split='byclass', train=True, download=True, transform=transform)
        testset = EMNIST("./dataset", split='byclass', train=False, download=True, transform=transform)


    elif dataset =='cifar10':

        transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465),
                             (0.2023, 0.1994, 0.2010)),
        ])

        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465),
                                (0.2023, 0.1994, 0.2010)),
        ])
        trainset = CIFAR10("./dataset", train=True, download=True, transform=transform_train)
        testset = CIFAR10("./dataset", train=False, download=True, transform=transform_test) 

    return trainset, testset


def partition_cifar_data(
    dataset,
    num_clients,
    iid: Optional[bool] = False,
    balance: Optional[bool] = True,
    s: Optional[float] = 0.2,
    seed: Optional[int] = 42,
) -> Tuple[List[Dataset], Dataset]:
    """Split training set into iid or non iid partitions to simulate the
    federated setting.

    Parameters
    ----------
    num_clients : int
        The number of clients that hold a part of the data
    iid : bool, optional
        Whether the data should be independent and identically distributed between
        the clients or if the data should first be sorted by labels and distributed by chunks
        to each client (used to test the convergence in a worst case scenario), by default False
    s : float, optional
        fraction of iid data for each client. 0.2 by default from paper.
    seed : int, optional
        Used to set a fix seed to replicate experiments, by default 42

    Returns
    -------
    Tuple[List[Dataset], Dataset]
        A list of dataset for each client and a single dataset to be use for testing the model.
    """
    trainset, testset = _download_data(dataset)
    if balance:
        trainset = _balance_classes(trainset, seed)


    partition_size = int(len(trainset) / num_clients) 
    lengths = [partition_size] * num_clients
    labels = np.unique(trainset.targets)
    num_classes = len(labels)

    if iid:
        datasets = random_split(trainset, lengths, torch.Generator().manual_seed(seed))
        return datasets, testset
    else:
        noniid_labels_list = [[0,1,2], [2,3,4], [4,5,6], [6,7,8], [8,9,0]]
        iid_partition_size = int(partition_size * s)
        noniid_partition_size = partition_size - iid_partition_size
        idxs = trainset.targets.argsort()
        num_idxs_per_class = int(len(idxs)/num_classes)
        iid_shard_size = int(iid_partition_size/num_classes)
        noniid_shard_size = int(noniid_partition_size/(len(noniid_labels_list)-1))
        sorted_data = Subset(trainset, idxs)
        label_index = {}
        for i in labels:
            label_index[int(i)] = int(i)*num_idxs_per_class

        tmp = []
        for idx in range(num_clients):
            for i in labels:
                tmp.append(
                    Subset(
                        sorted_data, np.arange(label_index[int(i)], label_index[int(i)]+iid_shard_size)
                    )
                )

                label_index[int(i)] += iid_shard_size
            noniid_labels = noniid_labels_list[idx%5]
            for ni in noniid_labels:
                tmp.append(
                Subset(
                    sorted_data, np.arange(label_index[int(ni)], label_index[int(ni)]+noniid_shard_size)
                )
            )   
                label_index[int(ni)] += noniid_shard_size


        m = int(len(tmp)/num_clients)
        datasets = [
            ConcatDataset(tmp[m*c : m*(c+1)])
            for c in range(num_clients)
        ]

    return datasets, testset



def partition_emnist_data(
    dataset,
    num_clients,
    iid: Optional[bool] = False,
    balance: Optional[bool] = True,
    s: Optional[float] = 0.2,
    seed: Optional[int] = 42,
) -> Tuple[List[Dataset], Dataset]:
    
    """Split training set into iid or non iid partitions to simulate the
    federated setting.

    Parameters
    ----------
    num_clients : int
        The number of clients that hold a part of the data
    iid : bool, optional
        Whether the data should be independent and identically distributed between
        the clients or if the data should first be sorted by labels and distributed by chunks
        to each client (used to test the convergence in a worst case scenario), by default False
    s : float, optional
        fraction of iid data for each client. 0.2 by default from paper.
    seed : int, optional
        Used to set a fix seed to replicate experiments, by default 42

    Returns
    -------
    Tuple[List[Dataset], Dataset]
        A list of dataset for each client and a single dataset to be use for testing the model.
    """
    trainset, testset = _download_data(dataset)
    
    if balance:
        trainset = _balance_classes(trainset, seed)
    print(len(trainset))

    partition_size = int(len(trainset) / num_clients) 
    lengths = [partition_size] * num_clients
    labels = np.unique(trainset.targets)
    num_classes = len(labels)

    if iid:
        datasets = random_split(trainset, lengths, torch.Generator().manual_seed(seed))
        return datasets, testset
    else:
        noniid_labels_list = [[i for i in range(10)],[i for i in range(10, 36)],[i for i in range(36,62)]]
        iid_partition_size = int(partition_size * s)
        noniid_partition_size = partition_size - iid_partition_size
        idxs = trainset.targets.argsort()
        num_idxs_per_class = int(len(idxs)/num_classes)
        iid_shard_size = int(iid_partition_size/num_classes)
        noniid_shard_size = int(noniid_partition_size/num_classes)
        sorted_data = Subset(trainset, idxs)
        start = timeit.default_timer()
        label_index = get_label_list(sorted_data, num_classes)
        print(timeit.default_timer()-start)
        total_index = [sum(label_index[:i+1]) for i in labels]
        print(iid_shard_size, noniid_shard_size)
        # print(label_index)
        # print(total_index[-1])


        tmp = []
        for idx in range(num_clients):
            for i in labels:
                if label_index[i]+iid_shard_size>total_index[i]:
                    label_index[i]=total_index[i-1]+1
                tmp.append(
                    Subset(
                        sorted_data, np.arange(label_index[i], label_index[i]+iid_shard_size)
                    )
                )
                label_index[i] += iid_shard_size
            noniid_labels = noniid_labels_list[idx%3]
            # for ni in noniid_labels:
            #     tmp.append(
            #     Subset(
            #         sorted_data, np.arange(label_index[int(ni)], label_index[int(ni)]+noniid_shard_size)
            #     )
            # )   
            #     label_index[int(ni)] += noniid_shard_size


        m = int(len(tmp)/num_clients)
        datasets = [
            ConcatDataset(tmp[m*c : m*(c+1)])
            for c in range(num_clients)
        ]
    for d in datasets:
        l = get_label_list(d, num_classes)
        print(l)
    return datasets, testset



def _balance_classes(
    trainset: Dataset,
    seed: Optional[int] = 42,
) -> Dataset:
    """Balance the classes of the trainset.

    Trims the dataset so each class contains as many elements as the
    class that contained the least elements.

    Parameters
    ----------
    trainset : Dataset
        The training dataset that needs to be balanced.
    seed : int, optional
        Used to set a fix seed to replicate experiments, by default 42.

    Returns
    -------
    Dataset
        The balanced training dataset.
    """
    class_counts = np.bincount(trainset.targets)
    smallest = np.min(class_counts)
    if isinstance(trainset.targets, list):
        trainset.targets = torch.tensor(trainset.targets)
    idxs = trainset.targets.argsort()
    tmp = [Subset(trainset, idxs[: int(smallest)])]
    tmp_targets = [trainset.targets[idxs[: int(smallest)]]]
    for count in np.cumsum(class_counts):
        tmp.append(Subset(trainset, idxs[int(count) : int(count + smallest)]))
        tmp_targets.append(trainset.targets[idxs[int(count) : int(count + smallest)]])
    unshuffled = ConcatDataset(tmp)
    unshuffled_targets = torch.cat(tmp_targets)
    shuffled_idxs = torch.randperm(
        len(unshuffled), generator=torch.Generator().manual_seed(seed)
    )
    shuffled = Subset(unshuffled, shuffled_idxs)
    shuffled.targets = unshuffled_targets[shuffled_idxs]

    return shuffled