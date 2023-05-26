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
"""Aggregation function tests."""


from typing import List, Tuple

import numpy as np

from .aggregate import _check_weights_equality, aggregate, weighted_loss_avg


def test_aggregate() -> None:
    """Test aggregate function."""

    # Prepare
    weights0_0 = np.array([[1, 2, 3], [4, 5, 6]])
    weights0_1 = np.array([7, 8, 9, 10])
    weights1_0 = np.array([[1, 2, 3], [4, 5, 6]])
    weights1_1 = np.array([7, 8, 9, 10])
    results = [([weights0_0, weights0_1], 1), ([weights1_0, weights1_1], 2)]

    expected = [np.array([[1, 2, 3], [4, 5, 6]]), np.array([7, 8, 9, 10])]

    # Execute
    actual = aggregate(results)

    # Assert
    np.testing.assert_equal(expected, actual)  # type: ignore


def test_weighted_loss_avg_single_value() -> None:
    """Test weighted loss averaging."""
    # Prepare
    results: List[Tuple[int, float]] = [(5, 0.5)]
    expected = 0.5

    # Execute
    actual = weighted_loss_avg(results)

    # Assert
    assert expected == actual


def test_weighted_loss_avg_multiple_values() -> None:
    """Test weighted loss averaging."""
    # Prepare
    results: List[Tuple[int, float]] = [(1, 2.0), (2, 1.0), (1, 2.0)]
    expected = 1.5

    # Execute
    actual = weighted_loss_avg(results)

    # Assert
    assert expected == actual


def test_check_weights_equality_true() -> None:
    w1 = [np.array([1, 2]), np.array([[1, 2], [3, 4]])]
    w2 = [np.array([1, 2]), np.array([[1, 2], [3, 4]])]
    results = _check_weights_equality(w1, w2)
    expected = True
    assert expected == results


def test_check_weights_equality_numeric_false() -> None:
    w1 = [np.array([1, 2]), np.array([[1, 2], [3, 4]])]
    w2 = [np.array([2, 2]), np.array([[1, 2], [3, 4]])]
    results = _check_weights_equality(w1, w2)
    expected = False
    assert expected == results


def test_check_weights_equality_various_legnth_false() -> None:
    w1 = [np.array([1, 2]), np.array([[1, 2], [3, 4]])]
    w2 = [np.array([1, 2])]
    results = _check_weights_equality(w1, w2)
    expected = False
    assert expected == results
