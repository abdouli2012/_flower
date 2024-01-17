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
"""RecordSet utilities."""

from .parametersrecord import Array, ParametersRecord
from .typing import Parameters


def parametersrecord_to_parameters(record: ParametersRecord) -> Parameters:
    """Convert ParameterRecord to legacy Parameters.

    The data in ParameterRecord will be freed. Because legacy Parameters do not keep
    names of tensors, this information will be discarded.
    """
    parameters = Parameters(tensors=[], tensor_type="")

    for key in list(record.data.keys()):
        parameters.tensors.append(record.data[key].data)

        del record.data[key]

    return parameters


def parameters_to_parametersrecord(parameters: Parameters) -> ParametersRecord:
    """Convert legacy Parameters into a single ParametersRecord.

    The memory occupied by inputed parameters will be freed. Because there is no concept
    of names in the legacy Parameters, arbitrary keys will be used when constructing the
    ParametersRecord. Similarly, the shape won't be recorded in the Array objects.
    """
    tensor_type = parameters.tensor_type

    p_record = ParametersRecord()

    for idx in range(len(parameters.tensors)):
        tensor = parameters.tensors.pop(0)
        p_record.set_parameters(
            {str(idx): Array(data=tensor, dtype=tensor_type, stype="", shape=[])}
        )

    return p_record
