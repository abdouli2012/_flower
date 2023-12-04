import os
import random
import time
from collections import OrderedDict
from functools import partial

import flwr as fl
import hydra
import numpy as np
import pandas as pd
import torch
from flwr.common import ndarrays_to_parameters
from flwr.server.strategy import FedAvg, FedProx
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

from fednova.client import gen_clients_fednova
from fednova.baseline_client import gen_clients_fedavg
from fednova.dataset import load_datasets
from fednova.models import test
from fednova.strategy import FedNova, weighted_average
from fednova.utils import fit_config


@hydra.main(config_path="conf", config_name="base", version_base=None)
def main(cfg: DictConfig) -> None:
	"""Run the baseline.

    Parameters
    ----------
    cfg : DictConfig
        An omegaconf object that stores the hydra config.
    """
	start = time.time()

	# Set seeds for reproduceability
	torch.manual_seed(cfg.seed)
	np.random.seed(cfg.seed)
	random.seed(cfg.seed)
	if torch.cuda.is_available():
		torch.cuda.manual_seed(cfg.seed)
	# torch.backends.cudnn.deterministic = True

	# 1. Print parsed config
	print(OmegaConf.to_yaml(cfg))

	# 2. Prepare your dataset and directories

	if not os.path.exists(cfg.datapath):
		os.makedirs(cfg.datapath)
	if not os.path.exists(cfg.checkpoint_path):
		os.makedirs(cfg.checkpoint_path)

	trainloaders, testloader, data_sizes = load_datasets(cfg)
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	if cfg.mode == "test":
		checkpoint = np.load(f"{cfg.checkpoint_path}bestModel_{cfg.exp_name}_varEpochs_{cfg.var_local_epochs}.npz",
							 allow_pickle=True)
		model = instantiate(cfg.model)
		params_dict = zip(model.state_dict().keys(), checkpoint['arr_0'])
		state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
		model.load_state_dict(state_dict)
		loss, metrics = test(model.to(device), testloader, device)
		print("----Loss: {}, Accuracy: {} on Test set ------".format(loss, metrics["accuracy"]))
		return None

	# 3. Define your clients

	if cfg.strategy == "fednova":
		client_function = gen_clients_fednova
	else:
		client_function = gen_clients_fedavg

	client_fn = client_function(num_epochs=cfg.num_epochs,
								trainloaders=trainloaders,
								testloader=testloader,
								data_sizes=data_sizes,
								model=cfg.model,
								exp_config=cfg)

	# 4. Define your strategy

	init_parameters = [layer_param.cpu().numpy() for _, layer_param in instantiate(cfg.model).state_dict().items()]
	init_parameters = ndarrays_to_parameters(init_parameters)

	eval_fn = partial(test, instantiate(cfg.model), testloader, device)
	fit_config_fn = partial(fit_config, cfg)

	if cfg.strategy == "fednova":
		strategy = FedNova(exp_config=cfg,
						   evaluate_metrics_aggregation_fn=weighted_average,
						   accept_failures=False,
						   on_fit_config_fn=fit_config_fn,
						   initial_parameters=init_parameters,
						   evaluate_fn=eval_fn,
						   fraction_evaluate=0.0
						   )

	elif cfg.strategy == "fedavg" or cfg.strategy == "fedprox":

		# Both FedAvg and FedProx use same strategy for weight aggregation
		# The difference is that FedProx uses a proximal term in the loss function in the local client updates
		# Check fednova/models.py train() for more details

		strategy = FedAvg(evaluate_metrics_aggregation_fn=weighted_average,
						  accept_failures=False,
						  on_fit_config_fn=fit_config_fn,
						  initial_parameters=init_parameters,
						  evaluate_fn=eval_fn,
						  fraction_evaluate=0.0
						  )

	else:
		raise NotImplementedError

	# 5. Start Simulation

	history = fl.simulation.start_simulation(client_fn=client_fn,
											 num_clients=cfg.num_clients,
											 config=fl.server.ServerConfig(num_rounds=cfg.num_rounds),
											 strategy=strategy,
											 client_resources=cfg.client_resources,
											 ray_init_args={"ignore_reinit_error": True, "num_cpus": 8})

	# 6. Save your results
	# save_path = HydraConfig.get().runtime.output_dir
	save_path = cfg.results_dir
	if not os.path.exists(save_path):
		os.makedirs(save_path)

	# round, train_loss = zip(*history.losses_distributed)
	# _, train_accuracy = zip(*history.metrics_distributed["accuracy"])
	round, test_loss = zip(*history.losses_centralized)
	_, test_accuracy = zip(*history.metrics_centralized["accuracy"])

	if len(round) != cfg.num_rounds:
		# drop zeroth evaluation round before start of training
		test_loss = test_loss[1:]
		test_accuracy = test_accuracy[1:]
		round = round[1:]

	file_name = f"{save_path}{cfg.exp_name}_{cfg.strategy}_varEpoch_{cfg.var_local_epochs}_seed_{cfg.seed}_Dec3.csv"

	# df = pd.DataFrame({"round": round, "train_loss": train_loss, "train_accuracy": train_accuracy,
	# 				   "test_loss": test_loss, "test_accuracy": test_accuracy})

	df = pd.DataFrame({"round": round, "test_loss": test_loss, "test_accuracy": test_accuracy})

	df.to_csv(file_name, index=False)

	print("---------Experiment Completed in : {} minutes".format((time.time() - start) / 60))


if __name__ == "__main__":
	main()
