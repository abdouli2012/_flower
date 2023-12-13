import numpy as np

from typing import Callable, Dict, List, Optional, Tuple, Union
from flwr.server.strategy.fedavg import FedAvg
from flwr.server.client_manager import ClientManager
from .utils import (
    save_params, 
    save_predicted_params,
    load_all_time_series, 
    load_time_series, 
    flatten_params
)

from flwr.common import (
    FitRes,
    MetricsAggregationFn,
    NDArrays,
    Parameters,
    Scalar,
    FitIns,
)
from flwr.server.client_proxy import ClientProxy

WARNING_MIN_AVAILABLE_CLIENTS_TOO_LOW = """
Setting `min_available_clients` lower than `min_fit_clients` or
`min_evaluate_clients` can cause the server to fail when there are too few clients
connected to the server. `min_available_clients` must be set to a value larger
than or equal to the values of `min_fit_clients` and `min_evaluate_clients`.
"""

class Flanders(FedAvg):
    """
    Aggregation function based on MAR.
    """

    # pylint: disable=too-many-arguments,too-many-instance-attributes
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
        fit_metrics_aggregation_fn: Optional[MetricsAggregationFn] = None,
        evaluate_metrics_aggregation_fn: Optional[MetricsAggregationFn] = None,
        dataset_name: str = "mnist",
        attack_name: str = "not specified",
        iid: bool = True,
        warmup_rounds: int = 1,
        to_keep: int = 1,
        window: int = 0,
        maxiter: int = 100,
        sampling: str = None,
        alpha: float = 1,
        beta: float = 1,
        distance_function: Callable = None,
    ) -> None:
        """
        Parameters
        ----------
        fraction_malicious : float, otional
            Fraction of malicious clients. Defaults to 0.
        """

        super().__init__(
                fraction_fit=fraction_fit, 
                fraction_evaluate = fraction_evaluate, 
                min_fit_clients = min_fit_clients, 
                min_evaluate_clients = min_evaluate_clients, 
                min_available_clients = min_available_clients,
                evaluate_fn = evaluate_fn, 
                on_fit_config_fn = on_fit_config_fn, 
                on_evaluate_config_fn = on_evaluate_config_fn,
                accept_failures = accept_failures,
                initial_parameters = initial_parameters,
                fit_metrics_aggregation_fn = fit_metrics_aggregation_fn,
                evaluate_metrics_aggregation_fn = evaluate_metrics_aggregation_fn
            )
        self.dataset_name = dataset_name
        self.attack_name = attack_name
        self.iid = iid
        self.warmup_rounds = warmup_rounds
        self.to_keep = to_keep
        self.window = window
        self.maxiter = maxiter
        self.sampling = sampling
        self.alpha = alpha
        self.beta = beta
        self.params_indexes = None
        self.malicious_selected = False
        self.distance_function = distance_function

    def configure_fit(
        self, server_round: int, parameters: Parameters, client_manager: ClientManager
    ) -> List[Tuple[ClientProxy, FitIns]]:
        """Configure the next round of training."""
        
        # Sample clients
        sample_size, min_num_clients = self.num_fit_clients(
            client_manager.num_available()
        )
        
        # Custom FitIns object for each client
        fit_ins_list = [
            FitIns(parameters, {} if not self.on_fit_config_fn else self.on_fit_config_fn(server_round)) 
            for _ in range(sample_size)
        ]

        clients = client_manager.sample(
            num_clients=sample_size, min_num_clients=min_num_clients
        )

        # Return client/config pairs
        return [(client, fit) for client, fit in zip(clients, fit_ins_list)]
        
    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
        clients_state: Dict[int, bool],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        """
        Apply MAR forecasting to exclude malicious clients from FedAvg.

        Parameters
        ----------
        server_round : int
            Current server round.
        results : List[Tuple[ClientProxy, FitRes]]
            List of results from the clients.
        failures : List[Union[Tuple[ClientProxy, FitRes], BaseException]]
            List of failures from the clients.

        Returns
        -------
        parameters_aggregated: Optional[Parameters]
            Aggregated parameters.
        metrics_aggregated: Dict[str, Scalar]
            Aggregated metrics.
        malicious_clients_idx: List[int]
            List of malicious clients' cids (indexes).
        """
        malicious_clients_idx = []
        if server_round > 1:
            win = self.window
            if server_round < self.window:
                win = server_round
            M = load_all_time_series(dir="clients_params", window=win)
            M = np.transpose(M, (0, 2, 1))  # (clients, params, time)

            M_hat = M[:,:,-1].copy()
            pred_step = 1
            print(f"aggregate_fit - Computing MAR on M {M.shape}")
            Mr = mar(M[:,:,:-1], pred_step, maxiter=self.maxiter, alpha=self.alpha, beta=self.beta)

            print("aggregate_fit - Computing anomaly scores")
            anomaly_scores = self.distance_function(M_hat, Mr[:,:,0])
            print(f"aggregate_fit - Anomaly scores: {anomaly_scores}")

            print("aggregate_fit - Selecting good clients")
            good_clients_idx = sorted(np.argsort(anomaly_scores)[:self.to_keep])
            malicious_clients_idx = sorted(np.argsort(anomaly_scores)[self.to_keep:])
            results = np.array(results)[good_clients_idx].tolist()
            print(f"aggregate_fit - Good clients: {good_clients_idx}")

            print(f"aggregate_fit - clients_state: {clients_state}")
            for idx in good_clients_idx:
                if clients_state[str(idx)]:
                    self.malicious_selected = True
                    break
                else:
                    self.malicious_selected = False

            # Apply FedAvg for the remaining clients
            print("aggregate_fit - Applying FedAvg for the remaining clients")
            parameters_aggregated, metrics_aggregated = super().aggregate_fit(server_round, results, failures)
        else:
            # Apply FedAvg on every clients' params during the first round
            parameters_aggregated, metrics_aggregated = super().aggregate_fit(server_round, results, failures)

        return parameters_aggregated, metrics_aggregated, malicious_clients_idx

def mar(X, pred_step, alpha=1, beta=1, maxiter=100, window=0):
    '''
    Code provided by Xinyu Chen at: 
    https://towardsdatascience.com/matrix-autoregressive-model-for-multidimensional-time-series-forecasting-6a4d7dce5143
    '''
    m, n, T = X.shape
    start = 0
    if window > 0:
        start = T - window

    A = np.random.randn(m, m)
    B = np.random.randn(n, n)
    X_norm = (X-np.min(X))/np.max(X)
   
    for _ in range(maxiter):
        temp0 = B.T @ B
        temp1 = np.zeros((m, m))
        temp2 = np.zeros((m, m))
        identity_m = np.identity(m)
       
        for t in range(start, T):
            temp1 += X_norm[:, :, t] @ B @ X_norm[:, :, t - 1].T
            temp2 += X_norm[:, :, t - 1] @ temp0 @ X_norm[:, :, t - 1].T

        temp2 += (alpha * identity_m)
        A = temp1 @ np.linalg.inv(temp2)
       
        temp0 = A.T @ A
        temp1 = np.zeros((n, n))
        temp2 = np.zeros((n, n))
        identity_n = np.identity(n)
       
        for t in range(start, T):
            temp1 += X_norm[:, :, t].T @ A @ X_norm[:, :, t - 1]
            temp2 += X_norm[:, :, t - 1].T @ temp0 @ X_norm[:, :, t - 1]

        temp2 += (beta * identity_n)
        B = temp1 @ np.linalg.inv(temp2)
   
    tensor = np.append(X, np.zeros((m, n, pred_step)), axis = 2)
    for s in range(pred_step):
        tensor[:, :, T + s] = A @ tensor[:, :, T + s - 1] @ B.T
    return tensor[:, :, - pred_step :]
