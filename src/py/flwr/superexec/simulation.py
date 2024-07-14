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
"""Simulation engine executor."""


import subprocess
import sys
from logging import ERROR, INFO
from pathlib import Path
from typing import Dict, Optional

from typing_extensions import override

from flwr.cli.config_utils import get_fab_metadata
from flwr.cli.install import install_from_fab
from flwr.common.constant import RUN_ID_NUM_BYTES
from flwr.common.logger import log
from flwr.server.superlink.state.utils import generate_rand_int_from_bytes

from .executor import Executor, RunTracker


class SimulationEngine(Executor):
    """Simulation engine executor.

    Parameters
    ----------
    num_supernodes: Opitonal[str] (default: None)
        Total number of nodes to involve in the simulation.
    """

    def __init__(
        self,
        num_supernodes: Optional[str] = None,
    ) -> None:
        self.num_supernodes = num_supernodes

    @override
    def set_config(
        self,
        config: Dict[str, str],
    ) -> None:
        """Set executor config arguments.

        Parameters
        ----------
        config : Dict[str, str]
            A dictionary for configuration values.
            Supported configuration key/value pairs:
            - "num-supernodes": str
                Number of nodes to register for the Simulation.
        """
        if not config:
            return
        if num_supernodes := config.get("num-supernodes"):
            self.num_supernodes = num_supernodes

    @override
    def start_run(
        self, fab_file: bytes, override_config: Dict[str, str]
    ) -> Optional[RunTracker]:
        """Start run using the Flower Simulation Engine."""
        try:
            if self.num_supernodes is None:
                log(
                    ERROR,
                    "To start a run with the simulation plugin, please specify "
                    "the number of supernodes. You can do this by using the "
                    "`--executor-config` argument when launching the SuperExec.",
                )
                raise ValueError("Need to set `num-supernodes`.")

            if override_config:
                raise ValueError(
                    "Overriding the run config is not yet supported with the "
                    "simulation plugin.",
                )

            # Install FAB to flwr dir
            _, fab_id = get_fab_metadata(fab_file)
            fab_path = install_from_fab(fab_file, None, True)

            # Install FAB Python package
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", str(fab_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # In Simulation there is no SuperLink, still we create a run_id
            run_id = generate_rand_int_from_bytes(RUN_ID_NUM_BYTES)
            log(INFO, "Created run %s", str(run_id))

            fab_name = Path(fab_id).name

            # Start Simulation
            proc = subprocess.Popen(  # pylint: disable=consider-using-with
                [
                    "flower-simulation",
                    "--client-app",
                    f"{fab_name}.client:app",
                    "--server-app",
                    f"{fab_name}.server:app",
                    "--num-supernodes",
                    f"{self.num_supernodes}",
                    "--run-id",
                    str(run_id),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            log(INFO, "Started run %s", str(run_id))

            return RunTracker(
                run_id=run_id,
                proc=proc,
            )

        # pylint: disable-next=broad-except
        except Exception as e:
            log(ERROR, "Could not start run: %s", str(e))
            return None


executor = SimulationEngine()
