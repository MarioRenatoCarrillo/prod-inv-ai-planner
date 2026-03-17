from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ModelParams, SimParams
from .kpi import compute_kpis
from .simulate import run_simulation


def search_best_S(
    mp: ModelParams,
    sp: SimParams,
    S_grid: np.ndarray,
) -> pd.DataFrame:
    """
    Evaluate multiple candidate base-stock levels and return
    a sorted DataFrame of results, including both cost and KPI metrics.
    """
    rows: list[dict[str, float]] = []

    for S in S_grid:
        avg_total_cost, breakdown, trajectory, path_summary = run_simulation(
            mp,
            sp,
            S=float(S),
        )

        kpis = compute_kpis(path_summary)

        rows.append(
            {
                "S": float(S),
                "avg_total_cost": avg_total_cost,
                "production_cost": breakdown["production_cost"],
                "holding_cost": breakdown["holding_cost"],
                "backorder_cost": breakdown["backorder_cost"],
                "avg_inventory": kpis["avg_inventory"],
                "avg_production": kpis["avg_production"],
                "production_volatility": kpis["production_volatility"],
                "avg_demand": kpis["avg_demand"],
                "stockout_probability": kpis["stockout_probability"],
                "avg_stockout_rate": kpis["avg_stockout_rate"],
                "fill_rate": kpis["fill_rate"],
                "cost_mean": kpis["cost_mean"],
                "cost_std": kpis["cost_std"],
            }
        )

    results = pd.DataFrame(rows)
    results = results.sort_values("avg_total_cost", ascending=True).reset_index(drop=True)

    return results