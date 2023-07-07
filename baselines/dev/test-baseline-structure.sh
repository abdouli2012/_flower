#!/bin/bash

set -e
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <baseline-name=directory-of-the-baseline>"
    exit 1
fi
baseline_dir=$1

# Specify the exceptions to the structure requirement
declare -a structure_exceptions=()

# List of require to check
declare -a required_files=("client.py" "dataset.py" "dataset_preparation.py" "main.py" "models.py" "server.py" "strategy.py" "utils.py")

# Check and pass the test if the baseline directory is in the list of exceptions
for exception in "${structure_exceptions[@]}"; do
  if [[ "$baseline_dir" == "$exception" ]]; then
    exit 0
  fi
done

# If the baseline directory is not in the list of exceptions
for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    echo "$file exists."
  else
    echo "$file does not exist."
    exit 1
  fi
done

