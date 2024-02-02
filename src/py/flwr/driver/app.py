# Copyright 2022 Flower Labs GmbH. All Rights Reserved.
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
"""Flower driver app."""


import sys
import threading
import time
import timeit
from dataclasses import dataclass
from logging import INFO
from pathlib import Path
from typing import Dict, List, Optional, Union, Union, cast

from flwr.common import EventType, event
from flwr.common.address import parse_address
from flwr.common.logger import log
from flwr.common.typing import Parameters
from flwr.proto.driver_pb2 import (
    CreateRunRequest,
    GetNodesRequest,
    PullTaskResRequest,
    PushTaskInsRequest,
)
from flwr.proto.node_pb2 import Node
from flwr.proto.task_pb2 import Task, TaskIns, TaskRes
from flwr.server import ServerConfig
from flwr.server.client_manager import ClientManager, SimpleClientManager
from flwr.server.history import History
from flwr.server.strategy import FedAvg, Strategy

from .driver_client_proxy import DriverClientProxy
from .workflow.workflow_factory import (
    FlowerWorkflowFactory,
    FLWorkflowFactory,
    WorkflowState,
)

DEFAULT_SERVER_ADDRESS_DRIVER = "[::]:9091"

ERROR_MESSAGE_DRIVER_NOT_CONNECTED = """
[Driver] Error: Not connected.

Call `connect()` on the `Driver` instance before calling any of the other `Driver`
methods.
"""


@dataclass
class DriverConfig:
    """Flower driver config.

    All attributes have default values which allows users to configure just the ones
    they care about.
    """

    num_rounds: int = 1
    round_timeout: Optional[float] = None


def start_driver(  # pylint: disable=too-many-arguments, too-many-locals
    *,
    server_address: str = DEFAULT_SERVER_ADDRESS_DRIVER,
    config: Optional[Union[DriverConfig, ServerConfig]] = None,
    strategy: Optional[Strategy] = None,
    client_manager: Optional[ClientManager] = None,
    root_certificates: Optional[Union[bytes, str]] = None,
    fl_workflow_factory: Optional[FlowerWorkflowFactory] = None,
) -> History:
    """Start a Flower Driver API server.

    Parameters
    ----------
    server_address : Optional[str]
        The IPv4 or IPv6 address of the Driver API server.
        Defaults to `"[::]:8080"`.
    server : Optional[flwr.server.Server] (default: None)
        A server implementation, either `flwr.server.Server` or a subclass
        thereof. If no instance is provided, then `start_driver` will create
        one.
    config : Optional[DriverConfig] (default: None)
        Currently supported values are `num_rounds` (int, default: 1) and
        `round_timeout` in seconds (float, default: None).
    strategy : Optional[flwr.server.Strategy] (default: None).
        An implementation of the abstract base class
        `flwr.server.strategy.Strategy`. If no strategy is provided, then
        `start_server` will use `flwr.server.strategy.FedAvg`.
    client_manager : Optional[flwr.server.DriverClientManager] (default: None)
        An implementation of the class `flwr.server.ClientManager`. If no
        implementation is provided, then `start_driver` will use
        `flwr.server.SimpleClientManager`.
    root_certificates : Optional[Union[bytes, str]] (default: None)
        The PEM-encoded root certificates as a byte string or a path string.
        If provided, a secure connection using the certificates will be
        established to an SSL-enabled Flower server.

    Returns
    -------
    hist : flwr.server.history.History
        Object containing training and evaluation metrics.

    Examples
    --------
    Starting a driver that connects to an insecure server:

    >>> start_driver()

    Starting a driver that connects to an SSL-enabled server:

    >>> start_driver(
    >>>     root_certificates=Path("/crts/root.pem").read_bytes()
    >>> )
    """
    event(EventType.START_DRIVER_ENTER)

    # Backward compatibility
    if isinstance(config, ServerConfig):
        config = DriverConfig(
            num_rounds=config.num_rounds, round_timeout=config.round_timeout
        )

    # Parse IP address
    parsed_address = parse_address(server_address)
    if not parsed_address:
        sys.exit(f"Server IP address ({server_address}) cannot be parsed.")
    host, port, is_v6 = parsed_address
    address = f"[{host}]:{port}" if is_v6 else f"{host}:{port}"

    # Create the Driver
    if isinstance(root_certificates, str):
        root_certificates = Path(root_certificates).read_bytes()
    driver = GrpcDriver(
        driver_service_address=address, root_certificates=root_certificates
    )
    driver.connect()
    lock = threading.Lock()

    # Request workload_id
    workload_id = driver.create_workload(CreateWorkloadRequest()).workload_id

    # Initialization
    hist = History()
    if client_manager is None:
        client_manager = SimpleClientManager()
    if strategy is None:
        strategy = FedAvg()
    if config is None:
        config = DriverConfig()
    if fl_workflow_factory is None:
        fl_workflow_factory = cast(FlowerWorkflowFactory, FLWorkflowFactory())
    workflow_state = WorkflowState(
        num_rounds=config.num_rounds,
        current_round=0,  # This field will be set inside the workflow
        strategy=strategy,
        parameters=Parameters(
            tensors=[], tensor_type=""
        ),  # This field will be set inside the workflow,
        client_manager=client_manager,
        history=hist,
    )
    log(
        INFO,
        "Starting Flower driver, config: %s",
        config,
    )

    # Start the thread updating nodes
    thread = threading.Thread(
        target=update_client_manager,
        args=(
            driver,
            workload_id,
            client_manager,
            lock,
        ),
    )
    thread.start()

    # Start training
    fl_workflow = fl_workflow_factory(workflow_state)

    instructions = next(fl_workflow)
    while True:
        node_responses = fetch_responses(
            driver, workload_id, instructions, config.round_timeout
        )
        try:
            instructions = fl_workflow.send(node_responses)
        except StopIteration:
            break

    fl_workflow.close()

    # Stop the Driver API server and the thread
    with lock:
        driver.disconnect()
    thread.join()

    # Log history
    log(INFO, "app_fit: losses_distributed %s", str(hist.losses_distributed))
    log(INFO, "app_fit: metrics_distributed_fit %s", str(hist.metrics_distributed_fit))
    log(INFO, "app_fit: metrics_distributed %s", str(hist.metrics_distributed))
    log(INFO, "app_fit: losses_centralized %s", str(hist.losses_centralized))
    log(INFO, "app_fit: metrics_centralized %s", str(hist.metrics_centralized))

    event(EventType.START_SERVER_LEAVE)

    return hist


def update_client_manager(
    driver: Driver,
    workload_id: int,
    client_manager: ClientManager,
    lock: threading.Lock,
) -> None:
    """Update the nodes list in the client manager.

    This function periodically communicates with the associated driver to get all
    node_ids. Each node_id is then converted into a `DriverClientProxy` instance
    and stored in the `registered_nodes` dictionary with node_id as key.

    New nodes will be added to the ClientManager via `client_manager.register()`,
    and dead nodes will be removed from the ClientManager via
    `client_manager.unregister()`.
    """
    # Loop until the driver is disconnected
    registered_nodes: Dict[int, DriverClientProxy] = {}
    while True:
        with lock:
            # End the while loop if the driver is disconnected
            if driver.stub is None:
                break
            get_nodes_res = driver.get_nodes(
                req=GetNodesRequest(workload_id=workload_id)
            )
        all_node_ids = {node.node_id for node in get_nodes_res.nodes}
        dead_nodes = set(registered_nodes).difference(all_node_ids)
        new_nodes = all_node_ids.difference(registered_nodes)

        # Unregister dead nodes
        for node_id in dead_nodes:
            client_proxy = registered_nodes[node_id]
            client_manager.unregister(client_proxy)
            del registered_nodes[node_id]

        # Register new nodes
        for node_id in new_nodes:
            client_proxy = DriverClientProxy(
                node_id=node_id,
                driver=driver,
                anonymous=False,
                run_id=run_id,
            )
            if client_manager.register(client_proxy):
                registered_nodes[node_id] = client_proxy
            else:
                raise RuntimeError("Could not register node.")

        # Sleep for 3 seconds
        time.sleep(3)


# pylint: disable-next=too-many-locals
def fetch_responses(
    driver: Driver,
    workload_id: int,
    instructions: Dict[int, Task],
    timeout: Optional[float],
) -> Dict[int, Task]:
    """Send instructions to clients and return their responses."""
    # Build the list of TaskIns
    task_ins_list: List[TaskIns] = []
    driver_node = Node(node_id=0, anonymous=True)
    for node_id, task in instructions.items():
        # Set the `consumer` and `producer` fields in Task
        #
        # Note that protobuf API `protobuf.message.MergeFrom(other_msg)`
        # does NOT always overwrite fields that are set in `other_msg`.
        # Please refer to:
        # https://googleapis.dev/python/protobuf/latest/google/protobuf/message.html
        consumer = Node(node_id=node_id, anonymous=False)
        task.MergeFrom(Task(producer=driver_node, consumer=consumer))
        # Create TaskIns and add it to the list
        task_ins = TaskIns(
            task_id="",  # Do not set, will be created and set by the DriverAPI
            group_id="",
            workload_id=workload_id,
            task=task,
        )
        task_ins_list.append(task_ins)

    # Push TaskIns
    push_res = driver.push_task_ins(PushTaskInsRequest(task_ins_list=task_ins_list))
    task_ids = [task_id for task_id in push_res.task_ids if task_id != ""]

    time.sleep(1.0)

    # Pull TaskRes
    task_res_list: List[TaskRes] = []
    if timeout:
        start_time = timeit.default_timer()
    while timeout is None or timeit.default_timer() - start_time < timeout:
        pull_res = driver.pull_task_res(
            PullTaskResRequest(node=driver_node, task_ids=task_ids)
        )
        task_res_list.extend(pull_res.task_res_list)
        if len(task_res_list) == len(task_ids):
            break

        time.sleep(3.0)

    # Build and return response dictionary
    node_responses: Dict[int, Task] = {
        task_res.task.producer.node_id: task_res.task for task_res in task_res_list
    }
    return node_responses
