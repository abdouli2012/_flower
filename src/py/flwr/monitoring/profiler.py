import logging
import os
import platform
import socket
import time
from dataclasses import dataclass, field
from functools import wraps
from threading import Thread
from typing import Callable, Dict, List, Tuple, TypeVar, Union, cast

import numpy as np
import nvsmi
import psutil
from importlib_metadata import SelectableGroups

from flwr.common import NDArrays, Scalar

logger = logging.getLogger(__name__)

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
class SimpleGPUProcess:
    uuid: str
    mem_proc_used: Dict[int, List[FloatSample]] = field(default_factory=dict)
    mem_total: float = 0.0
    mem_total_used: List[FloatSample] = field(default_factory=list)
    utilization: List[FloatSample] = field(default_factory=list)


class SystemMonitor(Thread):
    """Class for system usage utilization monitoring.

    It keeps track of CPU and GPU utilization, and both RAM and VRAM
    usage (each gpu separately) by pinging for information every
    `interval` seconds in a separate thread.
    """

    def __init__(self, pids: List[int], interval: float = 0.7):
        super(SystemMonitor, self).__init__()
        self.fqdn = socket.getfqdn().replace(".", "|")
        self.pids: List[int] = pids
        self.gpus: Dict[str, SimpleGPUProcess] = dict()
        self.cpu_name: str = platform.processor()
        self.cpu_samples: Dict[int, List[FloatSample]] = dict()
        self.start_time_ns: int = 0
        self.stop_time_ns: int = 0
        self.stopped: bool = False
        self.interval = interval

    def run(self):
        self.start_time_ns = time.time_ns()
        while not self.stopped:
            self._read_utilization()
            time.sleep(self.interval)

    def stop(self):
        self.stop_time_ns = time.time_ns()
        self.stopped = True

    def _get_gpu_stats(self):
        if nvsmi is not None:
            # Retrieve GPU process specific info
            pros = nvsmi.get_gpu_processes()
            timestamp = time.time_ns()
            for pro in pros:
                if pro.pid in self.pids:
                    uuid = pro.gpu_uuid
                    if uuid not in self.gpus:
                        self.gpus[uuid] = SimpleGPUProcess(uuid)
                    if pro.pid not in self.gpus[uuid].mem_proc_used:
                        self.gpus[uuid].mem_proc_used[pro.pid] = []
                    self.gpus[uuid].mem_proc_used[pro.pid].append(
                        (timestamp, pro.used_memory)
                    )

            # Retrieve GPU general info
            gpus_all = nvsmi.get_gpus()
            timestamp = time.time_ns()
            for gpu in gpus_all:
                if gpu.uuid in self.gpus.keys():
                    uuid = gpu.uuid
                    self.gpus[uuid].mem_total = gpu.mem_total
                    self.gpus[uuid].mem_total_used.append((timestamp, gpu.mem_used))
                    self.gpus[uuid].utilization.append((timestamp, gpu.gpu_util))

    def _get_cpu_stats(self):
        if psutil is not None:
            timestamp = time.time_ns()
            for pid in self.pids:
                cpu_percent = psutil.Process(pid).cpu_percent(interval=self.interval)
                if pid not in self.cpu_samples:
                    self.cpu_samples[pid] = []
                self.cpu_samples[pid].append((timestamp, cpu_percent))

    def _read_utilization(self):
        self._get_cpu_stats()
        self._get_gpu_stats()

    @staticmethod
    def _get_basic_stats_from_list(prefix: str, values: List[float]):
        stats = dict()
        stats[f"{prefix}.mean"] = np.mean(values)
        stats[f"{prefix}.median"] = np.median(values)
        stats[f"{prefix}.min"] = np.min(values)
        stats[f"{prefix}.max"] = np.max(values)
        return stats

    def aggregate_statistics(self) -> Dict[str, Scalar]:
        stats: Dict[str, Scalar] = {}
        basename = f"_flwr.sys_monitor.{self.fqdn}"
        stats[f"{basename}.duration_ns"] = self.stop_time_ns - self.start_time_ns
        # GPUs
        for gpu_uuid, gpu in self.gpus.items():
            for att_name in gpu.__dict__.keys():
                base_gpu_att = f"{basename}.gpu_info.{gpu_uuid}.{att_name}"
                att = getattr(gpu, att_name)
                if isinstance(att, list) and all(isinstance(v, float) for _, v in att):
                    values = [v for _, v in att]
                    stats = {
                        **stats,
                        **self._get_basic_stats_from_list(base_gpu_att, values),
                    }
                if isinstance(att, dict):
                    for pid, l in att.items():
                        base_gpu_att_pid = (
                            f"{basename}.gpu_info.{gpu_uuid}.{att_name}.{pid}"
                        )
                        values = [v for _, v in l]
                        stats = {
                            **stats,
                            **self._get_basic_stats_from_list(base_gpu_att_pid, values),
                        }

                elif isinstance(att, float):
                    stats[f"{basename}.{att_name}."] = att
        # CPU
        for pid, samples in self.cpu_samples.items():
            base_cpu_util = f"{basename}.cpu_info.{self.cpu_name}.utilization.{pid}"
            values = [v for _, v in samples]
            stats = {**stats, **self._get_basic_stats_from_list(base_cpu_util, values)}

        return stats


def basic_profiler(interval: float = 0.1):
    def basic_profiler(_func: ProfFunDec) -> ProfFunDec:
        @wraps(_func)
        def wrapper(*args, **kwargs):
            list_pids = [os.getpid()]
            system_monitor = SystemMonitor(pids=list_pids, interval=interval)
            system_monitor.start()
            output, num_examples, metrics = _func(*args, **kwargs)
            system_monitor.stop()
            stats_dict = system_monitor.aggregate_statistics()
            metrics = {**metrics, **stats_dict}
            return output, num_examples, metrics

        return cast(ProfFunDec, wrapper)

    return basic_profiler
