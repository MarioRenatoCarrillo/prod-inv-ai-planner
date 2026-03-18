from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ModelParams, SimParams
from .demand import sample_demand
from .econ import production_cost, holding_cost, backorder_cost
from .policies import base_stock_policy


def run_dynamic_simulation(
    mp: ModelParams,
    sp: SimParams,
    S_series: np.ndarray,
) -> tuple[float, dict[str, float], pd.DataFrame]:
    """
    Simulate a dynamic base-stock policy where S changes by period.

    Parameters
    ----------
    mp : ModelParams
        Economic and demand parameters.
    sp : SimParams
        Simulation settings.
    S_series : np.ndarray
        Time-varying base-stock targets, one per period.

    Returns
    -------
    avg_total_cost : float
        Average total cost per period across all paths.
    breakdown : dict[str, float]
        Average cost breakdown per period.
    trajectory : pd.DataFrame
        Average inventory / production / demand trajectory.
    """
    if len(S_series) != sp.T:
        raise ValueError("S_series length must match simulation horizon T")

    rng = np.random.default_rng(sp.seed)

    total_prod_cost = 0.0
    total_hold_cost = 0.0
    total_back_cost = 0.0

    x_sum = np.zeros(sp.T + 1)
    q_sum = np.zeros(sp.T)
    d_sum = np.zeros(sp.T)
    s_sum = np.zeros(sp.T)

    for _ in range(sp.n_paths):
        x = float(sp.x0)
        x_sum[0] += x

        demands = sample_demand(rng, mp, size=sp.T)

        for t in range(sp.T):
            d_t = float(demands[t])
            S_t = float(S_series[t]) # The key idea with the simulation is in this equation --the model uses 
                                     # a different inventory target each week.
                                     # In other words: The policy can react to:
                                     #      forecasted demand changes
                                     #      seasonality
                                     #      uncertainty buffer
                                     
            q_t = base_stock_policy(x, S_t)

            total_prod_cost += production_cost(q_t, mp)
            total_hold_cost += holding_cost(x, mp)
            total_back_cost += backorder_cost(x, mp)

            x = x + q_t - d_t

            q_sum[t] += q_t
            d_sum[t] += d_t
            s_sum[t] += S_t
            x_sum[t + 1] += x

    denom = sp.n_paths * sp.T

    breakdown = {
        "production_cost": total_prod_cost / denom,
        "holding_cost": total_hold_cost / denom,
        "backorder_cost": total_back_cost / denom,
    }

    avg_total_cost = sum(breakdown.values())

    trajectory = pd.DataFrame(
        {
            "t": np.arange(sp.T),
            "avg_x_start": x_sum[:-1] / sp.n_paths,
            "avg_q": q_sum / sp.n_paths,
            "avg_demand": d_sum / sp.n_paths,
            "avg_S": s_sum / sp.n_paths,
            "avg_x_end": x_sum[1:] / sp.n_paths,
        }
    )

    return avg_total_cost, breakdown, trajectory