from __future__ import annotations

from typing import Any

import numpy as np

from .data_gen import generate_synthetic_weekly_demand
from .features import prepare_supervised_dataset
from .model import (
    evaluate_forecast,
    fit_linear_regression,
    predict_linear_regression,
    train_test_split_time_series,
)


def forecast_next_period(
    forecast_month: str,
    n_weeks: int = 156,
    base_demand: float = 100_000,
    trend_per_week: float = 50,
    seasonal_amplitude: float = 12_000,
    noise_std: float = 6_000,
    seed: int = 7,
) -> dict[str, Any]:
    """
    Generate a dynamic one-period-ahead demand forecast.

    This is Forecast Agent v1:
    - generate historical weekly demand
    - create lag and seasonal features
    - train a linear regression model
    - predict the next demand value
    - estimate forecast uncertainty using RMSE
    """
    raw_df = generate_synthetic_weekly_demand(
        n_weeks=n_weeks,
        base_demand=base_demand,
        trend_per_week=trend_per_week,
        seasonal_amplitude=seasonal_amplitude,
        noise_std=noise_std,
        seed=seed,
    )

    supervised_df = prepare_supervised_dataset(raw_df)

    feature_cols = [
        "demand",
        "demand_lag_1",
        "demand_lag_2",
        "demand_lag_3",
        "demand_lag_4",
        "sin_week",
        "cos_week",
    ]

    train, test = train_test_split_time_series(supervised_df, test_size=0.2)

    X_train = train[feature_cols].to_numpy()
    y_train = train["target"].to_numpy()

    X_test = test[feature_cols].to_numpy()
    y_test = test["target"].to_numpy()

    beta = fit_linear_regression(X_train, y_train)
    y_pred = predict_linear_regression(X_test, beta)

    metrics = evaluate_forecast(y_test, y_pred)

    latest_features = supervised_df[feature_cols].iloc[[-1]].to_numpy()
    next_forecast = float(predict_linear_regression(latest_features, beta)[0])

    rmse = float(metrics["RMSE"])

    forecast_low = next_forecast - 1.65 * rmse
    forecast_high = next_forecast + 1.65 * rmse

    return {
        "forecast_month": forecast_month,
        "expected_demand": round(next_forecast, 2),
        "forecast_low": round(max(forecast_low, 0), 2),
        "forecast_high": round(forecast_high, 2),
        "forecast_std_dev": round(rmse, 2),
        "confidence": 0.90,
        "model_type": "linear_regression",
        "training_weeks": n_weeks,
        "mae": round(float(metrics["MAE"]), 2),
        "rmse": round(rmse, 2),
        "bias": round(float(metrics["Bias"]), 2),
    }