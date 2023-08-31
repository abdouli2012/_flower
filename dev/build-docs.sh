#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../

ROOT=`pwd`

cd doc
sh build-versioned-docs.sh no_translate

cd $ROOT
cd baselines/doc
make html

cd $ROOT
./dev/update-examples.sh
cd examples/doc
make html
