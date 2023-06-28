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

# create a directory to save generated api reference
mkdir -p SwiftDoc
# making sure to start a clean build
find ~/Library/Developer/Xcode/DerivedData -name "flwr.doccarchive" -exec rm -Rf {} \; || true

# change directory to the swift sdk source code folder
# Generate API reference for the Swift SDK by running `xcodebuild docbuild` in src directory
cd src/swift/flwr && \
arch -x86_64 xcodebuild docbuild -scheme flwr -destination 'platform=iOS Simulator,name=iPhone 14 Pro Max,OS=16.4'

# find the generated doccarchive file in Xcode derived data folder and copy it to the SwiftDoc directory
find ~/Library/Developer/Xcode/DerivedData -name "flwr.doccarchive" -exec cp -R {} SwiftDoc \;
# Transform the `doccarchive` file to static HTML and store the output in the `SwiftDoc/html` folder
$(xcrun --find docc) process-archive transform-for-static-hosting "SwiftDoc/flwr.doccarchive" --output-path "SwiftDoc/html" 
