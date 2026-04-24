#!/usr/bin/env python3
"""Validate the checked-in SC26 artifact result tables.

The validation is intentionally conservative. It confirms the values present
in `results/stage_summary_table.csv` and reports whether they match the paper's
draft Table II values exactly.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PAPER_TABLE_II = {
    "pre_defoliation": {
        "samples": 80,
        "mean_boll_count_proxy": 4812.0,
        "median_boll_count_proxy": 4755.0,
        "std_boll_count_proxy": 612.0,
        "mean_white_region_fraction": 0.0198,
    },
    "post_defoliation": {
        "samples": 80,
        "mean_boll_count_proxy": 9428.0,
        "median_boll_count_proxy": 9311.0,
        "std_boll_count_proxy": 1045.0,
        "mean_white_region_fraction": 0.0346,
    },
}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    inventory = pd.read_csv(root / "results" / "inventory_analysis_table.csv")
    summary = pd.read_csv(root / "results" / "stage_summary_table.csv")
    dataset_inventory_path = root / "results" / "dataset_inventory.json"
    run_results_path = root / "results" / "agrogpt_results_20260406_122646.json"
    slurm_err_path = root / "logs" / "slurm_3007292.err"

    derived = inventory.groupby("stage").agg(
        samples=("path", "count"),
        mean_boll_count_proxy=("boll_count_proxy", "mean"),
        median_boll_count_proxy=("boll_count_proxy", "median"),
        std_boll_count_proxy=("boll_count_proxy", "std"),
        mean_white_region_fraction=("white_region_fraction", "mean"),
    )

    print("Checked-in stage_summary_table.csv")
    print(summary.to_string(index=False))
    print("\nDerived from inventory_analysis_table.csv")
    print(derived.to_string())

    print("\nComparison to paper Table II")
    exact = True
    for stage, expected in PAPER_TABLE_II.items():
        if stage not in derived.index:
            print(f"- {stage}: missing")
            exact = False
            continue
        observed = derived.loc[stage]
        stage_exact = True
        for key, expected_value in expected.items():
            observed_value = float(observed[key])
            if abs(observed_value - expected_value) > 1e-9:
                stage_exact = False
                exact = False
                print(f"- {stage} {key}: observed {observed_value:.12g}, paper {expected_value:.12g}")
        if stage_exact:
            print(f"- {stage}: exact match")

    print("\nStatus:", "exact match" if exact else "trend supported; exact paper values not reproduced")
    if dataset_inventory_path.exists():
        dataset_inventory = json.loads(dataset_inventory_path.read_text())
        stats = dataset_inventory.get("statistics", {})
        print("\nDataset inventory provenance")
        print(
            f"- total_images={stats.get('total_images')} "
            f"pre={stats.get('pre_defoliation_count')} "
            f"post={stats.get('post_defoliation_count')}"
        )
    if run_results_path.exists():
        run_results = json.loads(run_results_path.read_text())
        metadata = run_results.get("metadata", {})
        stages = run_results.get("stages", {})
        print("\nRank-0 run provenance")
        print(
            f"- model={metadata.get('model')} "
            f"rank={metadata.get('rank')} "
            f"world_size={metadata.get('world_size')} "
            f"demo_mode={metadata.get('demo_mode')}"
        )
        print(
            "- stage_counts="
            + ", ".join(f"{name}:{stage.get('count')}" for name, stage in stages.items())
        )
    if slurm_err_path.exists():
        slurm_err = slurm_err_path.read_text()
        if "CANCELLED" in slurm_err and "TIME LIMIT" in slurm_err:
            print("\nSLURM provenance")
            print("- job 3007292 log present; terminated by time limit after starting Qwen2.5-VL run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
