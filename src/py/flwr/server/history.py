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
"""Training history."""

from functools import reduce
from typing import Dict, List, Tuple

from flwr.common.typing import Scalar


class History:
    """History class for training and/or evaluation metrics collection."""

    def __init__(self) -> None:
        self.losses_distributed: List[Tuple[int, float]] = []
        self.losses_centralized: List[Tuple[int, float]] = []
        self.metrics_distributed: Dict[str, List[Tuple[int, Scalar]]] = {}
        self.metrics_centralized: Dict[str, List[Tuple[int, Scalar]]] = {}
        self.clip_norms: List[Tuple[int, float]] = []
    def add_clip_norm(self, rnd:int, clip_norm: float) -> None:
        """Add one clip norm entry."""
        self.clip_norms.append((rnd, clip_norm))

    def add_loss_distributed(self, rnd: int, loss: float) -> None:
        """Add one loss entry (from distributed evaluation)."""
        self.losses_distributed.append((rnd, loss))

    def add_loss_centralized(self, rnd: int, loss: float) -> None:
        """Add one loss entry (from centralized evaluation)."""
        self.losses_centralized.append((rnd, loss))

    def add_metrics_distributed(self, rnd: int, metrics: Dict[str, Scalar]) -> None:
        """Add metrics entries (from distributed evaluation)."""
        for key in metrics:
            # if not (isinstance(metrics[key], float) or isinstance(metrics[key], int)):
            #     continue  # ignore non-numeric key/value pairs
            if key not in self.metrics_distributed:
                self.metrics_distributed[key] = []
            self.metrics_distributed[key].append((rnd, metrics[key]))

    def add_metrics_centralized(self, rnd: int, metrics: Dict[str, Scalar]) -> None:
        """Add metrics entries (from centralized evaluation)."""
        for key in metrics:
            # if not (isinstance(metrics[key], float) or isinstance(metrics[key], int)):
            #     continue  # ignore non-numeric key/value pairs
            if key not in self.metrics_centralized:
                self.metrics_centralized[key] = []
            self.metrics_centralized[key].append((rnd, metrics[key]))

    def __repr__(self) -> str:
        rep = ""
        if self.losses_distributed:
            rep += "History (loss, distributed):\n" + reduce(
                lambda a, b: a + b,
                [f"\tround {rnd}: {loss}\n" for rnd, loss in self.losses_distributed],
            )
        if self.losses_centralized:
            rep += "History (loss, centralized):\n" + reduce(
                lambda a, b: a + b,
                [f"\tround {rnd}: {loss}\n" for rnd, loss in self.losses_centralized],
            )
        if self.metrics_distributed:
            rep += "History (metrics, distributed):\n" + str(self.metrics_distributed)
        if self.metrics_centralized:
            rep += "History (metrics, centralized):\n" + str(self.metrics_centralized)
        return rep
