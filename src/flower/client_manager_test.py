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
"""Tests for Flower ClientManager."""

from unittest.mock import MagicMock

from flower.client_manager import SimpleClientManager
from flower.grpc_server.grpc_proxy_client import GRPCProxyClient


def test_simple_client_manager_register():
    """Tests if the register method works correctly"""
    # Prepare
    cid = "1"
    bridge = MagicMock()
    client = GRPCProxyClient(cid=cid, bridge=bridge)
    client_manager = SimpleClientManager()

    # Execute
    first = client_manager.register(client)
    second = client_manager.register(client)

    # Assert
    assert first
    assert not second
    assert len(client_manager) == 1


def test_simple_client_manager_unregister():
    """Tests if the unregister method works correctly"""
    # Prepare
    cid = "1"
    bridge = MagicMock()
    client = GRPCProxyClient(cid=cid, bridge=bridge)
    client_manager = SimpleClientManager()
    client_manager.register(client)

    # Execute
    client_manager.unregister(client)

    # Assert
    assert len(client_manager) == 0
