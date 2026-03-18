from __future__ import annotations

import numpy as np
import pandas as pd


def create_lag_features(
    df: pd.DataFrame,
    lags: list[int] = [1, 2, 3, 4],
) -> pd.DataFrame:
    """
    Create lag features for demand forecasting.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain 'demand' column.
    lags : list[int]
        Number of lag periods to include.

    Returns
    -------
    pd.DataFrame
        DataFrame with lag features added.
    """
    df = df.copy()

    for lag in lags:
        df[f"demand_lag_{lag}"] = df["demand"].shift(lag)

    return df


def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based seasonal features.
    """
    df = df.copy()

    # Week-of-year style feature on a 52-week cycle
    df["week_of_year"] = df["week"] % 52

    # Cyclical encoding for seasonality
    df["sin_week"] = np.sin(2 * np.pi * df["week_of_year"] / 52)
    df["cos_week"] = np.cos(2 * np.pi * df["week_of_year"] / 52)

    return df


def prepare_supervised_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature engineering pipeline for one-step-ahead demand forecasting.

    Returns a supervised learning dataset where:
    - features are based on current/past information
    - target is next week's demand
    """
    df = create_lag_features(df)
    df = create_time_features(df)

    # Predict next week's demand
    df["target"] = df["demand"].shift(-1)

    # Drop rows with NaNs introduced by lagging/target shifting
    df = df.dropna().reset_index(drop=True)

    return df