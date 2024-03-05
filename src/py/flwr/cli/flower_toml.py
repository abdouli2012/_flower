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
"""Utility to validate the flower.toml file.

This module will be improved over time.
"""

import importlib
import os
from typing import Any, Dict, List, Optional, Tuple

import tomli


def load_flower_toml(path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Load flower.toml and return as dict."""
    if path is None:
        cur_dir = os.getcwd()
        toml_path = os.path.join(cur_dir, "flower.toml")
    else:
        toml_path = path

    if not os.path.isfile(toml_path):
        return None

    with open(toml_path, encoding="utf-8") as toml_file:
        data = tomli.loads(toml_file.read())
        return data


def validate_flower_toml_fields(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate flower.toml fields."""
    invalid_reasons = []

    if "project" not in config:
        invalid_reasons.append("Missing [project] section")
    else:
        if "name" not in config["project"]:
            invalid_reasons.append('Property "name" missing in [project]')
        if "version" not in config["project"]:
            invalid_reasons.append('Property "version" missing in [project]')
        if "description" not in config["project"]:
            invalid_reasons.append('Property "description" missing in [project]')
        if "license" not in config["project"]:
            invalid_reasons.append('Property "license" missing in [project]')
        if "authors" not in config["project"]:
            invalid_reasons.append('Property "authors" missing in [project]')

    if "flower" not in config:
        invalid_reasons.append("Missing [flower] section")
    elif "components" not in config["flower"]:
        invalid_reasons.append("Missing [flower.components] section")
    else:
        if "serverapp" not in config["flower"]["components"]:
            invalid_reasons.append(
                'Property "serverapp" missing in [flower.components]'
            )
        if "clientapp" not in config["flower"]["components"]:
            invalid_reasons.append(
                'Property "clientapp" missing in [flower.components]'
            )

    return len(invalid_reasons) == 0, invalid_reasons


def validate_object_reference(ref: str) -> Tuple[bool, Optional[str]]:
    """Validate object reference.

    Returns
    -------
    tuple(bool, Optional[str]): is_valid as bool, reason as string in case string is not valid
    """
    module_str, _, attributes_str = ref.partition(":")
    if not module_str:
        return (
            False,
            f"Missing module in {ref}",
        )
    if not attributes_str:
        return (
            False,
            f"Missing attribute in {ref}",
        )

    # Load module
    try:
        module = importlib.import_module(module_str)
    except ModuleNotFoundError:
        return False, f"Unable to load module {module_str}"

    # Recursively load attribute
    attribute = module
    try:
        for attribute_str in attributes_str.split("."):
            attribute = getattr(attribute, attribute_str)
    except AttributeError:
        return (
            False,
            f"Unable to load attribute {attributes_str} from module {module_str}",
        )

    return (True, None)


def validate_flower_toml(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate flower.toml."""

    is_valid, reasons = validate_flower_toml_fields(config)

    if not is_valid:
        return False, reasons

    # Validate serverapp
    is_valid, reason = validate_object_reference(
        config["flower"]["components"]["serverapp"]
    )
    if not is_valid:
        return False, [reason]

    # Validate clientapp
    is_valid, reason = validate_object_reference(
        config["flower"]["components"]["clientapp"]
    )

    if not is_valid:
        return False, [reason]

    return True, []
