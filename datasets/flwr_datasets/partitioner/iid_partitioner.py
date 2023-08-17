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
"""Iid partitioner class that works with HuggingFace Dataset."""


import datasets
from flwr_datasets.partitioner.partitioner import Partitioner


class IidPartitioner(Partitioner):
    """Partitioner creates each partition sampled randomly from the dataset.

    Parameters
    ----------
    num_partitions: int
        The total number of partitions that the data will be divided into.
    """

    def __init__(self, num_partitions: int) -> None:
        super().__init__()
        self._num_partitions = num_partitions

    def load_partition(self, partition_index: int) -> datasets.Dataset:
        """Load a single iid partition based on the partition index."""
        self._check_if_dataset_assigned()
        return self.dataset.shard(
            num_shards=self._num_partitions, index=partition_index, contiguous=True
        )
