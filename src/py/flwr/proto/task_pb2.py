# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/task.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import node_pb2 as flwr_dot_proto_dot_node__pb2
from flwr.proto import transport_pb2 as flwr_dot_proto_dot_transport__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66lwr/proto/task.proto\x12\nflwr.proto\x1a\x15\x66lwr/proto/node.proto\x1a\x1a\x66lwr/proto/transport.proto\"\x93\x02\n\x04Task\x12\"\n\x08producer\x18\x01 \x01(\x0b\x32\x10.flwr.proto.Node\x12\"\n\x08\x63onsumer\x18\x02 \x01(\x0b\x32\x10.flwr.proto.Node\x12\x12\n\ncreated_at\x18\x03 \x01(\t\x12\x14\n\x0c\x64\x65livered_at\x18\x04 \x01(\t\x12\x0b\n\x03ttl\x18\x05 \x01(\t\x12\x10\n\x08\x61ncestry\x18\x06 \x03(\t\x12<\n\x15legacy_server_message\x18\x65 \x01(\x0b\x32\x19.flwr.proto.ServerMessageB\x02\x18\x01\x12<\n\x15legacy_client_message\x18\x66 \x01(\x0b\x32\x19.flwr.proto.ClientMessageB\x02\x18\x01\"a\n\x07TaskIns\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\t\x12\x13\n\x0bworkload_id\x18\x03 \x01(\t\x12\x1e\n\x04task\x18\x04 \x01(\x0b\x32\x10.flwr.proto.Task\"a\n\x07TaskRes\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\t\x12\x13\n\x0bworkload_id\x18\x03 \x01(\t\x12\x1e\n\x04task\x18\x04 \x01(\x0b\x32\x10.flwr.proto.Taskb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flwr.proto.task_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TASK.fields_by_name['legacy_server_message']._options = None
  _TASK.fields_by_name['legacy_server_message']._serialized_options = b'\030\001'
  _TASK.fields_by_name['legacy_client_message']._options = None
  _TASK.fields_by_name['legacy_client_message']._serialized_options = b'\030\001'
  _TASK._serialized_start=89
  _TASK._serialized_end=364
  _TASKINS._serialized_start=366
  _TASKINS._serialized_end=463
  _TASKRES._serialized_start=465
  _TASKRES._serialized_end=562
# @@protoc_insertion_point(module_scope)
