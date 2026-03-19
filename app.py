from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

import streamlit as st
import numpy as np
import pandas as pd

from prodinv.config import ModelParams, SimParams
from prodinv.optimize import search_best_S
from prodinv.simulate import run_simulation

st.set_page_config(layout="wide")

st.title("AI + OR Inventory Optimization Dashboard")

# Sidebar controls
st.sidebar.header("Model Parameters")

mu = st.sidebar.slider("Mean Demand (mu)", 80, 120, 100)
sigma = st.sidebar.slider("Demand Volatility (sigma)", 10, 40, 20)

# Model setup
mp = ModelParams(
    mu=mu,
    sigma=sigma,
    truncate_demand_at_zero=True,
    C1=2.0,
    C2=0.02,
    K1=0.5,
    K2=0.01,
    B1=4.0,
    B2=0.02,
)

sp = SimParams(
    T=52,
    n_paths=300,
    seed=7,
    x0=0.0,
)

# Optimization
s_grid = np.arange(100, 132, 2)
results = search_best_S(mp, sp, s_grid)

best_S = float(results.iloc[0]["S"])

st.subheader("Optimal Policy")
st.write(f"Optimal S: {best_S:.2f}")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Cost vs S")
    st.line_chart(results.set_index("S")["avg_total_cost"])

with col2:
    st.subheader("Cost Breakdown")
    st.bar_chart(
        results.set_index("S")[[
            "production_cost",
            "holding_cost",
            "backorder_cost"
        ]]
    )

# Trajectory
_, _, trajectory, _ = run_simulation(mp, sp, best_S)

st.subheader("Inventory Trajectory")
st.line_chart(
    trajectory[["avg_x_start", "avg_x_end"]]
)

# Show raw data
with st.expander("Show Data"):
    st.dataframe(results)