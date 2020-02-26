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
"""Servicer for FlowerService.

Relevant knowledge for reading this modules code:
    - https://github.com/grpc/grpc/blob/master/doc/statuscodes.md
"""
from typing import Callable, Dict, Iterator

import grpc
from google.protobuf.json_format import MessageToDict

from flower.client_manager import ClientManager
from flower.grpc_server.grpc_proxy_client import GRPCProxyClient
from flower.proto import transport_pb2_grpc
from flower.proto.transport_pb2 import ClientMessage, ServerMessage


class ClientInfoMessageError(Exception):
    """Signifies the first message did not contain a ClientMessage.Info message."""


class ClientManagerRejectionError(Exception):
    """Signifies the client has been rejected by the client manager."""


def default_client_factory(cid: str, info: Dict[str, str]) -> GRPCProxyClient:
    """Return NetworkClient instance."""
    return GRPCProxyClient(cid=cid, info=info)


def register_client(
    client_manager: ClientManager,
    client: GRPCProxyClient,
    context: grpc.ServicerContext,
) -> None:
    """Try registering NetworkClient with ClientManager.
    If not successful raise Exception."""
    if not client_manager.register(client):
        raise ClientManagerRejectionError()

    def rpc_termination_callback():
        client.bridge.close()
        client_manager.unregister(client)

    context.add_callback(rpc_termination_callback)


def is_client_message_info(message: ClientMessage) -> None:
    """Check if message contains a ClientMessage.Info message"""
    if not message.HasField("info"):
        raise ClientInfoMessageError()


def is_not_client_message_info(message: ClientMessage) -> None:
    """Check if message contains other than ClientMessage.Info message"""
    if message.HasField("info"):
        raise ClientInfoMessageError()


class FlowerServiceServicer(transport_pb2_grpc.FlowerServiceServicer):
    """FlowerServiceServicer for bi-directional gRPC instruction stream."""

    def __init__(
        self,
        client_manager: ClientManager,
        client_factory: Callable[
            [str, Dict[str, str]], GRPCProxyClient
        ] = default_client_factory,
    ) -> None:
        self.client_manager: ClientManager = client_manager
        self.client_factory: Callable[
            [str, Dict[str, str]], GRPCProxyClient
        ] = client_factory

    def Join(  # pylint: disable=invalid-name
        self, request_iterator: Iterator[ClientMessage], context: grpc.ServicerContext,
    ) -> Iterator[ServerMessage]:
        """Method will be invoked by each NetworkClient which participates in the network.

        Protocol:
            - The first ClientMessage has always have the connect field set
            - Subsequent messages should not have the connect field set
        """
        client_message_iterator = request_iterator

        yield ServerMessage(info=ServerMessage.GetClientInfo())

        try:
            # TODO: How to timeout this?
            client_message = next(client_message_iterator)
        except StopIteration:
            # This might happen if the remote client side operator
            # is also raising StopIteration. In that case we will
            # just return as nothing happend yet
            return

        try:
            is_client_message_info(client_message)
        except ClientInfoMessageError:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Wrong answer!",
            )
            return

        # A string identifying the peer that invoked the RPC being serviced.
        peer = context.peer()
        info = MessageToDict(client_message.info, including_default_value_fields=True)
        client = self.client_factory(peer, info)

        try:
            # A rpc_termination_callback is registered in the register_client function.
            # The rpc_termination_callback will take care of unregistering the client
            # from the client_manager.
            register_client(self.client_manager, client, context)
        except ClientManagerRejectionError:
            # Definitoin of gRPC Status Code UNAVAILABLE:
            # The service is currently unavailable. This is most likely a transient
            # condition, which can be corrected by retrying with a backoff. Note that
            # it is not always safe to retry non-idempotent operations.
            context.abort(grpc.StatusCode.UNAVAILABLE, "Client registeration failed!")
            return

        # All subsequent messages will be pushed to client bridge directly
        while True:
            server_message = client.bridge.get_server_message()
            yield server_message

            try:
                client_message = next(client_message_iterator)
            except StopIteration:
                break

            client.bridge.set_client_message(client_message)

            # In case its a disconnect message we break out of the
            # loop and unregister the client.
            if client_message.HasField("disconnect"):
                break
