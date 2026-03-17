from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ModelParams, SimParams
from .demand import sample_demand
from .econ import production_cost, holding_cost, backorder_cost
from .policies import base_stock_policy


def run_simulation(
    mp: ModelParams,
    sp: SimParams,
    S: float,
) -> tuple[float, dict[str, float], pd.DataFrame, pd.DataFrame]:
    """
    Simulate a base-stock policy over many Monte Carlo demand paths.

    Returns
    -------
    avg_total_cost : float
        Average total cost per period across all paths.
    breakdown : dict[str, float]
        Average cost breakdown per period.
    trajectory : pd.DataFrame
        Average inventory / production / demand trajectory by period.
    path_summary : pd.DataFrame
        Path-level summary metrics for each Monte Carlo scenario.
    """
    rng = np.random.default_rng(sp.seed)

    total_prod_cost = 0.0
    total_hold_cost = 0.0
    total_back_cost = 0.0

    x_sum = np.zeros(sp.T + 1)
    q_sum = np.zeros(sp.T)
    d_sum = np.zeros(sp.T)

    path_rows: list[dict[str, float]] = []

    for path_id in range(sp.n_paths):
        x = float(sp.x0)
        x_sum[0] += x

        demands = sample_demand(rng, mp, size=sp.T)

        path_prod_cost = 0.0
        path_hold_cost = 0.0
        path_back_cost = 0.0

        path_x_values = []
        path_q_values = []
        path_d_values = []

        immediate_fulfilled_total = 0.0
        total_demand = 0.0
        stockout_periods = 0

        for t in range(sp.T):
            d_t = float(demands[t])
            q_t = base_stock_policy(x, S)

            # Costs at start of period
            prod_c = production_cost(q_t, mp)
            hold_c = holding_cost(x, mp)
            back_c = backorder_cost(x, mp)

            path_prod_cost += prod_c
            path_hold_cost += hold_c
            path_back_cost += back_c

            total_prod_cost += prod_c
            total_hold_cost += hold_c
            total_back_cost += back_c

            # Record state for path-level KPIs
            path_x_values.append(x)
            path_q_values.append(q_t)
            path_d_values.append(d_t)

            if x < 0:
                stockout_periods += 1

            available_now = max(x, 0.0) + q_t
            fulfilled_now = min(available_now, d_t)
            immediate_fulfilled_total += fulfilled_now
            total_demand += d_t

            # Inventory update
            x = x + q_t - d_t

            # Record for average trajectory
            q_sum[t] += q_t
            d_sum[t] += d_t
            x_sum[t + 1] += x

        path_total_cost = path_prod_cost + path_hold_cost + path_back_cost

        path_rows.append(
            {
                "path_id": float(path_id),
                "total_cost": path_total_cost,
                "production_cost": path_prod_cost,
                "holding_cost": path_hold_cost,
                "backorder_cost": path_back_cost,
                "avg_inventory": float(np.mean(path_x_values)),
                "avg_production": float(np.mean(path_q_values)),
                "avg_demand": float(np.mean(path_d_values)),
                "stockout_rate": float(stockout_periods / sp.T),
                "fill_rate": float(immediate_fulfilled_total / total_demand) if total_demand > 0 else 1.0,
            }
        )

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
            "avg_x_end": x_sum[1:] / sp.n_paths,
        }
    )

    path_summary = pd.DataFrame(path_rows)

    return avg_total_cost, breakdown, trajectory, path_summary