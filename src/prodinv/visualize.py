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
### the bellow plot Shows:
# As we increase buffer inventory, how often do simulated yearly 
# scenarios still experience at least one stockout?

def plot_stockout_probability_vs_S(
    results: pd.DataFrame,
    output_dir: str | Path = "reports/figures",
    filename: str = "stockout_probability_vs_S.png",
) -> Path:
    """
    Plot stockout probability vs base-stock level S.
    """
    out_dir = ensure_output_dir(output_dir)
    out_path = out_dir / filename

    plt.figure(figsize=(8, 5))
    plt.plot(results["S"], results["stockout_probability"], marker="o")
    plt.xlabel("Base-stock level S")
    plt.ylabel("Stockout probability")
    plt.title("Stockout Probability vs Inventory Buffer")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path

### The bellow plot shows What fraction of total demand is served immediately as S increases? 

def plot_fill_rate_vs_S(
    results: pd.DataFrame,
    output_dir: str | Path = "reports/figures",
    filename: str = "fill_rate_vs_S.png",
) -> Path:
    """
    Plot fill rate vs base-stock level S.
    """
    out_dir = ensure_output_dir(output_dir)
    out_path = out_dir / filename

    plt.figure(figsize=(8, 5))
    plt.plot(results["S"], results["fill_rate"], marker="o")
    plt.xlabel("Base-stock level S")
    plt.ylabel("Fill rate")
    plt.title("Fill Rate vs Inventory Buffer")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path



### The bellow plot shows: How much inventory are we carrying to achieve that service improvement?

def plot_avg_inventory_vs_S(
    results: pd.DataFrame,
    output_dir: str | Path = "reports/figures",
    filename: str = "avg_inventory_vs_S.png",
) -> Path:
    """
    Plot average inventory vs base-stock level S.
    """
    out_dir = ensure_output_dir(output_dir)
    out_path = out_dir / filename

    plt.figure(figsize=(8, 5))
    plt.plot(results["S"], results["avg_inventory"], marker="o")
    plt.xlabel("Base-stock level S")
    plt.ylabel("Average inventory")
    plt.title("Average Inventory vs Inventory Buffer")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path