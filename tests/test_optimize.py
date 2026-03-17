import numpy as np

from prodinv.config import ModelParams, SimParams
from prodinv.optimize import search_best_S


def test_search_best_S_returns_sorted_results():
    mp = ModelParams(
        mu=100.0,
        sigma=20.0,
        truncate_demand_at_zero=True,
        C1=2.0,
        C2=0.02,
        K1=0.5,
        K2=0.01,
        B1=4.0,
        B2=0.02,
    )

    sp = SimParams(
        T=12,
        n_paths=100,
        seed=7,
        x0=0.0,
    )

    s_grid = np.array([100.0, 110.0, 120.0])

    results = search_best_S(mp, sp, s_grid)

    assert len(results) == 3
    assert "S" in results.columns
    assert "avg_total_cost" in results.columns
    assert "production_cost" in results.columns
    assert "holding_cost" in results.columns
    assert "backorder_cost" in results.columns

    assert results["avg_total_cost"].is_monotonic_increasing
    
    assert "stockout_probability" in results.columns
    assert "avg_stockout_rate" in results.columns
    assert "fill_rate" in results.columns
    assert "avg_inventory" in results.columns