from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml


@dataclass(frozen=True)
class ModelParams:
    mu: float
    sigma: float
    truncate_demand_at_zero: bool

    C1: float
    C2: float

    K1: float
    K2: float

    B1: float
    B2: float


@dataclass(frozen=True)
class SimParams:
    T: int
    n_paths: int
    seed: int
    x0: float


@dataclass(frozen=True)
class PolicyParams:
    type: str
    S: float


@dataclass(frozen=True)
class AppConfig:
    model: ModelParams
    sim: SimParams
    policy: PolicyParams


def load_config(path: str | Path) -> AppConfig:
    data: dict[str, Any] = yaml.safe_load(Path(path).read_text())

    return AppConfig(
        model=ModelParams(**data["model"]),
        sim=SimParams(**data["sim"]),
        policy=PolicyParams(**data["policy"]),
    )