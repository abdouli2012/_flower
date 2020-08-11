#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../

echo "=== test.sh ==="

isort --skip src/flwr/proto --check-only -rc src/flwr     && echo "- isort:  done" &&
black -q --exclude "src\/flwr\/proto" --check src/flwr  && echo "- black:  done" &&
# docformatter is missing --exclude src/flwr/proto 
docformatter -c -r src/flwr  && echo "- docformatter:  done" &&
# mypy src                                                  && echo "- mypy:   done" &&
pylint --ignore=src/flwr/proto src/flwr                   && echo "- pylint: done" &&
pytest -q src/flwr                                        && echo "- pytest: done" &&
echo "- All Python checks passed"
