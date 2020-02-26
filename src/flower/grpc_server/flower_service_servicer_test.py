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
"""Tests for FlowerServiceServicer."""
import unittest
from unittest.mock import MagicMock, call

from flower.grpc_server.flower_service_servicer import (
    FlowerServiceServicer,
    default_grpc_client_factory,
    register_client,
)
from flower.grpc_server.grpc_bridge import GRPCBridge
from flower.grpc_server.grpc_proxy_client import GRPCProxyClient
from flower.proto.transport_pb2 import (
    ClientInfo,
    ClientMessage,
    Disconnect,
    ServerMessage,
)

CLIENT_MESSAGE = ClientMessage()
SERVER_MESSAGE = ServerMessage()
CLIENT_CID = "some_client_cid"


class FlowerServiceServicerTestCase(unittest.TestCase):
    """Test suite for class FlowerServiceServicer and helper functions."""

    def setUp(self) -> None:
        """Create mocks for tests."""
        # Mock for the gRPC context argument
        self.context_mock = MagicMock()
        self.context_mock.peer.return_value = CLIENT_CID

        # Define client_messages to be processed by FlowerServiceServicer instance
        self.client_messages = [CLIENT_MESSAGE for _ in range(5)]
        self.client_messages_iterator = iter(self.client_messages)

        # Define corosponding responses from bridge
        self.server_messages = [SERVER_MESSAGE for _ in self.client_messages]
        self.server_messages_iterator = iter(self.server_messages)

        # Mock for GRPCBridge
        self.grpc_bridge_mock = MagicMock()
        self.grpc_bridge_mock.server_message_iterator.return_value = (
            self.server_messages_iterator
        )

        self.grpc_bridge_factory_mock = MagicMock()
        self.grpc_bridge_factory_mock.return_value = self.grpc_bridge_mock

        # Create a NetworkClient mock which we will use to test if correct
        # methods where called and client_messages are getting passed to it
        self.grpc_client_proxy_mock = MagicMock()
        self.grpc_client_proxy_mock.cid = CLIENT_CID

        self.client_factory_mock = MagicMock()
        self.client_factory_mock.return_value = self.grpc_client_proxy_mock

        self.client_manager_mock = MagicMock()

    def test_default_client_factory(self):
        """Confirm that the default client factory returns a NetworkClient."""
        # Prepare
        bridge = self.grpc_bridge_mock

        # Execute
        client = default_grpc_client_factory(cid=CLIENT_CID, bridge=bridge)

        # Assert
        self.assertIsInstance(client, GRPCProxyClient)

    def test_register_client(self):
        """Test register_client function."""
        # Prepare
        self.client_manager_mock.register.return_value = True

        # Execute
        register_client(
            client_manager=self.client_manager_mock,
            client=self.grpc_client_proxy_mock,
            context=self.context_mock,
        )

        # call_args contains the arguments each wrapped in a unittest.mock.call object
        # which holds the args in wrapped in a tuple. Therefore we need to take [0][0]
        rpc_termination_callback = self.context_mock.add_callback.call_args[0][0]
        rpc_termination_callback()

        # Assert
        self.client_manager_mock.register.assert_called_once_with(
            self.grpc_client_proxy_mock
        )
        self.context_mock.add_callback.assert_called_once()
        self.client_manager_mock.unregister.assert_called_once_with(
            self.grpc_client_proxy_mock
        )

    def test_join(self):
        """Test Join method of FlowerServiceServicer."""
        # Prepare

        # Create a instance of FlowerServiceServicer
        servicer = FlowerServiceServicer(
            client_manager=self.client_manager_mock,
            grpc_bridge_factory=self.grpc_bridge_factory_mock,
            grpc_client_factory=self.client_factory_mock,
        )

        # Execute
        server_message_iterator = servicer.Join(
            self.client_messages_iterator, self.context_mock
        )

        # Assert
        num_server_messages = 0

        for server_message in server_message_iterator:
            num_server_messages += 1
            assert isinstance(server_message, ServerMessage)

        assert len(self.client_messages) == num_server_messages
        assert self.grpc_client_proxy_mock.cid == CLIENT_CID

        # After the first client_message is processed the CLIENT_MESSAGE_CONNECT
        # the ClientFactory should have been called
        self.client_factory_mock.assert_called_once_with(
            cid=CLIENT_CID, bridge=self.grpc_bridge_mock
        )

        # Check if the client was registered with the client_manager
        self.client_manager_mock.register.assert_called_once_with(
            self.grpc_client_proxy_mock
        )

        self.grpc_bridge_mock.set_client_message.assert_has_calls(
            [call(message) for message in self.client_messages]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
