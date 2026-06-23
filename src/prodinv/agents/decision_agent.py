from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from src.prodinv.config import ModelParams, SimParams
from src.prodinv.forecasting import forecast_next_period
from src.prodinv.optimize import search_best_S

from src.prodinv.kpi import compute_kpis
from src.prodinv.simulate import run_simulation


@dataclass
class MonthlyDecisionRequest:
    commodity: str
    location: str
    forecast_month: str
    current_inventory: float
    current_capacity: float
    lead_time_days: int
    target_service_level: float = 0.95


class SupplyChainDecisionAgent:
    def run_monthly_inventory_decision(
        self,
        request: MonthlyDecisionRequest,
    ) -> dict[str, Any]:
        forecast = self.run_forecast_agent(request)
        risk = self.run_risk_agent(request, forecast)
        inventory = self.run_inventory_agent(request, forecast, risk)
        procurement = self.run_procurement_agent(request, inventory)
        decision_rationale = self.run_decision_rationale_agent(
            request=request,
            forecast=forecast,
            risk=risk,
            inventory=inventory,
            procurement=procurement,
        )
        executive_summary = self.run_executive_agent(
            request=request,
            forecast=forecast,
            risk=risk,
            inventory=inventory,
            procurement=procurement,
        )

        return {
            "decision_type": "monthly_inventory_decision",
            "commodity": request.commodity,
            "location": request.location,
            "forecast": forecast,
            "risk": risk,
            "inventory": inventory,
            "procurement": procurement,
            "decision_rationale": decision_rationale,
            "executive_summary": executive_summary,
        }

    def run_forecast_agent(self, request: MonthlyDecisionRequest) -> dict[str, Any]:
        return forecast_next_period(forecast_month=request.forecast_month)
    
    def run_risk_agent(
        self,
        request: MonthlyDecisionRequest,
        forecast: dict[str, Any],
    ) -> dict[str, Any]:
        mp = ModelParams(
            mu=forecast["expected_demand"],
            sigma=forecast["forecast_std_dev"],
            truncate_demand_at_zero=True,
            C1=1.0,
            C2=0.002,
            K1=0.2,
            K2=0.0005,
            B1=5.0,
            B2=0.005,
        )

        sp = SimParams(
            T=12,
            n_paths=500,
            seed=7,
            x0=request.current_inventory,
        )

        # Initial risk check: simulate current inventory as the policy level
        current_policy_S = request.current_inventory

        avg_total_cost, breakdown, trajectory, path_summary = run_simulation(
            mp=mp,
            sp=sp,
            S=current_policy_S,
        )

        kpis = compute_kpis(path_summary)

        stockout_probability = float(kpis["stockout_probability"])
        fill_rate = float(kpis["fill_rate"])

        if stockout_probability >= 0.50:
            risk_level = "HIGH"
        elif stockout_probability >= 0.20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "policy_evaluated": "CURRENT_INVENTORY_POLICY",
            "current_policy_S": round(current_policy_S, 2),
            "stockout_probability": round(stockout_probability, 4),
            "avg_stockout_rate": round(float(kpis["avg_stockout_rate"]), 4),
            "fill_rate": round(fill_rate, 4),
            "avg_inventory": round(float(kpis["avg_inventory"]), 2),
            "avg_demand": round(float(kpis["avg_demand"]), 2),
            "avg_total_cost": round(float(avg_total_cost), 2),
            "production_cost": round(float(breakdown["production_cost"]), 2),
            "holding_cost": round(float(breakdown["holding_cost"]), 2),
            "backorder_cost": round(float(breakdown["backorder_cost"]), 2),
            "risk_level": risk_level,
        }
    
    def run_inventory_agent(
        self,
        request: MonthlyDecisionRequest,
        forecast: dict[str, Any],
        risk: dict[str, Any],
    ) -> dict[str, Any]:
        mp = ModelParams(
            mu=forecast["expected_demand"],
            sigma=forecast["forecast_std_dev"],
            truncate_demand_at_zero=True,
            C1=1.0,
            C2=0.002,
            K1=0.2,
            K2=0.0005,
            B1=5.0,
            B2=0.005,
        )

        sp = SimParams(
            T=12,
            n_paths=500,
            seed=7,
            x0=request.current_inventory,
        )

        s_grid = np.arange(
            forecast["expected_demand"] * 0.80,
            min(request.current_capacity, forecast["expected_demand"] * 1.30),
            forecast["expected_demand"] * 0.05,
        )

        results = search_best_S(mp=mp, sp=sp, S_grid=s_grid)
        best_policy = results.iloc[0]

        return {
            "recommended_inventory": round(float(best_policy["S"]), 2),
            "target_service_level": request.target_service_level,
            "estimated_total_cost": round(float(best_policy["avg_total_cost"]), 2),
            "production_cost": round(float(best_policy["production_cost"]), 2),
            "holding_cost": round(float(best_policy["holding_cost"]), 2),
            "backorder_cost": round(float(best_policy["backorder_cost"]), 2),
            "stockout_probability": round(float(best_policy["stockout_probability"]), 4),
            "fill_rate": round(float(best_policy["fill_rate"]), 4),
            "capacity_utilization_after_recommendation": round(
                float(best_policy["S"]) / request.current_capacity,
                4,
            ),
        }

    def run_procurement_agent(
        self,
        request: MonthlyDecisionRequest,
        inventory: dict[str, Any],
    ) -> dict[str, Any]:
        recommended_purchase = max(
            inventory["recommended_inventory"] - request.current_inventory,
            0,
        )

        return {
            "recommended_purchase": round(recommended_purchase, 2),
            "lead_time_days": request.lead_time_days,
            "procurement_action": (
                "PLACE_ORDER"
                if recommended_purchase > 0
                else "NO_ADDITIONAL_ORDER_REQUIRED"
            ),
        }

    def run_decision_rationale_agent(
        self,
        request: MonthlyDecisionRequest,
        forecast: dict[str, Any],
        risk: dict[str, Any],
        inventory: dict[str, Any],
        procurement: dict[str, Any],
    ) -> list[str]:

        rationale = []

        if (
            forecast["expected_demand"]
            > request.current_inventory
        ):
            rationale.append(
                "Forecasted demand exceeds current inventory."
            )

        if risk["risk_level"] == "HIGH":
            rationale.append(
                "Current inventory policy presents high stockout risk."
            )

        if (
            inventory["fill_rate"]
            > risk["fill_rate"]
        ):
            rationale.append(
                f"Optimized inventory policy improves fill rate "
                f"from {risk['fill_rate']:.1%} "
                f"to {inventory['fill_rate']:.1%}."
            )

        total_cost_reduction = (
            risk["avg_total_cost"]
            - inventory["estimated_total_cost"]
        )

        if total_cost_reduction > 0:
            rationale.append(
                f"Optimization reduces expected total cost by "
                f"${total_cost_reduction:,.0f}."
            )

        backorder_reduction = (
            risk["backorder_cost"]
            - inventory["backorder_cost"]
        )

        if backorder_reduction > 0:
            rationale.append(
                f"Optimization reduces expected backorder costs by "
                f"${backorder_reduction:,.0f}."
            )

        if procurement["recommended_purchase"] > 0:
            rationale.append(
                f"Additional procurement of "
                f"{procurement['recommended_purchase']:,.0f} units "
                f"is required to support service-level objectives."
            )

        return rationale

    def run_executive_agent(
        self,
        request: MonthlyDecisionRequest,
        forecast: dict[str, Any],
        risk: dict[str, Any],
        inventory: dict[str, Any],
        procurement: dict[str, Any],
    ) -> str:

        current_fill_rate = risk["fill_rate"]
        optimized_fill_rate = inventory["fill_rate"]

        current_stockout = risk["stockout_probability"]
        optimized_stockout = inventory["stockout_probability"]

        backorder_reduction = (
            risk["backorder_cost"] - inventory["backorder_cost"]
        )

        total_cost_reduction = (
            risk["avg_total_cost"] - inventory["estimated_total_cost"]
        )

        return (
            f"For {request.commodity} at {request.location}, "
            f"demand for {request.forecast_month} is forecasted at "
            f"{forecast['expected_demand']:,.0f} units "
            f"(range: {forecast['forecast_low']:,.0f} - "
            f"{forecast['forecast_high']:,.0f}). "

            f"Under the current inventory policy "
            f"({risk['current_policy_S']:,.0f} units), "
            f"simulation results indicate a "
            f"{current_stockout:.1%} probability of experiencing at least one stockout event, "
            f"a fill rate of {current_fill_rate:.1%}, "
            f"and an expected total cost of "
            f"${risk['avg_total_cost']:,.0f}. "

            f"The optimization engine recommends increasing inventory to "
            f"{inventory['recommended_inventory']:,.0f} units. "
            f"This improves fill rate to {optimized_fill_rate:.1%}, "
            f"reduces expected total cost by ${total_cost_reduction:,.0f}, "
            f"and lowers expected backorder cost by ${backorder_reduction:,.0f}. "

            f"This recommendation requires procuring "
            f"{procurement['recommended_purchase']:,.0f} additional units. "

            f"Recommended action: "
            f"{procurement['procurement_action']}."
        )    

