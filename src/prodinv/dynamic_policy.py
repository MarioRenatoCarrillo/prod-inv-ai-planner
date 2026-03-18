from __future__ import annotations

import numpy as np


def compute_safety_stock(rmse: float, z: float = 1.65) -> float:
    """
    Compute safety stock using forecast uncertainty.
    z = service level (1.65 ≈ 95%)
    """
    return z * rmse


def compute_dynamic_S(
    forecast: np.ndarray,
    rmse: float,
    z: float = 1.65,
) -> np.ndarray:
    """
    Compute dynamic base-stock level S_t.
    """
    safety_stock = compute_safety_stock(rmse, z)
    return forecast + safety_stock