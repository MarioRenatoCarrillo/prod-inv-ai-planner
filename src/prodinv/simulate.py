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
) -> tuple[float, dict[str, float], pd.DataFrame]:
    """
    Simulate a base-stock policy over many Monte Carlo demand paths.

    Parameters
    ----------
    mp : ModelParams
        Economic and demand parameters.
    sp : SimParams
        Simulation settings.
    S : float
        Base-stock level.

    Returns
    -------
    avg_total_cost : float
        Average total cost per period across all paths.
    breakdown : dict[str, float]
        Average cost breakdown per period.
    trajectory : pd.DataFrame
        Average inventory / production / demand trajectory by period.
    """
    ###Random number generator #### The randomnes in critical for 
    # debugging, comparing policies 
    # and publishing reproducible results.

    rng = np.random.default_rng(sp.seed)
   ### Accumulators these keep track of three economic drivers
    total_prod_cost = 0.0
    total_hold_cost = 0.0
    total_back_cost = 0.0



    ### Trajectory tracking  these produce arrays
    #  that help us to compute average trajectories across many simulations:
    ### average inventory, average production, average demand and it is
    ### useful for chart and Power BI

    x_sum = np.zeros(sp.T + 1)
    q_sum = np.zeros(sp.T)
    d_sum = np.zeros(sp.T)


    ### Monte Carlo loop: The n_paths simulate one demand path then another and so on

    for _ in range(sp.n_paths):
        x = float(sp.x0)
        x_sum[0] += x

        demands = sample_demand(rng, mp, size=sp.T)

    ### for period loop

        for t in range(sp.T):
            d_t = float(demands[t])

            # production decision: This uses the current inventory to choose production.

            q_t = base_stock_policy(x, S)

            # Costs based on the starting inventory x_t and chosen production q_t
            total_prod_cost += production_cost(q_t, mp)
            total_hold_cost += holding_cost(x, mp)
            total_back_cost += backorder_cost(x, mp)

            # Inventory update
            x = x + q_t - d_t

            # Store averages for reporting
            q_sum[t] += q_t
            d_sum[t] += d_t
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
            "avg_x_end": x_sum[1:] / sp.n_paths,
        }
    )

    return avg_total_cost, breakdown, trajectory