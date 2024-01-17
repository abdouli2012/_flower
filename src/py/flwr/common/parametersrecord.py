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
"""ParametersRecord and Array."""

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Array:
    """Array type.

    A datacalss conatining serialized data from an array-like or tensor-like object
    alongwith some metata about it.

    Parameters
    ----------
    dtype : str
        A string representing the data type of the serialised object (e.g. `np.float32`)

    shape : List[int]
        A list representing the shape of the unserliazed array-like object. This is used
        to deserialize the data (depending on the serialization method) or simply as a
        metadata field.

    stype : str
        For compatibility when converting from/to `flwr.common.typing.Parameters`. A
        sting stating that then data comes from a NumPy NDArray.

    data: bytes
        A buffer of bytes containing the data.
    """

    dtype: str
    shape: List[int]
    stype: str
    data: bytes


@dataclass
class ParametersRecord:
    """Parameters record.

    A dataclass storing named Arrays in order. This means that it holds entries as an
    OrderedDict[str, Array]. ParametersRecord objects can be viewed as an equivalent to
    PyTorch's state_dict but holding serialised tensors instead.
    """

    keep_input: bool
    data: OrderedDict[str, Array] = field(default_factory=OrderedDict[str, Array])

    def __init__(
        self,
        array_dict: Optional[Dict[str, Array]] = None,
        keep_input: bool = False,
    ) -> None:
        """Construct a ParametersRecord object.

        Parameters
        ----------
        keep_input : bool (default: False)
            A boolean indicating whether parameters should be deleted from the input
            dictionary inmediately after adding them to the record. If True, the
            dictionary passed to `set_parameters()` will be empty once exiting from that
            function. This is the desired behaviour when working with very large
            models/tensors/arrays. However, if you plan to continue working with your
            parameters after adding it to the record, set this flag to False. When set
            to False, the data is duplicated inmemory.

        data : Optional[OrderedDict[str, Array]] (default: None)
            An OrderedDict that stores serialized array-like or tensor-like objects.
        """
        self.keep_input = keep_input
        self.data = OrderedDict()
        if array_dict:
            self.set_parameters(array_dict)

    def set_parameters(self, array_dict: Dict[str, Array]) -> None:
        """Add parameters to record.

        Parameters
        ----------
        data : Optional[OrderedDict[str, Array]] (default: None)
            An OrderedDict that stores serialized array-like or tensor-like objects.
        """
        if any(not isinstance(k, str) for k in array_dict.keys()):
            raise TypeError(f"Not all keys are of valide type. Expected {str}")
        if any(not isinstance(v, Array) for v in array_dict.values()):
            raise TypeError(f"Not all values are of valide type. Expected {Array}")

        if self.keep_input:
            # Copy
            self.data = OrderedDict(array_dict)
        else:
            # Add entries to dataclass without duplicating memory
            for key in list(array_dict.keys()):
                self.data[key] = array_dict[key]
                del array_dict[key]
