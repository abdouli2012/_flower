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
"""Tests for module server."""

from flower.client_manager import SimpleClientManager
from flower.transport.flower_service_servicer import FlowerServiceServicer
from flower.transport.server import create_server
from flower_testing import network


def test_integration_create_and_shutdown_server():
    """Create server and check if FlowerServiceServicer is returned."""
    # Prepare
    port = network.unused_tcp_port()
    client_manager = SimpleClientManager()

    # Execute
    servicer, server = create_server(client_manager=client_manager, port=port)

    # Assert
    assert isinstance(servicer, FlowerServiceServicer)

    # Teardown
    server.stop(1)
