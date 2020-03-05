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
"""Flower server strategy."""

from abc import ABC, abstractmethod


class Strategy(ABC):
    """Abstract class to implement custom server strategies."""

    def __init__(self) -> None:
        self.current_round: int = 0

    def next_round(self) -> None:
        """Inform the strategy implementation that the next round of FL has begun."""
        self.current_round += 1

    @abstractmethod
    def should_evaluate(self) -> bool:
        """Decide if the current global model should be evaluated or not."""

    @abstractmethod
    def num_fit_clients(self, num_available_clients: int) -> int:
        """Determine the number of clients used for training."""

    @abstractmethod
    def num_evaluation_clients(self, num_available_clients: int) -> int:
        """Determine the number of clients used for evaluation."""


class DefaultStrategy(Strategy):
    """Strategy implementation used when no custom strategy is provided."""

    def should_evaluate(self) -> bool:
        """Evaluate every round."""
        return True

    def num_fit_clients(self, num_available_clients: int) -> int:
        """Use 10% of available clients for training (minimum: 3)."""
        return int(max(num_available_clients * 0.1, 3))

    def num_evaluation_clients(self, num_available_clients: int) -> int:
        """Use 5% of available clients for evaluation (minimum: 3)."""
        return int(max(num_available_clients * 0.05, 3))
