from __future__ import annotations

import numpy as np

from .config import ModelParams


def sample_demand(
    rng: np.random.Generator,
    mp: ModelParams,
    size: int,
) -> np.ndarray:
    """
    Generate stochastic demand.

    Demand model:
        D_t = mu + epsilon_t
        epsilon_t ~ N(0, sigma^2)

    Parameters
    ----------
    rng : np.random.Generator
        Random number generator for reproducibility.
    mp : ModelParams
        Model parameters containing mu, sigma, and truncation setting.
    size : int
        Number of demand observations to generate.

    Returns
    -------
    np.ndarray
        Array of simulated demand values.
    """
    demand = mp.mu + rng.normal(loc=0.0, scale=mp.sigma, size=size)

    if mp.truncate_demand_at_zero:
        demand = np.maximum(demand, 0.0)

    return demand