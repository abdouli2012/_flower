#!/bin/bash

# Copyright 2023 Flower Labs GmbH. All Rights Reserved.
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

set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../

# Purpose of this script is to evaluate if the user changed the pyproject.toml definitions
# but did not regenerate or commit the new requirements.txt files

# Regenerate requirements.txt
pip install pipreqs

for path in $(find ./examples -type f -name 'pyproject.toml' | sed -E 's|/[^/]+$||' |sort -u)
do
    echo $path
    pipreqs $path
done

# Fail if user forgot to recompile
CHANGED=$(git diff --name-only HEAD examples)

if [ -n "$CHANGED" ]; then
    echo "Changes detected"
    exit 1
fi

echo "No changes detected"
exit 0
