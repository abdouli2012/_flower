# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/fleet.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='flwr/proto/fleet.proto',
  package='flwr.server.fleet.proto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16\x66lwr/proto/fleet.proto\x12\x17\x66lwr.server.fleet.proto\"\x12\n\x04Task\x12\n\n\x02id\x18\x01 \x01(\t\"\x11\n\x0fGetTasksRequest\"?\n\x10GetTasksResponse\x12+\n\x04task\x18\x01 \x03(\x0b\x32\x1d.flwr.server.fleet.proto.Task\"\x19\n\x06Result\x12\x0f\n\x07task_id\x18\x01 \x01(\t\"H\n\x14\x43reateResultsRequest\x12\x30\n\x07results\x18\x01 \x03(\x0b\x32\x1f.flwr.server.fleet.proto.Result\"\x17\n\x15\x43reateResultsResponse2\xdc\x01\n\x05\x46leet\x12\x61\n\x08GetTasks\x12(.flwr.server.fleet.proto.GetTasksRequest\x1a).flwr.server.fleet.proto.GetTasksResponse\"\x00\x12p\n\rCreateResults\x12-.flwr.server.fleet.proto.CreateResultsRequest\x1a..flwr.server.fleet.proto.CreateResultsResponse\"\x00\x62\x06proto3'
)




_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='flwr.server.fleet.proto.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='flwr.server.fleet.proto.Task.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=51,
  serialized_end=69,
)


_GETTASKSREQUEST = _descriptor.Descriptor(
  name='GetTasksRequest',
  full_name='flwr.server.fleet.proto.GetTasksRequest',
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
  serialized_start=71,
  serialized_end=88,
)


_GETTASKSRESPONSE = _descriptor.Descriptor(
  name='GetTasksResponse',
  full_name='flwr.server.fleet.proto.GetTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='flwr.server.fleet.proto.GetTasksResponse.task', index=0,
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
  serialized_start=90,
  serialized_end=153,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='flwr.server.fleet.proto.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='flwr.server.fleet.proto.Result.task_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=155,
  serialized_end=180,
)


_CREATERESULTSREQUEST = _descriptor.Descriptor(
  name='CreateResultsRequest',
  full_name='flwr.server.fleet.proto.CreateResultsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='flwr.server.fleet.proto.CreateResultsRequest.results', index=0,
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
  serialized_start=182,
  serialized_end=254,
)


_CREATERESULTSRESPONSE = _descriptor.Descriptor(
  name='CreateResultsResponse',
  full_name='flwr.server.fleet.proto.CreateResultsResponse',
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
  serialized_start=256,
  serialized_end=279,
)

_GETTASKSRESPONSE.fields_by_name['task'].message_type = _TASK
_CREATERESULTSREQUEST.fields_by_name['results'].message_type = _RESULT
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['GetTasksRequest'] = _GETTASKSREQUEST
DESCRIPTOR.message_types_by_name['GetTasksResponse'] = _GETTASKSRESPONSE
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['CreateResultsRequest'] = _CREATERESULTSREQUEST
DESCRIPTOR.message_types_by_name['CreateResultsResponse'] = _CREATERESULTSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'flwr.proto.fleet_pb2'
  # @@protoc_insertion_point(class_scope:flwr.server.fleet.proto.Task)
  })
_sym_db.RegisterMessage(Task)

GetTasksRequest = _reflection.GeneratedProtocolMessageType('GetTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETTASKSREQUEST,
  '__module__' : 'flwr.proto.fleet_pb2'
  # @@protoc_insertion_point(class_scope:flwr.server.fleet.proto.GetTasksRequest)
  })
_sym_db.RegisterMessage(GetTasksRequest)

GetTasksResponse = _reflection.GeneratedProtocolMessageType('GetTasksResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTASKSRESPONSE,
  '__module__' : 'flwr.proto.fleet_pb2'
  # @@protoc_insertion_point(class_scope:flwr.server.fleet.proto.GetTasksResponse)
  })
_sym_db.RegisterMessage(GetTasksResponse)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), {
  'DESCRIPTOR' : _RESULT,
  '__module__' : 'flwr.proto.fleet_pb2'
  # @@protoc_insertion_point(class_scope:flwr.server.fleet.proto.Result)
  })
_sym_db.RegisterMessage(Result)

CreateResultsRequest = _reflection.GeneratedProtocolMessageType('CreateResultsRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATERESULTSREQUEST,
  '__module__' : 'flwr.proto.fleet_pb2'
  # @@protoc_insertion_point(class_scope:flwr.server.fleet.proto.CreateResultsRequest)
  })
_sym_db.RegisterMessage(CreateResultsRequest)

CreateResultsResponse = _reflection.GeneratedProtocolMessageType('CreateResultsResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATERESULTSRESPONSE,
  '__module__' : 'flwr.proto.fleet_pb2'
  # @@protoc_insertion_point(class_scope:flwr.server.fleet.proto.CreateResultsResponse)
  })
_sym_db.RegisterMessage(CreateResultsResponse)



_FLEET = _descriptor.ServiceDescriptor(
  name='Fleet',
  full_name='flwr.server.fleet.proto.Fleet',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=282,
  serialized_end=502,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetTasks',
    full_name='flwr.server.fleet.proto.Fleet.GetTasks',
    index=0,
    containing_service=None,
    input_type=_GETTASKSREQUEST,
    output_type=_GETTASKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateResults',
    full_name='flwr.server.fleet.proto.Fleet.CreateResults',
    index=1,
    containing_service=None,
    input_type=_CREATERESULTSREQUEST,
    output_type=_CREATERESULTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FLEET)

DESCRIPTOR.services_by_name['Fleet'] = _FLEET

# @@protoc_insertion_point(module_scope)
