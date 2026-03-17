# AI + Operations Research for Agricultural Supply Chains  
## Stochastic Production Planning for a Soybean Processing Facility

---

## Executive Summary

This project demonstrates an end-to-end decision-support system for production and inventory optimization under uncertainty in an agricultural commodity context.

The use case models a soybean processing facility that must balance:

- uncertain weekly demand  
- nonlinear production costs  
- inventory holding costs  
- service risk from backorders  

The solution combines:

- Operations Research (stochastic inventory modeling)  
- Monte Carlo simulation  
- KPI and service-risk analytics  
- Python-based production-ready architecture  

This project is designed to evolve into a full system with:

- ML demand forecasting  
- dynamic safety stock policies  
- OpenAI-powered decision explanations  
- Power BI dashboards  
- AWS deployment  

---

## Business Problem

A soybean processing facility must decide:

How much inventory buffer should be maintained to minimize cost while ensuring reliable service?

Too little inventory:
- increases backorders  
- disrupts customer fulfillment  

Too much inventory:
- increases storage cost  
- ties up working capital  

This project models that tradeoff and identifies the optimal inventory policy.

---

## Model Overview

### Demand

D_t = μ + ε_t  
ε_t ~ N(0, σ²)

- μ = average demand  
- σ = demand volatility  

---

### Inventory Dynamics

x_(t+1) = x_t + q_t - D_t

---

### Cost Functions

Production Cost  
C(q) = C1*q + 0.5*C2*q²  

Holding Cost  
k(x⁺) = K1*x⁺ + 0.5*K2*(x⁺)²  

Backorder Cost  
b(x⁻) = B1*x⁻ + 0.5*B2*(x⁻)²  

---

### Policy

q_t = max(0, S - x_t)

Goal: Find optimal S*

---

## Repository Structure

prod-inv-ai-planner/  
├── README.md  
├── configs/  
│   └── default.yaml  
├── reports/  
│   └── figures/  
├── src/  
│   └── prodinv/  
│       ├── cli.py  
│       ├── config.py  
│       ├── demand.py  
│       ├── econ.py  
│       ├── kpi.py  
│       ├── optimize.py  
│       ├── policies.py  
│       ├── simulate.py  
│       └── visualize.py  
└── tests/  

---

## How to Run

### 1. Clone repository

git clone https://github.com/YOUR_USERNAME/prod-inv-ai-planner.git  
cd prod-inv-ai-planner  

---

### 2. (Optional) Create virtual environment

python -m venv .venv  
source .venv/bin/activate  

---

### 3. Install dependencies

pip install -r requirements.txt  

---

### 4. Run simulation

PYTHONPATH=src python -m prodinv.cli simulate --config ./configs/default.yaml  

Outputs:
- cost breakdown  
- KPIs  
- system trajectory  

---

### 5. Run optimization

PYTHONPATH=src python -m prodinv.cli optimize --config ./configs/default.yaml  

Finds optimal inventory buffer S*

---

### 6. Generate plots

PYTHONPATH=src python -m prodinv.cli plot --config ./configs/default.yaml  

Outputs saved in:

reports/figures/  

---

### 7. Run tests

PYTHONPATH=src pytest -q  

---

## Results

Optimal inventory policy:

S* = 120  

Interpretation:

- Lower S → high backorder cost  
- Higher S → high holding cost  
- Optimal S balances both  

---

## Key Insights

1. Inventory acts as a shock absorber  
Production remains stable while inventory absorbs demand variability  

2. Tradeoff is holding vs backorder cost  
Production cost remains relatively stable  

3. Service improves with diminishing returns  
Higher inventory increases service but at decreasing marginal benefit  

4. Optimal policy does not eliminate risk  
Some stockouts still occur, but at economically optimal levels  

---

## Figures

Total Cost vs Inventory  
reports/figures/total_cost_vs_S.png  

Cost Breakdown  
reports/figures/cost_breakdown_vs_S.png  

Fill Rate  
reports/figures/fill_rate_vs_S.png  

Stockout Risk  
reports/figures/stockout_probability_vs_S.png  

Average Inventory  
reports/figures/avg_inventory_vs_S.png  

System Dynamics  
reports/figures/inventory_trajectory.png  

---

## Skills Demonstrated

- Stochastic modeling  
- Monte Carlo simulation  
- Inventory optimization  
- Python engineering (modular design)  
- CLI tool development  
- Data visualization  
- KPI and risk analytics  
- Test-driven development  

---

## Roadmap

Phase 1 (Completed)
- stochastic simulation  
- optimization  
- KPI reporting  
- visualization  
- CLI + tests  

Phase 2 (Next)
- synthetic demand data  
- ML forecasting  
- dynamic safety stock  

Phase 3 (Planned)
- OpenAI explanation layer  
- automated insights  

Phase 4 (Planned)
- Power BI dashboard  
- API + AWS deployment  

