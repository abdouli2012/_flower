# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import transport_pb2 as transport__pb2


class ClientManagerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Connect = channel.stream_stream(
        '/ClientManager/Connect',
        request_serializer=transport__pb2.ClientMessage.SerializeToString,
        response_deserializer=transport__pb2.ServerMessage.FromString,
        )


class ClientManagerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Connect(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ClientManagerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Connect': grpc.stream_stream_rpc_method_handler(
          servicer.Connect,
          request_deserializer=transport__pb2.ClientMessage.FromString,
          response_serializer=transport__pb2.ServerMessage.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ClientManager', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
