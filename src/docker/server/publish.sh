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
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

BROWN='\033[0;33m'
NC='\033[0m' # No Color

# Define default values first
BUILD_TARGET="${BUILD_TARGET:=server}"
FLWR_VERSION="${FLWR_VERSION:=1.5.0}"

echo -e "${BROWN}\nUsing:"
echo -e "BUILD_TARGET: $BUILD_TARGET"
echo -e "FLWR_VERSION: $FLWR_VERSION"
echo -e "${NC}"

# Tag image with FLWR_VERSION as latest and push all to remote
docker tag flwr/$BUILD_TARGET:$FLWR_VERSION flwr/$BUILD_TARGET:latest
docker push flwr/$BUILD_TARGET:$FLWR_VERSION
docker push flwr/$BUILD_TARGET:latest
