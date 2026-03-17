import numpy as np

from prodinv.config import ModelParams
from prodinv.demand import sample_demand


def test_sample_demand_returns_correct_length():
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

    rng = np.random.default_rng(7)
    demand = sample_demand(rng, mp, size=12)

    assert len(demand) == 12


def test_sample_demand_is_nonnegative_when_truncated():
    mp = ModelParams(
        mu=10.0,
        sigma=50.0,
        truncate_demand_at_zero=True,
        C1=2.0,
        C2=0.02,
        K1=0.5,
        K2=0.01,
        B1=4.0,
        B2=0.02,
    )

    rng = np.random.default_rng(7)
    demand = sample_demand(rng, mp, size=100)

    assert np.all(demand >= 0.0)