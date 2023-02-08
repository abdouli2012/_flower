import datetime
import os
import pickle
import platform
import time
import socket
from copy import deepcopy
from dataclasses import dataclass, field
from functools import wraps
from multiprocessing.connection import Client, Listener
from pathlib import Path, PurePath
from subprocess import check_output
from threading import Lock, Thread
from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union, cast
from uuid import uuid4
import numpy as np
import nvsmi
import psutil
from psutil import cpu_count

from flwr.common import NDArrays, Scalar

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"

FloatSample = Tuple[int, float]

ProfFunDec = TypeVar(
    "ProfFunDec",
    bound=Callable[
        [NDArrays, Dict[str, Scalar]],  # parameters, config
        Union[
            Tuple[NDArrays, int, Dict[str, Scalar]],  # parameters, num_samples, metrics
            Tuple[float, int, Dict[str, Scalar]],  # loss, num_samples, metrics
        ],
    ],
)


@dataclass
class SimpleCPU:
    name: str = "cpu"
    total_mem_mb: float = 0.0
    all_proc_mem_used_mb: List[FloatSample] = field(default_factory=list)
    num_cores: int = 1


@dataclass
class SimpleCPUProcess:
    this_proc_mem_used_mb: List[FloatSample] = field(default_factory=list)
    utilization: List[FloatSample] = field(default_factory=list)


@dataclass
class SimpleGPU:
    uuid: str
    gpu_id: int
    name: str
    total_mem_mb: float = 0.0
    utilization: List[FloatSample] = field(default_factory=list)
    all_proc_mem_used_mb: List[FloatSample] = field(default_factory=list)


@dataclass
class SimpleGPUProcess:
    this_proc_mem_used_mb: List[FloatSample] = field(default_factory=list)


@dataclass
class Node:
    id: str
    list_gpus: Dict[str, SimpleGPU] = field(default_factory=dict)


@dataclass(eq=True, frozen=False)
class Transaction: # Set by the Server / Strategy
    id: str
    pid: int
    start_time_ns: int = 0
    stop_time_ns: int = 0
    cpu_process: SimpleCPUProcess = SimpleCPUProcess()
    gpu_processes: Dict[str, SimpleGPUProcess] = field(default_factory=dict)


class SystemMonitor(Thread):
    """Class used for monitoring system usage utilization.

    It keeps track of CPU and GPU utilization, and both RAM and VRAM
    usage (each gpu separately) by pinging for information every
    `interval_s` seconds in a separate thread.
    """

    def __init__(
        self,
        *,
        address: Tuple[str, int],
        sampling_interval_s: float = 1.0,
        path_save_stats: Optional[Path] = None,
    ):
        super(SystemMonitor, self).__init__()
        self.node_id = socket.getfqdn()
        self.tasks: Dict[str, Task] = dict()
        self.node_cpu: SimpleCPU = SimpleCPU()
        self.node_gpus: Dict[str, SimpleGPU] = dict()
        self.start_time_ns: int = 0
        self.stop_time_ns: int = 0
        self.stopped: bool = True
        self.sampling_interval: float = sampling_interval_s
        self.address: Tuple[str, int] = address
        self._lock: Lock = Lock()
        self.path_save_stats = path_save_stats
        self.active_task_ids: List["str"] = []

    def get_resources(self) -> Dict[str, Union[SimpleCPU, SimpleGPU]]:
        return {**self.node_gpus, "cpu": self.node_cpu}

    def get_tasks(self) -> Dict[str, Task]:
        return self.tasks

    def get_active_tasks(self) -> Dict[str, Task]:
        return {k: v for k, v in self.tasks.items() if k in self.active_task_ids}

    def get_active_tasks_ids(self) -> List[str]:
        t = []
        with self._lock:
            t = deepcopy(self.active_task_ids)
        return t

    def is_running(self) -> bool:
        return not self.stopped

    def _register_tasks(self, tasks: List[Tuple[str, str, int]]) -> bool:
        """Include list of tasks in set of tasks that are being monitored.

        Args:
            tasks (List[Tuple[str, int, str, List[int]]]): List of (task_id,pid,task_name, gpu_ids)s to be included
        """
        with self._lock:
            for task in tasks:
                task_id, cid, pid = task
                self.tasks[task_id] = Task(
                    id=task_id,
                    pid=pid,
                    cid=cid,
                    start_time_ns=time.time_ns(),
                )
                self.active_task_ids.append(task_id)
        return True

    def _unregister_tasks(
        self, tags: List[(str, str, int)]
    ) -> bool:  # Is there a risk of having two the same task_id being sent to the same client. DO we need the concept of transaction?
        with self._lock:
            for tag in tags:
                task_id, cid, pid = args
                if task_id in self.active_task_ids:
                    self.active_task_ids.remove(task_id)
                    self.tasks[task_id].stop_time_ns = time.time_ns()

        return True

    def _save_tasks_and_resources(self, sub_folder: PurePath) -> bool:
        save_successful = False
        if self.path_save_stats is not None:
            save_path = self.path_save_stats / sub_folder / self.node_id
            resources_folder = save_path / "resources"
            resources_folder.mkdir(parents=True, exist_ok=True)
            task_folder = save_path / "tasks"
            task_folder.mkdir(parents=True, exist_ok=True)

            # Save Tasks
            for task_id, task in self.tasks.items():
                filename = task_folder / f"{task_id}.pickle"
                with open(filename, "wb") as handle:
                    pickle.dump(task, handle)

            # Save Resources
            for hw in ["cpu", "gpus"]:
                filename = resources_folder / f"{hw}.pickle"
                with open(filename, "wb") as handle:
                    pickle.dump(getattr(self, hw), handle)

            save_successful = True

        return save_successful

    def _clear_tasks_and_resources(self):
        # Clear CPU and GPU
        del self.cpu.all_proc_mem_used_mb[:]
        for k in self.node_gpus.keys():
            del self.node_gpus[k].all_proc_mem_used_mb[:]
            del self.node_gpus[k].utilization[:]

        # Release memory from Tasks
        self.tasks.clear()

    def _collect_resources(self) -> bool:
        # Retrieve GPU info
        all_gpus = nvsmi.get_gpus()
        for gpu in all_gpus:
            self.node_gpus[gpu.uuid] = SimpleGPU(
                uuid=gpu.uuid, gpu_id=gpu.id, name=gpu.name
            )
            self.node_gpus[gpu.uuid].total_mem_mb = gpu.mem_total

        # Retrieve CPU and system RAM info
        cpu_name = platform.processor()
        self.cpu = SimpleCPU(
            name=cpu_name,
            total_mem_mb=psutil.virtual_memory().total,
            num_cores=cpu_count(logical=False),
        )
        return True

    def _safe_copy_task_ids_and_pids(self) -> List[Tuple[str, int]]:
        """Returns temporary copy of tasks to be monitored.

        Returns:
            List[Task]: List of tasks to be tracked
        """
        with self._lock:
            return [(task.id, task.pid) for task in self.tasks.values()]

    def _switch(self):
        with Listener(address=self.address) as listener:
            with listener.accept() as conn:
                while True:
                    try:
                        command, args = conn.recv()
                        if (
                            command == "register_task"
                        ):  # TaskID set by the "server"/strategy, who should also know the type.
                            task_id, cid, pid = args
                            with self._lock:
                                self._register_tasks([(task_id, cid, pid)])
                        elif command == "unregister_task":
                            task_id, cid, pid = args
                            with self._lock:
                                self._unregister_tasks([(task_id, cid, pid)])
                    except EOFError:
                        print("Connection closed.")
                    break

    def run(self) -> None:
        """Runs thread and sleeps for self.interval_s seconds."""
        self.start_time_ns = time.time_ns()
        self.stopped = False
        while not self.stopped:
            current_active_tasks = self.get_active_tasks_ids()
            if current_active_tasks:
                self._collect_system_usage(current_active_tasks)
            time.sleep(self.sampling_interval)  # Sleep is managed by collect_cpu
        self.stop_time_ns = time.time_ns()

    def stop(self) -> None:
        """Stops thread."""
        self.stopped = True
        self.stop_time_ns = time.time_ns()

    def _collect_gpu_usage(self, active_task_ids: List[str]) -> None:
        # Need to get PID of a task, same order guaranteed in Python 3.7
        # task_id_pid_map = {task.pid: task.id for task in self.tasks.values()}
        pid_task_id_map = {}
        try:
            pid_task_id_map = {
                self.tasks[task_id].pid: task_id for task_id in active_task_ids
            }
        except:
            pass
        # self.tasks[task_id].pid: task_id for task_id in active_task_ids

        # Retrieve single process GPU memory usage
        timestamp = time.time_ns()

        pros = nvsmi.get_gpu_processes()
        try:
            for pro in pros:
                if pro.pid in pid_task_id_map.keys():
                    uuid = pro.gpu_uuid
                    task_id = pid_task_id_map[pro.pid]
                    if uuid not in self.tasks[task_id].gpu_processes.keys():
                        self.tasks[task_id].gpu_processes[uuid] = SimpleGPUProcess()

                    self.tasks[task_id].gpu_processes[
                        uuid
                    ].this_proc_mem_used_mb.append((timestamp, pro.used_memory))
        except:
            pass

        # Retrieve GPU total memory utilization
        gpus_all = nvsmi.get_gpus()
        timestamp = time.time_ns()
        for gpu in gpus_all:
            uuid: str = gpu.uuid
            if uuid in self.node_gpus.keys():
                self.node_gpus[uuid].all_proc_mem_used_mb.append(
                    (timestamp, gpu.mem_used)
                )
                self.node_gpus[uuid].utilization.append((timestamp, gpu.gpu_util))

    def _collect_cpu_usage(self, active_task_ids: List[str]) -> None:
        timestamp = time.time_ns()
        if psutil is not None:
            # Total System Memory Utilization
            cpu_mem_used = psutil.virtual_memory().used
            self.cpu.all_proc_mem_used_mb.append((timestamp, cpu_mem_used))

        # Tracked Processed Memory and CPU

        pid_task_id_map = {}
        for id in active_task_ids:
            try:
                pid_task_id_map = {
                    self.tasks[task_id].pid: task_id for task_id in active_task_ids
                }
            except:
                pass

        try:
            pid_list = ",".join([str(x) for x in pid_task_id_map.keys()])

            output = check_output(
                ["ps", "-p", pid_list, "--no-headers", "-o", "pid,%mem,%cpu"]
            )
            for line in output.splitlines():
                pid, mem, cpu_percent = line.split()
                self.tasks[pid_task_id_map[int(pid)]].cpu_process.utilization.append(
                    (timestamp, float(cpu_percent))
                )
                self.tasks[
                    pid_task_id_map[int(pid)]
                ].cpu_process.this_proc_mem_used_mb.append((timestamp, float(mem)))
        except:
            pass

    def _collect_system_usage(self, current_active_tasks) -> None:
        with self._lock:
            self._collect_cpu_usage(current_active_tasks)
            self._collect_gpu_usage(current_active_tasks)

    def aggregate_statistics(self, task_ids: Optional[List[str]]) -> Dict[str, Scalar]:
        # System-wise
        metrics = {}
        stop_time_ns = self.stop_time_ns if self.stop_time_ns > 0 else time.time_ns()
        metrics["round_duration"] = stop_time_ns - self.start_time_ns

        # Max GPU memory across all clients for all GPUs
        max_this_proc_mem_used_mb: Dict[
            str, Dict[str, float]
        ] = {}  # task_id: {uuid:mem_mb}
        print(self.active_task_ids)
        selected_task_ids = task_ids if task_ids else self.active_task_ids
        for task_id in selected_task_ids:
            task = self.tasks[task_id]
            max_this_proc_mem_used_mb[task_id] = {}
            for uuid, gpu_process in task.gpu_processes.items():
                this_task_uuid_mem_usage_mb = [
                    x[1] for x in gpu_process.this_proc_mem_used_mb
                ]
                this_max: float = max(this_task_uuid_mem_usage_mb)
                max_this_proc_mem_used_mb[task_id][uuid] = this_max

        metrics["max_this_proc_mem_used_mb"] = max_this_proc_mem_used_mb

        # Max GPU Memory Used for all process
        max_all_proc_mem_used_mb: Dict[str, float] = {}
        for gpu_uuid, gpu in self.gpus.items():
            mem_values = [x[1] for x in gpu.all_proc_mem_used_mb]
            max_all_proc_mem_used_mb[gpu_uuid] = max(mem_values)
        metrics["max_all_proc_mem_used_mb"] = max_all_proc_mem_used_mb

        # Training Times per task
        training_times_ns: Dict[str, Tuple[int, int]] = {}  # task_id:
        for task_id in selected_task_ids:
            task = self.tasks[task_id]
            training_times_ns[task_id] = (task.start_time_ns, task.stop_time_ns)

        metrics["training_times_ns"] = training_times_ns

        # CPU
        """metrics["cpu_all_procs_mem_used_mb"] = max(
            [x[1] for x in self.cpu]
        )
        for resource in self.gpus.values():
            gpu_id = resource.gpu_id
            metrics[f"gpu{gpu_id}_max_utilization"] = max(
                [x[1] for x in resource.utilization]
            )
            metrics[f"gpu{gpu_id}_all_process_mem_used_mb"] = max(
                [x[1] for x in resource.all_procs_mem_used_mb]
            )
            metrics[f"gpu{gpu_id}_total_mem_mb"] = resource.total_mem_mb
            """

        return metrics


##### Client function wrapper #####
def send_message_to_system_monitor(
    task_id: str, msg: str, address: Tuple[str, int]
) -> None:
    try:
        with Client(address) as conn:
            conn.send((msg, task_id, os.getpid()))
    except Exception as e:
        print(f"Error trying to register with System Monitor. {e}")


def profile(port: int = 6000):
    def numpy_profiler(_func: ProfFunDec) -> ProfFunDec:
        @wraps(_func)
        def wrapper(
            *args, **kwargs
        ) -> Tuple[Union[NDArrays, float], int, Dict[str, Scalar]]:
            task_id = _func.__name__
            address = ("localhost", port)
            # Register
            send_message_to_system_monitor(
                task_id=task_id, msg="register", address=address
            )
            # Run methods
            output, num_examples, metrics = _func(*args, **kwargs)
            # De-register
            send_message_to_system_monitor(
                task_id=task_id, msg="deregister", address=address
            )
            return output, num_examples, metrics

        return cast(ProfFunDec, wrapper)

    return numpy_profiler


##### Strategy fit and aggregate wrappers
