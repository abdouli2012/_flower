from logging import WARNING, DEBUG
from typing import Callable, Dict, List, Optional, Tuple, Union
import torch.nn.functional as F
import matplotlib.pyplot as plt
from flwr.common import (
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    MetricsAggregationFn,
    NDArrays,
    Parameters,
    Scalar,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
)
from flwr.common.logger import log
from flwr.server.client_manager import ClientManager
from flwr.server.client_proxy import ClientProxy

from flwr.server.utils import Generator, ResNet18, VAE, CVAE, infoVAE
from .aggregate import aggregate, weighted_loss_avg
from .fedavg import FedAvg
import wandb
import matplotlib
import numpy as np
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

matplotlib.use("Agg")
WARNING_MIN_AVAILABLE_CLIENTS_TOO_LOW = """
Setting `min_available_clients` lower than `min_fit_clients` or
`min_evaluate_clients` can cause the server to fail when there are too few clients
connected to the server. `min_available_clients` must be set to a value larger
than or equal to the values of `min_fit_clients` and `min_evaluate_clients`.
"""
import torch
import torch.nn as nn
from collections import OrderedDict


def visualize_plotly_latent_representation(
    model, test_loader, device, use_PCA=False, num_class=10
):
    model.eval()
    all_recons = []
    all_labels = []
    all_means = []

    with torch.no_grad():
        for data, labels in test_loader:
            data = data.to(device)
            recon, mu, _ = model(data)
            all_recons.append(recon.cpu().numpy())
            all_means.append(mu.cpu().numpy())
            all_labels.append(labels.numpy())

    all_recons = np.concatenate(all_recons, axis=0)
    all_means = np.concatenate(all_means, axis=0)
    all_labels = np.concatenate(all_labels, axis=0)
    reduced_latents = all_means
    if use_PCA:

        from sklearn.decomposition import PCA

        pca = PCA(n_components=2)
        reduced_latents = pca.fit_transform(all_means)

    traces = []
    for label in np.unique(all_labels):
        indices = np.where(all_labels == label)
        trace = go.Scatter(
            x=reduced_latents[indices, 0].flatten(),
            y=reduced_latents[indices, 1].flatten(),
            mode="markers",
            name=f"Digit {label}",
            marker=dict(size=8),
        )
        traces.append(trace)

    layout = go.Layout(
        title="Latent Representation with True Labels",
        xaxis=dict(title="Principal Component 1"),
        yaxis=dict(title="Principal Component 2"),
        legend=dict(title="True Labels"),
        hovermode="closest",
    )
    fig = go.Figure(data=traces, layout=layout)

    return fig


def info_vae_loss(recon_x, x, mu, logvar, y, y_pred, lambda_kl=0.01, lambda_info=10.0):
    # Reconstruction loss
    recon_loss = F.binary_cross_entropy(
        recon_x, x.view(-1, 784), reduction="mean"
    )  # Adjust for your data type

    # KL divergence loss
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), dim=1).mean()

    # Information loss (cross-entropy between predicted and true auxiliary variable)
    info_loss = F.cross_entropy(y_pred, y, reduction="mean")

    # Total loss
    total_loss = recon_loss + lambda_kl * kl_loss + lambda_info * info_loss

    return total_loss, recon_loss.item(), kl_loss.item(), info_loss.item()


def vae_loss(recon_img, img, mu, logvar, beta=1.0, separate=False):
    # Reconstruction loss using binary cross-entropy
    condition = (recon_img >= 0.0) & (recon_img <= 1.0)
    # assert torch.all(condition), "Values should be between 0 and 1"
    if not torch.all(condition):
        ValueError("Values should be between 0 and 1")
        recon_img = torch.clamp(recon_img, 0.0, 1.0)
    bce_loss_per_pixel = F.binary_cross_entropy(
        recon_img, img.view(-1, img.shape[2] * img.shape[3]), reduction="none"
    )
    # Sum along dimension 1 (sum over pixels for each image)
    bce_loss_sum_per_image = torch.sum(
        bce_loss_per_pixel, dim=1
    )  # Shape: (batch_size,)

    # Take the mean along dimension 0 (mean over images in the batch)
    recon_loss = torch.mean(bce_loss_sum_per_image)  # Shape: scalar

    # KL divergence loss
    kld_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), dim=1)
    # Take the mean along dimension 0 (mean over images in the batch)
    kld_loss = torch.mean(kld_loss)
    # Total VAE loss
    total_loss = recon_loss + kld_loss * beta
    if separate:
        return total_loss, recon_loss.item(), kld_loss.item()
    else:
        return total_loss


def pca_cluster_loss(z, torch_label, lambda_pca=2):
    pca = PCA(n_components=2)
    z_pca = pca.fit_transform(z.detach().cpu().numpy())
    labels = torch_label.cpu().numpy()
    # Calculate Silhouette score to measure cluster separation
    sil_score = silhouette_score(z_pca, labels)

    # Encourage a high silhouette score (well-separated clusters)
    pca_loss = -sil_score  # Negative Silhouette score to be minimized

    return lambda_pca * pca_loss


class FedCiR(FedAvg):
    """Configurable FedCiRs strategy implementation."""

    # pylint: disable=too-many-arguments,too-many-instance-attributes, line-too-long
    def __init__(
        self,
        *,
        fraction_fit: float = 1.0,
        fraction_evaluate: float = 1.0,
        min_fit_clients: int = 2,
        min_evaluate_clients: int = 2,
        min_available_clients: int = 2,
        evaluate_fn: Optional[
            Callable[
                [int, NDArrays, Dict[str, Scalar]],
                Optional[Tuple[float, Dict[str, Scalar]]],
            ]
        ] = None,
        on_fit_config_fn: Optional[Callable[[int], Dict[str, Scalar]]] = None,
        on_evaluate_config_fn: Optional[Callable[[int], Dict[str, Scalar]]] = None,
        accept_failures: bool = True,
        initial_parameters: Optional[Parameters] = None,
        initial_generator_params: Optional[Parameters] = None,
        fit_metrics_aggregation_fn: Optional[MetricsAggregationFn] = None,
        evaluate_metrics_aggregation_fn: Optional[MetricsAggregationFn] = None,
        lr_g=1e-3,
        steps_g=10,
        gen_stats=None,
        num_classes=10,
        alignment_dataloader=None,
        device=None,
        lambda_align_g=1.0,
        prior_steps=5000,
        stats_run_file=None,
        latent_dim=16,
    ) -> None:
        """Federated Averaging strategy.

        Implementation based on https://arxiv.org/abs/1602.05629

        Parameters
        ----------
        fraction_fit : float, optional
            Fraction of clients used during training. In case `min_fit_clients`
            is larger than `fraction_fit * available_clients`, `min_fit_clients`
            will still be sampled. Defaults to 1.0.
        fraction_evaluate : float, optional
            Fraction of clients used during validation. In case `min_evaluate_clients`
            is larger than `fraction_evaluate * available_clients`,
            `min_evaluate_clients` will still be sampled. Defaults to 1.0.
        min_fit_clients : int, optional
            Minimum number of clients used during training. Defaults to 2.
        min_evaluate_clients : int, optional
            Minimum number of clients used during validation. Defaults to 2.
        min_available_clients : int, optional
            Minimum number of total clients in the system. Defaults to 2.
        evaluate_fn : Optional[Callable[[int, NDArrays, Dict[str, Scalar]], Optional[Tuple[float, Dict[str, Scalar]]]]]
            Optional function used for validation. Defaults to None.
        on_fit_config_fn : Callable[[int], Dict[str, Scalar]], optional
            Function used to configure training. Defaults to None.
        on_evaluate_config_fn : Callable[[int], Dict[str, Scalar]], optional
            Function used to configure validation. Defaults to None.
        accept_failures : bool, optional
            Whether or not accept rounds containing failures. Defaults to True.
        initial_parameters : Parameters, optional
            Initial global model parameters.
        fit_metrics_aggregation_fn : Optional[MetricsAggregationFn]
            Metrics aggregation function, optional.
        evaluate_metrics_aggregation_fn : Optional[MetricsAggregationFn]
            Metrics aggregation function, optional.
        """
        super().__init__()

        if (
            min_fit_clients > min_available_clients
            or min_evaluate_clients > min_available_clients
        ):
            log(WARNING, WARNING_MIN_AVAILABLE_CLIENTS_TOO_LOW)

        self.fraction_fit = fraction_fit
        self.fraction_evaluate = fraction_evaluate
        self.min_fit_clients = min_fit_clients
        self.min_evaluate_clients = min_evaluate_clients
        self.min_available_clients = min_available_clients
        self.evaluate_fn = evaluate_fn
        self.on_fit_config_fn = on_fit_config_fn
        self.on_evaluate_config_fn = on_evaluate_config_fn
        self.accept_failures = accept_failures
        self.initial_parameters = initial_parameters
        self.fit_metrics_aggregation_fn = fit_metrics_aggregation_fn
        self.evaluate_metrics_aggregation_fn = evaluate_metrics_aggregation_fn
        self.lr_gen = lr_g
        self.num_classes = num_classes
        self.steps_gen = steps_g
        self.gen_stats = gen_stats
        self.device = device
        self.latent_dim = latent_dim
        self.gen_model = VAE(z_dim=self.latent_dim, encoder_only=True).to(self.device)
        self.prior_steps = prior_steps
        self.alignment_loader = alignment_dataloader
        self.stats_run_file = stats_run_file
        # self.ref_mu, self.ref_logvar = self.compute_ref_stats()
        self.ref_mu, self.ref_logvar = None, None
        self.lambda_align_g = lambda_align_g
        self.initial_generator_params = self.pretrain_generator(
            initial_generator_params
        )

    def pretrain_generator(self, initial_generator_params):

        temp_local_model = VAE(z_dim=self.latent_dim).to(self.device)

        # load generator weights
        gen_params_dict = zip(
            self.gen_model.state_dict().keys(),
            parameters_to_ndarrays(initial_generator_params),
        )
        gen_state_dict = OrderedDict({k: torch.tensor(v) for k, v in gen_params_dict})
        self.gen_model.load_state_dict(gen_state_dict, strict=True)
        optimizer = torch.optim.Adam(self.gen_model.parameters(), lr=self.lr_gen)

        temp_local_model.eval()

        for ep_g in range(self.steps_gen):
            for step, (align_img, _) in enumerate(self.alignment_loader):

                optimizer.zero_grad()
                align_img = align_img.to(self.device)

                params_dict = zip(
                    temp_local_model.state_dict().keys(),
                    parameters_to_ndarrays(self.initial_parameters),
                )
                state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
                temp_local_model.load_state_dict(state_dict, strict=True)
                z_g, mu_g, logvar_g = self.gen_model(align_img)
                preds = temp_local_model.decoder(z_g)

                loss = vae_loss(
                    preds,
                    align_img,
                    mu_g,
                    logvar_g,
                    self.lambda_align_g,
                    False,
                )

                threshold = 1e-6  # Define a threshold for the negligible loss
                log(DEBUG, f"generator loss at ep {ep_g} step {step}: {loss}")

                if (
                    loss.item() > threshold
                ):  # Check if the loss is greater than the threshold
                    loss.backward(retain_graph=True)
                    optimizer.step()
                else:
                    log(
                        DEBUG,
                        f"Skipping optimization at step {step} due to negligible loss",
                    )
        #     tmp_gen_fig = visualize_plotly_latent_representation(
        #         self.gen_model,
        #         self.alignment_loader,
        #         self.device,
        #         use_PCA=False,
        #         num_class=self.num_classes,
        #     )
        # wandb.log(
        #     data={
        #         f"final_gen_loss": loss.item(),
        #         "client_round": 0,
        #         "tmp_gen_latent_space": tmp_gen_fig,
        #     },
        #     step=0,
        # )
        print("Pretraining generator")

        return ndarrays_to_parameters(
            [val.cpu().numpy() for _, val in self.gen_model.state_dict().items()]
        )

    def compute_ref_stats(self, use_PCA=True, given_labels=False):
        if given_labels:
            ref_model = infoVAE(latent_size=self.latent_dim, dis_hidden_size=4).to(
                self.device
            )
        else:
            ref_model = VAE(z_dim=self.latent_dim).to(self.device)
        opt_ref = torch.optim.Adam(ref_model.parameters(), lr=1e-3)
        for ep in range(self.prior_steps):
            for images, labels in self.alignment_loader:
                images = images.to(self.device)
                labels = labels.to(self.device)
                opt_ref.zero_grad()
                if given_labels:
                    recon_images, mu, logvar, y_pred, z = ref_model(images, labels)
                    total_loss, recon_loss, kl_loss, info_loss = info_vae_loss(
                        recon_images,
                        images,
                        mu,
                        logvar,
                        labels,
                        y_pred,
                        1,
                        10,
                    )
                else:
                    recon_images, mu, logvar = ref_model(images)
                    total_loss, recon_loss, kl_loss = vae_loss(
                        recon_images, images, mu, logvar, beta=1.0, separate=True
                    )

                total_loss.backward()
                opt_ref.step()
            if ep % 100 == 0:
                if given_labels:
                    log(
                        DEBUG,
                        f"Epoch {ep}, Loss {total_loss.item()}, Recon Loss {recon_loss}, KL Loss {kl_loss}, Info Loss {info_loss}",
                    )
                else:
                    log(
                        DEBUG,
                        f"Epoch {ep}, Loss {total_loss.item()}, Recon Loss {recon_loss}, KL Loss {kl_loss}",
                    )

                log(DEBUG, f"--------------------------------------------------")
        ref_model.eval()
        test_latents = []
        test_labels = []
        with torch.no_grad():
            for images, labels in self.alignment_loader:
                images = images.to(self.device)
                labels = labels.to(self.device)
                if given_labels:
                    _, ref_mu, ref_logvar, _, _ = ref_model(images, labels)
                else:
                    _, ref_mu, ref_logvar = ref_model(images)
                test_latents.append(ref_mu.cpu().numpy())
                test_labels.append(labels.cpu().numpy())
            test_latents = np.concatenate(test_latents, axis=0)
            test_labels = np.concatenate(test_labels, axis=0)
            with open(self.stats_run_file, "wb") as f:
                np.save(f, test_latents)
            if use_PCA:
                # Apply PCA using PyTorch
                # cov_matrix = torch.tensor(np.cov(test_latents.T), dtype=torch.float32)
                # _, _, V = torch.svd_lowrank(cov_matrix, q=2)

                # # Project data onto the first two principal components
                # reduced_latents = torch.mm(
                #     torch.tensor(test_latents, dtype=torch.float32), V
                # )

                # # Convert to numpy array
                # test_latents = reduced_latents.numpy()
                from sklearn.decomposition import PCA

                pca = PCA(n_components=2)
                reduced_latents = pca.fit_transform(test_latents)
            # Create traces for each class
            traces = []
            for label in np.unique(test_labels):
                indices = np.where(test_labels == label)
                trace = go.Scatter(
                    x=reduced_latents[indices, 0].flatten(),
                    y=reduced_latents[indices, 1].flatten(),
                    mode="markers",
                    name=str(label),
                    marker=dict(size=8),
                )
                traces.append(trace)

            # Create layout
            layout = go.Layout(
                title="Latent Space Visualization of Test Set with Class Highlight",
                xaxis=dict(title="Latent Dimension 1"),
                yaxis=dict(title="Latent Dimension 2"),
                legend=dict(title="Class"),
            )

            # Create figure
            fig = go.Figure(data=traces, layout=layout)
            wandb.log({"latent_space": fig})
            self.gen_stats = (ref_mu, ref_logvar)
        return ref_mu, ref_logvar

    def __repr__(self) -> str:
        """Compute a string representation of the strategy."""
        rep = f"FedCiRs(accept_failures={self.accept_failures})"
        return rep

    def evaluate(
        self, server_round: int, parameters: Parameters
    ) -> Optional[Tuple[float, Dict[str, Scalar]]]:
        """Evaluate model parameters using an evaluation function."""
        if self.evaluate_fn is None:
            # No evaluation function provided
            return None
        parameters_ndarrays = parameters_to_ndarrays(parameters)
        eval_res = self.evaluate_fn(server_round, parameters_ndarrays, {})
        if eval_res is None:
            return None
        loss, metrics = eval_res
        return loss, metrics

    def configure_fit(
        self, server_round: int, parameters: Parameters, client_manager: ClientManager
    ) -> List[Tuple[ClientProxy, FitIns]]:
        """Configure the next round of training."""

        if self.on_fit_config_fn is not None:
            # Custom fit config function provided
            config = self.on_fit_config_fn(server_round)
            # config["gen_params"] = self.gen_stats
            config["gen_params"] = self.initial_generator_params
        fit_ins = FitIns(parameters, config)

        # Sample clients
        sample_size, min_num_clients = self.num_fit_clients(
            client_manager.num_available()
        )
        clients = client_manager.sample(
            num_clients=sample_size, min_num_clients=min_num_clients
        )

        # Return client/config pairs
        return [(client, fit_ins) for client in clients]

    def configure_evaluate(
        self, server_round: int, parameters: Parameters, client_manager: ClientManager
    ) -> List[Tuple[ClientProxy, EvaluateIns]]:
        """Configure the next round of evaluation."""
        # Do not configure federated evaluation if fraction eval is 0.
        if self.fraction_evaluate == 0.0:
            return []

        # Parameters and config
        config = {}
        if self.on_evaluate_config_fn is not None:
            # Custom evaluation config function provided
            config = self.on_evaluate_config_fn(server_round)

        evaluate_ins = EvaluateIns(parameters, config)

        # Sample clients
        sample_size, min_num_clients = self.num_evaluation_clients(
            client_manager.num_available()
        )
        clients = client_manager.sample(
            num_clients=sample_size, min_num_clients=min_num_clients
        )

        # Return client/config pairs
        return [(client, evaluate_ins) for client in clients]

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        """Aggregate fit results using weighted average."""
        if not results:
            return None, {}
        # Do not aggregate if there are failures and failures are not accepted
        if not self.accept_failures and failures:
            return None, {}

        def vae_loss_connect(recon_img, img, mu, logvar, mu_ref, logvar_ref, beta):
            # Reconstruction loss using binary cross-entropy
            condition = (recon_img >= 0.0) & (recon_img <= 1.0)
            # assert torch.all(condition), "Values should be between 0 and 1"
            if not torch.all(condition):
                ValueError("Values should be between 0 and 1")
                recon_img = torch.clamp(recon_img, 0.0, 1.0)
            bce_loss_per_pixel = F.binary_cross_entropy(
                recon_img, img.view(-1, img.shape[2] * img.shape[3]), reduction="none"
            )
            # Sum along dimension 1 (sum over pixels for each image)
            bce_loss_sum_per_image = torch.sum(
                bce_loss_per_pixel, dim=1
            )  # Shape: (batch_size,)

            # Take the mean along dimension 0 (mean over images in the batch)
            recon_loss = torch.mean(bce_loss_sum_per_image)  # Shape: scalar

            # KL divergence loss
            loss_align = 0.5 * (logvar_ref - logvar - 1) + (
                logvar.exp() + (mu - mu_ref).pow(2)
            ) / (2 * logvar_ref.exp())
            loss_align_reduced = torch.mean(loss_align.sum(dim=1))
            # Total VAE loss
            total_loss = beta * loss_align_reduced + recon_loss

            return total_loss

        # Convert results
        weights_results = [
            (parameters_to_ndarrays(fit_res.parameters), fit_res.num_examples)
            for _, fit_res in results
        ]
        temp_local_models = [
            VAE(z_dim=self.latent_dim).to(self.device)
            for _ in range(len(weights_results))
        ]
        # load generator weights
        gen_params_dict = zip(
            self.gen_model.state_dict().keys(),
            parameters_to_ndarrays(self.initial_generator_params),
        )
        gen_state_dict = OrderedDict({k: torch.tensor(v) for k, v in gen_params_dict})
        self.gen_model.load_state_dict(gen_state_dict, strict=True)
        optimizer = torch.optim.Adam(self.gen_model.parameters(), lr=self.lr_gen)

        for temp_local_model in temp_local_models:
            temp_local_model.eval()

        for ep_g in range(self.steps_gen):
            for step, (align_img, _) in enumerate(self.alignment_loader):
                loss = []
                # mu_s = []
                # logvar_s = []
                optimizer.zero_grad()
                align_img = align_img.to(self.device)

                for idx, (weights, _) in enumerate(weights_results):
                    params_dict = zip(
                        temp_local_models[idx].state_dict().keys(), weights
                    )
                    state_dict = OrderedDict(
                        {k: torch.tensor(v) for k, v in params_dict}
                    )
                    temp_local_models[idx].load_state_dict(state_dict, strict=True)
                    z_g, mu_g, logvar_g = self.gen_model(align_img)
                    # _, mu, logvar = temp_local_models[idx](align_img)
                    # mu_s.append(mu)
                    # logvar_s.append(logvar)

                    loss_ = vae_loss(
                        temp_local_models[idx].decoder(z_g),
                        align_img,
                        mu_g,
                        logvar_g,
                        self.lambda_align_g,
                        False,
                    )
                    loss.append(loss_)
                loss = torch.stack(loss).mean(dim=0)

                # loss = vae_loss_connect(
                #     torch.stack(preds).mean(dim=0),
                #     align_img,
                #     mu_g,
                #     logvar_g,
                #     self.ref_mu,
                #     self.ref_logvar,
                #     self.lambda_align_g,
                # )
                threshold = 1e-6  # Define a threshold for the negligible loss
                log(DEBUG, f"generator loss at ep {ep_g} step {step}: {loss}")

                if (
                    loss.item() > threshold
                ):  # Check if the loss is greater than the threshold
                    loss.backward(retain_graph=True)
                    optimizer.step()
                else:
                    log(
                        DEBUG,
                        f"Skipping optimization at step {step} due to negligible loss",
                    )
            tmp_gen_fig = visualize_plotly_latent_representation(
                self.gen_model,
                self.alignment_loader,
                self.device,
                use_PCA=False,
                num_class=self.num_classes,
            )
        wandb.log(
            data={
                f"final_gen_loss": loss.item(),
                "client_round": server_round,
                "tmp_gen_latent_space": tmp_gen_fig,
            },
            step=server_round,
        )
        # self.gen_stats = ndarrays_to_parameters(
        #     [val.cpu().numpy() for _, val in self.gen_model.state_dict().items()]
        # )
        self.initial_generator_params = ndarrays_to_parameters(
            [val.cpu().numpy() for _, val in self.gen_model.state_dict().items()]
        )
        parameters_aggregated = ndarrays_to_parameters(aggregate(weights_results))

        # Aggregate custom metrics if aggregation fn was provided
        metrics_aggregated = {}
        if self.fit_metrics_aggregation_fn:
            fit_metrics = [(res.num_examples, res.metrics) for _, res in results]
            metrics_aggregated = self.fit_metrics_aggregation_fn(fit_metrics)
        elif server_round == 1:  # Only log this warning once
            log(WARNING, "No fit_metrics_aggregation_fn provided")

        fit_metrics = [(res.num_examples, res.metrics) for _, res in results]

        # for fit_metric in fit_metrics:
        #     data = {
        #         f"train_num_examples_{fit_metric[1]['cid']}": fit_metric[0],
        #         f"train_vae_loss_term_{fit_metric[1]['cid']}": fit_metric[1][
        #             "vae_loss_term"
        #         ],
        #         f"train_reg_term_{fit_metric[1]['cid']}": fit_metric[1]["reg_term"],
        #         f"train_align_term_{fit_metric[1]['cid']}": fit_metric[1]["align_term"],
        #         f"train_total_loss_{fit_metric[1]['cid']}": fit_metric[1][
        #             "train_total_loss"
        #         ],
        #         f"train_true_image_{fit_metric[1]['cid']}": wandb.Image(
        #             fit_metric[1]["true_image"]
        #         ),
        #         f"train_gen_image_{fit_metric[1]['cid']}": wandb.Image(
        #             fit_metric[1]["gen_image"]
        #         ),
        #         f"train_latent_rep_{fit_metric[1]['cid']}": fit_metric[1]["latent_rep"],
        #         "client_round": fit_metric[1]["client_round"],
        #     }

        #     wandb.log(data=data, step=server_round)
        #     plt.close("all")
        for fit_metric in fit_metrics:
            data = {}
            for key, value in fit_metric[1].items():
                if key in ["cid", "gen_image", "true_image"]:
                    continue
                data = {
                    f"train_{key}_{fit_metric[1]['cid']}": value,
                }

            data[f"train_num_examples_{fit_metric[1]['cid']}"] = fit_metric[0]
            data[f"train_true_image_{fit_metric[1]['cid']}"] = wandb.Image(
                fit_metric[1]["true_image"]
            )
            data[f"train_gen_image_{fit_metric[1]['cid']}"] = wandb.Image(
                fit_metric[1]["gen_image"]
            )

            wandb.log(data=data, step=server_round)
        return parameters_aggregated, metrics_aggregated

    def aggregate_evaluate(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, EvaluateRes]],
        failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
    ) -> Tuple[Optional[float], Dict[str, Scalar]]:
        """Aggregate evaluation losses using weighted average."""
        if not results:
            return None, {}
        # Do not aggregate if there are failures and failures are not accepted
        if not self.accept_failures and failures:
            return None, {}

        # Aggregate loss
        loss_aggregated = weighted_loss_avg(
            [
                (evaluate_res.num_examples, evaluate_res.loss)
                for _, evaluate_res in results
            ]
        )

        # Aggregate custom metrics if aggregation fn was provided
        metrics_aggregated = {}
        if self.evaluate_metrics_aggregation_fn:
            eval_metrics = [(res.num_examples, res.metrics) for _, res in results]
            metrics_aggregated = self.evaluate_metrics_aggregation_fn(eval_metrics)
        elif server_round == 1:  # Only log this warning once
            log(WARNING, "No evaluate_metrics_aggregation_fn provided")
        eval_metrics = [(res.num_examples, res.metrics) for _, res in results]

        for eval_metric in eval_metrics:
            data = {}
            for key, value in eval_metric[1].items():
                if key in ["cid"]:
                    continue
                data = {
                    f"eval_{key}_{eval_metric[1]['cid']}": value,
                }
            data[f"eval_num_examples_{eval_metric[1]['cid']}"] = eval_metric[0]
            # data = {
            #     f"eval_num_examples_{eval_metric[1]['cid']}": eval_metric[0],
            #     # f"eval_accuracy_{eval_metric[1]['cid']}": eval_metric[1]["accuracy"],
            #     f"eval_local_val_loss_{eval_metric[1]['cid']}": eval_metric[1][
            #         "local_val_loss"
            #     ],
            #     "client_round": server_round,
            # }

            wandb.log(data=data, step=server_round)
        data_agg = {
            f"eval_{key}_aggregated": value for key, value in metrics_aggregated.items()
        }
        wandb.log(
            data={
                "eval_loss_aggregated": loss_aggregated,
                **data_agg,
            },
            step=server_round,
        )

        return loss_aggregated, metrics_aggregated
