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
"""Clipping modifier for central DP with client side clipping."""


from flwr.client.typing import ClientAppCallable
from flwr.common import ndarrays_to_parameters, parameters_to_ndarrays
from flwr.common import recordset_compat as compat
from flwr.common.constant import MESSAGE_TYPE_FIT
from flwr.common.context import Context
from flwr.common.differential_privacy import (
    compute_adaptive_clip_model_update,
    compute_clip_model_update,
)
from flwr.common.differential_privacy_constants import KEY_CLIPPING_NORM, KEY_NORM_BIT
from flwr.common.message import Message


def fixedclipping_mod(
    msg: Message, ctxt: Context, call_next: ClientAppCallable
) -> Message:
    """Clip the client model updates before sending them to the server."""
    if msg.metadata.message_type == MESSAGE_TYPE_FIT:
        fit_ins = compat.recordset_to_fitins(msg.message, keep_input=True)
        if KEY_CLIPPING_NORM not in fit_ins.config:
            raise KeyError(f"{KEY_CLIPPING_NORM} is not supplied by the server.")
        clipping_norm = float(fit_ins.config[KEY_CLIPPING_NORM])
        server_to_client_params = parameters_to_ndarrays(fit_ins.parameters)

        # Call inner app
        out_msg = call_next(msg, ctxt)
        fit_res = compat.recordset_to_fitres(out_msg.content, keep_input=True)

        client_to_server_params = parameters_to_ndarrays(fit_res.parameters)

        # Clip the client update
        compute_clip_model_update(
            client_to_server_params,
            server_to_client_params,
            clipping_norm,
        )

        fit_res.parameters = ndarrays_to_parameters(client_to_server_params)
        out_msg.content = compat.fitres_to_recordset(fit_res, keep_input=True)
        return out_msg
    return call_next(msg, ctxt)


def adaptiveclipping_mod(
    msg: Message, ctxt: Context, call_next: ClientAppCallable
) -> Message:
    """Clip the client model updates before sending them to the server."""
    if msg.metadata.message_type == TASK_TYPE_FIT:
        fit_ins = compat.recordset_to_fitins(msg.content, keep_input=True)

        if KEY_CLIPPING_NORM not in fit_ins.config:
            raise KeyError(f"{KEY_CLIPPING_NORM} is not supplied by the server.")
        if not isinstance(fit_ins.config[KEY_CLIPPING_NORM], float):
            raise ValueError(f"{KEY_CLIPPING_NORM} should be a float value.")
        clipping_norm = float(fit_ins.config[KEY_CLIPPING_NORM])

        server_to_client_params = parameters_to_ndarrays(fit_ins.parameters)

        # Call inner app
        out_msg = call_next(msg, ctxt)
        fit_res = compat.recordset_to_fitres(out_msg.content, keep_input=True)

        client_to_server_params = parameters_to_ndarrays(fit_res.parameters)

        # Clip the client update
        norm_bit = compute_adaptive_clip_model_update(
            client_to_server_params,
            server_to_client_params,
            clipping_norm,
        )

        fit_res.parameters = ndarrays_to_parameters(client_to_server_params)

        fit_res.metrics[KEY_NORM_BIT] = norm_bit
        out_msg.content = compat.fitres_to_recordset(fit_res, keep_input=True)
        return out_msg
    return call_next(msg, ctxt)
