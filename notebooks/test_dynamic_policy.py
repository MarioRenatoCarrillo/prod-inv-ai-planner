import numpy as np

from prodinv.config import ModelParams, SimParams
from prodinv.data_gen import generate_synthetic_weekly_demand
from prodinv.features import prepare_supervised_dataset
from prodinv.model import (
    train_test_split_time_series,
    fit_linear_regression,
    predict_linear_regression,
    evaluate_forecast,
)
from prodinv.dynamic_policy import compute_dynamic_S
from prodinv.dynamic_simulate import run_dynamic_simulation

df = generate_synthetic_weekly_demand()
df_ml = prepare_supervised_dataset(df)

feature_cols = [
    "demand_lag_1",
    "demand_lag_2",
    "demand_lag_3",
    "demand_lag_4",
    "sin_week",
    "cos_week",
]

train, test = train_test_split_time_series(df_ml)

X_train = train[feature_cols].values
y_train = train["target"].values
X_test = test[feature_cols].values
y_test = test["target"].values

beta = fit_linear_regression(X_train, y_train)
y_pred = predict_linear_regression(X_test, beta)
metrics = evaluate_forecast(y_test, y_pred)

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

for z in [1.65, 1.80, 2.00, 2.20]:
    S_dynamic = compute_dynamic_S(y_pred, rmse=metrics["RMSE"], z=z)

    sp_dynamic = SimParams(
        T=len(S_dynamic),
        n_paths=500,
        seed=7,
        x0=0.0,
    )

    dyn_total_cost, dyn_breakdown, dyn_trajectory = run_dynamic_simulation(
        mp=mp,
        sp=sp_dynamic,
        S_series=S_dynamic,
    )

    print(f"z={z:.2f} -> cost={dyn_total_cost:.2f}")