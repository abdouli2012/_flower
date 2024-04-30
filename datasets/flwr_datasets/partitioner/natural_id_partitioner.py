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
"""Natural id partitioner class that works with Hugging Face Datasets."""


from typing import Dict, Union

import numpy as np
from tqdm import tqdm

import datasets
from flwr_datasets.common.typing import NDArrayInt
from flwr_datasets.partitioner.partitioner import Partitioner


class NaturalIdPartitioner(Partitioner):
    """Partitioner for dataset that can be divided by a reference to id in dataset.

    Parameters
    ----------
    partition_by: str
        The name of the column that contains the unique values of partitions.
    creation_mode: str
        "full" or "lazy". "full" to create the whole mapping of natural id to indices
        during the first call to the `load_partition` or to lazily filter the dataset
        once the request for a specific partition id happens. It is recommended to use
        "full" mode in case of the dataset < 10,000,000 samples and < 10,000 unique
        values in `partition_by` column

    Examples
    --------
    "flwrlabs/shakespeare" dataset should be used with "full" mode (4226158 samples and
    1129 unique values in the "character_id" column

    >>> from flwr_datasets import FederatedDataset
    >>> from flwr_datasets.partitioner import NaturalIdPartitioner
    >>>
    >>> partitioner = NaturalIdPartitioner(partition_by="character_id")
    >>> fds = FederatedDataset(dataset="flwrlabs/shakespeare",
    >>>                        partitioners={"train": partitioner})
    >>> partition = fds.load_partition(0)
    >>> # Note that no additional computation happens when the call for the new
    >>> # partition is triggered
    >>> partition1 = fds.load_partition(1)

    "sentiment140" (aka Twitter) dataset should be used with "lazy" mode because of the
     huge value of the unique samples in the (1,600,000
    samples BUT 659,775 unique values in the "user" column
    >>> from flwr_datasets import FederatedDataset
    >>> from flwr_datasets.partitioner import NaturalIdPartitioner
    >>>
    >>> partitioner = NaturalIdPartitioner(partition_by="character_id")
    >>> fds = FederatedDataset(dataset="sentiment140",
    >>>                        partitioners={"train": partitioner})
    >>> partition = fds.load_partition(0)
    >>> # Note that the dataset will need to be filtered for a new (not asked for
    >>> # before) partition
    >>> partition1 = fds.load_partition(1)
    """

    def __init__(
        self,
        partition_by: str,
        creation_mode: str = "full",
    ):
        super().__init__()
        self._partition_id_to_natural_id: Dict[int, str] = {}
        self._natural_id_to_partition_id: Dict[str, int] = {}
        self._partition_id_to_indices: Dict[int, NDArrayInt] = {}
        self._partition_by = partition_by
        self._creation_mode = creation_mode

    def _create_int_partition_id_to_natural_id(self) -> None:
        """Create a mapping from int indices to unique client ids from dataset.

        Natural ids come from the column specified in `partition_by`.
        """
        unique_natural_ids = self.dataset.unique(self._partition_by)
        self._partition_id_to_natural_id = dict(
            zip(range(len(unique_natural_ids)), unique_natural_ids)
        )

    def _create_natural_id_to_int_partition_id(self) -> None:
        """Create a mapping from unique client ids from dataset to int indices.

        Natural ids come from the column specified in `partition_by`. This object is
        inverse of the `self._partition_id_to_natural_id`. This method assumes that
        `self._partition_id_to_natural_id` already exist.
        """
        self._natural_id_to_partition_id = {
            value: key for key, value in self._partition_id_to_natural_id.items()
        }

    def _create_partition_id_to_indices(self) -> None:
        """Create an assignment of indices to the partition indices."""
        natural_ids = np.array(self.dataset[self._partition_by])
        unique_natural_ids = self.dataset.unique(self._partition_by)

        none_present = False
        if None in unique_natural_ids:
            none_present = True
            dtype = self.dataset.features[self._partition_by].dtype
            none_replacement: Union[int, str]
            if dtype == "string":
                none_replacement = "None"
                new_term = ""
                counter = 0
                # Ensure the replacement is not in the dataset
                while True:
                    if none_replacement + new_term not in unique_natural_ids:
                        none_replacement = none_replacement + new_term
                        break
                    counter += 1
                    new_term = f"{counter}"
            elif "unit" in dtype:
                none_replacement = max(natural_ids) + 1
            elif "int" in dtype:
                none_replacement = -1
                if none_replacement in unique_natural_ids:
                    none_replacement = max(natural_ids) + 1
            else:
                raise ValueError(
                    "The type of values in the `partition_by` column needs "
                    "to be int or string"
                )

            # Replace the None by the none_replacement (in order to be able to use the
            # np.unique(value, return_inverse) that requires no None and same val types
            is_none = np.vectorize(lambda x: x is None)
            mask = is_none(natural_ids)
            natural_ids[mask] = none_replacement

        unique_natural_ids, inverse = np.unique(natural_ids, return_inverse=True)

        for i, natural_id in tqdm(
            enumerate(unique_natural_ids), desc="Generating partition_id_to_indices"
        ):
            if none_present and natural_id == none_replacement:
                # Use the natural_id that is present in the dataset (not replacement)
                natural_id = None
            partition_id = self._natural_id_to_partition_id[natural_id]
            self._partition_id_to_indices[partition_id] = np.where(inverse == i)[0]

    def load_partition(self, partition_id: int) -> datasets.Dataset:
        """Load a single partition corresponding to a single `partition_id`.

        The choice of the partition is based on unique integers assigned to each
        natural id present in the dataset in the `partition_by` column.

        Parameters
        ----------
        partition_id : int
            the index that corresponds to the requested partition

        Returns
        -------
        dataset_partition : Dataset
            single dataset partition
        """
        if len(self._partition_id_to_natural_id) == 0:
            self._check_supported_type_of_value_in_partition_by()
            self._create_int_partition_id_to_natural_id()
            self._create_natural_id_to_int_partition_id()

        if self._creation_mode == "full":
            if len(self._partition_id_to_indices) == 0:
                self._create_partition_id_to_indices()

            return self.dataset.select(self._partition_id_to_indices[partition_id])
        if self._creation_mode == "lazy":
            return self.dataset.filter(
                lambda x: x == self._partition_id_to_natural_id[partition_id],
                input_columns=self._partition_by,
            )

        raise ValueError(
            f"The `creation_mode` can be only 'full` or 'lazy'."
            f"Instead given: {self._creation_mode}"
        )

    @property
    def num_partitions(self) -> int:
        """Total number of partitions."""
        if len(self._partition_id_to_natural_id) == 0:
            self._check_supported_type_of_value_in_partition_by()
            self._create_int_partition_id_to_natural_id()
            self._create_natural_id_to_int_partition_id()
        return len(self._partition_id_to_natural_id)

    @property
    def partition_id_to_natural_id(self) -> Dict[int, str]:
        """Node id to corresponding natural id present.

        Natural ids are the unique values in `partition_by` column in dataset.
        """
        return self._partition_id_to_natural_id

    # pylint: disable=R0201
    @partition_id_to_natural_id.setter
    def partition_id_to_natural_id(self, value: Dict[int, str]) -> None:
        raise AttributeError(
            "Setting the partition_id_to_natural_id dictionary is not allowed."
        )

    def _check_supported_type_of_value_in_partition_by(self) -> None:
        values = self.dataset[0][self._partition_by]
        values_np = np.array(values)
        dtype = values_np.dtype
        if not (
            np.issubdtype(dtype, np.object_)
            or np.issubdtype(dtype, np.integer)
            or np.issubdtype(dtype, np.str_)
        ):
            raise ValueError(
                f"The specified column in {self._partition_by} is of type {dtype} "
                f"however only ints (with None) and strings (with None) are acceptable."
            )
