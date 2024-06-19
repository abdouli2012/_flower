# Copyright 2022 Flower Labs GmbH. All Rights Reserved.
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
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/task.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import node_pb2 as flwr_dot_proto_dot_node__pb2
from flwr.proto import recordset_pb2 as flwr_dot_proto_dot_recordset__pb2
from flwr.proto import transport_pb2 as flwr_dot_proto_dot_transport__pb2
from flwr.proto import error_pb2 as flwr_dot_proto_dot_error__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66lwr/proto/task.proto\x12\nflwr.proto\x1a\x15\x66lwr/proto/node.proto\x1a\x1a\x66lwr/proto/recordset.proto\x1a\x1a\x66lwr/proto/transport.proto\x1a\x16\x66lwr/proto/error.proto\"\x89\x02\n\x04Task\x12\"\n\x08producer\x18\x01 \x01(\x0b\x32\x10.flwr.proto.Node\x12\"\n\x08\x63onsumer\x18\x02 \x01(\x0b\x32\x10.flwr.proto.Node\x12\x12\n\ncreated_at\x18\x03 \x01(\x01\x12\x14\n\x0c\x64\x65livered_at\x18\x04 \x01(\t\x12\x11\n\tpushed_at\x18\x05 \x01(\x01\x12\x0b\n\x03ttl\x18\x06 \x01(\x01\x12\x10\n\x08\x61ncestry\x18\x07 \x03(\t\x12\x11\n\ttask_type\x18\x08 \x01(\t\x12(\n\trecordset\x18\t \x01(\x0b\x32\x15.flwr.proto.RecordSet\x12 \n\x05\x65rror\x18\n \x01(\x0b\x32\x11.flwr.proto.Error\"\\\n\x07TaskIns\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\t\x12\x0e\n\x06run_id\x18\x03 \x01(\x12\x12\x1e\n\x04task\x18\x04 \x01(\x0b\x32\x10.flwr.proto.Task\"\\\n\x07TaskRes\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\t\x12\x0e\n\x06run_id\x18\x03 \x01(\x12\x12\x1e\n\x04task\x18\x04 \x01(\x0b\x32\x10.flwr.proto.Taskb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flwr.proto.task_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TASK']._serialized_start=141
  _globals['_TASK']._serialized_end=406
  _globals['_TASKINS']._serialized_start=408
  _globals['_TASKINS']._serialized_end=500
  _globals['_TASKRES']._serialized_start=502
  _globals['_TASKRES']._serialized_end=594
# @@protoc_insertion_point(module_scope)