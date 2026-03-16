from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def ensure_output_dir(output_dir: str | Path) -> Path:
    """
    Ensure the output directory exists.
    """
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def plot_total_cost_vs_S(
    results: pd.DataFrame,
    output_dir: str | Path = "reports/figures",
    filename: str = "total_cost_vs_S.png",
) -> Path:
    """
    Plot average total cost vs base-stock level S.
    """

    out_dir = ensure_output_dir(output_dir)
    out_path = out_dir / filename

    plt.figure(figsize=(8, 5))

    plt.plot(
        results["S"],
        results["avg_total_cost"],
        marker="o"
    )

    plt.xlabel("Base-stock level S")
    plt.ylabel("Average total cost per period")
    plt.title("Total Cost vs Inventory Buffer")

    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path


def plot_cost_breakdown_vs_S(
    results: pd.DataFrame,
    output_dir: str | Path = "reports/figures",
    filename: str = "cost_breakdown_vs_S.png",
) -> Path:
    """
    Plot production, holding, and backorder costs vs S.
    """

    out_dir = ensure_output_dir(output_dir)
    out_path = out_dir / filename

    plt.figure(figsize=(8, 5))

    plt.plot(
        results["S"],
        results["production_cost"],
        marker="o",
        label="Production Cost"
    )

    plt.plot(
        results["S"],
        results["holding_cost"],
        marker="o",
        label="Holding Cost"
    )

    plt.plot(
        results["S"],
        results["backorder_cost"],
        marker="o",
        label="Backorder Cost"
    )

    plt.xlabel("Base-stock level S")
    plt.ylabel("Average cost per period")

    plt.title("Cost Breakdown vs Inventory Buffer")

    plt.legend()

    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path


def plot_trajectory(
    trajectory: pd.DataFrame,
    output_dir: str | Path = "reports/figures",
    filename: str = "inventory_trajectory.png",
) -> Path:
    """
    Plot average inventory, production, and demand over time.
    """

    out_dir = ensure_output_dir(output_dir)
    out_path = out_dir / filename

    plt.figure(figsize=(9, 5))

    plt.plot(
        trajectory["t"],
        trajectory["avg_x_start"],
        marker="o",
        label="Average Inventory"
    )

    plt.plot(
        trajectory["t"],
        trajectory["avg_q"],
        marker="o",
        label="Average Production"
    )

    plt.plot(
        trajectory["t"],
        trajectory["avg_demand"],
        marker="o",
        label="Average Demand"
    )

    plt.xlabel("Time Period")
    plt.ylabel("Units")

    plt.title("Inventory, Production, and Demand Over Time")

    plt.legend()

    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path