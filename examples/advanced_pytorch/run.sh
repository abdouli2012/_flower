#!/bin/bash

# download the CIFAR10 dataset if not already downloaded
python -c "from torchvision.datasets import CIFAR10; \
    CIFAR10('./dataset', train=True, download=True)" 

python server.py &
sleep 2 # Sleep for 2s to give the server enough time to start

for i in `seq 0 9`; do
    echo "Starting client $i"
    python client.py --partition=${i} &
done

# This will allow you to use CTRL+C to stop all background processes
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
# Wait for all background processes to complete
wait
