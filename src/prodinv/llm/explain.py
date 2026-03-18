from __future__ import annotations

from openai import OpenAI


client = OpenAI()


def explain_inventory_results(payload: dict) -> dict:
    """
    Use OpenAI to generate a structured executive explanation
    for inventory optimization results.
    """
    schema = {
        "type": "json_schema",
        "name": "inventory_explanation",
        "schema": {
            "type": "object",
            "properties": {
                "executive_summary": {"type": "string"},
                "key_drivers": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "recommended_action": {"type": "string"},
                "risk_notes": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": [
                "executive_summary",
                "key_drivers",
                "recommended_action",
                "risk_notes"
            ],
            "additionalProperties": False
        }
    }

    response = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a supply chain analytics advisor. "
                    "Explain results clearly for commercial and operations leaders."
                ),
            },
            {
                "role": "user",
                "content": f"Explain these inventory optimization results: {payload}"
            },
        ],
        text={"format": schema},
    )

    return response.output_parsed