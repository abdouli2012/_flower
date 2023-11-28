"""Create and connect the building blocks for your experiments; start the simulation.

It includes processioning the dataset, instantiate strategy, specify how the global
model is going to be evaluated, etc. At the end, this script saves the results.
"""
# these are the basic packages you'll need here
# feel free to remove some if aren't needed

import warnings
import subprocess
import textwrap
from argparse import Namespace
from collections import OrderedDict
from typing import Dict

import flwr as fl
import hydra
import numpy as np
import torch
from flwr.common import parameters_to_ndarrays
from hydra.utils import instantiate
from mmengine.config import Config
from omegaconf import DictConfig, OmegaConf
from hydra.core.hydra_config import HydraConfig

from .client import SslClient
from .CtP.pyvrl.builder import build_model
from .utils import init_p_paths, load_data, load_model, set_config_mmcv


warnings.filterwarnings("ignore", category=UserWarning)


def t_f(arg):
    """Transfer bool format."""
    label = str(arg).upper()
    if "TRUE".startswith(label):
        return True
    elif "FALSE".startswith(label):
        return False


def initial_setup(
    cid, base_work_dir, rounds, data_dir, num_gpus, partition_dir, cfg_path
):
    """Initialise setup for instantiating client class."""
    cid_plus_one = str(int(cid) + 1)
    args = Namespace(
        cfg=cfg_path,  # Path to the pretraining configuration file
        checkpoint=None,
        cid=int(cid),
        data_dir=data_dir,
        gpus=num_gpus,
        launcher="none",
        local_rank=0,
        progress=False,
        resume_from=None,
        rounds=rounds,
        seed=7,
        validate=False,
        work_dir=base_work_dir + "/client" + cid_plus_one,
    )

    print("Starting client", args.cid)
    # fetch the configuration file
    cfg = Config.fromfile(args.cfg)
    # define the client data files;
    # usually contains paths to the samples and annotations
    cfg.data.train.data_source.ann_file = (
        partition_dir + "/client_dist" + cid_plus_one + ".json"
    )

    distributed, logger = set_config_mmcv(args, cfg)
    # These two arguments needs to be false during federated pretraining
    # otherwise the client will load the previously saved checkpoint

    cfg.resume_from = False
    cfg.load_from = False

    # load the model
    model = load_model(cfg)
    # load the training data
    train_dataset = load_data(cfg)

    # since during pretraining of FedVSSL
    # we don't need any testing data, we can left it empty.
    test_dataset = " "

    return args, cfg, distributed, logger, model, train_dataset, test_dataset


def fit_config(rnd: int) -> Dict[str, str]:
    """Return a configuration with global epochs."""
    config = {
        "epoch_global": str(rnd),
    }
    return config


@hydra.main(config_path="conf", config_name="base", version_base=None)
def main(cfg: DictConfig) -> None:
    """Define the main function for FL pre-training or fine-tuning."""
    # print config structured as YAML
    print(OmegaConf.to_yaml(cfg))

    save_path = HydraConfig.get().runtime.output_dir

    if cfg.pre_training:
        # first the paths needs to be defined
        # otherwise the program may not be able to locate the files of the ctp

        init_p_paths("fedvssl")

        client_resources = {
            "num_cpus": cfg.client_resources.num_cpus,
            "num_gpus": cfg.client_resources.num_gpus,
        }
        base_work_dir = save_path + f"/{cfg.exp_name}"
        rounds = cfg.rounds
        data_dir = cfg.data_dir + "/ucf101"
        partition_dir = cfg.partition_dir
        num_gpus = int(np.ceil(cfg.client_resources.num_gpus))

        def client_fn(cid: str):
            (
                args,
                config,
                distributed,
                logger,
                model,
                train_dataset,
                test_dataset,
            ) = initial_setup(
                cid,
                base_work_dir,
                rounds,
                data_dir,
                num_gpus,
                partition_dir,
                cfg.cfg_path_pretrain,
            )
            return SslClient(
                model,
                train_dataset,
                test_dataset,
                config,
                args,
                distributed,
                logger,
            )

        # configure the strategy
        strategy = instantiate(
            cfg.strategy,
            on_fit_config_fn=fit_config,
        )

        # (optional) specify ray config
        ray_config = {"include_dashboard": cfg.client_resources.include_dashboard}

        # start simulation
        fl.simulation.start_simulation(
            client_fn=client_fn,
            num_clients=cfg.pool_size,
            client_resources=client_resources,
            config=fl.server.ServerConfig(num_rounds=cfg.rounds),
            strategy=strategy,
            ray_init_args=ray_config,
        )
    else:
        # we give an example on how one can perform fine-tuning uisng UCF-101 dataset.
        cfg_path = cfg.cfg_path_finetune
        cfg_ = Config.fromfile(cfg_path)
        cfg_.model.backbone["pretrained"] = None
        work_dir_finetune = save_path + f"/{cfg.exp_name_finetune}"

        # build a model using the configuration file from Ctp repository
        model = build_model(cfg_.model)

        # path to the pretrained model.
        # We provide certain federated pretrained model that can be easily downloaded
        # from the following link: https://github.com/yasar-rehman/FEDVSSL
        # here we gave an example with FedVSSL (alpha=0, beta=0) checkpoint file
        # The files after federated pretraining are usually saved in .npz format.

        pretrained = cfg.pretrained_model_path

        # conversion of the .npz files to the .pth format.
        # If the files are saved in .npz format
        if pretrained and pretrained.endswith(".npz"):
            # following changes are made here
            params = np.load(pretrained, allow_pickle=True)
            params = params["arr_0"].item()
            params = parameters_to_ndarrays(params)
            params_dict = zip(model.state_dict().keys(), params)
            state_dict = {
                "state_dict": OrderedDict(
                    {k: torch.from_numpy(v) for k, v in params_dict}
                )
            }
            torch.save(state_dict, "./model_pretrained.pth")

        # ---------------------------------------------------
        # The cfg_path need to be updated with the following updated
        # configuration contents to be able to load the pretrained model.
        # Instead of executing the blow mentioned code,
        # one can also directly modify the "pretrained" variable by
        # opening the path represented by the config_path variable

        config_content = textwrap.dedent(
            f"""\
                _base_ = ['../../recognizers/_base_/model_r3d18.py',
                '../../recognizers/_base_/runtime_ucf101.py']
                work_dir = '{work_dir_finetune}'
                model = dict(
                    backbone=dict(
                        pretrained='./model_pretrained.pth',
                    ),
                )
               """
        ).strip("\n")

        with open(cfg_path, "w") as f_w:
            f_w.write(config_content)

        subprocess.run(
            [
                "bash",
                f"{cfg.dist_train_path}",
                f"{cfg_path}",
                "1",
                f"--work_dir {work_dir_finetune}",
                f"--data_dir {cfg.data_dir}",
            ]
        )

        # -----------------------------------------
        # The cfg_path need to be updated with the following
        # updated configuration contents to be able to load the pretrained model.
        # Instead of executing the blow mentioned code,
        # one can also directly modify the "pretrained" variable by
        # opening the file represented by the cfg_path_test variable

        config_content_test = textwrap.dedent(
            f"""\
                _base_ = ['../../recognizers/_base_/model_r3d18.py',
                '../../recognizers/_base_/runtime_ucf101.py']
                work_dir = '{work_dir_finetune}'
                model = dict(
                    backbone=dict(
                    pretrained='/finetune/ucf101/epoch_150.pth',
                ),
                )
               """
        ).strip("\n")

        cfg_path_test = cfg.test_script
        with open(cfg_path_test, "w") as f_w:
            f_w.write(config_content_test)

        # Evaluating the finetuned model
        subprocess.run(
            [
                "bash",
                f"{cfg.dist_test_path}",
                f"{cfg_path_test}",
                f"{cfg.finetune_num_gpus}",
                f"--work_dir {work_dir_finetune}",
                f"--data_dir {cfg.data_dir}",
                "--progress",
            ]
        )


if __name__ == "__main__":
    main()
