# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/recordset.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x66lwr/proto/recordset.proto\x12\nflwr.proto\"\x1a\n\nDoubleList\x12\x0c\n\x04list\x18\x01 \x03(\x01\"\x1a\n\nSint64List\x12\x0c\n\x04list\x18\x01 \x03(\x12\"\x18\n\x08\x42oolList\x12\x0c\n\x04list\x18\x01 \x03(\x08\"\x1a\n\nStringList\x12\x0c\n\x04list\x18\x01 \x03(\t\"\x19\n\tBytesList\x12\x0c\n\x04list\x18\x01 \x03(\x0c\"B\n\x05\x41rray\x12\r\n\x05\x64type\x18\x01 \x01(\t\x12\r\n\x05shape\x18\x02 \x03(\x05\x12\r\n\x05stype\x18\x03 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\"\x9f\x01\n\x12MetricsRecordValue\x12\x10\n\x06\x64ouble\x18\x01 \x01(\x01H\x00\x12\x10\n\x06sint64\x18\x02 \x01(\x12H\x00\x12-\n\x0b\x64ouble_list\x18\x15 \x01(\x0b\x32\x16.flwr.proto.DoubleListH\x00\x12-\n\x0bsint64_list\x18\x16 \x01(\x0b\x32\x16.flwr.proto.Sint64ListH\x00\x42\x07\n\x05value\"\xd9\x02\n\x12\x43onfigsRecordValue\x12\x10\n\x06\x64ouble\x18\x01 \x01(\x01H\x00\x12\x10\n\x06sint64\x18\x02 \x01(\x12H\x00\x12\x0e\n\x04\x62ool\x18\x03 \x01(\x08H\x00\x12\x10\n\x06string\x18\x04 \x01(\tH\x00\x12\x0f\n\x05\x62ytes\x18\x05 \x01(\x0cH\x00\x12-\n\x0b\x64ouble_list\x18\x15 \x01(\x0b\x32\x16.flwr.proto.DoubleListH\x00\x12-\n\x0bsint64_list\x18\x16 \x01(\x0b\x32\x16.flwr.proto.Sint64ListH\x00\x12)\n\tbool_list\x18\x17 \x01(\x0b\x32\x14.flwr.proto.BoolListH\x00\x12-\n\x0bstring_list\x18\x18 \x01(\x0b\x32\x16.flwr.proto.StringListH\x00\x12+\n\nbytes_list\x18\x19 \x01(\x0b\x32\x15.flwr.proto.BytesListH\x00\x42\x07\n\x05value\"M\n\x10ParametersRecord\x12\x11\n\tdata_keys\x18\x01 \x03(\t\x12&\n\x0b\x64\x61ta_values\x18\x02 \x03(\x0b\x32\x11.flwr.proto.Array\"\x8f\x01\n\rMetricsRecord\x12\x31\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32#.flwr.proto.MetricsRecord.DataEntry\x1aK\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12-\n\x05value\x18\x02 \x01(\x0b\x32\x1e.flwr.proto.MetricsRecordValue:\x02\x38\x01\"\x8f\x01\n\rConfigsRecord\x12\x31\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32#.flwr.proto.ConfigsRecord.DataEntry\x1aK\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12-\n\x05value\x18\x02 \x01(\x0b\x32\x1e.flwr.proto.ConfigsRecordValue:\x02\x38\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flwr.proto.recordset_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_METRICSRECORD_DATAENTRY']._options = None
  _globals['_METRICSRECORD_DATAENTRY']._serialized_options = b'8\001'
  _globals['_CONFIGSRECORD_DATAENTRY']._options = None
  _globals['_CONFIGSRECORD_DATAENTRY']._serialized_options = b'8\001'
  _globals['_DOUBLELIST']._serialized_start=42
  _globals['_DOUBLELIST']._serialized_end=68
  _globals['_SINT64LIST']._serialized_start=70
  _globals['_SINT64LIST']._serialized_end=96
  _globals['_BOOLLIST']._serialized_start=98
  _globals['_BOOLLIST']._serialized_end=122
  _globals['_STRINGLIST']._serialized_start=124
  _globals['_STRINGLIST']._serialized_end=150
  _globals['_BYTESLIST']._serialized_start=152
  _globals['_BYTESLIST']._serialized_end=177
  _globals['_ARRAY']._serialized_start=179
  _globals['_ARRAY']._serialized_end=245
  _globals['_METRICSRECORDVALUE']._serialized_start=248
  _globals['_METRICSRECORDVALUE']._serialized_end=407
  _globals['_CONFIGSRECORDVALUE']._serialized_start=410
  _globals['_CONFIGSRECORDVALUE']._serialized_end=755
  _globals['_PARAMETERSRECORD']._serialized_start=757
  _globals['_PARAMETERSRECORD']._serialized_end=834
  _globals['_METRICSRECORD']._serialized_start=837
  _globals['_METRICSRECORD']._serialized_end=980
  _globals['_METRICSRECORD_DATAENTRY']._serialized_start=905
  _globals['_METRICSRECORD_DATAENTRY']._serialized_end=980
  _globals['_CONFIGSRECORD']._serialized_start=983
  _globals['_CONFIGSRECORD']._serialized_end=1126
  _globals['_CONFIGSRECORD_DATAENTRY']._serialized_start=1051
  _globals['_CONFIGSRECORD_DATAENTRY']._serialized_end=1126
# @@protoc_insertion_point(module_scope)
