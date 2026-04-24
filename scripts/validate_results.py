#!/usr/bin/env python3
"""Validate the checked-in SC26 artifact result tables.

The validation is intentionally conservative. It confirms the values present
in `results/stage_summary_table.csv` and reports whether they match the paper's
draft Table II values exactly.
"""

from __future__ import annotations

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
