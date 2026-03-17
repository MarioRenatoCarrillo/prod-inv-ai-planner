from prodinv.policies import base_stock_policy


def test_base_stock_policy_produces_when_inventory_below_target():
    q = base_stock_policy(x_t=80.0, S=120.0)
    assert q == 40.0


def test_base_stock_policy_produces_zero_when_inventory_above_target():
    q = base_stock_policy(x_t=140.0, S=120.0)
    assert q == 0.0


def test_base_stock_policy_recovers_backlog():
    q = base_stock_policy(x_t=-15.0, S=120.0)
    assert q == 135.0