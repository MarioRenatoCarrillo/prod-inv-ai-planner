"""This file encodes the economic incentives of the system.
The company wants to avoid:
Production spikes
Because the marginal production cost increases with volume we can see this 
as I take the first derivative with repect to q the cost increase """
from __future__ import annotations

from .config import ModelParams


def production_cost(q: float, mp: ModelParams) -> float:
    """
    Production cost function.

    C(q) = C1*q + 0.5*C2*q^2

    q : production quantity
    mp : model parameters
    """

    return mp.C1 * q + 0.5 * mp.C2 * q**2


def holding_cost(x: float, mp: ModelParams) -> float:
    """
    Holding cost applies only when inventory is positive. Also, Holding cost grows with inventory
    Large inventory means: warehouse congestion, spoilage, capital tied up.
    k(x+) = K1*x+ + 0.5*K2*(x+)^2
    """

    x_pos = max(x, 0.0)

    return mp.K1 * x_pos + 0.5 * mp.K2 * x_pos**2


def backorder_cost(x: float, mp: ModelParams) -> float:
    """
    Backorder cost applies only when inventory is negative.

    b(x-) = B1*x- + 0.5*B2*(x-)^2
    The quadratic term means:

    small backlog = manageable
    large backlog = crisis
    """

    x_neg = max(-x, 0.0)

    return mp.B1 * x_neg + 0.5 * mp.B2 * x_neg**2