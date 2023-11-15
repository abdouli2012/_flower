"""Define any utility function.

They are not directly relevant to  the other (more FL specific) python modules. For
example, you may define here things like: loading a model from a checkpoint, saving
results, plotting.
"""

import pickle, yaml
from pathlib import Path
import matplotlib.pyplot as plt

def saveFig(name, fig):
    fig.savefig(
        name,
        dpi=None,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        orientation="portrait",
        format="png",
        transparent=False,
        bbox_inches="tight",
        pad_inches=0.2,
        metadata=None,
    )


def _read_pickle_and_config(path_to_pickle):
    with open(path_to_pickle, "rb") as handle:
        data = pickle.load(handle)

    config_path = Path(path_to_pickle).parent / ".hydra" / "config.yaml"
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return data, config

def _fuse_by_dataset(losses):
    fussed_losses = {}
    keys = losses[0][1].keys()

    for _, loss_dict in losses:
        for k,v in loss_dict.items():
            if k in fussed_losses:
                fussed_losses[k].append(v)
            else:
                fussed_losses[k] = [v]
    return fussed_losses

def quick_plot(path_to_pickled_history: str):

    data, config = _read_pickle_and_config(path_to_pickled_history)

    pre_train_loss = data['history'].metrics_distributed_fit['pre_train_losses']

    fussed_losses = _fuse_by_dataset(pre_train_loss)

    fig, axs = plt.subplots(figsize=(10,6))
    for dataset, loss in fussed_losses.items():
        plt.plot(range(len(loss)), loss, label=dataset)
        plt.title(f"client: {config['client']['_target_']}\n num_clients: {config['num_clients']}, percent: {config['dataset']['percent']}")
        plt.legend()
        plt.grid()
        plt.xlabel('Round')
        plt.ylabel('Train Loss')
    
    dir_path = Path(path_to_pickled_history).parent
    saveFig(f'{dir_path}/train_loss.png', fig)
