"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2020 Adap GmbH. All Rights Reserved.

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
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Code:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CodeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Code.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    OK: _Code.ValueType  # 0
    GET_PROPERTIES_NOT_IMPLEMENTED: _Code.ValueType  # 1
    GET_PARAMETERS_NOT_IMPLEMENTED: _Code.ValueType  # 2
    FIT_NOT_IMPLEMENTED: _Code.ValueType  # 3
    EVALUATE_NOT_IMPLEMENTED: _Code.ValueType  # 4

class Code(_Code, metaclass=_CodeEnumTypeWrapper): ...

OK: Code.ValueType  # 0
GET_PROPERTIES_NOT_IMPLEMENTED: Code.ValueType  # 1
GET_PARAMETERS_NOT_IMPLEMENTED: Code.ValueType  # 2
FIT_NOT_IMPLEMENTED: Code.ValueType  # 3
EVALUATE_NOT_IMPLEMENTED: Code.ValueType  # 4
global___Code = Code

class _Reason:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ReasonEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Reason.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNKNOWN: _Reason.ValueType  # 0
    RECONNECT: _Reason.ValueType  # 1
    POWER_DISCONNECTED: _Reason.ValueType  # 2
    WIFI_UNAVAILABLE: _Reason.ValueType  # 3
    ACK: _Reason.ValueType  # 4

class Reason(_Reason, metaclass=_ReasonEnumTypeWrapper): ...

UNKNOWN: Reason.ValueType  # 0
RECONNECT: Reason.ValueType  # 1
POWER_DISCONNECTED: Reason.ValueType  # 2
WIFI_UNAVAILABLE: Reason.ValueType  # 3
ACK: Reason.ValueType  # 4
global___Reason = Reason

@typing_extensions.final
class Status(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    code: global___Code.ValueType
    message: builtins.str
    def __init__(
        self,
        *,
        code: global___Code.ValueType = ...,
        message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code", "message", b"message"]) -> None: ...

global___Status = Status

@typing_extensions.final
class Parameters(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TENSORS_FIELD_NUMBER: builtins.int
    TENSOR_TYPE_FIELD_NUMBER: builtins.int
    @property
    def tensors(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bytes]: ...
    tensor_type: builtins.str
    def __init__(
        self,
        *,
        tensors: collections.abc.Iterable[builtins.bytes] | None = ...,
        tensor_type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["tensor_type", b"tensor_type", "tensors", b"tensors"]) -> None: ...

global___Parameters = Parameters

@typing_extensions.final
class ServerMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ReconnectIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        SECONDS_FIELD_NUMBER: builtins.int
        seconds: builtins.int
        def __init__(
            self,
            *,
            seconds: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["seconds", b"seconds"]) -> None: ...

    @typing_extensions.final
    class GetPropertiesIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class ConfigEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.str
            @property
            def value(self) -> global___Scalar: ...
            def __init__(
                self,
                *,
                key: builtins.str = ...,
                value: global___Scalar | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        CONFIG_FIELD_NUMBER: builtins.int
        @property
        def config(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Scalar]: ...
        def __init__(
            self,
            *,
            config: collections.abc.Mapping[builtins.str, global___Scalar] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["config", b"config"]) -> None: ...

    @typing_extensions.final
    class GetParametersIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class ConfigEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.str
            @property
            def value(self) -> global___Scalar: ...
            def __init__(
                self,
                *,
                key: builtins.str = ...,
                value: global___Scalar | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        CONFIG_FIELD_NUMBER: builtins.int
        @property
        def config(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Scalar]: ...
        def __init__(
            self,
            *,
            config: collections.abc.Mapping[builtins.str, global___Scalar] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["config", b"config"]) -> None: ...

    @typing_extensions.final
    class FitIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class ConfigEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.str
            @property
            def value(self) -> global___Scalar: ...
            def __init__(
                self,
                *,
                key: builtins.str = ...,
                value: global___Scalar | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        PARAMETERS_FIELD_NUMBER: builtins.int
        CONFIG_FIELD_NUMBER: builtins.int
        @property
        def parameters(self) -> global___Parameters: ...
        @property
        def config(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Scalar]: ...
        def __init__(
            self,
            *,
            parameters: global___Parameters | None = ...,
            config: collections.abc.Mapping[builtins.str, global___Scalar] | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["parameters", b"parameters"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["config", b"config", "parameters", b"parameters"]) -> None: ...

    @typing_extensions.final
    class EvaluateIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class ConfigEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.str
            @property
            def value(self) -> global___Scalar: ...
            def __init__(
                self,
                *,
                key: builtins.str = ...,
                value: global___Scalar | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        PARAMETERS_FIELD_NUMBER: builtins.int
        CONFIG_FIELD_NUMBER: builtins.int
        @property
        def parameters(self) -> global___Parameters: ...
        @property
        def config(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Scalar]: ...
        def __init__(
            self,
            *,
            parameters: global___Parameters | None = ...,
            config: collections.abc.Mapping[builtins.str, global___Scalar] | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["parameters", b"parameters"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["config", b"config", "parameters", b"parameters"]) -> None: ...

    @typing_extensions.final
    class ExampleIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        QUESTION_FIELD_NUMBER: builtins.int
        L_FIELD_NUMBER: builtins.int
        question: builtins.str
        @property
        def l(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            question: builtins.str = ...,
            l: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["l", b"l", "question", b"question"]) -> None: ...

    @typing_extensions.final
    class SendVectorAIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        VECTOR_A_FIELD_NUMBER: builtins.int
        @property
        def vector_a(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            vector_a: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["vector_a", b"vector_a"]) -> None: ...

    @typing_extensions.final
    class SendAllpubIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        AGGREGATED_ALLPUB_FIELD_NUMBER: builtins.int
        @property
        def aggregated_allpub(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            aggregated_allpub: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["aggregated_allpub", b"aggregated_allpub"]) -> None: ...

    @typing_extensions.final
    class RequestEncryptedIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        REQUEST_FIELD_NUMBER: builtins.int
        request: builtins.str
        def __init__(
            self,
            *,
            request: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["request", b"request"]) -> None: ...

    @typing_extensions.final
    class SendCsumIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        CSUM1_FIELD_NUMBER: builtins.int
        @property
        def csum1(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            csum1: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["csum1", b"csum1"]) -> None: ...

    @typing_extensions.final
    class SendNewWeightsIns(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NEW_WEIGHTS_FIELD_NUMBER: builtins.int
        @property
        def new_weights(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            new_weights: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["new_weights", b"new_weights"]) -> None: ...

    RECONNECT_INS_FIELD_NUMBER: builtins.int
    GET_PROPERTIES_INS_FIELD_NUMBER: builtins.int
    GET_PARAMETERS_INS_FIELD_NUMBER: builtins.int
    FIT_INS_FIELD_NUMBER: builtins.int
    EVALUATE_INS_FIELD_NUMBER: builtins.int
    EXAMPLE_INS_FIELD_NUMBER: builtins.int
    SEND_VECTOR_A_INS_FIELD_NUMBER: builtins.int
    SEND_ALLPUB_INS_FIELD_NUMBER: builtins.int
    REQUEST_ENCRYPTED_INS_FIELD_NUMBER: builtins.int
    SEND_CSUM_INS_FIELD_NUMBER: builtins.int
    SEND_NEW_WEIGHTS_INS_FIELD_NUMBER: builtins.int
    @property
    def reconnect_ins(self) -> global___ServerMessage.ReconnectIns: ...
    @property
    def get_properties_ins(self) -> global___ServerMessage.GetPropertiesIns: ...
    @property
    def get_parameters_ins(self) -> global___ServerMessage.GetParametersIns: ...
    @property
    def fit_ins(self) -> global___ServerMessage.FitIns: ...
    @property
    def evaluate_ins(self) -> global___ServerMessage.EvaluateIns: ...
    @property
    def example_ins(self) -> global___ServerMessage.ExampleIns: ...
    @property
    def send_vector_a_ins(self) -> global___ServerMessage.SendVectorAIns: ...
    @property
    def send_allpub_ins(self) -> global___ServerMessage.SendAllpubIns: ...
    @property
    def request_encrypted_ins(self) -> global___ServerMessage.RequestEncryptedIns: ...
    @property
    def send_csum_ins(self) -> global___ServerMessage.SendCsumIns: ...
    @property
    def send_new_weights_ins(self) -> global___ServerMessage.SendNewWeightsIns: ...
    def __init__(
        self,
        *,
        reconnect_ins: global___ServerMessage.ReconnectIns | None = ...,
        get_properties_ins: global___ServerMessage.GetPropertiesIns | None = ...,
        get_parameters_ins: global___ServerMessage.GetParametersIns | None = ...,
        fit_ins: global___ServerMessage.FitIns | None = ...,
        evaluate_ins: global___ServerMessage.EvaluateIns | None = ...,
        example_ins: global___ServerMessage.ExampleIns | None = ...,
        send_vector_a_ins: global___ServerMessage.SendVectorAIns | None = ...,
        send_allpub_ins: global___ServerMessage.SendAllpubIns | None = ...,
        request_encrypted_ins: global___ServerMessage.RequestEncryptedIns | None = ...,
        send_csum_ins: global___ServerMessage.SendCsumIns | None = ...,
        send_new_weights_ins: global___ServerMessage.SendNewWeightsIns | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["evaluate_ins", b"evaluate_ins", "example_ins", b"example_ins", "fit_ins", b"fit_ins", "get_parameters_ins", b"get_parameters_ins", "get_properties_ins", b"get_properties_ins", "msg", b"msg", "reconnect_ins", b"reconnect_ins", "request_encrypted_ins", b"request_encrypted_ins", "send_allpub_ins", b"send_allpub_ins", "send_csum_ins", b"send_csum_ins", "send_new_weights_ins", b"send_new_weights_ins", "send_vector_a_ins", b"send_vector_a_ins"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["evaluate_ins", b"evaluate_ins", "example_ins", b"example_ins", "fit_ins", b"fit_ins", "get_parameters_ins", b"get_parameters_ins", "get_properties_ins", b"get_properties_ins", "msg", b"msg", "reconnect_ins", b"reconnect_ins", "request_encrypted_ins", b"request_encrypted_ins", "send_allpub_ins", b"send_allpub_ins", "send_csum_ins", b"send_csum_ins", "send_new_weights_ins", b"send_new_weights_ins", "send_vector_a_ins", b"send_vector_a_ins"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["msg", b"msg"]) -> typing_extensions.Literal["reconnect_ins", "get_properties_ins", "get_parameters_ins", "fit_ins", "evaluate_ins", "example_ins", "send_vector_a_ins", "send_allpub_ins", "request_encrypted_ins", "send_csum_ins", "send_new_weights_ins"] | None: ...

global___ServerMessage = ServerMessage

@typing_extensions.final
class ClientMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class DisconnectRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        REASON_FIELD_NUMBER: builtins.int
        reason: global___Reason.ValueType
        def __init__(
            self,
            *,
            reason: global___Reason.ValueType = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["reason", b"reason"]) -> None: ...

    @typing_extensions.final
    class GetPropertiesRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class PropertiesEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.str
            @property
            def value(self) -> global___Scalar: ...
            def __init__(
                self,
                *,
                key: builtins.str = ...,
                value: global___Scalar | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        STATUS_FIELD_NUMBER: builtins.int
        PROPERTIES_FIELD_NUMBER: builtins.int
        @property
        def status(self) -> global___Status: ...
        @property
        def properties(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Scalar]: ...
        def __init__(
            self,
            *,
            status: global___Status | None = ...,
            properties: collections.abc.Mapping[builtins.str, global___Scalar] | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["status", b"status"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["properties", b"properties", "status", b"status"]) -> None: ...

    @typing_extensions.final
    class GetParametersRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        STATUS_FIELD_NUMBER: builtins.int
        PARAMETERS_FIELD_NUMBER: builtins.int
        @property
        def status(self) -> global___Status: ...
        @property
        def parameters(self) -> global___Parameters: ...
        def __init__(
            self,
            *,
            status: global___Status | None = ...,
            parameters: global___Parameters | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["parameters", b"parameters", "status", b"status"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["parameters", b"parameters", "status", b"status"]) -> None: ...

    @typing_extensions.final
    class FitRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class MetricsEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.str
            @property
            def value(self) -> global___Scalar: ...
            def __init__(
                self,
                *,
                key: builtins.str = ...,
                value: global___Scalar | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        STATUS_FIELD_NUMBER: builtins.int
        PARAMETERS_FIELD_NUMBER: builtins.int
        NUM_EXAMPLES_FIELD_NUMBER: builtins.int
        METRICS_FIELD_NUMBER: builtins.int
        @property
        def status(self) -> global___Status: ...
        @property
        def parameters(self) -> global___Parameters: ...
        num_examples: builtins.int
        @property
        def metrics(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Scalar]: ...
        def __init__(
            self,
            *,
            status: global___Status | None = ...,
            parameters: global___Parameters | None = ...,
            num_examples: builtins.int = ...,
            metrics: collections.abc.Mapping[builtins.str, global___Scalar] | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["parameters", b"parameters", "status", b"status"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["metrics", b"metrics", "num_examples", b"num_examples", "parameters", b"parameters", "status", b"status"]) -> None: ...

    @typing_extensions.final
    class EvaluateRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class MetricsEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.str
            @property
            def value(self) -> global___Scalar: ...
            def __init__(
                self,
                *,
                key: builtins.str = ...,
                value: global___Scalar | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        STATUS_FIELD_NUMBER: builtins.int
        LOSS_FIELD_NUMBER: builtins.int
        NUM_EXAMPLES_FIELD_NUMBER: builtins.int
        METRICS_FIELD_NUMBER: builtins.int
        @property
        def status(self) -> global___Status: ...
        loss: builtins.float
        num_examples: builtins.int
        @property
        def metrics(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Scalar]: ...
        def __init__(
            self,
            *,
            status: global___Status | None = ...,
            loss: builtins.float = ...,
            num_examples: builtins.int = ...,
            metrics: collections.abc.Mapping[builtins.str, global___Scalar] | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["status", b"status"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["loss", b"loss", "metrics", b"metrics", "num_examples", b"num_examples", "status", b"status"]) -> None: ...

    @typing_extensions.final
    class ExampleRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        RESPONSE_FIELD_NUMBER: builtins.int
        ANSWER_FIELD_NUMBER: builtins.int
        response: builtins.str
        answer: builtins.int
        def __init__(
            self,
            *,
            response: builtins.str = ...,
            answer: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["answer", b"answer", "response", b"response"]) -> None: ...

    @typing_extensions.final
    class SendVectorBRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        VECTOR_B_FIELD_NUMBER: builtins.int
        @property
        def vector_b(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            vector_b: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["vector_b", b"vector_b"]) -> None: ...

    @typing_extensions.final
    class SendAllpubRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        PUBKEY_CONFIRMED_FIELD_NUMBER: builtins.int
        pubkey_confirmed: builtins.bool
        def __init__(
            self,
            *,
            pubkey_confirmed: builtins.bool = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["pubkey_confirmed", b"pubkey_confirmed"]) -> None: ...

    @typing_extensions.final
    class SendEncryptedRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        C0_FIELD_NUMBER: builtins.int
        C1_FIELD_NUMBER: builtins.int
        @property
        def c0(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        @property
        def c1(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            c0: collections.abc.Iterable[builtins.int] | None = ...,
            c1: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["c0", b"c0", "c1", b"c1"]) -> None: ...

    @typing_extensions.final
    class SendDecShareRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        DECRYPTION_SHARE_FIELD_NUMBER: builtins.int
        @property
        def decryption_share(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
        def __init__(
            self,
            *,
            decryption_share: collections.abc.Iterable[builtins.int] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["decryption_share", b"decryption_share"]) -> None: ...

    @typing_extensions.final
    class SendNewWeightsRes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        WEIGHTS_CONFIRMED_FIELD_NUMBER: builtins.int
        weights_confirmed: builtins.bool
        def __init__(
            self,
            *,
            weights_confirmed: builtins.bool = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["weights_confirmed", b"weights_confirmed"]) -> None: ...

    DISCONNECT_RES_FIELD_NUMBER: builtins.int
    GET_PROPERTIES_RES_FIELD_NUMBER: builtins.int
    GET_PARAMETERS_RES_FIELD_NUMBER: builtins.int
    FIT_RES_FIELD_NUMBER: builtins.int
    EVALUATE_RES_FIELD_NUMBER: builtins.int
    EXAMPLE_RES_FIELD_NUMBER: builtins.int
    SEND_VECTOR_B_RES_FIELD_NUMBER: builtins.int
    SEND_ALLPUB_RES_FIELD_NUMBER: builtins.int
    SEND_ENCRYPTED_RES_FIELD_NUMBER: builtins.int
    SEND_DEC_SHARE_RES_FIELD_NUMBER: builtins.int
    SEND_NEW_WEIGHTS_RES_FIELD_NUMBER: builtins.int
    @property
    def disconnect_res(self) -> global___ClientMessage.DisconnectRes: ...
    @property
    def get_properties_res(self) -> global___ClientMessage.GetPropertiesRes: ...
    @property
    def get_parameters_res(self) -> global___ClientMessage.GetParametersRes: ...
    @property
    def fit_res(self) -> global___ClientMessage.FitRes: ...
    @property
    def evaluate_res(self) -> global___ClientMessage.EvaluateRes: ...
    @property
    def example_res(self) -> global___ClientMessage.ExampleRes: ...
    @property
    def send_vector_b_res(self) -> global___ClientMessage.SendVectorBRes: ...
    @property
    def send_allpub_res(self) -> global___ClientMessage.SendAllpubRes: ...
    @property
    def send_encrypted_res(self) -> global___ClientMessage.SendEncryptedRes: ...
    @property
    def send_dec_share_res(self) -> global___ClientMessage.SendDecShareRes: ...
    @property
    def send_new_weights_res(self) -> global___ClientMessage.SendNewWeightsRes: ...
    def __init__(
        self,
        *,
        disconnect_res: global___ClientMessage.DisconnectRes | None = ...,
        get_properties_res: global___ClientMessage.GetPropertiesRes | None = ...,
        get_parameters_res: global___ClientMessage.GetParametersRes | None = ...,
        fit_res: global___ClientMessage.FitRes | None = ...,
        evaluate_res: global___ClientMessage.EvaluateRes | None = ...,
        example_res: global___ClientMessage.ExampleRes | None = ...,
        send_vector_b_res: global___ClientMessage.SendVectorBRes | None = ...,
        send_allpub_res: global___ClientMessage.SendAllpubRes | None = ...,
        send_encrypted_res: global___ClientMessage.SendEncryptedRes | None = ...,
        send_dec_share_res: global___ClientMessage.SendDecShareRes | None = ...,
        send_new_weights_res: global___ClientMessage.SendNewWeightsRes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["disconnect_res", b"disconnect_res", "evaluate_res", b"evaluate_res", "example_res", b"example_res", "fit_res", b"fit_res", "get_parameters_res", b"get_parameters_res", "get_properties_res", b"get_properties_res", "msg", b"msg", "send_allpub_res", b"send_allpub_res", "send_dec_share_res", b"send_dec_share_res", "send_encrypted_res", b"send_encrypted_res", "send_new_weights_res", b"send_new_weights_res", "send_vector_b_res", b"send_vector_b_res"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["disconnect_res", b"disconnect_res", "evaluate_res", b"evaluate_res", "example_res", b"example_res", "fit_res", b"fit_res", "get_parameters_res", b"get_parameters_res", "get_properties_res", b"get_properties_res", "msg", b"msg", "send_allpub_res", b"send_allpub_res", "send_dec_share_res", b"send_dec_share_res", "send_encrypted_res", b"send_encrypted_res", "send_new_weights_res", b"send_new_weights_res", "send_vector_b_res", b"send_vector_b_res"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["msg", b"msg"]) -> typing_extensions.Literal["disconnect_res", "get_properties_res", "get_parameters_res", "fit_res", "evaluate_res", "example_res", "send_vector_b_res", "send_allpub_res", "send_encrypted_res", "send_dec_share_res", "send_new_weights_res"] | None: ...

global___ClientMessage = ClientMessage

@typing_extensions.final
class Scalar(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DOUBLE_FIELD_NUMBER: builtins.int
    SINT64_FIELD_NUMBER: builtins.int
    BOOL_FIELD_NUMBER: builtins.int
    STRING_FIELD_NUMBER: builtins.int
    BYTES_FIELD_NUMBER: builtins.int
    double: builtins.float
    sint64: builtins.int
    """float float = 2;
    int32 int32 = 3;
    int64 int64 = 4;
    uint32 uint32 = 5;
    uint64 uint64 = 6;
    sint32 sint32 = 7;
    """
    bool: builtins.bool
    """fixed32 fixed32 = 9;
    fixed64 fixed64 = 10;
    sfixed32 sfixed32 = 11;
    sfixed64 sfixed64 = 12;
    """
    string: builtins.str
    bytes: builtins.bytes
    def __init__(
        self,
        *,
        double: builtins.float = ...,
        sint64: builtins.int = ...,
        bool: builtins.bool = ...,
        string: builtins.str = ...,
        bytes: builtins.bytes = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool", b"bool", "bytes", b"bytes", "double", b"double", "scalar", b"scalar", "sint64", b"sint64", "string", b"string"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool", b"bool", "bytes", b"bytes", "double", b"double", "scalar", b"scalar", "sint64", b"sint64", "string", b"string"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["scalar", b"scalar"]) -> typing_extensions.Literal["double", "sint64", "bool", "string", "bytes"] | None: ...

global___Scalar = Scalar
