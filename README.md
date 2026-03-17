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
- Machine Learning (demand forecasting)  
- KPI and service-risk analytics  
- Python-based production-ready architecture  

---

## Business Problem

A soybean processing facility must decide:

**How much inventory buffer should be maintained to minimize cost while ensuring reliable service?**

Too little inventory:
- increases backorders  
- disrupts customer fulfillment  

Too much inventory:
- increases storage cost  
- ties up working capital  

---

## Model Overview

### Demand

D_t = μ + ε_t  
ε_t ~ N(0, σ²)

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

# 🔥 Key Results (ML + OR Integration)

- Optimal fixed base-stock level: **S* ≈ 120**

### Initial ML Attempt

- Forecast Bias: **+3 units**
- Dynamic policy **underperformed** due to:
  - overestimated demand
  - excessive safety stock

### After Calibration

- Tuned service level: **z = 2.20**
- Dynamic policy cost: **328.82**
- Fixed policy cost: **329.00**

✅ **Final Result: ML + OR policy outperformed static policy**

---

## Business Insight

A naïve integration of machine learning into decision systems can increase costs.

However, when properly calibrated:

- bias correction  
- safety stock tuning  

forecast-driven policies can outperform traditional static rules.

### Key takeaway:

Real value comes from combining:

- Predictive modeling (ML)
- Prescriptive optimization (OR)
- Decision calibration

---

# 📊 Key Visualizations

### Cost vs Inventory Policy
![Total Cost](reports/figures/total_cost_vs_S.png)

### Service vs Risk Tradeoff
![Fill Rate](reports/figures/fill_rate_vs_S.png)

### Dynamic vs Fixed Inventory
![Inventory Comparison](reports/figures/dynamic_vs_fixed_inventory.png)

### Dynamic Inventory Target
![Dynamic S](reports/figures/dynamic_S_over_time.png)

---

## Repository Structure

prod-inv-ai-planner/  
├── README.md  
├── configs/  
├── reports/  
│   └── figures/  
├── src/  
└── tests/  

---

## How to Run

```bash
git clone https://github.com/MarioRenatoCarrillo/prod-inv-ai-planner.git
cd prod-inv-ai-planner

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

PYTHONPATH=src python -m prodinv.cli simulate --config ./configs/default.yaml
PYTHONPATH=src python -m prodinv.cli optimize --config ./configs/default.yaml
PYTHONPATH=src python -m prodinv.cli plot --config ./configs/default.yaml

PYTHONPATH=src pytest -q