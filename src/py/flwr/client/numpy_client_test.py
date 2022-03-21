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
"""Flower NumPyClient tests."""


from typing import Dict, List, Tuple

import numpy as np

from flwr.common import Config, Properties, Scalar

from .numpy_client import NumPyClient


class OverridingClient(NumPyClient):
    """Client overriding `get_properties`."""

    def get_properties(self, config: Config) -> Properties:
        return {}

    def get_parameters(self) -> List[np.ndarray]:
        # This method is not expected to be called
        raise Exception()

    def fit(
        self, parameters: List[np.ndarray], config: Dict[str, Scalar]
    ) -> Tuple[List[np.ndarray], int, Dict[str, Scalar]]:
        # This method is not expected to be called
        raise Exception()

    def evaluate(
        self, parameters: List[np.ndarray], config: Dict[str, Scalar]
    ) -> Tuple[float, int, Dict[str, Scalar]]:
        # This method is not expected to be called
        raise Exception()


class NotOverridingClient(NumPyClient):
    """Client not overriding `get_properties`."""

    def get_parameters(self) -> List[np.ndarray]:
        # This method is not expected to be called
        raise Exception()

    def fit(
        self, parameters: List[np.ndarray], config: Dict[str, Scalar]
    ) -> Tuple[List[np.ndarray], int, Dict[str, Scalar]]:
        # This method is not expected to be called
        raise Exception()

    def evaluate(
        self, parameters: List[np.ndarray], config: Dict[str, Scalar]
    ) -> Tuple[float, int, Dict[str, Scalar]]:
        # This method is not expected to be called
        raise Exception()


def test_has_get_properties_true() -> None:
    """Test fit_clients."""
    # Prepare
    client = OverridingClient()

    # Execute
    try:
        client.get_properties({})
    except AttributeError:
        assert False
    else:
        assert True


def test_has_get_properties_false() -> None:
    """Test fit_clients."""
    # Prepare
    client = NotOverridingClient()

    # Execute
    try:
        client.get_properties({})
    except AttributeError:
        assert True
    else:
        assert False

