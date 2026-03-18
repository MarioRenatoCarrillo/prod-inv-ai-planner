from __future__ import annotations

import numpy as np
import pandas as pd


def train_test_split_time_series(
    df: pd.DataFrame,
    test_size: float = 0.2,
):
    """
    Split dataset into train/test using time ordering.
    """
    n = len(df)
    split_idx = int(n * (1 - test_size))

    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()

    return train, test


def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Fit linear regression using normal equation.
    """
    # Add intercept
    X = np.c_[np.ones(len(X)), X]

    # Normal equation: beta = (X^T X)^-1 X^T y
    beta = np.linalg.inv(X.T @ X) @ X.T @ y

    return beta


def predict_linear_regression(X: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    Make predictions using linear regression coefficients.
    """
    X = np.c_[np.ones(len(X)), X]
    return X @ beta


def evaluate_forecast(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Evaluate forecast performance.
    """
    errors = y_true - y_pred

    return {
        "MAE": np.mean(np.abs(errors)),
        "RMSE": np.sqrt(np.mean(errors**2)),
        "Bias": np.mean(errors),
    }