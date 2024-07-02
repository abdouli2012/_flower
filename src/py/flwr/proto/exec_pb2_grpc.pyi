"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import flwr.proto.exec_pb2
import grpc
import typing

class ExecStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    StartRun: grpc.UnaryUnaryMultiCallable[
        flwr.proto.exec_pb2.StartRunRequest,
        flwr.proto.exec_pb2.StartRunResponse]
    """Start run upon request"""

    StreamLogs: grpc.UnaryStreamMultiCallable[
        flwr.proto.exec_pb2.StreamLogsRequest,
        flwr.proto.exec_pb2.StreamLogsResponse]
    """Start log stream upon request"""


class ExecServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def StartRun(self,
        request: flwr.proto.exec_pb2.StartRunRequest,
        context: grpc.ServicerContext,
    ) -> flwr.proto.exec_pb2.StartRunResponse:
        """Start run upon request"""
        pass

    @abc.abstractmethod
    def StreamLogs(self,
        request: flwr.proto.exec_pb2.StreamLogsRequest,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[flwr.proto.exec_pb2.StreamLogsResponse]:
        """Start log stream upon request"""
        pass


def add_ExecServicer_to_server(servicer: ExecServicer, server: grpc.Server) -> None: ...
