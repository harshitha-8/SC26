# Artifact Evaluation Checklist

This checklist is written for SC26 artifact review. It separates available
materials from materials that are still needed for full numerical
reproducibility.

## Available

- [x] Public README with artifact scope and reproduction commands.
- [x] Figure assets for the pipeline, PCA, quantitative panel, and pre/post grid.
- [x] Per-image descriptor table: `results/inventory_analysis_table.csv`.
- [x] Stage summary table: `results/stage_summary_table.csv`.
- [x] Four-sample Qwen2.5-VL qualitative output: `results/model_comparison_results.csv`.
- [x] Original Colab notebook: `notebooks/TACC_SC26.ipynb`.
- [x] Standalone figure-generation script: `scripts/generate_publication_figures.py`.
- [x] Validation script: `scripts/validate_results.py`.
- [x] GitHub Actions workflow for table validation.
- [x] Traceability matrix: `docs/traceability.md`.
- [x] Colab H100 validation/proxy workflow in `notebooks/TACC_SC26.ipynb`.
- [x] Submitted SLURM script: `slurm/submission.slurm`.
- [x] SLURM job logs: `logs/slurm_3007292.log` and `logs/slurm_3007292.err`.
- [x] Rank-0 inference log: `logs/inference_rank0.log`.
- [x] Dataset inventory JSON: `results/dataset_inventory.json`.
- [x] Rank-0 run result JSON: `results/agrogpt_results_20260406_122646.json`.

## Partially Available

- [ ] Table I reasoning outputs: only Qwen2.5-VL outputs are currently public.
      A public AgroGPT LoRA checkpoint is not included.
- [ ] Table II statistics: the checked-in CSV supports the stage trend, but the
      exact paper 80/80 split is not included.
- [ ] Figure 1 pipeline: the final figure asset is included, but no editable
      source file or drawing script is included.
- [ ] Table III scaling: SLURM run provenance is checked in, but the exact
      parsed 4/8/16/32 normalized scaling table is not checked in.

## Missing

- [ ] Exact 80 pre-defoliation / 80 post-defoliation split used in the paper.
- [ ] Parsed scaling CSV or JSON backing the exact normalized Table III values.
- [ ] Figure 5 generation script.
- [ ] Public AgroGPT LoRA adapter or documented access instructions.
- [ ] Environment lock file from the original Colab/Stampede3 execution.

## Recommended Acceptance Path

1. Verify that `scripts/validate_results.py` runs successfully.
2. Confirm that the checked-in figures correspond to the qualitative paper
   figures.
3. Treat the artifact as supporting the public figure-generation workflow and
   qualitative cotton-visibility trend.
4. Use the checked-in SLURM logs as execution provenance, and request only the
   parsed 4/8/16/32 scaling table before accepting exact normalized Table III
   values.
