from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .config import load_config
from .kpi import compute_kpis
from .optimize import search_best_S
from .simulate import run_simulation
from .visualize import (
    plot_cost_breakdown_vs_S,
    plot_total_cost_vs_S,
    plot_trajectory,
)


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line interface parser.
    """
    parser = argparse.ArgumentParser(
        prog="prodinv",
        description="AI + Operations Research for Agricultural Supply Chains",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # simulate
    sim_parser = subparsers.add_parser(
        "simulate",
        help="Run Monte Carlo simulation for one base-stock level S",
    )
    sim_parser.add_argument("--config", required=True, type=str)

    # optimize
    opt_parser = subparsers.add_parser(
        "optimize",
        help="Search for the best base-stock level S over a grid",
    )
    opt_parser.add_argument("--config", required=True, type=str)
    opt_parser.add_argument("--s-min", type=float, default=80.0)
    opt_parser.add_argument("--s-max", type=float, default=160.0)
    opt_parser.add_argument("--s-step", type=float, default=10.0)

    # plot
    plot_parser = subparsers.add_parser(
        "plot",
        help="Generate optimization and trajectory plots",
    )
    plot_parser.add_argument("--config", required=True, type=str)
    plot_parser.add_argument("--s-min", type=float, default=80.0)
    plot_parser.add_argument("--s-max", type=float, default=160.0)
    plot_parser.add_argument("--s-step", type=float, default=10.0)
    plot_parser.add_argument("--output-dir", type=str, default="reports/figures")

    return parser


def run_simulate_command(config_path: str) -> None:
    """
    Run a single simulation at the configured base-stock level.
    """
    cfg = load_config(config_path)

    avg_total_cost, breakdown, trajectory, path_summary = run_simulation(
        mp=cfg.model,
        sp=cfg.sim,
        S=cfg.policy.S,
    )

    kpis = compute_kpis(path_summary)

    print("\n=== Simulation Results ===")
    print(f"Policy type: {cfg.policy.type}")
    print(f"Base-stock level S: {cfg.policy.S:.2f}")
    print(f"Average total cost / period: {avg_total_cost:.4f}")

    print("\nCost breakdown / period:")
    for key, value in breakdown.items():
        print(f"  - {key}: {value:.4f}")

    print("\nOperational KPIs:")
    for key, value in kpis.items():
        print(f"  - {key}: {value:.4f}")

    print("\nTrajectory preview:")
    print(trajectory.head(10).to_string(index=False))

    print("\nPath summary preview:")
    print(path_summary.head(10).to_string(index=False))


def run_optimize_command(
    config_path: str,
    s_min: float,
    s_max: float,
    s_step: float,
) -> None:
    """
    Search across a grid of S values and print the sorted results.
    """
    cfg = load_config(config_path)

    s_grid = np.arange(s_min, s_max + s_step, s_step)

    results = search_best_S(
        mp=cfg.model,
        sp=cfg.sim,
        S_grid=s_grid,
    )

    best_row = results.iloc[0]

    print("\n=== Optimization Results ===")
    print(results.to_string(index=False))

    print("\n=== Best Policy Found ===")
    print(f"S*: {best_row['S']:.2f}")
    print(f"Average total cost: {best_row['avg_total_cost']:.4f}")
    print(f"Production cost: {best_row['production_cost']:.4f}")
    print(f"Holding cost: {best_row['holding_cost']:.4f}")
    print(f"Backorder cost: {best_row['backorder_cost']:.4f}")


def run_plot_command(
    config_path: str,
    s_min: float,
    s_max: float,
    s_step: float,
    output_dir: str,
) -> None:
    """
    Generate plots from optimization results and the best-S trajectory.
    """
    cfg = load_config(config_path)

    s_grid = np.arange(s_min, s_max + s_step, s_step)

    results = search_best_S(
        mp=cfg.model,
        sp=cfg.sim,
        S_grid=s_grid,
    )

    best_s = float(results.iloc[0]["S"])

    avg_total_cost, breakdown, trajectory, path_summary = run_simulation(
        mp=cfg.model,
        sp=cfg.sim,
        S=best_s,
    )

    p1 = plot_total_cost_vs_S(results, output_dir=output_dir)
    p2 = plot_cost_breakdown_vs_S(results, output_dir=output_dir)
    p3 = plot_trajectory(trajectory, output_dir=output_dir)

    print("\n=== Plot Generation Complete ===")
    print(f"Best S used for trajectory: {best_s:.2f}")
    print(f"Average total cost: {avg_total_cost:.4f}")
    print(f"Saved: {Path(p1)}")
    print(f"Saved: {Path(p2)}")
    print(f"Saved: {Path(p3)}")


def main() -> None:
    """
    Entry point for the CLI.
    """
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "simulate":
        run_simulate_command(args.config)

    elif args.command == "optimize":
        run_optimize_command(
            config_path=args.config,
            s_min=args.s_min,
            s_max=args.s_max,
            s_step=args.s_step,
        )

    elif args.command == "plot":
        run_plot_command(
            config_path=args.config,
            s_min=args.s_min,
            s_max=args.s_max,
            s_step=args.s_step,
            output_dir=args.output_dir,
        )


if __name__ == "__main__":
    main()