# Copyright 2023 Flower Labs GmbH. All Rights Reserved.
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
"""Custom types for Flower clients."""

from dataclasses import dataclass
from typing import Callable

from flwr.client.run_state import RunState
from flwr.common.context import Context
from flwr.common.message import Message
from flwr.proto.task_pb2 import TaskIns, TaskRes  # pylint: disable=E0611

from .client import Client as Client


@dataclass
class Fwd:
    """."""

    task_ins: TaskIns
    state: RunState


@dataclass
class Bwd:
    """."""

    task_res: TaskRes
    state: RunState


FlowerCallable = Callable[[Message, Context], Message]
ClientFn = Callable[[str], Client]
Layer = Callable[[Message, FlowerCallable, Context], Message]
