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
"""Flower client (abstract base class)"""
import unittest
from unittest.mock import MagicMock

import numpy as np

from flower import typing
from flower.grpc_server.grpc_proxy_client import GRPCProxyClient
from flower.proto.transport_pb2 import ClientMessage, Weights

CLIENT_MESSAGE_WEIGHT_UPDATES = ClientMessage(
    weight_update=ClientMessage.WeightUpdate(
        weights=Weights(weights=[]), num_examples=10
    )
)


class GRPCProxyClientTestCase(unittest.TestCase):
    def setUp(self):
        self.bridge_mock = MagicMock()
        self.bridge_factory = lambda: self.bridge_mock

        # Set return_value for usually blocking get_client_message method
        self.bridge_mock.get_client_message.return_value = CLIENT_MESSAGE_WEIGHT_UPDATES

    def test_get_weights(self):
        """This test is currently quite simple and should be improved"""
        # Prepare
        client = GRPCProxyClient(cid="1", bridge_factory=self.bridge_factory)

        # Execute
        value = client.get_weights()

        # Assert
        assert [] == value

    def test_fit(self):
        """This test is currently quite simple and should be improved"""
        # Prepare
        client = GRPCProxyClient(cid="1", bridge_factory=self.bridge_factory)

        # Execute
        weights = [np.ones((2, 2))]
        value = client.fit(weights=weights)

        # Assert
        assert ([], 10) == value

    def test_evaluate(self):
        """This test is currently quite simple and should be improved"""
        # Prepare
        client = GRPCProxyClient(cid="1", bridge_factory=self.bridge_factory)

        # Execute
        value = client.evaluate([])

        # Assert
        assert (1, 1.0) == value
