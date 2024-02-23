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
"""Generic Backend class for Fleet API using the Simulation Engine."""


from abc import ABC, abstractmethod
from typing import Callable, Dict, Tuple

from flwr.client.clientapp import ClientApp
from flwr.common.context import Context
from flwr.common.message import Message
from flwr.common.typing import ConfigsRecordValues

BackendConfig = Dict[str, Dict[str, ConfigsRecordValues]]


class Backend(ABC):
    """Abstract base class for a Simulation Engine Backend."""

    def __init__(self, backend_config: BackendConfig, work_dir: str) -> None:
        """Construct a backend."""

    @abstractmethod
    async def build(self) -> None:
        """Build backend asynchronously.

        Different components need to be in place before workers in a backend are ready
        to accept jobs. When this method finishes executing, the backend should be fully
        ready to run jobs.
        """

    @property
    def num_workers(self) -> int:
        """Return number of workers in the backend.

        This is the number of TaskIns that can be processed concurrently.
        """
        return 0

    @abstractmethod
    def is_worker_idle(self) -> bool:
        """Report whether a backend worker is idle and can therefore run a ClientApp."""

    @abstractmethod
    async def process_message(
        self,
        app: Callable[[], ClientApp],
        message: Message,
        context: Context,
    ) -> Tuple[Message, Context]:
        """Submit a job to the backend."""
