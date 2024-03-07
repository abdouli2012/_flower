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
"""Workflow for the SecAgg+ protocol."""


from __future__ import annotations

import random
from dataclasses import dataclass, field
from logging import ERROR, WARN

import numpy as np

import flwr.common.recordset_compat as compat
from flwr.common import (
    ConfigsRecord,
    Context,
    Message,
    MessageType,
    NDArrays,
    RecordSet,
    bytes_to_ndarray,
    log,
)
from flwr.common.secure_aggregation.crypto.shamir import combine_shares
from flwr.common.secure_aggregation.crypto.symmetric_encryption import (
    bytes_to_private_key,
    bytes_to_public_key,
    generate_shared_key,
)
from flwr.common.secure_aggregation.ndarrays_arithmetic import (
    get_parameters_shape,
    parameters_addition,
    parameters_mod,
    parameters_subtraction,
)
from flwr.common.secure_aggregation.quantization import dequantize, quantize
from flwr.common.secure_aggregation.secaggplus_constants import (
    RECORD_KEY_CONFIGS,
    Key,
    Stage,
)
from flwr.common.secure_aggregation.secaggplus_utils import pseudo_rand_gen
from flwr.server.compat.legacy_context import LegacyContext
from flwr.server.driver import Driver

from ..default_constant import MAIN_CONFIGS_RECORD, MAIN_PARAMS_RECORD
from ..default_constant import Key as DefaultKey

LOG_EXPLAIN = True


@dataclass
class WorkflowState:
    """The state of the SecAgg+ protocol."""

    nid_to_fitins: dict[int, RecordSet] = field(default_factory=dict)
    sampled_node_ids: set[int] = field(default_factory=set)
    active_node_ids: set[int] = field(default_factory=set)
    num_shares: int = 0
    threshold: int = 0
    clipping_range: float = 0.0
    quantization_range: int = 0
    mod_range: int = 0
    nid_to_neighbours: dict[int, set[int]] = field(default_factory=dict)
    nid_to_publickeys: dict[int, tuple[int, int]] = field(default_factory=dict)
    forward_srcs: dict[int, list[int]] = field(default_factory=dict)
    forward_ciphertexts: dict[int, list[bytes]] = field(default_factory=dict)
    aggregate_ndarrays: NDArrays = field(default_factory=list)


class SecAggPlusWorkflow:
    """The workflow for the SecAgg+ protocol.

    Parameters
    ----------
    num_shares : Union[int, float]
        The number of shares into which each client's private key is split under
        the SecAgg+ protocol. If specified as a float, it represents the proportion
        of all selected clients, and the number of shares will be set dynamically in
        the run time. A private key can be reconstructed from these shares, allowing
        for the secure aggregation of model updates. Each client sends one share to
        each of its neighbors while retaining one.
    reconstruction_threshold : Union[int, float]
        The minimum number of shares required to reconstruct a client's private key,
        or, if specified as a float, it represents the proportion of the total number
        of shares needed for reconstruction. This threshold ensures privacy by allowing
        for the recovery of contributions from dropped clients during aggregation,
        without compromising individual client data.
    max_weight : Optional[float] (default: 1000.0)
        The maximum value of the weight that can be assigned to any single client's
        update during the weighted average calculation on the server side, e.g., in the
        FedAvg algorithm.
    clipping_range : float, optional (default: 8.0)
        The range within which model parameters are clipped before quantization.
        This parameter ensures each model parameter is bounded within
        [-clipping_range, clipping_range], facilitating quantization.
    quantization_range : int, optional (default: 1048576, this equals 2**20)
        The size of the range into which floating-point model parameters are quantized,
        mapping each parameter to an integer in [0, quantization_range-1]. This
        facilitates cryptographic operations on the model updates.
    modulus_range : int, optional (default: 2147483648, this equals 2**30)
        The range of values from which random mask entries are uniformly sampled
        ([0, modulus_range-1]).
    timeout : Optional[float] (default: None)
        The timeout duration in seconds. If specified, the workflow will wait for
        replies for this duration each time. If `None`, there is no time limit and
        the workflow will wait until replies for all messages are received.

    Notes
    -----
    - Generally, higher `num_shares` means more robust to dropouts while increasing the
    computational costs; higher `reconstruction_threshold` means better privacy
    guarantees but less tolerance to dropouts.
    - Too large `max_weight` may compromise the precision of the quantization.
    - `modulus_range` must be larger than `quantization_range`.
    - When `num_shares` is a float, it is interpreted as the proportion of all selected
    clients, and hence the number of shares will be determined in the runtime. This
    allows for dynamic adjustment based on the total number of participating clients.
    - Similarly, when `reconstruction_threshold` is a float, it is interpreted as the
    proportion of the number of shares needed for the reconstruction of a private key.
    This feature enables flexibility in setting the security threshold relative to the
    number of distributed shares.
    - `num_shares`, `reconstruction_threshold`, and the quantization parameters
    (`clipping_range`, `target_quantization_range`, `modulus_range`) play critical roles
    in balancing privacy, robustness, and efficiency within the SecAgg+ protocol.
    """

    def __init__(
        self,
        num_shares: int | float,
        reconstruction_threshold: int | float,
        *,
        max_weight: float = 1000.0,
        clipping_range: float = 8.0,
        quantization_range: int = 1048576,
        modulus_range: int = 2147483648,
        timeout: float | None = None,
    ) -> None:
        self.num_shares = num_shares
        self.reconstruction_threshold = reconstruction_threshold
        self.max_weight = max_weight
        self.clipping_range = clipping_range
        self.quantization_range = quantization_range
        self.modulus_range = modulus_range
        self.timeout = timeout

        self._check_init_params()

    def __call__(self, driver: Driver, context: Context) -> None:
        """Run the SecAgg+ protocol."""
        if not isinstance(context, LegacyContext):
            raise TypeError(
                f"Expect a LegacyContext, but get {type(context).__name__}."
            )
        state = WorkflowState()

        steps = (
            self._setup,
            self._share_keys,
            self._collect_masked_input,
            self._unmask,
        )
        for step in steps:
            if not step(driver, context, state):
                return

    def _check_init_params(self) -> None:
        # Check `num_shares`
        if not isinstance(self.num_shares, (int, float)):
            raise TypeError("`num_shares` must be of type int or float.")
        if isinstance(self.num_shares, int):
            if self.num_shares <= 2:
                raise ValueError("`num_shares` as an integer must be greater than 2.")
            if self.num_shares > self.modulus_range / self.quantization_range:
                log(
                    WARN,
                    "A `num_shares` larger than `mod_range / target_range` "
                    "will potentially cause overflow when computing the aggregated "
                    "model parameters.",
                )
            if self.num_shares == 1:
                self.num_shares = 1.0
        elif self.num_shares <= 0:
            raise ValueError("`num_shares` as a float must be greater than 0.")

        # Check `reconstruction_threshold`
        if not isinstance(self.reconstruction_threshold, (int, float)):
            raise TypeError("`reconstruction_threshold` must be of type int or float.")
        if isinstance(self.reconstruction_threshold, int):
            if isinstance(self.num_shares, int):
                if self.reconstruction_threshold >= self.num_shares:
                    raise ValueError(
                        "`reconstruction_threshold` must be less than `num_shares`."
                    )
            if self.reconstruction_threshold == 1:
                self.reconstruction_threshold = 1.0
        else:
            if not (0 < self.reconstruction_threshold <= 1):
                raise ValueError(
                    "If `reconstruction_threshold` is a float, "
                    "it must be greater than 0 and less than or equal to 1."
                )

        # Check `max_weight`
        if self.max_weight <= 0:
            raise ValueError("`max_weight` must be greater than 0.")

        # Check `quantization_range`
        if self.quantization_range <= 0:
            raise ValueError("`quantization_range` must be greater than 0.")

        # Check `target_range`
        if not isinstance(self.quantization_range, int) or self.quantization_range <= 0:
            raise ValueError("`target_range` must be an integer and greater than 0.")

        # Check `mod_range`
        if (
            not isinstance(self.modulus_range, int)
            or self.modulus_range <= self.quantization_range
        ):
            raise ValueError(
                "`mod_range` must be an integer and greater than `target_range`."
            )

    def _check_threshold(self, state: WorkflowState) -> bool:
        for node_id in state.sampled_node_ids:
            active_neighbors = state.nid_to_neighbours[node_id] & state.active_node_ids
            if len(active_neighbors) < state.threshold:
                log(ERROR, "Insufficient available nodes.")
                return False
        return True

    def _setup(
        self, driver: Driver, context: LegacyContext, state: WorkflowState
    ) -> bool:
        # Obtain fit instructions
        cfg = context.state.configs_records[MAIN_CONFIGS_RECORD]
        parameters = compat.parametersrecord_to_parameters(
            context.state.parameters_records[MAIN_PARAMS_RECORD],
            keep_input=True,
        )
        proxy_fitins_lst = context.strategy.configure_fit(
            cfg[DefaultKey.CURRENT_ROUND], parameters, context.client_manager
        )
        for idx, (proxy, fitins) in enumerate(proxy_fitins_lst):
            fitins.config["drop"] = (idx == 0)
            state.nid_to_fitins[proxy.node_id] = compat.fitins_to_recordset(fitins, True)
        # state.nid_to_fitins = {
        #     proxy.node_id: compat.fitins_to_recordset(fitins, False)
        #     for proxy, fitins in proxy_fitins_lst
        # }

        # Protocol config
        sampled_node_ids = list(state.nid_to_fitins.keys())
        num_samples = len(sampled_node_ids)
        if num_samples < 2:
            log(ERROR, "The number of samples should be greater than 1.")
            return False
        if isinstance(self.num_shares, float):
            state.num_shares = round(self.num_shares * num_samples)
            # If even
            if state.num_shares < num_samples and state.num_shares & 1 == 0:
                state.num_shares += 1
            # If too small
            if state.num_shares <= 2:
                state.num_shares = num_samples
        else: 
            state.num_shares = self.num_shares
        if isinstance(self.reconstruction_threshold, float):
            state.threshold = round(self.reconstruction_threshold * state.num_shares)
            # If too small
            if state.threshold < 2:
                state.threshold = 2
        else:
            state.threshold = self.reconstruction_threshold
        state.active_node_ids = set(sampled_node_ids)
        state.clipping_range = self.clipping_range
        state.quantization_range = self.quantization_range
        state.mod_range = self.modulus_range
        if LOG_EXPLAIN:
            _quantized = quantize(
                [np.ones(3) for _ in range(num_samples)],
                state.clipping_range,
                state.quantization_range,
            )
            print(
                "\n\n################################ Introduction ################################\n"
                "In the example, each client will upload a vector [1.0, 1.0, 1.0] instead of\n"
                "model updates for demonstration purposes.\n"
                "Client 0 is configured to drop out before uploading the masked vector.\n"
                "After quantization, the raw vectors will be:"
            )
            for i in range(1, num_samples):
                print(f"\t{_quantized[i]} from Client {i}")
            print(
                "Numbers are rounded to integers stochastically during the quantization\n"
                ", and thus not all entries are identical."
            )
            print(
                "The above raw vectors are hidden from the driver through adding masks.\n"
            )
            print(
                "########################## Secure Aggregation Start ##########################"
            )
        sa_params_dict = {
            Key.STAGE: Stage.SETUP,
            Key.SAMPLE_NUMBER: num_samples,
            Key.SHARE_NUMBER: state.num_shares,
            Key.THRESHOLD: state.threshold,
            Key.CLIPPING_RANGE: state.clipping_range,
            Key.TARGET_RANGE: state.quantization_range,
            Key.MOD_RANGE: state.mod_range,
        }
        print(sa_params_dict)

        # The number of shares should better be odd in the SecAgg+ protocol.
        if num_samples != state.num_shares and state.num_shares & 1 == 0:
            log(WARN, "Number of shares in the SecAgg+ protocol should be odd.")
            state.num_shares += 1

        # Shuffle node IDs
        random.shuffle(sampled_node_ids)
        # Build neighbour relations (node ID -> secure IDs of neighbours)
        half_share = state.num_shares >> 1
        state.nid_to_neighbours = {
            nid: {
                sampled_node_ids[(idx + offset) % num_samples]
                for offset in range(-half_share, half_share + 1)
            }
            for idx, nid in enumerate(sampled_node_ids)
        }

        state.sampled_node_ids = state.active_node_ids

        # Send setup configuration to clients
        cfgs_record = ConfigsRecord(sa_params_dict)
        content = RecordSet(configs_records={RECORD_KEY_CONFIGS: cfgs_record})

        def make(nid: int) -> Message:
            return driver.create_message(
                content=content,
                message_type=MessageType.TRAIN,
                dst_node_id=nid,
                group_id=str(cfg[DefaultKey.CURRENT_ROUND]),
                ttl="",
            )

        if LOG_EXPLAIN:
            print(
                f"Sending configurations to {num_samples} clients and allocating secure IDs..."
            )
        msgs = driver.send_and_receive(
            [make(node_id) for node_id in state.active_node_ids], timeout=self.timeout
        )
        state.active_node_ids = {
            msg.metadata.src_node_id for msg in msgs if not msg.has_error()
        }

        if LOG_EXPLAIN:
            print(f"Received public keys from {len(state.active_node_ids)} clients.")

        for msg in msgs:
            if msg.has_error():
                continue
            key_dict = msg.content.configs_records[RECORD_KEY_CONFIGS]
            node_id = msg.metadata.src_node_id
            pk1, pk2 = key_dict[Key.PUBLIC_KEY_1], key_dict[Key.PUBLIC_KEY_2]
            state.nid_to_publickeys[node_id] = (pk1, pk2)

        return self._check_threshold(state)

    def _share_keys(
        self, driver: Driver, context: LegacyContext, state: WorkflowState
    ) -> bool:
        if LOG_EXPLAIN:
            print("\nForwarding public keys...")
        cfg = context.state.configs_records[MAIN_CONFIGS_RECORD]

        def make(nid: int) -> Message:
            neighbours = state.nid_to_neighbours[nid]
            cfgs_record = ConfigsRecord(
                {str(nid): state.nid_to_publickeys[nid] for nid in neighbours}
            )
            cfgs_record[Key.STAGE] = Stage.SHARE_KEYS
            content = RecordSet(configs_records={RECORD_KEY_CONFIGS: cfgs_record})
            return driver.create_message(
                content=content,
                message_type=MessageType.TRAIN,
                dst_node_id=nid,
                group_id=str(cfg[DefaultKey.CURRENT_ROUND]),
                ttl="",
            )

        # Broadcast public keys to clients and receive secret key shares
        msgs = driver.send_and_receive(
            [make(node_id) for node_id in state.active_node_ids], timeout=self.timeout
        )
        state.active_node_ids = {
            msg.metadata.src_node_id for msg in msgs if not msg.has_error()
        }

        if LOG_EXPLAIN:
            print(
                f"Received encrypted key shares from {len(state.active_node_ids)} clients."
            )

        # Build forward packet list dictionary
        srcs, dsts, ciphertexts = [], [], []
        fwd_ciphertexts: dict[int, list[bytes]] = {
            nid: [] for nid in state.active_node_ids
        }  # dest node ID -> list of ciphertexts
        fwd_srcs: dict[int, list[bytes]] = {
            nid: [] for nid in fwd_ciphertexts
        }  # dest node ID -> list of src secure IDs
        for msg in msgs:
            node_id = msg.metadata.src_node_id
            res_dict = msg.content.configs_records[RECORD_KEY_CONFIGS]
            srcs += [node_id] * len(res_dict[Key.DESTINATION_LIST])
            dsts += res_dict[Key.DESTINATION_LIST]
            ciphertexts += res_dict[Key.CIPHERTEXT_LIST]

        for src, dst, ciphertext in zip(srcs, dsts, ciphertexts):
            if dst in fwd_ciphertexts:
                fwd_ciphertexts[dst].append(ciphertext)
                fwd_srcs[dst].append(src)

        state.forward_srcs = fwd_srcs
        state.forward_ciphertexts = fwd_ciphertexts

        return self._check_threshold(state)

    def _collect_masked_input(
        self, driver: Driver, context: LegacyContext, state: WorkflowState
    ) -> bool:
        if LOG_EXPLAIN:
            print("\nForwarding encrypted key shares and requesting masked input...")
        cfg = context.state.configs_records[MAIN_CONFIGS_RECORD]

        # Send secret key shares to clients (plus FitIns) and collect masked input
        def make(nid: int) -> Message:
            cfgs_dict = {
                Key.STAGE: Stage.COLLECT_MASKED_INPUT,
                Key.CIPHERTEXT_LIST: state.forward_ciphertexts[nid],
                Key.SOURCE_LIST: state.forward_srcs[nid],
            }
            cfgs_record = ConfigsRecord(cfgs_dict)
            content = state.nid_to_fitins[nid]
            content.configs_records[RECORD_KEY_CONFIGS] = cfgs_record
            return driver.create_message(
                content=content,
                message_type=MessageType.TRAIN,
                dst_node_id=nid,
                group_id=str(cfg[DefaultKey.CURRENT_ROUND]),
                ttl="",
            )

        msgs = driver.send_and_receive(
            [make(node_id) for node_id in state.active_node_ids], timeout=self.timeout
        )
        state.active_node_ids = {
            msg.metadata.src_node_id for msg in msgs if not msg.has_error()
        }

        # Clear cache
        del state.forward_ciphertexts, state.forward_srcs, state.nid_to_fitins

        # Add all collected masked vectors and compuute available and dropout clients set
        if LOG_EXPLAIN:
            dead_nids = state.sampled_node_ids - state.active_node_ids
            for nid in dead_nids:
                print(f"Client {nid} dropped out.")
        masked_vector = None
        for msg in msgs:
            res_dict = msg.content.configs_records[RECORD_KEY_CONFIGS]
            client_masked_vec = [
                bytes_to_ndarray(b) for b in res_dict[Key.MASKED_PARAMETERS]
            ]
            if LOG_EXPLAIN:
                print(f"Received {client_masked_vec[1]} from Client {nid}.")
            if masked_vector is None:
                masked_vector = client_masked_vec
            else:
                masked_vector = parameters_addition(masked_vector, client_masked_vec)
        masked_vector = parameters_mod(masked_vector, state.mod_range)
        state.aggregate_ndarrays = masked_vector

        return self._check_threshold(state)

    def _unmask(
        self, driver: Driver, context: LegacyContext, state: WorkflowState
    ) -> bool:
        if LOG_EXPLAIN:
            print("\nRequesting key shares to unmask the aggregate vector...")
        cfg = context.state.configs_records[MAIN_CONFIGS_RECORD]

        # Construct active node IDs and dead node IDs
        active_nids = state.active_node_ids
        dead_nids = state.sampled_node_ids - active_nids

        # Send secure IDs of active and dead clients and collect key shares from clients
        def make(nid: int) -> Message:
            neighbours = state.nid_to_neighbours[nid]
            cfgs_dict = {
                Key.STAGE: Stage.UNMASK,
                Key.ACTIVE_NODE_ID_LIST: list(neighbours & active_nids),
                Key.DEAD_NODE_ID_LIST: list(neighbours & dead_nids),
            }
            cfgs_record = ConfigsRecord(cfgs_dict)
            content = RecordSet(configs_records={RECORD_KEY_CONFIGS: cfgs_record})
            return driver.create_message(
                content=content,
                message_type=MessageType.TRAIN,
                dst_node_id=nid,
                group_id=str(cfg[DefaultKey.CURRENT_ROUND]),
                ttl="",
            )

        msgs = driver.send_and_receive(
            [make(node_id) for node_id in state.active_node_ids], timeout=self.timeout
        )
        state.active_node_ids = {
            msg.metadata.src_node_id for msg in msgs if not msg.has_error()
        }
        if LOG_EXPLAIN:
            print(f"Received key shares from {len(state.active_node_ids)} clients.")

        # Build collected shares dict
        collected_shares_dict: dict[int, list[bytes]] = {}
        for nid in state.sampled_node_ids:
            collected_shares_dict[nid] = []
        for msg in msgs:
            res_dict = msg.content.configs_records[RECORD_KEY_CONFIGS]
            for owner_nid, share in zip(
                res_dict[Key.NODE_ID_LIST], res_dict[Key.SHARE_LIST]
            ):
                collected_shares_dict[owner_nid].append(share)

        # Remove mask for every client who is available after collect_masked_input stage
        masked_vector = state.aggregate_ndarrays
        del state.aggregate_ndarrays
        for nid, share_list in collected_shares_dict.items():
            if len(share_list) < state.threshold:
                log(
                    ERROR, "Not enough shares to recover secret in unmask vectors stage"
                )
                return False
            secret = combine_shares(share_list)
            if nid in active_nids:
                # The seed for PRG is the private mask seed of an active client.
                private_mask = pseudo_rand_gen(
                    secret, state.mod_range, get_parameters_shape(masked_vector)
                )
                masked_vector = parameters_subtraction(masked_vector, private_mask)
            else:
                # The seed for PRG is the secret key 1 of a dropped client.
                neighbours = state.nid_to_neighbours[nid]
                neighbours.remove(nid)

                for neighbor_nid in neighbours:
                    shared_key = generate_shared_key(
                        bytes_to_private_key(secret),
                        bytes_to_public_key(state.nid_to_publickeys[neighbor_nid][0]),
                    )
                    pairwise_mask = pseudo_rand_gen(
                        shared_key, state.mod_range, get_parameters_shape(masked_vector)
                    )
                    if nid > neighbor_nid:
                        masked_vector = parameters_addition(
                            masked_vector, pairwise_mask
                        )
                    else:
                        masked_vector = parameters_subtraction(
                            masked_vector, pairwise_mask
                        )
        recon_parameters = parameters_mod(masked_vector, state.mod_range)
        if LOG_EXPLAIN:
            print(f"Unmasked sum of vectors (quantized): {recon_parameters[0]}")
        # recon_parameters = parameters_divide(recon_parameters, total_weights_factor)
        aggregated_vector = dequantize(
            recon_parameters,
            state.clipping_range,
            state.quantization_range,
        )
        offset = -(len(active_nids) - 1) * state.clipping_range
        for vec in aggregated_vector:
            vec += offset
        if LOG_EXPLAIN:
            print(f"Unmasked sum of vectors (dequantized): {aggregated_vector[0]}")
            print(f"Aggregate vector: {aggregated_vector[0] / len(active_nids)}")
            print(
                "########################### Secure Aggregation End ###########################\n\n"
            )

        return True
