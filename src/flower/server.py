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
"""Flower server."""


import concurrent.futures
from functools import reduce
from logging import DEBUG, INFO
from typing import List, Optional, Tuple

import numpy as np

from flower.client import Client
from flower.client_manager import ClientManager
from flower.history import History
from flower.logger import log
from flower.strategy import DefaultStrategy, Strategy
from flower.typing import Weights


class Server:
    """Flower server."""

    def __init__(
        self, client_manager: ClientManager, strategy: Optional[Strategy] = None
    ) -> None:
        self._client_manager: ClientManager = client_manager
        self.weights: Weights = []
        self.strategy: Strategy = strategy if strategy is not None else DefaultStrategy()

    def client_manager(self) -> ClientManager:
        """Return ClientManager."""
        return self._client_manager

    def fit(self, num_rounds: int) -> History:
        """Run federated averaging for a number of rounds"""
        # Initialize weights by asking one client to return theirs
        self.weights = self._get_initial_weights()
        res = self.strategy.evaluate(weights=self.weights)
        if res is not None:
            log(
                INFO, "initial weights (loss/accuracy): %s, %s", res[0], res[1],
            )

        # Run federated averaging for num_rounds
        history = History()
        for current_round in range(1, num_rounds + 1):
            # Refine model
            self.fit_round()

            # Evaluate model using strategy implementation
            res = self.strategy.evaluate(weights=self.weights)
            if res is not None:
                log(
                    INFO,
                    "progress (round/loss/accuracy): %s, %s, %s",
                    current_round,
                    res[0],
                    res[1],
                )
                history.add_loss_centralized(rnd=current_round, loss=res[0])
                history.add_accuracy_centralized(rnd=current_round, acc=res[1])

            # Evaluate model on a sample of available clients
            if self.strategy.should_evaluate():
                loss_avg = self.evaluate()
                history.add_loss_distributed(rnd=current_round, loss=loss_avg)

            # Inform strategy that the next round is about to begin
            self.strategy.next_round()
        return history

    def evaluate(self) -> float:
        """Validate current global model on a number of clients"""
        # Sample clients for evaluation
        sample_size, min_num_clients = self.strategy.num_evaluation_clients(
            self._client_manager.num_available()
        )
        log(
            DEBUG,
            "evaluate: sample %s cids once %s clients are available",
            sample_size,
            min_num_clients,
        )
        clients = self._client_manager.sample(
            num_clients=sample_size, min_num_clients=min_num_clients
        )
        log(
            DEBUG,
            "evaluate: sampled %s cids: %s",
            len(clients),
            [c.cid for c in clients],
        )

        # Evaluate current global weights on those clients
        results, failures = eval_clients(clients, self.weights)
        log(
            DEBUG,
            "evaluate received %s results and %s failures",
            len(results),
            len(failures),
        )
        # Aggregate the evaluation results
        return weighted_loss_avg(results)

    def fit_round(self) -> None:
        """Perform a single round of federated averaging"""
        # Sample a number of clients (dependent on the strategy)
        sample_size, min_num_clients = self.strategy.num_fit_clients(
            self._client_manager.num_available()
        )
        log(
            DEBUG,
            "fit_round: sample %s cids once %s clients are available",
            sample_size,
            min_num_clients,
        )
        clients = self._client_manager.sample(
            num_clients=sample_size, min_num_clients=min_num_clients
        )
        log(
            DEBUG,
            "fit_round: sampled %s cids: %s",
            len(clients),
            [c.cid for c in clients],
        )

        # Collect training results from all clients participating in this round
        results, failures = fit_clients(clients, self.weights)
        log(
            DEBUG,
            "fit_round received %s results and %s failures",
            len(results),
            len(failures),
        )

        # Aggregate training results and replace previous global model
        if results:
            weights_prime = aggregate(results)
            self.weights = weights_prime

    def _get_initial_weights(self) -> Weights:
        """Get initial weights from one of the available clients"""
        random_client = self._client_manager.sample(1)[0]
        return random_client.get_weights()


def fit_clients(
    clients: List[Client], weights: Weights
) -> Tuple[List[Tuple[Weights, int]], List[BaseException]]:
    """Refine weights concurrently on all selected clients"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fit_client, c, weights) for c in clients]
        concurrent.futures.wait(futures)
    # Gather results
    results: List[Tuple[Weights, int]] = []
    failures: List[BaseException] = []
    for future in futures:
        failure = future.exception()
        if failure is not None:
            failures.append(failure)
        else:
            # Success case
            results.append(future.result())
    return results, failures


def fit_client(client: Client, weights: Weights) -> Tuple[Weights, int]:
    """Refine weights on a single client"""
    return client.fit(weights)


def eval_clients(
    clients: List[Client], weights: Weights
) -> Tuple[List[Tuple[int, float]], List[BaseException]]:
    """Evaluate weights concurrently on all selected clients"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(eval_client, c, weights) for c in clients]
        concurrent.futures.wait(futures)
    # Gather results
    results: List[Tuple[int, float]] = []
    failures: List[BaseException] = []
    for future in futures:
        failure = future.exception()
        if failure is not None:
            failures.append(failure)
        else:
            # Success case
            results.append(future.result())
    return results, failures


def eval_client(client: Client, weights: Weights) -> Tuple[int, float]:
    """Evaluate weights on a single client"""
    return client.evaluate(weights)


def aggregate(results: List[Tuple[Weights, int]]) -> Weights:
    """Compute weighted average"""
    # Calculate the total number of examples used during training
    num_examples_total = sum([num_examples for _, num_examples in results])

    # Create a list of weights, each multiplied by the related number of examples
    weighted_weights = [
        [layer * num_examples for layer in weights] for weights, num_examples in results
    ]

    # Compute average weights of each layer
    weights_prime: Weights = [
        reduce(np.add, layer_updates) / num_examples_total
        for layer_updates in zip(*weighted_weights)
    ]
    return weights_prime


def weighted_loss_avg(results: List[Tuple[int, float]]) -> float:
    """Aggregate evaluation results obtained from multiple clients"""
    num_total_evaluation_examples = sum([num_examples for num_examples, _ in results])
    weighted_losses = [num_examples * loss for num_examples, loss in results]
    return sum(weighted_losses) / num_total_evaluation_examples
