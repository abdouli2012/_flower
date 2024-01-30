# Copyright 2020 Flower Labs GmbH. All Rights Reserved.
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
"""Tests for module connection."""


import concurrent.futures
import socket
from contextlib import closing
from typing import Iterator, cast
from unittest.mock import patch

import grpc

from flwr.common import recordset_compat as compat
from flwr.common.configsrecord import ConfigsRecord
from flwr.common.constant import TASK_TYPE_GET_PROPERTIES
from flwr.common.message import Message, Metadata
from flwr.common.recordset import RecordSet
from flwr.common.typing import Code, GetPropertiesRes, Status
from flwr.proto.transport_pb2 import (  # pylint: disable=E0611
    ClientMessage,
    ServerMessage,
)
from flwr.server.client_manager import SimpleClientManager
from flwr.server.fleet.grpc_bidi.grpc_server import start_grpc_server

from .connection import grpc_connection

EXPECTED_NUM_SERVER_MESSAGE = 10

SERVER_MESSAGE = ServerMessage(get_properties_ins=ServerMessage.GetPropertiesIns())
SERVER_MESSAGE_RECONNECT = ServerMessage(reconnect_ins=ServerMessage.ReconnectIns())

MESSAGE_GET_PROPERTIES = Message(
    metadata=Metadata(
        run_id=0,
        task_id="",
        group_id="",
        ttl="",
        task_type=TASK_TYPE_GET_PROPERTIES,
    ),
    message=compat.getpropertiesres_to_recordset(
        GetPropertiesRes(Status(Code.OK, ""), {})
    ),
)
MESSAGE_DISCONNECT = Message(
    metadata=Metadata(
        run_id=0,
        task_id="",
        group_id="",
        ttl="",
        task_type="reconnect",
    ),
    message=RecordSet(configs={"config": ConfigsRecord({"reason": 0})}),
)


def unused_tcp_port() -> int:
    """Return an unused port."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return cast(int, sock.getsockname()[1])


def mock_join(  # type: ignore # pylint: disable=invalid-name
    _self,
    request_iterator: Iterator[ClientMessage],
    _context: grpc.ServicerContext,
) -> Iterator[ServerMessage]:
    """Serve as mock for the Join method of class FlowerServiceServicer."""
    counter = 0

    while True:
        counter += 1

        if counter < EXPECTED_NUM_SERVER_MESSAGE:
            yield SERVER_MESSAGE
        else:
            yield SERVER_MESSAGE_RECONNECT

        try:
            client_message = next(request_iterator)
            if client_message.HasField("disconnect_res"):
                break
        except StopIteration:
            break


@patch(
    "flwr.server.fleet.grpc_bidi.flower_service_servicer.FlowerServiceServicer.Join",
    mock_join,
)
def test_integration_connection() -> None:
    """Create a server and establish a connection to it.

    Purpose of this integration test is to simulate multiple clients with multiple
    roundtrips between server and client.
    """
    # Prepare
    port = unused_tcp_port()

    server = start_grpc_server(
        client_manager=SimpleClientManager(), server_address=f"[::]:{port}"
    )

    # Execute
    # Multiple clients in parallel
    def run_client() -> int:
        messages_received: int = 0

        with grpc_connection(server_address=f"[::]:{port}", insecure=True) as conn:
            receive, send, _, _ = conn

            # Setup processing loop
            while True:
                # Block until server responds with a message
                message = receive()

                messages_received += 1
                if message.metadata.task_type == "reconnect":  # type: ignore
                    send(MESSAGE_DISCONNECT)
                    break

                # Process server_message and send client_message...
                send(MESSAGE_GET_PROPERTIES)

        return messages_received

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_client) for _ in range(3)]
        concurrent.futures.wait(futures)
        for future in futures:
            results.append(future.result())

    # Assert
    for messages_received in results:
        assert messages_received == EXPECTED_NUM_SERVER_MESSAGE

    # Teardown
    server.stop(1)
