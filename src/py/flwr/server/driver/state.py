# Copyright 2022 Adap GmbH. All Rights Reserved.
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
"""DriverState."""


from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Set
from uuid import UUID, uuid4

from flwr.proto.task_pb2 import TaskIns, TaskRes


class DriverState:
    """DriverState."""

    def __init__(self) -> None:
        self.task_ins_store: Dict[UUID, TaskIns] = {}
        self.task_res_store: Dict[UUID, TaskRes] = {}

    def store_task_ins(self, task_ins: TaskIns) -> Optional[UUID]:
        """Store one TaskIns."""

        # Create and set task_id
        task_id = uuid4()
        task_ins.task_id = str(task_id)

        # Set created_at
        created_at: datetime = _now()
        ttl: datetime = created_at + timedelta(hours=24)

        # Store TaskIns
        task_ins.task.created_at = created_at.isoformat()
        task_ins.task.ttl = ttl.isoformat()
        self.task_ins_store[task_id] = task_ins

        # Return the new task_id
        return task_id

    def get_task_ins(self, node_id: int, limit: Optional[int]) -> List[TaskIns]:
        """Get all TaskIns that have not been delivered yet."""

        # Find TaskIns for node_id that were not delivered yet
        task_ins_set: List[TaskIns] = []
        for _, task_ins in self.task_ins_store.items():
            if (
                task_ins.task.consumer.node_id == node_id
                and task_ins.task.delivered_at == ""
            ):
                task_ins_set.append(task_ins)
            if limit is not None and len(task_ins_set) == limit:
                break

        # Mark all of them as delivered
        delivered_at = _now().isoformat()
        for task_ins in task_ins_set:
            task_ins.task.delivered_at = delivered_at

        # Return TaskIns
        return task_ins_set

    def store_task_res(self, task_res: TaskRes) -> Optional[UUID]:
        """Store one TaskRes."""

        # Create and set task_id
        task_id = uuid4()
        task_res.task_id = str(task_id)

        # Set created_at
        created_at: datetime = _now()
        ttl: datetime = created_at + timedelta(hours=24)

        # Store TaskRes
        task_res.task.created_at = created_at.isoformat()
        task_res.task.ttl = ttl.isoformat()
        self.task_res_store[task_id] = task_res

        # Return the new task_id
        return task_id

    def get_task_res(self, task_ids: Set[UUID], limit: Optional[int]) -> List[TaskRes]:
        """Get all TaskRes that have not been delivered yet."""

        # Find TaskRes that were not delivered yet
        task_res_set: List[TaskRes] = []
        for _, task_res in self.task_res_store.items():
            if (
                UUID(task_res.task.ancestry[0]) in task_ids
                and task_res.task.delivered_at == ""
            ):
                task_res_set.append(task_res)
            if limit is not None and len(task_res_set) == limit:
                break

        # Mark all of them as delivered
        delivered_at = _now().isoformat()
        for task_res in task_res_set:
            task_res.task.delivered_at = delivered_at

        # Return TaskRes
        return task_res_set


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)
