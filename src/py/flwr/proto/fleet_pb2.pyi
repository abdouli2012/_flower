"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2022 Adap GmbH. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================
"""
import builtins
import collections.abc
import flwr.proto.node_pb2
import flwr.proto.task_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class PullTaskInsRequest(google.protobuf.message.Message):
    """PullTaskIns messages"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NODE_FIELD_NUMBER: builtins.int
    TASK_IDS_FIELD_NUMBER: builtins.int
    @property
    def node(self) -> flwr.proto.node_pb2.Node: ...
    @property
    def task_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        node: flwr.proto.node_pb2.Node | None = ...,
        task_ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["node", b"node"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["node", b"node", "task_ids", b"task_ids"]) -> None: ...

global___PullTaskInsRequest = PullTaskInsRequest

class PullTaskInsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RECONNECT_FIELD_NUMBER: builtins.int
    TASK_INS_LIST_FIELD_NUMBER: builtins.int
    @property
    def reconnect(self) -> global___Reconnect: ...
    @property
    def task_ins_list(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[flwr.proto.task_pb2.TaskIns]: ...
    def __init__(
        self,
        *,
        reconnect: global___Reconnect | None = ...,
        task_ins_list: collections.abc.Iterable[flwr.proto.task_pb2.TaskIns] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["reconnect", b"reconnect"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["reconnect", b"reconnect", "task_ins_list", b"task_ins_list"]) -> None: ...

global___PullTaskInsResponse = PullTaskInsResponse

class PushTaskResRequest(google.protobuf.message.Message):
    """PushTaskRes messages"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TASK_RES_LIST_FIELD_NUMBER: builtins.int
    @property
    def task_res_list(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[flwr.proto.task_pb2.TaskRes]: ...
    def __init__(
        self,
        *,
        task_res_list: collections.abc.Iterable[flwr.proto.task_pb2.TaskRes] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["task_res_list", b"task_res_list"]) -> None: ...

global___PushTaskResRequest = PushTaskResRequest

class PushTaskResResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class ResultsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.int
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    RECONNECT_FIELD_NUMBER: builtins.int
    RESULTS_FIELD_NUMBER: builtins.int
    @property
    def reconnect(self) -> global___Reconnect: ...
    @property
    def results(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.int]: ...
    def __init__(
        self,
        *,
        reconnect: global___Reconnect | None = ...,
        results: collections.abc.Mapping[builtins.str, builtins.int] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["reconnect", b"reconnect"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["reconnect", b"reconnect", "results", b"results"]) -> None: ...

global___PushTaskResResponse = PushTaskResResponse

class Reconnect(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RECONNECT_FIELD_NUMBER: builtins.int
    reconnect: builtins.int
    def __init__(
        self,
        *,
        reconnect: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["reconnect", b"reconnect"]) -> None: ...

global___Reconnect = Reconnect
