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
"""Plotting utils."""
from typing import Optional, Tuple

import numpy as np

from visualization.constants import PLOT_TYPES, SIZE_UNITS, AXIS_TYPES


def _validate_parameters(
    plot_type: str, size_unit: str, partition_id_axis: str
) -> None:
    if plot_type not in PLOT_TYPES:
        raise ValueError(
            f"Invalid plot_type: {plot_type}. Must be one of {PLOT_TYPES}."
        )
    if size_unit not in SIZE_UNITS:
        raise ValueError(
            f"Invalid size_unit: {size_unit}. Must be one of {SIZE_UNITS}."
        )
    if partition_id_axis not in AXIS_TYPES:
        raise ValueError(
            f"Invalid partition_id_axis: {partition_id_axis}. Must be one of {AXIS_TYPES}."
        )
def _initialize_figsize(
    figsize: Optional[Tuple[float, float]],
    plot_type: str,
    partition_id_axis: str,
    num_partitions: int,
    num_labels: int,
) -> Tuple[float, float]:
    if figsize is not None:
        if not isinstance(figsize, tuple):
            raise TypeError(
                f"'figsize' should of type 'tuple' but given: {type(figsize)}"
            )
        return figsize

    if plot_type == "bar":
        if partition_id_axis == "x":
            figsize = (6.4, 4.8)
        elif partition_id_axis == "y":
            figsize = (6.4, np.sqrt(num_partitions))
    elif plot_type == "heatmap":
        if partition_id_axis == "x":
            figsize = (3 * np.sqrt(num_partitions), np.sqrt(num_labels))
        elif partition_id_axis == "y":
            figsize = (3 * np.sqrt(num_labels), np.sqrt(num_partitions))
    else:
        raise ValueError(
            f"The type of plot must be 'bar' or 'heatmap' but given: {plot_type}"
        )
    assert figsize is not None
    return figsize


def _initialize_xy_labels(
    plot_type: str, size_unit: str, partition_id_axis: str
) -> Tuple[str, str]:
    if plot_type == "bar":
        xlabel = "Partition ID"
        ylabel = "Count" if size_unit == "absolute" else "Percent %"
    elif plot_type == "heatmap":
        xlabel = "Partition ID"
        ylabel = "Label"
    else:
        raise ValueError(f"Invalid plot_type: {plot_type}. Must be 'bar' or 'heatmap'.")

    if partition_id_axis == "y":
        xlabel, ylabel = ylabel, xlabel

    return xlabel, ylabel





def _initialize_cbar_title(plot_type: str, size_unit: str) -> Optional[str]:
    if plot_type == "heatmap":
        return "Count" if size_unit == "absolute" else "Percent %"
    return None


def _initialize_comparison_figsize(
    figsize: Optional[Tuple[float, float]], num_partitioners: int
) -> Tuple[float, float]:
    if figsize is not None:
        return figsize
    x_value = 4 + (num_partitioners - 1) * 2
    y_value = 4.8
    figsize = (x_value, y_value)
    return figsize


def _initialize_comparison_xy_labels(
    plot_type: str, partition_id_axis: str
) -> Tuple[str, str]:
    if plot_type == "bar":
        xlabel = "Partition ID"
        ylabel = "Class distribution"
    elif plot_type == "heatmap":
        xlabel = "Partition ID"
        ylabel = "Label"
    else:
        raise ValueError(f"Invalid plot_type: {plot_type}. Must be 'bar' or 'heatmap'.")

    if partition_id_axis == "y":
        xlabel, ylabel = ylabel, xlabel

    return xlabel, ylabel
