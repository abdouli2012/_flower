# Copyright 2020 Adap GmbH. All Rights Reserved.
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
"""Provides a variaty of benchmark settings."""

from dataclasses import dataclass
from typing import List


@dataclass
class ServerSetting:
    """Settings for the server."""

    rounds: int
    min_num_clients: int
    sample_fraction: float
    min_sample_size: int
    training_round_timeout: int
    lr_initial: float
    dry_run: bool


@dataclass
class ClientSetting:
    """Settings for the client."""

    # Individual per client
    cid: str
    partition: int
    delay_factor: float

    # Same across all clients
    iid_fraction: float
    num_clients: int
    dry_run: bool


@dataclass
class Setting:
    """One specific training setting."""

    server: ServerSetting
    clients: List[ClientSetting]


def get_setting(name: str) -> Setting:
    """Return appropriate setting."""
    if name not in SETTINGS:
        raise Exception(
            "Setting does not exist. Valid settings are: %s" % list(SETTINGS.keys())
        )

    return SETTINGS[name]


SETTINGS = {
    "dry": Setting(
        server=ServerSetting(
            rounds=1,
            min_num_clients=1,
            sample_fraction=1.0,
            min_sample_size=1,
            training_round_timeout=600,
            lr_initial=0.1,
            dry_run=True,
        ),
        clients=configure_uniform_clients(
            iid_fraction=0.0, num_clients=4, dry_run=True
        ),
    ),
    "minimal": Setting(
        server=ServerSetting(
            rounds=2,
            min_num_clients=4,
            sample_fraction=1.0,
            min_sample_size=3,
            training_round_timeout=3600,
            lr_initial=0.1,
            dry_run=False,
        ),
        clients=configure_uniform_clients(
            iid_fraction=0.0, num_clients=4, dry_run=False
        ),
    ),
    "fedavg-sync": Setting(
        server=ServerSetting(
            rounds=10,
            min_num_clients=80,
            sample_fraction=1.0,
            min_sample_size=80,
            training_round_timeout=40,
            lr_initial=0.1,
            dry_run=False,
        ),
        clients=configure_clients(
            iid_fraction=0.0,
            num_clients=100,
            dry_run=False,
            delay_factor_fast=0.0,
            delay_factor_slow=3.0,
        ),
    ),
    "fedavg-async": Setting(
        server=ServerSetting(
            rounds=10,
            min_num_clients=80,
            sample_fraction=1.0,
            min_sample_size=80,
            training_round_timeout=20,
            lr_initial=0.1,
            dry_run=False,
        ),
        clients=configure_clients(
            iid_fraction=0.0,
            num_clients=100,
            dry_run=False,
            delay_factor_fast=0.0,
            delay_factor_slow=3.0,
        ),
    ),
}


def configure_uniform_clients(
    iid_fraction: float, num_clients: int, dry_run: bool,
):
    clients = []
    for i in range(num_clients):
        client = ClientSetting(
            # Individual
            cid=str(i),
            partition=i,
            delay_factor=0.0,
            # Shared
            iid_fraction=iid_fraction,
            num_clients=num_clients,
            dry_run=dry_run,
        )
        clients.append(client)

    return clients


def configure_clients(
    iid_fraction: float,
    num_clients: int,
    dry_run: bool,
    delay_factor_fast: float,
    delay_factor_slow: float,
):
    clients = []
    for i in range(num_clients):
        client = ClientSetting(
            # Individual
            cid=str(i),
            partition=i,
            # Indices 0 to 49 fast, 50 to 99 slow
            delay_factor=delay_factor_fast
            if i < int(num_clients / 2)
            else delay_factor_slow,
            # Shared
            iid_fraction=iid_fraction,
            num_clients=num_clients,
            dry_run=dry_run,
        )
        clients.append(client)

    return clients
