# Copyright 2020 Flower Labs GmbH. All Rights Reserved.
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


def test_add_gaussian_noise() -> None:
    """Test add_gaussian_noise function."""
    # Prepare
    strategy = FedAvg()
    dp_wrapper = DPStrategyWrapperServerSideFixedClipping(strategy, 1.5, 1.5, 5)

    update = [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])]
    std_dev = 0.1

    # Execute
    update_noised = dp_wrapper.add_gaussian_noise(update, std_dev)

    # Assert
    # Check that the shape of the result is the same as the input
    for layer, layer_noised in zip(update, update_noised):
        assert layer.shape == layer_noised.shape

    # Check that the values have been changed and is not equal to the original update
    for layer, layer_noised in zip(update, update_noised):
        assert not np.array_equal(layer, layer_noised)

    # Check that the noise has been added
    for layer, layer_noised in zip(update, update_noised):
        noise_added = layer_noised - layer
        assert np.any(np.abs(noise_added) > 0)
