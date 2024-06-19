# Copyright 2024 Flower Labs GmbH. All Rights Reserved.
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
# source: flwr/proto/fab.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x66lwr/proto/fab.proto\x12\nflwr.proto\"$\n\x03\x46\x61\x62\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\x1d\n\rGetFabRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\".\n\x0eGetFabResponse\x12\x1c\n\x03\x66\x61\x62\x18\x01 \x01(\x0b\x32\x0f.flwr.proto.Fabb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flwr.proto.fab_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FAB']._serialized_start=36
  _globals['_FAB']._serialized_end=72
  _globals['_GETFABREQUEST']._serialized_start=74
  _globals['_GETFABREQUEST']._serialized_end=103
  _globals['_GETFABRESPONSE']._serialized_start=105
  _globals['_GETFABRESPONSE']._serialized_end=151
# @@protoc_insertion_point(module_scope)