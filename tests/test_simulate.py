from prodinv.config import ModelParams, SimParams
from prodinv.simulate import run_simulation


def test_run_simulation_returns_expected_outputs():
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

    avg_total_cost, breakdown, trajectory, path_summary = run_simulation(mp, sp, S=110.0)

    assert avg_total_cost > 0.0

    assert isinstance(breakdown, dict)
    assert "production_cost" in breakdown
    assert "holding_cost" in breakdown
    assert "backorder_cost" in breakdown

    assert len(trajectory) == sp.T
    assert "avg_x_start" in trajectory.columns
    assert "avg_q" in trajectory.columns
    assert "avg_demand" in trajectory.columns
    assert "avg_x_end" in trajectory.columns

    assert len(path_summary) == sp.n_paths
    assert "total_cost" in path_summary.columns
    assert "avg_inventory" in path_summary.columns
    assert "stockout_rate" in path_summary.columns
    assert "fill_rate" in path_summary.columns