# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/driver.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import task_pb2 as flwr_dot_proto_dot_task__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='flwr/proto/driver.proto',
  package='flwr.proto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x66lwr/proto/driver.proto\x12\nflwr.proto\x1a\x15\x66lwr/proto/task.proto\"\x13\n\x11GetClientsRequest\"(\n\x12GetClientsResponse\x12\x12\n\nclient_ids\x18\x01 \x03(\x03\"J\n\x12\x43reateTasksRequest\x12\x34\n\x10task_assignments\x18\x01 \x03(\x0b\x32\x1a.flwr.proto.TaskAssignment\"\'\n\x13\x43reateTasksResponse\x12\x10\n\x08task_ids\x18\x01 \x03(\x03\"%\n\x11GetResultsRequest\x12\x10\n\x08task_ids\x18\x01 \x03(\x03\"9\n\x12GetResultsResponse\x12#\n\x07results\x18\x01 \x03(\x0b\x32\x12.flwr.proto.Result2\xf8\x01\n\x06\x44river\x12M\n\nGetClients\x12\x1d.flwr.proto.GetClientsRequest\x1a\x1e.flwr.proto.GetClientsResponse\"\x00\x12P\n\x0b\x43reateTasks\x12\x1e.flwr.proto.CreateTasksRequest\x1a\x1f.flwr.proto.CreateTasksResponse\"\x00\x12M\n\nGetResults\x12\x1d.flwr.proto.GetResultsRequest\x1a\x1e.flwr.proto.GetResultsResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[flwr_dot_proto_dot_task__pb2.DESCRIPTOR,])




_GETCLIENTSREQUEST = _descriptor.Descriptor(
  name='GetClientsRequest',
  full_name='flwr.proto.GetClientsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=62,
  serialized_end=81,
)


_GETCLIENTSRESPONSE = _descriptor.Descriptor(
  name='GetClientsResponse',
  full_name='flwr.proto.GetClientsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_ids', full_name='flwr.proto.GetClientsResponse.client_ids', index=0,
      number=1, type=3, cpp_type=2, label=3,
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
  serialized_start=83,
  serialized_end=123,
)


_CREATETASKSREQUEST = _descriptor.Descriptor(
  name='CreateTasksRequest',
  full_name='flwr.proto.CreateTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_assignments', full_name='flwr.proto.CreateTasksRequest.task_assignments', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=125,
  serialized_end=199,
)


_CREATETASKSRESPONSE = _descriptor.Descriptor(
  name='CreateTasksResponse',
  full_name='flwr.proto.CreateTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_ids', full_name='flwr.proto.CreateTasksResponse.task_ids', index=0,
      number=1, type=3, cpp_type=2, label=3,
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
  serialized_start=201,
  serialized_end=240,
)


_GETRESULTSREQUEST = _descriptor.Descriptor(
  name='GetResultsRequest',
  full_name='flwr.proto.GetResultsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_ids', full_name='flwr.proto.GetResultsRequest.task_ids', index=0,
      number=1, type=3, cpp_type=2, label=3,
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
  serialized_start=242,
  serialized_end=279,
)


_GETRESULTSRESPONSE = _descriptor.Descriptor(
  name='GetResultsResponse',
  full_name='flwr.proto.GetResultsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='flwr.proto.GetResultsResponse.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=281,
  serialized_end=338,
)

_CREATETASKSREQUEST.fields_by_name['task_assignments'].message_type = flwr_dot_proto_dot_task__pb2._TASKASSIGNMENT
_GETRESULTSRESPONSE.fields_by_name['results'].message_type = flwr_dot_proto_dot_task__pb2._RESULT
DESCRIPTOR.message_types_by_name['GetClientsRequest'] = _GETCLIENTSREQUEST
DESCRIPTOR.message_types_by_name['GetClientsResponse'] = _GETCLIENTSRESPONSE
DESCRIPTOR.message_types_by_name['CreateTasksRequest'] = _CREATETASKSREQUEST
DESCRIPTOR.message_types_by_name['CreateTasksResponse'] = _CREATETASKSRESPONSE
DESCRIPTOR.message_types_by_name['GetResultsRequest'] = _GETRESULTSREQUEST
DESCRIPTOR.message_types_by_name['GetResultsResponse'] = _GETRESULTSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetClientsRequest = _reflection.GeneratedProtocolMessageType('GetClientsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCLIENTSREQUEST,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.GetClientsRequest)
  })
_sym_db.RegisterMessage(GetClientsRequest)

GetClientsResponse = _reflection.GeneratedProtocolMessageType('GetClientsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCLIENTSRESPONSE,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.GetClientsResponse)
  })
_sym_db.RegisterMessage(GetClientsResponse)

CreateTasksRequest = _reflection.GeneratedProtocolMessageType('CreateTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATETASKSREQUEST,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.CreateTasksRequest)
  })
_sym_db.RegisterMessage(CreateTasksRequest)

CreateTasksResponse = _reflection.GeneratedProtocolMessageType('CreateTasksResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATETASKSRESPONSE,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.CreateTasksResponse)
  })
_sym_db.RegisterMessage(CreateTasksResponse)

GetResultsRequest = _reflection.GeneratedProtocolMessageType('GetResultsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETRESULTSREQUEST,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.GetResultsRequest)
  })
_sym_db.RegisterMessage(GetResultsRequest)

GetResultsResponse = _reflection.GeneratedProtocolMessageType('GetResultsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETRESULTSRESPONSE,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.GetResultsResponse)
  })
_sym_db.RegisterMessage(GetResultsResponse)



_DRIVER = _descriptor.ServiceDescriptor(
  name='Driver',
  full_name='flwr.proto.Driver',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=341,
  serialized_end=589,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetClients',
    full_name='flwr.proto.Driver.GetClients',
    index=0,
    containing_service=None,
    input_type=_GETCLIENTSREQUEST,
    output_type=_GETCLIENTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateTasks',
    full_name='flwr.proto.Driver.CreateTasks',
    index=1,
    containing_service=None,
    input_type=_CREATETASKSREQUEST,
    output_type=_CREATETASKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetResults',
    full_name='flwr.proto.Driver.GetResults',
    index=2,
    containing_service=None,
    input_type=_GETRESULTSREQUEST,
    output_type=_GETRESULTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DRIVER)

DESCRIPTOR.services_by_name['Driver'] = _DRIVER

# @@protoc_insertion_point(module_scope)
