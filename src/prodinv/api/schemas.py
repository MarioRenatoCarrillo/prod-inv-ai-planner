from __future__ import annotations

from pydantic import BaseModel, Field


class ModelParamsRequest(BaseModel):
    mu: float = 100.0
    sigma: float = 20.0
    truncate_demand_at_zero: bool = True
    C1: float = 2.0
    C2: float = 0.02
    K1: float = 0.5
    K2: float = 0.01
    B1: float = 4.0
    B2: float = 0.02


class SimParamsRequest(BaseModel):
    T: int = 52
    n_paths: int = 500
    seed: int = 7
    x0: float = 0.0


class SimulateRequest(BaseModel):
    model: ModelParamsRequest
    sim: SimParamsRequest
    S: float = Field(..., description="Fixed base-stock level")


class OptimizeRequest(BaseModel):
    model: ModelParamsRequest
    sim: SimParamsRequest
    s_min: float = 80.0
    s_max: float = 160.0
    s_step: float = 10.0


class DynamicPolicyRequest(BaseModel):
    model: ModelParamsRequest
    sim: SimParamsRequest
    z: float = 2.2
    n_weeks: int = 156

class ExplainRequest(BaseModel):
    payload: dict