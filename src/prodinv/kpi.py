from __future__ import annotations

import numpy as np
import pandas as pd


def compute_kpis(trajectory: pd.DataFrame) -> dict[str, float]:
    """
    Compute operational KPIs from the average simulation trajectory.

    Parameters
    ----------
    trajectory : pd.DataFrame
        DataFrame with columns:
        - avg_x_start
        - avg_q
        - avg_demand

    Returns
    -------
    dict[str, float]
        Dictionary of KPI values.
    """
    avg_inventory = trajectory["avg_x_start"].mean()

    ## The above equation This averages the starting inventory across all periods.
    ## Interpretation: Over the simulation horizon, what inventory level does the plant tend to carry?

    avg_production = trajectory["avg_q"].mean()

    #The above equation: What is the typical weekly crush output?

    production_volatility = trajectory["avg_q"].std()

    ### Interpretation:
    # How much does the production plan swing week to week?
    # Low volatility is usually good because it means smoother operations.

    avg_demand = trajectory["avg_demand"].mean()

    stockout_probability = float(np.mean(trajectory["avg_x_start"] < 0))

    ### The above equation: This measures the fraction of periods where average starting inventory is negative.
    # Interpretation: In what share of periods is the system in backlog?

    immediately_available = np.maximum(trajectory["avg_x_start"], 0.0) + trajectory["avg_q"]
    demand_served_now = np.minimum(immediately_available, trajectory["avg_demand"])
    fill_rate = float(demand_served_now.sum() / trajectory["avg_demand"].sum())
    ### the 3 above equations have the follwoing meanings:
        # start with nonnegative available inventory
        # add this week’s production
        # compare against demand
        # whatever can be served immediately counts toward fill rate
    ###This is a good first business-facing approximation.
    return {
        "avg_inventory": float(avg_inventory),
        "avg_production": float(avg_production),
        "production_volatility": float(production_volatility),
        "avg_demand": float(avg_demand),
        "stockout_probability": stockout_probability,
        "fill_rate": fill_rate,
    }