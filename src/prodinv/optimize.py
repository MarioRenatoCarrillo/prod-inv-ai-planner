from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ModelParams, SimParams
from .simulate import run_simulation


def search_best_S(
    mp: ModelParams,
    sp: SimParams,
    S_grid: np.ndarray,
) -> pd.DataFrame:
    """
    Evaluate multiple candidate base-stock levels and return
    a sorted DataFrame of results.

    Parameters
    ----------
    mp : ModelParams
        Economic and demand parameters.
    sp : SimParams
        Simulation settings.
    S_grid : np.ndarray
        Candidate values of S to evaluate.

    Returns
    -------
    pd.DataFrame
        Results sorted by average total cost ascending.
    """
    rows: list[dict[str, float]] = []

    for S in S_grid:
        avg_total_cost, breakdown, trajectory, path_summary = run_simulation(
            mp,
            sp,
            S=float(S),
        )

        rows.append(
            {
                "S": float(S),
                "avg_total_cost": avg_total_cost,
                "production_cost": breakdown["production_cost"],
                "holding_cost": breakdown["holding_cost"],
                "backorder_cost": breakdown["backorder_cost"],
            }
        )

    results = pd.DataFrame(rows)
    results = results.sort_values("avg_total_cost", ascending=True).reset_index(drop=True)

    return results