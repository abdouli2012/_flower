# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/exec.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66lwr/proto/exec.proto\x12\nflwr.proto\"\xa4\x01\n\x0fStartRunRequest\x12\x10\n\x08\x66\x61\x62_file\x18\x01 \x01(\x0c\x12H\n\x0foverride_config\x18\x02 \x03(\x0b\x32/.flwr.proto.StartRunRequest.OverrideConfigEntry\x1a\x35\n\x13OverrideConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\"\n\x10StartRunResponse\x12\x0e\n\x06run_id\x18\x01 \x01(\x03\"#\n\x11StreamLogsRequest\x12\x0e\n\x06run_id\x18\x01 \x01(\x03\"(\n\x12StreamLogsResponse\x12\x12\n\nlog_output\x18\x01 \x01(\t2\xa0\x01\n\x04\x45xec\x12G\n\x08StartRun\x12\x1b.flwr.proto.StartRunRequest\x1a\x1c.flwr.proto.StartRunResponse\"\x00\x12O\n\nStreamLogs\x12\x1d.flwr.proto.StreamLogsRequest\x1a\x1e.flwr.proto.StreamLogsResponse\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flwr.proto.exec_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._options = None
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._serialized_options = b'8\001'
  _globals['_STARTRUNREQUEST']._serialized_start=38
  _globals['_STARTRUNREQUEST']._serialized_end=202
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._serialized_start=149
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._serialized_end=202
  _globals['_STARTRUNRESPONSE']._serialized_start=204
  _globals['_STARTRUNRESPONSE']._serialized_end=238
  _globals['_STREAMLOGSREQUEST']._serialized_start=240
  _globals['_STREAMLOGSREQUEST']._serialized_end=275
  _globals['_STREAMLOGSRESPONSE']._serialized_start=277
  _globals['_STREAMLOGSRESPONSE']._serialized_end=317
  _globals['_EXEC']._serialized_start=320
  _globals['_EXEC']._serialized_end=480
# @@protoc_insertion_point(module_scope)
