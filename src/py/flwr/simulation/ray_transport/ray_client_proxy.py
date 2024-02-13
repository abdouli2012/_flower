# Copyright 2020 Flower Labs GmbH. All Rights Reserved.
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
"""Ray-based Flower ClientProxy implementation."""


import traceback
from logging import ERROR
from typing import Optional

from flwr import common
from flwr.client import ClientFn
from flwr.client.clientapp import ClientApp
from flwr.client.node_state import NodeState
from flwr.common.constant import (
    TASK_TYPE_EVALUATE,
    TASK_TYPE_FIT,
    TASK_TYPE_GET_PARAMETERS,
    TASK_TYPE_GET_PROPERTIES,
)
from flwr.common.logger import log
from flwr.common.message import Message, Metadata
from flwr.common.recordset import RecordSet
from flwr.common.recordset_compat import (
    evaluateins_to_recordset,
    fitins_to_recordset,
    getparametersins_to_recordset,
    getpropertiesins_to_recordset,
    recordset_to_evaluateres,
    recordset_to_fitres,
    recordset_to_getparametersres,
    recordset_to_getpropertiesres,
)
from flwr.server.client_proxy import ClientProxy
from flwr.simulation.ray_transport.ray_actor import VirtualClientEngineActorPool


class RayActorClientProxy(ClientProxy):
    """Flower client proxy which delegates work using Ray."""

    def __init__(
        self, client_fn: ClientFn, cid: str, actor_pool: VirtualClientEngineActorPool
    ):
        super().__init__(cid)

        def _load_app() -> ClientApp:
            return ClientApp(client_fn=client_fn)

        self.app_fn = _load_app
        self.actor_pool = actor_pool
        self.proxy_state = NodeState()

    def _submit_job(self, message: Message, timeout: Optional[float]) -> Message:
        """Sumbit a message to the AcotrPool."""
        # For the time being, fixing run_id is a small compromise
        # This will be one of the first points to address integrating VCE + DriverAPI
        run_id = message.metadata.run_id

        # Register state
        self.proxy_state.register_context(run_id=run_id)

        # Retrieve state
        state = self.proxy_state.retrieve_context(run_id=run_id)

        try:
            self.actor_pool.submit_client_job(
                lambda a, a_fn, mssg, cid, state: a.run.remote(a_fn, mssg, cid, state),
                (self.app_fn, message, self.cid, state),
            )
            out_mssg, updated_context = self.actor_pool.get_client_result(
                self.cid, timeout
            )

            # Update state
            self.proxy_state.update_context(run_id=run_id, context=updated_context)

        except Exception as ex:
            if self.actor_pool.num_actors == 0:
                # At this point we want to stop the simulation.
                # since no more client runs will be executed
                log(ERROR, "ActorPool is empty!!!")
            log(ERROR, traceback.format_exc())
            log(ERROR, ex)
            raise ex

        return out_mssg

    def _wrap_recordset_in_message(
        self, recordset: RecordSet, task_type: str
    ) -> Message:
        """Wrap a RecordSet inside a Message."""
        return Message(
            content=recordset,
            metadata=Metadata(
                run_id=0,
                task_id="",
                group_id="",
                node_id=int(self.cid),
                ttl="",
                task_type=task_type,
            ),
        )

    def get_properties(
        self, ins: common.GetPropertiesIns, timeout: Optional[float]
    ) -> common.GetPropertiesRes:
        """Return client's properties."""
        recordset = getpropertiesins_to_recordset(ins)
        message = self._wrap_recordset_in_message(
            recordset, task_type=TASK_TYPE_GET_PROPERTIES
        )

        message_out = self._submit_job(message, timeout)

        return recordset_to_getpropertiesres(message_out.content)

    def get_parameters(
        self, ins: common.GetParametersIns, timeout: Optional[float]
    ) -> common.GetParametersRes:
        """Return the current local model parameters."""
        recordset = getparametersins_to_recordset(ins)
        message = self._wrap_recordset_in_message(
            recordset, task_type=TASK_TYPE_GET_PARAMETERS
        )

        message_out = self._submit_job(message, timeout)

        return recordset_to_getparametersres(message_out.content, keep_input=False)

    def fit(self, ins: common.FitIns, timeout: Optional[float]) -> common.FitRes:
        """Train model parameters on the locally held dataset."""
        recordset = fitins_to_recordset(
            ins, keep_input=True
        )  # This must stay TRUE since ins are in-memory
        message = self._wrap_recordset_in_message(recordset, task_type=TASK_TYPE_FIT)

        message_out = self._submit_job(message, timeout)

        return recordset_to_fitres(message_out.content, keep_input=False)

    def evaluate(
        self, ins: common.EvaluateIns, timeout: Optional[float]
    ) -> common.EvaluateRes:
        """Evaluate model parameters on the locally held dataset."""
        recordset = evaluateins_to_recordset(
            ins, keep_input=True
        )  # This must stay TRUE since ins are in-memory
        message = self._wrap_recordset_in_message(
            recordset, task_type=TASK_TYPE_EVALUATE
        )

        message_out = self._submit_job(message, timeout)

        return recordset_to_evaluateres(message_out.content)

    def reconnect(
        self, ins: common.ReconnectIns, timeout: Optional[float]
    ) -> common.DisconnectRes:
        """Disconnect and (optionally) reconnect later."""
        return common.DisconnectRes(reason="")  # Nothing to do here (yet)
