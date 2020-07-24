#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../

echo "=== test-baseline.sh ==="

isort --check-only -rc src/flwr_experimental/baseline  && echo "- isort:  done" &&
black -q --check src/flwr_experimental/baseline        && echo "- black:  done" &&
# mypy is covered by test.sh
pylint src/flwr_experimental/baseline                  && echo "- pylint: done" &&
pytest -q src/flwr_experimental/baseline               && echo "- pytest: done" &&
echo "- All Python checks passed"
