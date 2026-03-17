from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_synthetic_weekly_demand(
    n_weeks: int = 156,
    base_demand: float = 100.0,
    trend_per_week: float = 0.05,
    seasonal_amplitude: float = 12.0,
    noise_std: float = 8.0,
    shock_probability: float = 0.05,
    shock_magnitude_std: float = 20.0,
    seed: int = 7,
) -> pd.DataFrame:
    """
    Generate synthetic weekly soybean meal demand data.

    Parameters
    ----------
    n_weeks : int
        Number of weekly observations.
    base_demand : float
        Baseline average demand level.
    trend_per_week : float
        Linear demand trend added each week.
    seasonal_amplitude : float
        Amplitude of annual seasonality.
    noise_std : float
        Standard deviation of random weekly noise.
    shock_probability : float
        Probability of an additional demand shock in a given week.
    shock_magnitude_std : float
        Standard deviation of random shock size.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Synthetic weekly demand dataset.
    """
    rng = np.random.default_rng(seed)

    week = np.arange(n_weeks)

    # Linear trend
    trend = base_demand + trend_per_week * week

    # Annual seasonality (52-week cycle)
    seasonality = seasonal_amplitude * np.sin(2 * np.pi * week / 52)

    # Random week-to-week noise
    noise = rng.normal(loc=0.0, scale=noise_std, size=n_weeks)

    # Occasional shocks
    shock_flags = rng.binomial(n=1, p=shock_probability, size=n_weeks)
    shock_values = shock_flags * rng.normal(loc=0.0, scale=shock_magnitude_std, size=n_weeks)

    demand = trend + seasonality + noise + shock_values
    demand = np.maximum(demand, 0.0)

    df = pd.DataFrame(
        {
            "week": week,
            "trend": trend,
            "seasonality": seasonality,
            "noise": noise,
            "shock": shock_values,
            "demand": demand,
        }
    )

    return df


def save_synthetic_demand_csv(
    df: pd.DataFrame,
    output_path: str | Path = "reports/synthetic_weekly_demand.csv",
) -> Path:
    """
    Save synthetic demand data to CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path