# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/task.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import transport_pb2 as flwr_dot_proto_dot_transport__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='flwr/proto/task.proto',
  package='flwr.proto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15\x66lwr/proto/task.proto\x12\nflwr.proto\x1a\x1a\x66lwr/proto/transport.proto\"Q\n\x04Task\x12\x0f\n\x07task_id\x18\x01 \x01(\x03\x12\x38\n\x15legacy_server_message\x18\x65 \x01(\x0b\x32\x19.flwr.proto.ServerMessage\"S\n\x06Result\x12\x0f\n\x07task_id\x18\x01 \x01(\x03\x12\x38\n\x15legacy_client_message\x18\x65 \x01(\x0b\x32\x19.flwr.proto.ClientMessage\"D\n\x0eTaskAssignment\x12\x1e\n\x04task\x18\x01 \x01(\x0b\x32\x10.flwr.proto.Task\x12\x12\n\nclient_ids\x18\x02 \x03(\x03\x62\x06proto3'
  ,
  dependencies=[flwr_dot_proto_dot_transport__pb2.DESCRIPTOR,])




_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='flwr.proto.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='flwr.proto.Task.task_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='legacy_server_message', full_name='flwr.proto.Task.legacy_server_message', index=1,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=146,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='flwr.proto.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='flwr.proto.Result.task_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='legacy_client_message', full_name='flwr.proto.Result.legacy_client_message', index=1,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=148,
  serialized_end=231,
)


_TASKASSIGNMENT = _descriptor.Descriptor(
  name='TaskAssignment',
  full_name='flwr.proto.TaskAssignment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='flwr.proto.TaskAssignment.task', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='client_ids', full_name='flwr.proto.TaskAssignment.client_ids', index=1,
      number=2, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=233,
  serialized_end=301,
)

_TASK.fields_by_name['legacy_server_message'].message_type = flwr_dot_proto_dot_transport__pb2._SERVERMESSAGE
_RESULT.fields_by_name['legacy_client_message'].message_type = flwr_dot_proto_dot_transport__pb2._CLIENTMESSAGE
_TASKASSIGNMENT.fields_by_name['task'].message_type = _TASK
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['TaskAssignment'] = _TASKASSIGNMENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.Task)
  })
_sym_db.RegisterMessage(Task)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), {
  'DESCRIPTOR' : _RESULT,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.Result)
  })
_sym_db.RegisterMessage(Result)

TaskAssignment = _reflection.GeneratedProtocolMessageType('TaskAssignment', (_message.Message,), {
  'DESCRIPTOR' : _TASKASSIGNMENT,
  '__module__' : 'flwr.proto.task_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.TaskAssignment)
  })
_sym_db.RegisterMessage(TaskAssignment)


# @@protoc_insertion_point(module_scope)
