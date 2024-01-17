#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

# Download the EfficientNetB0 model
python -c "import torch; torch.hub.load( \
        'NVIDIA/DeepLearningExamples:torchhub', \
        'nvidia_efficientnet_b0', pretrained=True)"

python server.py --toy  &
sleep 10  # Sleep for 10s to give the server enough time to start

for i in `seq 0 9`; do
    echo "Starting client $i"
    python client.py --client-id=${i} --toy &
done

# Enable CTRL+C to stop all background processes
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
# Wait for all background processes to complete
wait
