"""Handle the dataset partitioning and (optionally) complex downloads.

Please add here all the necessary logic to either download, uncompress, pre/post-process
your dataset (or all of the above). If the desired way of running your baseline is to
first download the dataset and partition it and then run the experiments, please
uncomment the lines below and tell us in the README.md (see the "Running the Experiment"
block) that this file should be executed first.
"""
import json
import os
from typing import List, Optional, Tuple, Dict, DefaultDict
from collections import defaultdict
import numpy as np
from sklearn.model_selection import train_test_split


def _read_dataset(
        path: str
) -> Tuple[List, DefaultDict]:
    """Read (if necessary) and returns the leaf dataset.

    Returns
    -------
    Tuple[user, data[x,y]]
        The dataset for training and the dataset for testing Femnist.
    """
    users = []
    data = defaultdict(lambda: None)
    num_example = []

    files = [f for f in os.listdir(path) if f.endswith('.json')]

    for file_name in files:
        with open(f'{path}/{file_name}') as f:
            dataset = json.load(f)
        users.extend(dataset['users'])
        data.update(dataset['user_data'])
        num_example.extend(dataset['num_samples'])

    users = list(sorted(data.keys()))
    return users, data, num_example


def support_query_split(
        data: DefaultDict,
        label: List,
        support_ratio: float,
):

    x_train, x_test, y_train, y_test = train_test_split(data, label, train_size=support_ratio, stratify=label, random_state=42)

    return x_train, x_test, y_train, y_test


def split_train_validation_test_clients(
        clients: List,
        train_rate: Optional[float] = 0.8,
        val_rate: Optional[float] = 0.1,
) -> Tuple[List[str], List[str], List[str]]:

    np.random.seed(42)
    train_rate = int(train_rate * len(clients))
    val_rate = int(val_rate * len(clients))
    test_rate = len(clients) - train_rate - val_rate

    index = np.random.permutation(len(clients))
    trans_numpy = np.asarray(clients)
    train_clients = trans_numpy[index[:train_rate]].tolist()
    val_clients = trans_numpy[index[train_rate:train_rate + val_rate]].tolist()
    test_clients = trans_numpy[index[train_rate + val_rate:]].tolist()

    return train_clients, val_clients, test_clients


def _partition_data(
        data_type: str,
        dir_path: str,
        support_ratio: float,
) -> Tuple[Dict, Dict]:

    train_path = f'{dir_path}/train'
    test_path = f'{dir_path}/test'

    train_users, train_data, train_num = _read_dataset(train_path)
    test_users, test_data, test_num = _read_dataset(test_path)

    all_dataset = {'users': [], 'user_data': {}, 'num_samples': []}
    support_dataset = {'users': [], 'user_data': {}, 'num_samples': []}
    query_dataset = {'users': [], 'user_data': {}, 'num_samples': []}

    for user in train_users:
        all_x = np.asarray(train_data[user]['x'] + test_data[user]['x'])
        all_y = np.asarray(train_data[user]['y'] + test_data[user]['y'])

        if data_type == 'femnist':
            unique, counts = np.unique(all_y, return_counts=True)
            class_counts = dict(zip(unique, counts))

            # Find classes with only one sample
            classes_to_remove = [cls for cls, count in class_counts.items() if count == 1]

            # Filter out the samples of those classes
            mask = np.isin(all_y, classes_to_remove, invert=True)

            all_x = all_x[mask]
            all_y = all_y[mask]

            try:
                sup_x, qry_x, sup_y, qry_y = support_query_split(all_x, all_y, support_ratio)
            except Exception as e:
                continue

        elif data_type == 'shakespeare':
            sup_x, qry_x, sup_y, qry_y = train_test_split(all_x, all_y, train_size=support_ratio, random_state=42)

        all_dataset['users'].append(user)
        all_dataset['user_data'][user] = {'x': all_x.tolist(), 'y': all_y.tolist()}
        all_dataset['num_samples'].append(len(all_y.tolist()))

        support_dataset['users'].append(user)
        support_dataset['user_data'][user] = {'x': sup_x, 'y': sup_y}
        support_dataset['num_samples'].append(len(sup_y))

        query_dataset['users'].append(user)
        query_dataset['user_data'][user] = {'x': qry_x, 'y': qry_y}
        query_dataset['num_samples'].append(len(qry_y))

    return support_dataset, query_dataset
