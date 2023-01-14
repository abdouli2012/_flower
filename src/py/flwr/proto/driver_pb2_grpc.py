# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from flwr.proto import driver_pb2 as flwr_dot_proto_dot_driver__pb2


class DriverStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetNodes = channel.unary_unary(
                '/flwr.proto.Driver/GetNodes',
                request_serializer=flwr_dot_proto_dot_driver__pb2.GetNodesRequest.SerializeToString,
                response_deserializer=flwr_dot_proto_dot_driver__pb2.GetNodesResponse.FromString,
                )
        self.PushTaskIns = channel.unary_unary(
                '/flwr.proto.Driver/PushTaskIns',
                request_serializer=flwr_dot_proto_dot_driver__pb2.PushTaskInsRequest.SerializeToString,
                response_deserializer=flwr_dot_proto_dot_driver__pb2.PushTaskInsResponse.FromString,
                )
        self.PullTaskRes = channel.unary_unary(
                '/flwr.proto.Driver/PullTaskRes',
                request_serializer=flwr_dot_proto_dot_driver__pb2.PullTaskResRequest.SerializeToString,
                response_deserializer=flwr_dot_proto_dot_driver__pb2.PullTaskResResponse.FromString,
                )


class DriverServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetNodes(self, request, context):
        """Return a set of nodes
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PushTaskIns(self, request, context):
        """Create one or more tasks
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PullTaskRes(self, request, context):
        """Get task results
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DriverServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetNodes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNodes,
                    request_deserializer=flwr_dot_proto_dot_driver__pb2.GetNodesRequest.FromString,
                    response_serializer=flwr_dot_proto_dot_driver__pb2.GetNodesResponse.SerializeToString,
            ),
            'PushTaskIns': grpc.unary_unary_rpc_method_handler(
                    servicer.PushTaskIns,
                    request_deserializer=flwr_dot_proto_dot_driver__pb2.PushTaskInsRequest.FromString,
                    response_serializer=flwr_dot_proto_dot_driver__pb2.PushTaskInsResponse.SerializeToString,
            ),
            'PullTaskRes': grpc.unary_unary_rpc_method_handler(
                    servicer.PullTaskRes,
                    request_deserializer=flwr_dot_proto_dot_driver__pb2.PullTaskResRequest.FromString,
                    response_serializer=flwr_dot_proto_dot_driver__pb2.PullTaskResResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'flwr.proto.Driver', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Driver(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetNodes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/flwr.proto.Driver/GetNodes',
            flwr_dot_proto_dot_driver__pb2.GetNodesRequest.SerializeToString,
            flwr_dot_proto_dot_driver__pb2.GetNodesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PushTaskIns(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/flwr.proto.Driver/PushTaskIns',
            flwr_dot_proto_dot_driver__pb2.PushTaskInsRequest.SerializeToString,
            flwr_dot_proto_dot_driver__pb2.PushTaskInsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PullTaskRes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/flwr.proto.Driver/PullTaskRes',
            flwr_dot_proto_dot_driver__pb2.PullTaskResRequest.SerializeToString,
            flwr_dot_proto_dot_driver__pb2.PullTaskResResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
