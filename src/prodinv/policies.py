from __future__ import annotations


def base_stock_policy(x_t: float, S: float) -> float:
    """
    Base-stock production policy.

    Parameters
    ----------
    x_t : float
        Inventory level at the start of period t.
        Can be negative if backlog exists.
    S : float
        Target inventory level (base-stock level).

    Returns
    -------
    float
        Production quantity q_t.
    """
    return max(0.0, S - x_t) # This is the decision rule 

    ###note In this first model, production is constrained to: qt>or equal to 0