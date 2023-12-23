"""Create and connect the building blocks for your experiments; start the simulation.

It includes processioning the dataset, instantiate strategy, specify how the global
model is going to be evaluated, etc. At the end, this script saves the results.
"""
import os
import shutil

import flwr as fl
import hydra
from flwr.server.client_manager import SimpleClientManager
from hydra.core.hydra_config import HydraConfig
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

from .attacks import fang_attack, gaussian_attack, lie_attack, minmax_attack
from .client import CifarClient, HouseClient, IncomeClient, MnistClient
from .dataset import (
    do_fl_partitioning,
    get_cifar_10,
    get_partitioned_house,
    get_partitioned_income,
)
from .server import EnhancedServer
from .utils import (
    cifar_evaluate,
    house_evaluate,
    income_evaluate,
    l2_norm,
    mnist_evaluate,
)


# pylint: disable=too-many-locals
@hydra.main(config_path="conf", config_name="base", version_base=None)
def main(cfg: DictConfig) -> None:
    """Run the baseline.

    Parameters
    ----------
    cfg : DictConfig
        An omegaconf object that stores the hydra config.
    """
    # 1. Print parsed config
    print(OmegaConf.to_yaml(cfg))

    attacks = {
        "gaussian": gaussian_attack,
        "lie": lie_attack,
        "fang": fang_attack,
        "minmax": minmax_attack,
    }

    clients = {
        "mnist": (MnistClient, mnist_evaluate),
        "cifar": (CifarClient, cifar_evaluate),
        "house": (HouseClient, house_evaluate),
        "income": (IncomeClient, income_evaluate),
    }

    # Delete old client_params
    if os.path.exists(cfg.server.history_dir):
        shutil.rmtree(cfg.server.history_dir)

    # Output directory for results
    save_path = HydraConfig.get().runtime.output_dir

    dataset_name = cfg.dataset
    attack_fn = cfg.server.attack_fn
    num_malicious = cfg.server.num_malicious

    # 2. Prepare your dataset
    if dataset_name == "cifar":
        train_path, _ = get_cifar_10()
        fed_dir = do_fl_partitioning(
            train_path,
            pool_size=cfg.server.pool_size,
            alpha=10000,
            num_classes=10,
            val_ratio=0.5,
            seed=1234,
        )
    elif dataset_name == "income":
        x_train, x_test, y_train, y_test = get_partitioned_income(
            "flanders/datasets_files/adult.csv", cfg.server.pool_size
        )
    elif dataset_name == "house":
        x_train, x_test, y_train, y_test = get_partitioned_house(
            "flanders/datasets_files/houses_preprocessed.csv", cfg.server.pool_size
        )

    # 3. Define your clients
    # pylint: disable=no-else-return
    def client_fn(cid: str, pool_size: int = 10, dataset_name: str = dataset_name):
        client = clients[dataset_name][0]
        cid_idx = int(cid)
        if dataset_name == "cifar":
            return client(cid, fed_dir)
        elif dataset_name == "mnist":
            return client(cid, pool_size)
        elif dataset_name == "income":
            return client(
                cid,
                x_train[cid_idx],
                y_train[cid_idx],
                x_test[cid_idx],
                y_test[cid_idx],
            )
        elif dataset_name == "house":
            return client(
                cid,
                x_train[cid_idx],
                y_train[cid_idx],
                x_test[cid_idx],
                y_test[cid_idx],
            )
        else:
            raise ValueError("Dataset not supported")

    # 4. Define your strategy
    strategy = instantiate(
        cfg.strategy,
        evaluate_fn=clients[dataset_name][1],
        on_fit_config_fn=fit_config,
        fraction_fit=1,
        fraction_evaluate=0,
        min_fit_clients=cfg.server.pool_size,
        min_evaluate_clients=0,
        warmup_rounds=cfg.server.warmup_rounds,
        to_keep=cfg.strategy.to_keep,
        min_available_clients=cfg.server.pool_size,
        window=cfg.server.warmup_rounds,
        distance_function=l2_norm,
        maxiter=cfg.strategy.maxiter,
    )

    # 5. Start Simulation
    fl.simulation.start_simulation(
        client_fn=client_fn,
        client_resources={"num_cpus": 10},
        num_clients=cfg.server.pool_size,
        server=EnhancedServer(
            warmup_rounds=cfg.server.warmup_rounds,
            num_malicious=num_malicious,
            attack_fn=attacks[attack_fn],  # type: ignore
            magnitude=cfg.server.magnitude,
            client_manager=SimpleClientManager(),
            strategy=strategy,
            sampling=cfg.server.sampling,
            history_dir=cfg.server.history_dir,
            dataset_name=dataset_name,
            threshold=cfg.server.threshold,
            omniscent=cfg.server.omniscent,
            output_dir=save_path,
        ),
        config=fl.server.ServerConfig(num_rounds=cfg.server.num_rounds),
        strategy=strategy,
    )


# pylint: disable=unused-argument
def fit_config(server_round):
    """Return a configuration with static batch size and (local) epochs."""
    config = {
        "epochs": 1,  # number of local epochs
        "batch_size": 32,
    }
    return config


if __name__ == "__main__":
    main()
