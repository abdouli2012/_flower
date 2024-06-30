# Copyright 2024 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower ClientApp."""


from typing import Callable, List, Optional, Union

from flwr.client.client import Client
from flwr.client.message_handler.message_handler import (
    handle_legacy_message_from_msgtype,
)
from flwr.client.mod.utils import make_ffn
from flwr.client.typing import ClientFn, ClientFnExt, Mod
from flwr.common import Context, Message, MessageType
from flwr.common.logger import warn_deprecated_feature, warn_preview_feature

from .typing import ClientAppCallable


class ClientAppException(Exception):
    """Exception raised when an exception is raised while executing a ClientApp."""

    def __init__(self, message: str):
        ex_name = self.__class__.__name__
        self.message = f"\nException {ex_name} occurred. Message: " + message
        super().__init__(self.message)


def _inspect_maybe_adapt_client_fn_signature(
    client_fn: Union[ClientFn, ClientFnExt]
) -> ClientFnExt:

    if "cid" in client_fn.__annotations__:
        warn_deprecated_feature(
            "Passing a `client_fn` with signature `def client_fn(cid: str)` "
            "is deprecated. Use instead signature `def client_fn(node_id: int, "
            "partition_id: Optional[int])`.",
        )

        # Wrap depcreated client_fn inside a function with the expected signature
        def adaptor_fn(
            node_id: int, partition_id: Optional[int]  # pylint: disable=unused-argument
        ) -> Client:
            return client_fn(str(partition_id))  # type: ignore

    else:

        def adaptor_fn(node_id: int, partition_id: Optional[int]) -> Client:
            return client_fn(node_id, partition_id)  # type: ignore

    return adaptor_fn


class ClientApp:
    """Flower ClientApp.

    Examples
    --------
    Assuming a typical `Client` implementation named `FlowerClient`, you can wrap it in
    a `ClientApp` as follows:

    >>> class FlowerClient(NumPyClient):
    >>>     # ...
    >>>
    >>> def client_fn(cid):
    >>>    return FlowerClient().to_client()
    >>>
    >>> app = ClientApp(client_fn)

    If the above code is in a Python module called `client`, it can be started as
    follows:

    >>> flower-client-app client:app --insecure

    In this `client:app` example, `client` refers to the Python module `client.py` in
    which the previous code lives in and `app` refers to the global attribute `app` that
    points to an object of type `ClientApp`.
    """

    def __init__(
        self,
        client_fn: Optional[ClientFnExt] = None,  # Only for backward compatibility
        mods: Optional[List[Mod]] = None,
    ) -> None:
        self._mods: List[Mod] = mods if mods is not None else []

        # Create wrapper function for `handle`
        self._call: Optional[ClientAppCallable] = None
        self.client_fn = (
            _inspect_maybe_adapt_client_fn_signature(client_fn) if client_fn else None
        )

        # Step functions
        self._train: Optional[ClientAppCallable] = None
        self._evaluate: Optional[ClientAppCallable] = None
        self._query: Optional[ClientAppCallable] = None

    def _prep_call(self) -> ClientAppCallable:
        """Prepare for client_fn-based execution."""

        def ffn(
            message: Message,
            context: Context,
        ) -> Message:  # pylint: disable=invalid-name
            out_message = handle_legacy_message_from_msgtype(
                client_fn=self.client_fn,  # type: ignore
                message=message,
                context=context,
            )
            return out_message

        # Wrap mods around the wrapped handle function
        return make_ffn(ffn, self._mods)

    def __call__(self, message: Message, context: Context) -> Message:
        """Execute `ClientApp`."""
        # Execute message using `client_fn`
        if self.client_fn is not None:
            if self._call is None:
                self._call = self._prep_call()
            return self._call(message, context)

        # Execute message using a new
        if message.metadata.message_type == MessageType.TRAIN:
            if self._train:
                return self._train(message, context)
            raise ValueError("No `train` function registered")
        if message.metadata.message_type == MessageType.EVALUATE:
            if self._evaluate:
                return self._evaluate(message, context)
            raise ValueError("No `evaluate` function registered")
        if message.metadata.message_type == MessageType.QUERY:
            if self._query:
                return self._query(message, context)
            raise ValueError("No `query` function registered")

        # Message type did not match one of the known message types abvoe
        raise ValueError(f"Unknown message_type: {message.metadata.message_type}")

    def train(self) -> Callable[[ClientAppCallable], ClientAppCallable]:
        """Return a decorator that registers the train fn with the client app.

        Examples
        --------
        >>> app = ClientApp()
        >>>
        >>> @app.train()
        >>> def train(message: Message, context: Context) -> Message:
        >>>    print("ClientApp training running")
        >>>    # Create and return an echo reply message
        >>>    return message.create_reply(content=message.content())
        """

        def train_decorator(train_fn: ClientAppCallable) -> ClientAppCallable:
            """Register the train fn with the ServerApp object."""
            if self._call:
                raise _registration_error(MessageType.TRAIN)

            warn_preview_feature("ClientApp-register-train-function")

            # Register provided function with the ClientApp object
            # Wrap mods around the wrapped step function
            self._train = make_ffn(train_fn, self._mods)

            # Return provided function unmodified
            return train_fn

        return train_decorator

    def evaluate(self) -> Callable[[ClientAppCallable], ClientAppCallable]:
        """Return a decorator that registers the evaluate fn with the client app.

        Examples
        --------
        >>> app = ClientApp()
        >>>
        >>> @app.evaluate()
        >>> def evaluate(message: Message, context: Context) -> Message:
        >>>    print("ClientApp evaluation running")
        >>>    # Create and return an echo reply message
        >>>    return message.create_reply(content=message.content())
        """

        def evaluate_decorator(evaluate_fn: ClientAppCallable) -> ClientAppCallable:
            """Register the evaluate fn with the ServerApp object."""
            if self._call:
                raise _registration_error(MessageType.EVALUATE)

            warn_preview_feature("ClientApp-register-evaluate-function")

            # Register provided function with the ClientApp object
            # Wrap mods around the wrapped step function
            self._evaluate = make_ffn(evaluate_fn, self._mods)

            # Return provided function unmodified
            return evaluate_fn

        return evaluate_decorator

    def query(self) -> Callable[[ClientAppCallable], ClientAppCallable]:
        """Return a decorator that registers the query fn with the client app.

        Examples
        --------
        >>> app = ClientApp()
        >>>
        >>> @app.query()
        >>> def query(message: Message, context: Context) -> Message:
        >>>    print("ClientApp query running")
        >>>    # Create and return an echo reply message
        >>>    return message.create_reply(content=message.content())
        """

        def query_decorator(query_fn: ClientAppCallable) -> ClientAppCallable:
            """Register the query fn with the ServerApp object."""
            if self._call:
                raise _registration_error(MessageType.QUERY)

            warn_preview_feature("ClientApp-register-query-function")

            # Register provided function with the ClientApp object
            # Wrap mods around the wrapped step function
            self._query = make_ffn(query_fn, self._mods)

            # Return provided function unmodified
            return query_fn

        return query_decorator


class LoadClientAppError(Exception):
    """Error when trying to load `ClientApp`."""


def _registration_error(fn_name: str) -> ValueError:
    return ValueError(
        f"""Use either `@app.{fn_name}()` or `client_fn`, but not both.

        Use the `ClientApp` with an existing `client_fn`:

        >>> class FlowerClient(NumPyClient):
        >>>     # ...
        >>>
        >>> def client_fn(cid) -> Client:
        >>>     return FlowerClient().to_client()
        >>>
        >>> app = ClientApp(
        >>>     client_fn=client_fn,
        >>> )

        Use the `ClientApp` with a custom {fn_name} function:

        >>> app = ClientApp()
        >>>
        >>> @app.{fn_name}()
        >>> def {fn_name}(message: Message, context: Context) -> Message:
        >>>    print("ClientApp {fn_name} running")
        >>>    # Create and return an echo reply message
        >>>    return message.create_reply(
        >>>        content=message.content()
        >>>    )
        """,
    )
