from __future__ import annotations

import numpy as np
from fastapi import FastAPI

from prodinv.api.schemas import (
    DynamicPolicyRequest,
    ExplainRequest,
    OptimizeRequest,
    SimulateRequest,
)
from prodinv.config import ModelParams, SimParams
from prodinv.data_gen import generate_synthetic_weekly_demand
from prodinv.dynamic_policy import compute_dynamic_S
from prodinv.dynamic_simulate import run_dynamic_simulation
from prodinv.features import prepare_supervised_dataset
from prodinv.kpi import compute_kpis
from prodinv.llm.explain import explain_inventory_results
from prodinv.model import (
    evaluate_forecast,
    fit_linear_regression,
    predict_linear_regression,
    train_test_split_time_series,
)
from prodinv.optimize import search_best_S
from prodinv.simulate import run_simulation

app = FastAPI(
    title="Production Inventory Optimization API",
    description="AI + Operations Research for Agricultural Supply Chains",
    version="0.1.0",
)


def to_model_params(req) -> ModelParams:
    return ModelParams(
        mu=req.mu,
        sigma=req.sigma,
        truncate_demand_at_zero=req.truncate_demand_at_zero,
        C1=req.C1,
        C2=req.C2,
        K1=req.K1,
        K2=req.K2,
        B1=req.B1,
        B2=req.B2,
    )


def to_sim_params(req) -> SimParams:
    return SimParams(
        T=req.T,
        n_paths=req.n_paths,
        seed=req.seed,
        x0=req.x0,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/simulate")
def simulate_endpoint(payload: SimulateRequest) -> dict:
    mp = to_model_params(payload.model)
    sp = to_sim_params(payload.sim)

    avg_total_cost, breakdown, trajectory, path_summary = run_simulation(
        mp=mp,
        sp=sp,
        S=payload.S,
    )

    kpis = compute_kpis(path_summary)

    return {
        "policy_type": "fixed_base_stock",
        "S": payload.S,
        "avg_total_cost": avg_total_cost,
        "cost_breakdown": breakdown,
        "kpis": kpis,
        "trajectory_preview": trajectory.head(10).to_dict(orient="records"),
    }


@app.post("/optimize")
def optimize_endpoint(payload: OptimizeRequest) -> dict:
    mp = to_model_params(payload.model)
    sp = to_sim_params(payload.sim)

    s_grid = np.arange(payload.s_min, payload.s_max + payload.s_step, payload.s_step)
    results = search_best_S(mp=mp, sp=sp, S_grid=s_grid)

    best = results.iloc[0].to_dict()

    return {
        "best_policy": best,
        "results": results.to_dict(orient="records"),
    }


@app.post("/dynamic-policy")
def dynamic_policy_endpoint(payload: DynamicPolicyRequest) -> dict:
    mp = to_model_params(payload.model)

    # Generate synthetic history and build forecast
    df = generate_synthetic_weekly_demand(
        n_weeks=payload.n_weeks,
        seed=payload.sim.seed,
    )
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

    S_dynamic = compute_dynamic_S(
        y_pred,
        rmse=metrics["RMSE"],
        z=payload.z,
    )

    sp_dynamic = SimParams(
        T=len(S_dynamic),
        n_paths=payload.sim.n_paths,
        seed=payload.sim.seed,
        x0=payload.sim.x0,
    )

    dyn_total_cost, dyn_breakdown, dyn_trajectory = run_dynamic_simulation(
        mp=mp,
        sp=sp_dynamic,
        S_series=S_dynamic,
    )

    fixed_S = float(np.mean(S_dynamic))
    fix_total_cost, fix_breakdown, fix_trajectory, fix_path_summary = run_simulation(
        mp=mp,
        sp=sp_dynamic,
        S=fixed_S,
    )

    return {
        "forecast_metrics": metrics,
        "z": payload.z,
        "dynamic_policy": {
            "avg_total_cost": dyn_total_cost,
            "cost_breakdown": dyn_breakdown,
            "avg_S": float(np.mean(S_dynamic)),
            "trajectory_preview": dyn_trajectory.head(10).to_dict(orient="records"),
        },
        "fixed_policy_comparison": {
            "S": fixed_S,
            "avg_total_cost": fix_total_cost,
            "cost_breakdown": fix_breakdown,
            "kpis": compute_kpis(fix_path_summary),
            "trajectory_preview": fix_trajectory.head(10).to_dict(orient="records"),
        },
    }


@app.post("/explain")
def explain_endpoint(payload: ExplainRequest) -> dict:
    try:
        explanation = explain_inventory_results(payload.payload)
        return {"explanation": explanation}
    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__,
        }