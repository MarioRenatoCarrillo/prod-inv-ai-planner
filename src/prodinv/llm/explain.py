from __future__ import annotations

from openai import OpenAI

client = OpenAI()


def explain_inventory_results(payload: dict) -> str:
    """
    Generate a plain-language executive explanation for inventory optimization results.
    """
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
    )

    return response.output_text