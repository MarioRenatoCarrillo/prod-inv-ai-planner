from __future__ import annotations

import pandas as pd


def compute_kpis(path_summary: pd.DataFrame) -> dict[str, float]:
    """
    Compute operational KPIs from path-level Monte Carlo results.

    Parameters
    ----------
    path_summary : pd.DataFrame
        Path-level summary metrics from simulation.

    Returns
    -------
    dict[str, float]
        Dictionary of KPI values.
    """
    return {
        "avg_inventory": float(path_summary["avg_inventory"].mean()),
        "avg_production": float(path_summary["avg_production"].mean()),
        "production_volatility": float(path_summary["avg_production"].std()),
        "avg_demand": float(path_summary["avg_demand"].mean()),
        "stockout_probability": float((path_summary["stockout_rate"] > 0).mean()),
        "avg_stockout_rate": float(path_summary["stockout_rate"].mean()),
        "fill_rate": float(path_summary["fill_rate"].mean()),
        "cost_mean": float(path_summary["total_cost"].mean()),
        "cost_std": float(path_summary["total_cost"].std()),
    }