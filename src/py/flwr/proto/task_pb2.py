# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/task.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import node_pb2 as flwr_dot_proto_dot_node__pb2
from flwr.proto import transport_pb2 as flwr_dot_proto_dot_transport__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66lwr/proto/task.proto\x12\nflwr.proto\x1a\x15\x66lwr/proto/node.proto\x1a\x1a\x66lwr/proto/transport.proto\"\xbe\x02\n\x04Task\x12\"\n\x08producer\x18\x01 \x01(\x0b\x32\x10.flwr.proto.Node\x12\"\n\x08\x63onsumer\x18\x02 \x01(\x0b\x32\x10.flwr.proto.Node\x12\x12\n\ncreated_at\x18\x03 \x01(\t\x12\x14\n\x0c\x64\x65livered_at\x18\x04 \x01(\t\x12\x0b\n\x03ttl\x18\x05 \x01(\t\x12\x10\n\x08\x61ncestry\x18\x06 \x03(\t\x12)\n\x02sa\x18\x07 \x01(\x0b\x32\x1d.flwr.proto.SecureAggregation\x12<\n\x15legacy_server_message\x18\x65 \x01(\x0b\x32\x19.flwr.proto.ServerMessageB\x02\x18\x01\x12<\n\x15legacy_client_message\x18\x66 \x01(\x0b\x32\x19.flwr.proto.ClientMessageB\x02\x18\x01\"a\n\x07TaskIns\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\t\x12\x13\n\x0bworkload_id\x18\x03 \x01(\t\x12\x1e\n\x04task\x18\x04 \x01(\x0b\x32\x10.flwr.proto.Task\"a\n\x07TaskRes\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\t\x12\x13\n\x0bworkload_id\x18\x03 \x01(\t\x12\x1e\n\x04task\x18\x04 \x01(\x0b\x32\x10.flwr.proto.Task\"\x90\x04\n\x05Value\x12\x10\n\x06\x64ouble\x18\x01 \x01(\x01H\x00\x12\x10\n\x06sint64\x18\x02 \x01(\x12H\x00\x12\x0e\n\x04\x62ool\x18\x03 \x01(\x08H\x00\x12\x10\n\x06string\x18\x04 \x01(\tH\x00\x12\x0f\n\x05\x62ytes\x18\x05 \x01(\x0cH\x00\x12\x33\n\x0b\x64ouble_list\x18\x15 \x01(\x0b\x32\x1c.flwr.proto.Value.DoubleListH\x00\x12\x33\n\x0bsint64_list\x18\x16 \x01(\x0b\x32\x1c.flwr.proto.Value.Sint64ListH\x00\x12/\n\tbool_list\x18\x17 \x01(\x0b\x32\x1a.flwr.proto.Value.BoolListH\x00\x12\x33\n\x0bstring_list\x18\x18 \x01(\x0b\x32\x1c.flwr.proto.Value.StringListH\x00\x12\x31\n\nbytes_list\x18\x19 \x01(\x0b\x32\x1b.flwr.proto.Value.BytesListH\x00\x1a\x1a\n\nDoubleList\x12\x0c\n\x04vals\x18\x01 \x03(\x01\x1a\x1a\n\nSint64List\x12\x0c\n\x04vals\x18\x01 \x03(\x12\x1a\x18\n\x08\x42oolList\x12\x0c\n\x04vals\x18\x01 \x03(\x08\x1a\x1a\n\nStringList\x12\x0c\n\x04vals\x18\x01 \x03(\t\x1a\x19\n\tBytesList\x12\x0c\n\x04vals\x18\x01 \x03(\x0c\x1a\x1b\n\x0bNDArrayList\x12\x0c\n\x04vals\x18\x01 \x03(\x0c\x42\x07\n\x05value\"\xa0\x01\n\x11SecureAggregation\x12\x44\n\x0cnamed_values\x18\x01 \x03(\x0b\x32..flwr.proto.SecureAggregation.NamedValuesEntry\x1a\x45\n\x10NamedValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.flwr.proto.Value:\x02\x38\x01\x62\x06proto3')



_TASK = DESCRIPTOR.message_types_by_name['Task']
_TASKINS = DESCRIPTOR.message_types_by_name['TaskIns']
_TASKRES = DESCRIPTOR.message_types_by_name['TaskRes']
_VALUE = DESCRIPTOR.message_types_by_name['Value']
_VALUE_DOUBLELIST = _VALUE.nested_types_by_name['DoubleList']
_VALUE_SINT64LIST = _VALUE.nested_types_by_name['Sint64List']
_VALUE_BOOLLIST = _VALUE.nested_types_by_name['BoolList']
_VALUE_STRINGLIST = _VALUE.nested_types_by_name['StringList']
_VALUE_BYTESLIST = _VALUE.nested_types_by_name['BytesList']
_VALUE_NDARRAYLIST = _VALUE.nested_types_by_name['NDArrayList']
_SECUREAGGREGATION = DESCRIPTOR.message_types_by_name['SecureAggregation']
_SECUREAGGREGATION_NAMEDVALUESENTRY = _SECUREAGGREGATION.nested_types_by_name['NamedValuesEntry']
Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.Task)
  })
_sym_db.RegisterMessage(Task)

TaskIns = _reflection.GeneratedProtocolMessageType('TaskIns', (_message.Message,), {
  'DESCRIPTOR' : _TASKINS,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.TaskIns)
  })
_sym_db.RegisterMessage(TaskIns)

TaskRes = _reflection.GeneratedProtocolMessageType('TaskRes', (_message.Message,), {
  'DESCRIPTOR' : _TASKRES,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.TaskRes)
  })
_sym_db.RegisterMessage(TaskRes)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), {

  'DoubleList' : _reflection.GeneratedProtocolMessageType('DoubleList', (_message.Message,), {
    'DESCRIPTOR' : _VALUE_DOUBLELIST,
    '__module__' : 'flwr.proto.task_pb2'
    # @@protoc_insertion_point(class_scope:flwr.proto.Value.DoubleList)
    })
  ,

  'Sint64List' : _reflection.GeneratedProtocolMessageType('Sint64List', (_message.Message,), {
    'DESCRIPTOR' : _VALUE_SINT64LIST,
    '__module__' : 'flwr.proto.task_pb2'
    # @@protoc_insertion_point(class_scope:flwr.proto.Value.Sint64List)
    })
  ,

  'BoolList' : _reflection.GeneratedProtocolMessageType('BoolList', (_message.Message,), {
    'DESCRIPTOR' : _VALUE_BOOLLIST,
    '__module__' : 'flwr.proto.task_pb2'
    # @@protoc_insertion_point(class_scope:flwr.proto.Value.BoolList)
    })
  ,

  'StringList' : _reflection.GeneratedProtocolMessageType('StringList', (_message.Message,), {
    'DESCRIPTOR' : _VALUE_STRINGLIST,
    '__module__' : 'flwr.proto.task_pb2'
    # @@protoc_insertion_point(class_scope:flwr.proto.Value.StringList)
    })
  ,

  'BytesList' : _reflection.GeneratedProtocolMessageType('BytesList', (_message.Message,), {
    'DESCRIPTOR' : _VALUE_BYTESLIST,
    '__module__' : 'flwr.proto.task_pb2'
    # @@protoc_insertion_point(class_scope:flwr.proto.Value.BytesList)
    })
  ,

  'NDArrayList' : _reflection.GeneratedProtocolMessageType('NDArrayList', (_message.Message,), {
    'DESCRIPTOR' : _VALUE_NDARRAYLIST,
    '__module__' : 'flwr.proto.task_pb2'
    # @@protoc_insertion_point(class_scope:flwr.proto.Value.NDArrayList)
    })
  ,
  'DESCRIPTOR' : _VALUE,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.Value)
  })
_sym_db.RegisterMessage(Value)
_sym_db.RegisterMessage(Value.DoubleList)
_sym_db.RegisterMessage(Value.Sint64List)
_sym_db.RegisterMessage(Value.BoolList)
_sym_db.RegisterMessage(Value.StringList)
_sym_db.RegisterMessage(Value.BytesList)
_sym_db.RegisterMessage(Value.NDArrayList)

SecureAggregation = _reflection.GeneratedProtocolMessageType('SecureAggregation', (_message.Message,), {

  'NamedValuesEntry' : _reflection.GeneratedProtocolMessageType('NamedValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _SECUREAGGREGATION_NAMEDVALUESENTRY,
    '__module__' : 'flwr.proto.task_pb2'
    # @@protoc_insertion_point(class_scope:flwr.proto.SecureAggregation.NamedValuesEntry)
    })
  ,
  'DESCRIPTOR' : _SECUREAGGREGATION,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.SecureAggregation)
  })
_sym_db.RegisterMessage(SecureAggregation)
_sym_db.RegisterMessage(SecureAggregation.NamedValuesEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TASK.fields_by_name['legacy_server_message']._options = None
  _TASK.fields_by_name['legacy_server_message']._serialized_options = b'\030\001'
  _TASK.fields_by_name['legacy_client_message']._options = None
  _TASK.fields_by_name['legacy_client_message']._serialized_options = b'\030\001'
  _SECUREAGGREGATION_NAMEDVALUESENTRY._options = None
  _SECUREAGGREGATION_NAMEDVALUESENTRY._serialized_options = b'8\001'
  _TASK._serialized_start=89
  _TASK._serialized_end=407
  _TASKINS._serialized_start=409
  _TASKINS._serialized_end=506
  _TASKRES._serialized_start=508
  _TASKRES._serialized_end=605
  _VALUE._serialized_start=608
  _VALUE._serialized_end=1136
  _VALUE_DOUBLELIST._serialized_start=963
  _VALUE_DOUBLELIST._serialized_end=989
  _VALUE_SINT64LIST._serialized_start=991
  _VALUE_SINT64LIST._serialized_end=1017
  _VALUE_BOOLLIST._serialized_start=1019
  _VALUE_BOOLLIST._serialized_end=1043
  _VALUE_STRINGLIST._serialized_start=1045
  _VALUE_STRINGLIST._serialized_end=1071
  _VALUE_BYTESLIST._serialized_start=1073
  _VALUE_BYTESLIST._serialized_end=1098
  _VALUE_NDARRAYLIST._serialized_start=1100
  _VALUE_NDARRAYLIST._serialized_end=1127
  _SECUREAGGREGATION._serialized_start=1139
  _SECUREAGGREGATION._serialized_end=1299
  _SECUREAGGREGATION_NAMEDVALUESENTRY._serialized_start=1230
  _SECUREAGGREGATION_NAMEDVALUESENTRY._serialized_end=1299
# @@protoc_insertion_point(module_scope)
