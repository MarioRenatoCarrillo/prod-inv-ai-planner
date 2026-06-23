from src.prodinv.agents.decision_agent import (
    MonthlyDecisionRequest,
    SupplyChainDecisionAgent,
)


request = MonthlyDecisionRequest(
    commodity="Soybean Meal",
    location="Mankato Facility",
    forecast_month="2026-07",
    current_inventory=87_000,
    current_capacity=130_000,
    lead_time_days=14,
)

agent = SupplyChainDecisionAgent()
result = agent.run_monthly_inventory_decision(request)

print(result["executive_summary"])
print(result)