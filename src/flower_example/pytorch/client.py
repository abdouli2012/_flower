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
"""Flower client example using PyTorch for CIFAR-10 image classification."""


import argparse
import timeit

import torch
import torchvision

import flower as fl

from . import DEFAULT_SERVER_ADDRESS, cifar


class CifarClient(fl.Client):
    """Flower client implementing CIFAR-10 image classification using PyTorch."""

    def __init__(
        self,
        cid: str,
        model: cifar.Net,
        trainset: torchvision.datasets.CIFAR10,
        testset: torchvision.datasets.CIFAR10,
    ) -> None:
        super().__init__(cid)
        self.model = model
        self.trainset = trainset
        self.testset = testset

    def get_parameters(self) -> fl.ParametersRes:
        weights: fl.Weights = self.model.get_weights()
        parameters = fl.weights_to_parameters(weights)
        return fl.ParametersRes(parameters=parameters)

    def fit(self, ins: fl.FitIns) -> fl.FitRes:
        weights: fl.Weights = fl.parameters_to_weights(ins[0])
        config = ins[1]
        fit_begin = timeit.default_timer()

        # Get training config
        epochs = int(config["epochs"])
        batch_size = int(config["batch_size"])

        # Set model parameters
        self.model.set_weights(weights)

        # Train model
        trainloader = torch.utils.data.DataLoader(  # type: ignore
            self.trainset, batch_size=batch_size, shuffle=True
        )
        cifar.train(self.model, trainloader, epochs=epochs)

        # Return the refined weights and the number of examples used for training
        weights_prime: fl.Weights = self.model.get_weights()
        params_prime = fl.weights_to_parameters(weights_prime)
        num_examples_train = len(self.trainset)
        fit_duration = timeit.default_timer() - fit_begin
        return params_prime, num_examples_train, num_examples_train, fit_duration

    def evaluate(self, ins: fl.EvaluateIns) -> fl.EvaluateRes:
        weights = fl.parameters_to_weights(ins[0])
        config = ins[1]

        # Get evaluation config
        batch_size = int(config["batch_size"])

        # Use provided weights to update the local model
        self.model.set_weights(weights)

        # Evaluate the updated model on the local dataset
        testloader = torch.utils.data.DataLoader(  # type: ignore
            self.testset, batch_size=batch_size, shuffle=False
        )
        loss, accuracy = cifar.test(self.model, testloader)

        # Return the number of evaluation examples and the evaluation result (loss)
        return len(self.testset), float(loss), float(accuracy)


def main() -> None:
    """Load data, create and start CifarClient."""
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument(
        "--server_address",
        type=str,
        default=DEFAULT_SERVER_ADDRESS,
        help=f"gRPC server address (default: {DEFAULT_SERVER_ADDRESS})",
    )
    parser.add_argument(
        "--cid", type=str, required=True, help="Client CID (no default)"
    )
    parser.add_argument(
        "--partition", type=int, required=True, help="Partition index (no default)"
    )
    parser.add_argument(
        "--clients", type=int, required=True, help="Number of clients (no default)",
    )
    args = parser.parse_args()

    # Load model and data
    model = cifar.load_model()
    trainset, testset = cifar.load_data(
        partition=args.partition, num_partitions=args.clients
    )

    # Start client
    client = CifarClient(args.cid, model, trainset, testset)
    fl.app.start_client(args.server_address, client)


if __name__ == "__main__":
    main()
