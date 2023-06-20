"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import flwr.proto.node_pb2
import flwr.proto.transport_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Task(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PRODUCER_FIELD_NUMBER: builtins.int
    CONSUMER_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    DELIVERED_AT_FIELD_NUMBER: builtins.int
    TTL_FIELD_NUMBER: builtins.int
    ANCESTRY_FIELD_NUMBER: builtins.int
    SA_FIELD_NUMBER: builtins.int
    MESSAGE_TYPE_FIELD_NUMBER: builtins.int
    LEGACY_SERVER_MESSAGE_FIELD_NUMBER: builtins.int
    LEGACY_CLIENT_MESSAGE_FIELD_NUMBER: builtins.int
    @property
    def producer(self) -> flwr.proto.node_pb2.Node: ...
    @property
    def consumer(self) -> flwr.proto.node_pb2.Node: ...
    created_at: typing.Text
    delivered_at: typing.Text
    ttl: typing.Text
    @property
    def ancestry(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    @property
    def sa(self) -> global___SecureAggregation: ...
    message_type: typing.Text
    @property
    def legacy_server_message(self) -> flwr.proto.transport_pb2.ServerMessage: ...
    @property
    def legacy_client_message(self) -> flwr.proto.transport_pb2.ClientMessage: ...
    def __init__(self,
        *,
        producer: typing.Optional[flwr.proto.node_pb2.Node] = ...,
        consumer: typing.Optional[flwr.proto.node_pb2.Node] = ...,
        created_at: typing.Text = ...,
        delivered_at: typing.Text = ...,
        ttl: typing.Text = ...,
        ancestry: typing.Optional[typing.Iterable[typing.Text]] = ...,
        sa: typing.Optional[global___SecureAggregation] = ...,
        message_type: typing.Text = ...,
        legacy_server_message: typing.Optional[flwr.proto.transport_pb2.ServerMessage] = ...,
        legacy_client_message: typing.Optional[flwr.proto.transport_pb2.ClientMessage] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["consumer",b"consumer","legacy_client_message",b"legacy_client_message","legacy_server_message",b"legacy_server_message","producer",b"producer","sa",b"sa"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ancestry",b"ancestry","consumer",b"consumer","created_at",b"created_at","delivered_at",b"delivered_at","legacy_client_message",b"legacy_client_message","legacy_server_message",b"legacy_server_message","message_type",b"message_type","producer",b"producer","sa",b"sa","ttl",b"ttl"]) -> None: ...
global___Task = Task

class TaskIns(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TASK_ID_FIELD_NUMBER: builtins.int
    GROUP_ID_FIELD_NUMBER: builtins.int
    WORKLOAD_ID_FIELD_NUMBER: builtins.int
    TASK_FIELD_NUMBER: builtins.int
    task_id: typing.Text
    group_id: typing.Text
    workload_id: typing.Text
    @property
    def task(self) -> global___Task: ...
    def __init__(self,
        *,
        task_id: typing.Text = ...,
        group_id: typing.Text = ...,
        workload_id: typing.Text = ...,
        task: typing.Optional[global___Task] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["task",b"task"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["group_id",b"group_id","task",b"task","task_id",b"task_id","workload_id",b"workload_id"]) -> None: ...
global___TaskIns = TaskIns

class TaskRes(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TASK_ID_FIELD_NUMBER: builtins.int
    GROUP_ID_FIELD_NUMBER: builtins.int
    WORKLOAD_ID_FIELD_NUMBER: builtins.int
    TASK_FIELD_NUMBER: builtins.int
    task_id: typing.Text
    group_id: typing.Text
    workload_id: typing.Text
    @property
    def task(self) -> global___Task: ...
    def __init__(self,
        *,
        task_id: typing.Text = ...,
        group_id: typing.Text = ...,
        workload_id: typing.Text = ...,
        task: typing.Optional[global___Task] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["task",b"task"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["group_id",b"group_id","task",b"task","task_id",b"task_id","workload_id",b"workload_id"]) -> None: ...
global___TaskRes = TaskRes

class Value(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class DoubleList(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        VALS_FIELD_NUMBER: builtins.int
        @property
        def vals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
        def __init__(self,
            *,
            vals: typing.Optional[typing.Iterable[builtins.float]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["vals",b"vals"]) -> None: ...

    class Sint64List(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        VALS_FIELD_NUMBER: builtins.int
        @property
        def vals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(self,
            *,
            vals: typing.Optional[typing.Iterable[builtins.int]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["vals",b"vals"]) -> None: ...

    class BoolList(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        VALS_FIELD_NUMBER: builtins.int
        @property
        def vals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bool]: ...
        def __init__(self,
            *,
            vals: typing.Optional[typing.Iterable[builtins.bool]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["vals",b"vals"]) -> None: ...

    class StringList(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        VALS_FIELD_NUMBER: builtins.int
        @property
        def vals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
        def __init__(self,
            *,
            vals: typing.Optional[typing.Iterable[typing.Text]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["vals",b"vals"]) -> None: ...

    class BytesList(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        VALS_FIELD_NUMBER: builtins.int
        @property
        def vals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bytes]: ...
        def __init__(self,
            *,
            vals: typing.Optional[typing.Iterable[builtins.bytes]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["vals",b"vals"]) -> None: ...

    DOUBLE_FIELD_NUMBER: builtins.int
    SINT64_FIELD_NUMBER: builtins.int
    BOOL_FIELD_NUMBER: builtins.int
    STRING_FIELD_NUMBER: builtins.int
    BYTES_FIELD_NUMBER: builtins.int
    DOUBLE_LIST_FIELD_NUMBER: builtins.int
    SINT64_LIST_FIELD_NUMBER: builtins.int
    BOOL_LIST_FIELD_NUMBER: builtins.int
    STRING_LIST_FIELD_NUMBER: builtins.int
    BYTES_LIST_FIELD_NUMBER: builtins.int
    double: builtins.float
    """Single element"""

    sint64: builtins.int
    bool: builtins.bool
    string: typing.Text
    bytes: builtins.bytes
    @property
    def double_list(self) -> global___Value.DoubleList:
        """List types"""
        pass
    @property
    def sint64_list(self) -> global___Value.Sint64List: ...
    @property
    def bool_list(self) -> global___Value.BoolList: ...
    @property
    def string_list(self) -> global___Value.StringList: ...
    @property
    def bytes_list(self) -> global___Value.BytesList: ...
    def __init__(self,
        *,
        double: builtins.float = ...,
        sint64: builtins.int = ...,
        bool: builtins.bool = ...,
        string: typing.Text = ...,
        bytes: builtins.bytes = ...,
        double_list: typing.Optional[global___Value.DoubleList] = ...,
        sint64_list: typing.Optional[global___Value.Sint64List] = ...,
        bool_list: typing.Optional[global___Value.BoolList] = ...,
        string_list: typing.Optional[global___Value.StringList] = ...,
        bytes_list: typing.Optional[global___Value.BytesList] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool",b"bool","bool_list",b"bool_list","bytes",b"bytes","bytes_list",b"bytes_list","double",b"double","double_list",b"double_list","sint64",b"sint64","sint64_list",b"sint64_list","string",b"string","string_list",b"string_list","value",b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool",b"bool","bool_list",b"bool_list","bytes",b"bytes","bytes_list",b"bytes_list","double",b"double","double_list",b"double_list","sint64",b"sint64","sint64_list",b"sint64_list","string",b"string","string_list",b"string_list","value",b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value",b"value"]) -> typing.Optional[typing_extensions.Literal["double","sint64","bool","string","bytes","double_list","sint64_list","bool_list","string_list","bytes_list"]]: ...
global___Value = Value

class SecureAggregation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class NamedValuesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> global___Value: ...
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Optional[global___Value] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    NAMED_VALUES_FIELD_NUMBER: builtins.int
    @property
    def named_values(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, global___Value]: ...
    def __init__(self,
        *,
        named_values: typing.Optional[typing.Mapping[typing.Text, global___Value]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["named_values",b"named_values"]) -> None: ...
global___SecureAggregation = SecureAggregation
