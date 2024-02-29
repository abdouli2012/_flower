# Copyright 2023 Flower Labs GmbH. All Rights Reserved.
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
"""InnerDirichlet partitioner."""
import warnings
from typing import Dict, List, Optional, Union

import numpy as np

import datasets
from flwr_datasets.common.typing import NDArrayFloat, NDArrayInt
from flwr_datasets.partitioner.partitioner import Partitioner


class InnerDirichletPartitioner(Partitioner):  # pylint: disable=R0902
    """Partitioner based on Dirichlet distribution.

    Implementation based on Federated Learning Based on Dynamic Regularization
    https://arxiv.org/abs/2111.04263.

    Parameters
    ----------
    partition_sizes : Union[List[int], NDArrayInt]
        The sizes of all partitions.
    partition_by : str
        Column name of the labels (targets) based on which Dirichlet sampling works.
    alpha : Union[int, float, List[float], NDArrayFloat]
        Concentration parameter to the Dirichlet distribution
    shuffle: bool
        Whether to randomize the order of samples. Shuffling applied after the
        samples assignment to nodes.
    seed: int
        Seed used for dataset shuffling. It has no effect if `shuffle` is False.

    Examples
    --------
    >>> from flwr_datasets import FederatedDataset
    >>> from flwr_datasets.partitioner import InnerDirichletPartitioner
    >>>
    >>> partitioner = InnerDirichletPartitioner(
    >>>     partition_sizes=[6_000] * 10, partition_by="label", alpha=0.5
    >>> )
    >>> fds = FederatedDataset(dataset="mnist", partitioners={"train": partitioner})
    >>> partition = fds.load_partition(0)
    >>> print(partition[0])  # Print the first example
    """

    def __init__(  # pylint: disable=R0913
        self,
        partition_sizes: Union[List[int], NDArrayInt],
        partition_by: str,
        alpha: Union[int, float, List[float], NDArrayFloat],
        shuffle: bool = True,
        seed: Optional[int] = 42,
    ) -> None:
        super().__init__()
        # Attributes based on the constructor
        self._partition_sizes = _instantiate_partition_sizes(partition_sizes)
        self._initial_alpha = alpha
        self._alpha: Optional[NDArrayFloat] = None
        self._partition_by = partition_by
        self._shuffle = shuffle
        self._seed = seed

        # Utility attributes
        self._initialized_alpha = False
        self._rng = np.random.default_rng(seed=self._seed)  # NumPy random generator
        # The attributes below are determined during the first call to load_partition
        self._unique_classes: Optional[Union[List[int], List[str]]] = None
        self._num_unique_classes: Optional[int] = None
        self._num_partitions = len(self._partition_sizes)

        # self._avg_num_of_samples_per_node: Optional[float] = None
        self._node_id_to_indices: Dict[int, List[int]] = {}
        self._node_id_to_indices_determined = False

    def load_partition(self, node_id: int) -> datasets.Dataset:
        """Load a partition based on the partition index.

        Parameters
        ----------
        node_id : int
            the index that corresponds to the requested partition

        Returns
        -------
        dataset_partition : Dataset
            single partition of a dataset
        """
        # The partitioning is done lazily - only when the first partition is
        # requested. Only the first call creates the indices assignments for all the
        # partition indices.
        self._check_num_partitions_correctness_if_needed()
        self._check_partition_sizes_correctness_if_needed()
        self._check_the_sum_of_partition_sizes()
        self._determine_num_unique_classes_if_needed()
        self._alpha = self._initialize_alpha_if_needed(self._initial_alpha)
        self._determine_node_id_to_indices_if_needed()
        return self.dataset.select(self._node_id_to_indices[node_id])

    def _initialize_alpha_if_needed(
        self, alpha: Union[int, float, List[float], NDArrayFloat]
    ) -> NDArrayFloat:
        """Convert alpha to the used format in the code a NDArrayFloat.

        The alpha can be provided in constructor can be in different format for user
        convenience. The format into which it's transformed here is used throughout the
        code for computation.

        Parameters
        ----------
        alpha : Union[int, float, List[float], NDArrayFloat]
            Concentration parameter to the Dirichlet distribution

        Returns
        -------
        alpha : NDArrayFloat
            Concentration parameter in a format ready to used in computation.
        """
        if self._initialized_alpha:
            assert self._alpha is not None
            return self._alpha
        if isinstance(alpha, int):
            assert self._num_unique_classes is not None
            alpha = np.array([float(alpha)], dtype=float).repeat(
                self._num_unique_classes
            )
        elif isinstance(alpha, float):
            assert self._num_unique_classes is not None
            alpha = np.array([alpha], dtype=float).repeat(self._num_unique_classes)
        elif isinstance(alpha, List):
            if len(alpha) != self._num_unique_classes:
                raise ValueError(
                    "When passing alpha as a List, its length needs needs to be "
                    "of length equal to the number of unique classes."
                )
            alpha = np.asarray(alpha)
        elif isinstance(alpha, np.ndarray):
            # pylint: disable=R1720
            if alpha.ndim == 1 and alpha.shape[0] != self._num_unique_classes:
                raise ValueError(
                    "When passing alpha as an NDArray, its length needs needs to be "
                    "of length equal to the number of unique classes."
                )
            elif alpha.ndim == 2:
                alpha = alpha.flatten()
                if alpha.shape[0] != self._num_unique_classes:
                    raise ValueError(
                        "When passing alpha as an NDArray, its length needs needs to be"
                        " of length equal to the number of unique classes."
                    )
        else:
            raise ValueError("The given alpha format is not supported.")
        if not (alpha > 0).all():
            raise ValueError(
                f"Alpha values should be strictly greater than zero. "
                f"Instead it'd be converted to {alpha}"
            )
        return alpha

    def _determine_node_id_to_indices_if_needed(self) -> None:  # pylint: disable=R0914
        """Create an assignment of indices to the partition indices."""
        if self._node_id_to_indices_determined:
            return

        # Create class priors for the whole partitioning process
        assert self._alpha is not None
        class_priors = self._rng.dirichlet(alpha=self._alpha, size=self._num_partitions)
        targets = np.asarray(self.dataset[self._partition_by])
        # List representing indices of each class
        assert self._num_unique_classes is not None
        idx_list = [np.where(targets == i)[0] for i in range(self._num_unique_classes)]
        class_sizes = [len(idx_list[i]) for i in range(self._num_unique_classes)]

        client_indices = [
            np.zeros(self._partition_sizes[cid]).astype(np.int64)
            for cid in range(self._num_partitions)
        ]

        # Node id to number of sample left for allocation for that node id
        node_id_to_left_to_allocate = dict(
            zip(range(self._num_partitions), self._partition_sizes)
        )

        not_full_node_ids = list(range(self._num_partitions))
        while np.sum(list(node_id_to_left_to_allocate.values())) != 0:
            # Choose a node
            current_node_id = self._rng.choice(not_full_node_ids)
            # If current node is full resample a client
            if node_id_to_left_to_allocate[current_node_id] == 0:
                # When the node is full, exclude it from the sampling nodes list
                not_full_node_ids.pop(not_full_node_ids.index(current_node_id))
                continue
            node_id_to_left_to_allocate[current_node_id] -= 1
            # Access the label distribution of the chosen client
            current_probabilities = class_priors[current_node_id]
            while True:
                # curr_class = np.argmax(np.random.uniform() <= curr_prior)
                curr_class = self._rng.choice(
                    list(range(self._num_unique_classes)), p=current_probabilities
                )
                # Redraw class label if there are no samples left to be allocated from
                # that class
                if class_sizes[curr_class] == 0:
                    # Class got exhausted, set probabilities to 0
                    class_priors[:, curr_class] = 0
                    # Renormalize such that the probability sums to 1
                    row_sums = class_priors.sum(axis=1, keepdims=True)
                    class_priors = class_priors / row_sums
                    # Adjust the current_probabilities (it won't sum up to 1 otherwise)
                    current_probabilities = class_priors[current_node_id]
                    continue
                class_sizes[curr_class] -= 1
                # Store sample index at the empty array cell
                index = node_id_to_left_to_allocate[current_node_id]
                client_indices[current_node_id][index] = idx_list[curr_class][
                    class_sizes[curr_class]
                ]
                break

        node_id_to_indices = {
            cid: client_indices[cid].tolist() for cid in range(self._num_partitions)
        }
        # Shuffle the indices if the shuffle is True.
        # Note that the samples from this partitioning do not necessarily require
        # shuffling, the order should exhibit consecutive samples.
        if self._shuffle:
            for indices in node_id_to_indices.values():
                # In place shuffling
                self._rng.shuffle(indices)
        self._node_id_to_indices = node_id_to_indices
        self._node_id_to_indices_determined = True

    def _check_num_partitions_correctness_if_needed(self) -> None:
        """Test num_partitions when the dataset is given (in load_partition)."""
        if not self._node_id_to_indices_determined:
            if self._num_partitions > self.dataset.num_rows:
                raise ValueError(
                    "The number of partitions needs to be smaller or equal to "
                    " the number of samples in the dataset."
                )

    def _check_partition_sizes_correctness_if_needed(self) -> None:
        """Test partition_sizes when the dataset is given (in load_partition)."""
        if not self._node_id_to_indices_determined:
            if sum(self._partition_sizes) > self.dataset.num_rows:
                raise ValueError(
                    "The sum of the `partition_sizes` needs to be smaller or equal to "
                    "the number of samples in the dataset."
                )

    def _check_num_partitions_greater_than_zero(self) -> None:
        """Test num_partition left sides correctness."""
        if not self._num_partitions > 0:
            raise ValueError("The number of partitions needs to be greater than zero.")

    def _determine_num_unique_classes_if_needed(self) -> None:
        self._unique_classes = self.dataset.unique(self._partition_by)
        assert self._unique_classes is not None
        self._num_unique_classes = len(self._unique_classes)

    def _check_the_sum_of_partition_sizes(self) -> None:
        if np.sum(self._partition_sizes) != len(self.dataset):
            warnings.warn(
                "The sum of the partition_sizes does not sum to the whole "
                "dataset size. Make sure that is the desired behavior.",
                stacklevel=1,
            )


def _instantiate_partition_sizes(
    partition_sizes: Union[List[int], NDArrayInt]
) -> NDArrayInt:
    """Transform list to the ndarray of ints if needed."""
    if isinstance(partition_sizes, List):
        partition_sizes = np.asarray(partition_sizes)
    elif isinstance(partition_sizes, np.ndarray):
        pass
    else:
        raise ValueError(
            f"The type of partition_sizes is incorrect. Given: "
            f"{type(partition_sizes)}"
        )

    if not all(partition_sizes >= 0):
        raise ValueError("The samples numbers must be greater or equal to zero.")
    return partition_sizes
