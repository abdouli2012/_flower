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
"""Utility functions for model quantization."""


from typing import List, cast

import numpy as np

from flwr.common.typing import NDArrayFloat, NDArrayInt


def _stochastic_round(arr: NDArrayInt) -> NDArrayInt:
    ret: NDArrayInt = np.ceil(arr).astype(arr.dtype)
    rand_arr = np.random.rand(*ret.shape)
    ret[rand_arr < ret - arr] -= 1
    return ret


def quantize(
    weights: List[NDArrayFloat], clipping_range: float, target_range: int
) -> List[NDArrayInt]:
    """Quantize float Numpy arrays to integer Numpy arrays."""
    quantized_list = []
    quantizer = target_range / (2 * clipping_range)
    for arr in weights:
        # stochastic quantization
        quantized = (
            np.clip(arr, -clipping_range, clipping_range) + clipping_range
        ) * quantizer
        quantized = _stochastic_round(quantized)
        quantized_list.append(quantized)
    return quantized_list


# Transform weight vector to range [-clipping_range, clipping_range]
# Convert to float
def dequantize(
    quantized_weights: List[NDArrayInt],
    clipping_range: float,
    target_range: int,
) -> List[NDArrayFloat]:
    """Dequantize integer Numpy arrays to float Numpy arrays."""
    reverse_quantized_list: List[NDArrayFloat] = []
    quantizer = (2 * clipping_range) / target_range
    shift = -clipping_range
    for arr in quantized_weights:
        recon_arr = arr.view(np.ndarray).astype(float)
        recon_arr = cast(NDArrayFloat, recon_arr * quantizer + shift)
        reverse_quantized_list.append(recon_arr)
    return reverse_quantized_list
