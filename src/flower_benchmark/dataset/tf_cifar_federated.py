# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Federated versions of CIFAR-10/100 datasets."""
# pylint: disable=invalid-name

from typing import List, Tuple

import numpy as np
import tensorflow as tf

XY = Tuple[np.ndarray, np.ndarray]
XYList = List[XY]

SEED = 2020
np.random.seed(SEED)


def float_to_int(i: float) -> int:
    """Return float as int but raise if decimal is dropped."""
    if not i.is_integer():
        raise Exception("Cast would drop decimals")

    return int(i)


def sort_by_label(x: np.ndarray, y: np.ndarray) -> XY:
    """Sort by label."""
    idx = np.argsort(y, axis=0).reshape((y.shape[0]))
    return (x[idx], y[idx])


def sort_by_label_repeating(x: np.ndarray, y: np.ndarray) -> XY:
    """Sort by label repeating.

    Create sorting index which is applied to by label sorted x, y
    Example:
        # given:
        y = [
            0 0 1 1 2 2 3 3 4 4
            5 5 6 6 7 7 8 8 9 9
        ]

        use:
        idx = [
            0 2 4 6 8 10 12 14 16 18
            1 3 5 7 9 11 13 15 17 19
        ]

        so that y[idx] becomes:
        y = [
            0 1 2 3 4 5 6 7 8 9
            0 1 2 3 4 5 6 7 8 9
        ]
    """
    x, y = sort_by_label(x, y)

    num_example = x.shape[0]
    num_class = np.unique(y).shape[0]
    idx = (
        np.array(range(num_example), np.int64)
        .reshape((num_class, num_example // num_class))
        .transpose()
        .reshape(num_example)
    )

    return (x[idx], y[idx])


def split_at_fraction(x: np.ndarray, y: np.ndarray, fraction: float) -> Tuple[XY, XY]:
    """Split x,y at a certain fraction."""
    spliting_indice = float_to_int(x.shape[0] * fraction)
    # Take everything BEFORE spliting_indice
    x_0, y_0 = x[:spliting_indice], y[:spliting_indice]
    # Take everything AFTER spliting_indice
    x_1, y_1 = x[spliting_indice:], y[spliting_indice:]
    return (x_0, y_0), (x_1, y_1)


def shuffle(x: np.ndarray, y: np.ndarray) -> XY:
    """Shuffle x and y."""
    idx = np.random.permutation(len(x))
    return x[idx], y[idx]


def partition(x: np.ndarray, y: np.ndarray, num_partitions: int) -> List[XY]:
    """Return x,y as list of partitions."""
    return list(zip(np.split(x, num_partitions), np.split(y, num_partitions)))


def combine_partitions(xy_list_0: XYList, xy_list_1: XYList) -> XYList:
    """Combine two lists of ndarray Tuples into one list."""
    return [
        (np.concatenate([x_0, x_1], axis=0), np.concatenate([y_0, y_1], axis=0))
        for (x_0, y_0), (x_1, y_1) in zip(xy_list_0, xy_list_1)
    ]


def shift(x: np.ndarray, y: np.ndarray) -> XY:
    """Shift x_1, y_1 so that the first half contains only
    labels 0 to 4 and the second half 5 to 9."""
    x, y = sort_by_label(x, y)

    (x_0, y_0), (x_1, y_1) = split_at_fraction(x, y, fraction=0.5)
    (x_0, y_0), (x_1, y_1) = shuffle(x_0, y_0), shuffle(x_1, y_1)
    x, y = np.concatenate([x_0, x_1], axis=0), np.concatenate([y_0, y_1], axis=0)
    return x, y


def load(
    iid_fraction: float, num_partitions: int, cifar100: bool = False
) -> Tuple[XYList, XY]:
    """Load federated version of CIFAR-10/100."""

    cifar = tf.keras.datasets.cifar100 if cifar100 else tf.keras.datasets.cifar10
    (x, y), (x_test, y_test) = cifar.load_data()

    x, y = shuffle(x, y)

    # Make dataset IID
    x, y = sort_by_label_repeating(x, y)

    # Split IID dataset
    # TO_DO: handle fraction 0 and 1.0 edge cases
    (x_0, y_0), (x_1, y_1) = split_at_fraction(x, y, fraction=iid_fraction)

    # Shift in second split of dataset the classes into two groups
    x_1, y_1 = shift(x_1, y_1)

    xy_0_partitions = partition(x_0, y_0, num_partitions)
    xy_1_partitions = partition(x_1, y_1, num_partitions)

    xy_partitions = combine_partitions(xy_0_partitions, xy_1_partitions)

    return xy_partitions, (x_test, y_test)


if __name__ == "__main__":
    # Load a federated dataset and show distribution of examples
    xy_par, _ = load(iid_fraction=0.5, num_partitions=100)
    distro = [np.unique(y, return_counts=True) for _, y in xy_par]

    assert np.sum([d[1] for d in distro]) == 50000

    for d in distro:
        print(d)
