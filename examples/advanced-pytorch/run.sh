#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

# Download the EfficientNetB0 model
python -c "import torch; torch.hub.load( \
        'NVIDIA/DeepLearningExamples:torchhub', \
        'nvidia_efficientnet_b0', pretrained=True)"

python server.py --toy True&
sleep 3  # Sleep for 3s to give the server enough time to start

for i in `seq 0 9`; do
    echo "Starting client $i"
    python client.py --partition=${i} --toy True &
done

# Enable CTRL+C to stop all background processes
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
# Wait for all background processes to complete
wait
