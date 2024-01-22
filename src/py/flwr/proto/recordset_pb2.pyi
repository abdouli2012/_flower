"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import flwr.proto.task_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class DoubleList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LIST_FIELD_NUMBER: builtins.int
    @property
    def list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(self,
        *,
        list: typing.Optional[typing.Iterable[builtins.float]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["list",b"list"]) -> None: ...
global___DoubleList = DoubleList

class Sint64List(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LIST_FIELD_NUMBER: builtins.int
    @property
    def list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(self,
        *,
        list: typing.Optional[typing.Iterable[builtins.int]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["list",b"list"]) -> None: ...
global___Sint64List = Sint64List

class BoolList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LIST_FIELD_NUMBER: builtins.int
    @property
    def list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bool]: ...
    def __init__(self,
        *,
        list: typing.Optional[typing.Iterable[builtins.bool]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["list",b"list"]) -> None: ...
global___BoolList = BoolList

class StringList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LIST_FIELD_NUMBER: builtins.int
    @property
    def list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    def __init__(self,
        *,
        list: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["list",b"list"]) -> None: ...
global___StringList = StringList

class BytesList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LIST_FIELD_NUMBER: builtins.int
    @property
    def list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bytes]: ...
    def __init__(self,
        *,
        list: typing.Optional[typing.Iterable[builtins.bytes]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["list",b"list"]) -> None: ...
global___BytesList = BytesList

class Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DTYPE_FIELD_NUMBER: builtins.int
    SHAPE_FIELD_NUMBER: builtins.int
    STYPE_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    dtype: typing.Text
    @property
    def shape(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    stype: typing.Text
    data: builtins.bytes
    def __init__(self,
        *,
        dtype: typing.Text = ...,
        shape: typing.Optional[typing.Iterable[builtins.int]] = ...,
        stype: typing.Text = ...,
        data: builtins.bytes = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data","dtype",b"dtype","shape",b"shape","stype",b"stype"]) -> None: ...
global___Array = Array

class MetricsRecordValue(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DOUBLE_FIELD_NUMBER: builtins.int
    SINT64_FIELD_NUMBER: builtins.int
    DOUBLE_LIST_FIELD_NUMBER: builtins.int
    SINT64_LIST_FIELD_NUMBER: builtins.int
    double: builtins.float
    """Single element"""

    sint64: builtins.int
    @property
    def double_list(self) -> global___DoubleList:
        """List types"""
        pass
    @property
    def sint64_list(self) -> global___Sint64List: ...
    def __init__(self,
        *,
        double: builtins.float = ...,
        sint64: builtins.int = ...,
        double_list: typing.Optional[global___DoubleList] = ...,
        sint64_list: typing.Optional[global___Sint64List] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["double",b"double","double_list",b"double_list","sint64",b"sint64","sint64_list",b"sint64_list","value",b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["double",b"double","double_list",b"double_list","sint64",b"sint64","sint64_list",b"sint64_list","value",b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value",b"value"]) -> typing.Optional[typing_extensions.Literal["double","sint64","double_list","sint64_list"]]: ...
global___MetricsRecordValue = MetricsRecordValue

class ConfigsRecordValue(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
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
    def double_list(self) -> global___DoubleList:
        """List types"""
        pass
    @property
    def sint64_list(self) -> global___Sint64List: ...
    @property
    def bool_list(self) -> global___BoolList: ...
    @property
    def string_list(self) -> global___StringList: ...
    @property
    def bytes_list(self) -> global___BytesList: ...
    def __init__(self,
        *,
        double: builtins.float = ...,
        sint64: builtins.int = ...,
        bool: builtins.bool = ...,
        string: typing.Text = ...,
        bytes: builtins.bytes = ...,
        double_list: typing.Optional[global___DoubleList] = ...,
        sint64_list: typing.Optional[global___Sint64List] = ...,
        bool_list: typing.Optional[global___BoolList] = ...,
        string_list: typing.Optional[global___StringList] = ...,
        bytes_list: typing.Optional[global___BytesList] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool",b"bool","bool_list",b"bool_list","bytes",b"bytes","bytes_list",b"bytes_list","double",b"double","double_list",b"double_list","sint64",b"sint64","sint64_list",b"sint64_list","string",b"string","string_list",b"string_list","value",b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool",b"bool","bool_list",b"bool_list","bytes",b"bytes","bytes_list",b"bytes_list","double",b"double","double_list",b"double_list","sint64",b"sint64","sint64_list",b"sint64_list","string",b"string","string_list",b"string_list","value",b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value",b"value"]) -> typing.Optional[typing_extensions.Literal["double","sint64","bool","string","bytes","double_list","sint64_list","bool_list","string_list","bytes_list"]]: ...
global___ConfigsRecordValue = ConfigsRecordValue

class ParametersRecord(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATA_KEYS_FIELD_NUMBER: builtins.int
    DATA_VALUES_FIELD_NUMBER: builtins.int
    @property
    def data_keys(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    @property
    def data_values(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Array]: ...
    def __init__(self,
        *,
        data_keys: typing.Optional[typing.Iterable[typing.Text]] = ...,
        data_values: typing.Optional[typing.Iterable[global___Array]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data_keys",b"data_keys","data_values",b"data_values"]) -> None: ...
global___ParametersRecord = ParametersRecord

class MetricsRecord(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class DataEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> flwr.proto.task_pb2.Value: ...
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Optional[flwr.proto.task_pb2.Value] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, flwr.proto.task_pb2.Value]: ...
    def __init__(self,
        *,
        data: typing.Optional[typing.Mapping[typing.Text, flwr.proto.task_pb2.Value]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data"]) -> None: ...
global___MetricsRecord = MetricsRecord

class ConfigsRecord(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class DataEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> flwr.proto.task_pb2.Value: ...
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Optional[flwr.proto.task_pb2.Value] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, flwr.proto.task_pb2.Value]: ...
    def __init__(self,
        *,
        data: typing.Optional[typing.Mapping[typing.Text, flwr.proto.task_pb2.Value]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data"]) -> None: ...
global___ConfigsRecord = ConfigsRecord
