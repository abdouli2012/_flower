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
"""Tests for module serde"""
import numpy as np
import pytest

from flower.transport.serde import ndarray_to_proto, proto_to_ndarray


def test_serialisation_deserialisation() -> None:
    """Test if after serialization/deserialisation the np.ndarray is still identical"""
    arr = np.array([[1, 2], [3, 4], [5, 6]])

    arr_serialized = ndarray_to_proto(arr)
    arr_deserialized = proto_to_ndarray(arr_serialized)

    # Assert deserialized array is equal to original
    np.testing.assert_equal(arr_deserialized, arr)

    # Test false positive
    with pytest.raises(AssertionError, match="Arrays are not equal"):
        np.testing.assert_equal(arr_deserialized, np.ones((3, 2)))
