# SC26 Artifact Description Draft

This draft is intended as source material for the SC26 AD/AE appendix. It uses
only the paper, the public notebook, and the checked-in result files.

## Overview of Artifacts

The artifact contains a notebook-derived workflow for UAV cotton orthomosaic
analysis. It computes deterministic RGB descriptors, estimates a cotton
visibility proxy using bright-region thresholding and excess-green suppression,
generates PCA and quantitative figures, and stores checked-in summary tables.

The public files support qualitative reproduction of the paper's stage trend:
post-defoliation imagery has larger cotton-visibility proxy values and larger
white-region fraction than pre-defoliation imagery.

## Artifact Availability

The public repository contains:

- figure assets in `figures/`;
- result CSVs in `results/`;
- run-provenance JSON files in `results/`;
- SLURM and inference logs in `logs/`;
- the original Colab notebook in `notebooks/TACC_SC26.ipynb`;
- standalone reproduction scripts in `scripts/`;
- traceability and checklist documentation in `docs/`.

The repository does not currently contain the full UAV image dataset, the exact
80/80 paper split, a parsed 4/8/16/32 scaling-output table for exact normalized
Table III verification, Figure 5 generation scripts, or a public AgroGPT LoRA
checkpoint.

## Hardware Requirements

For figure regeneration from already available image folders, a CPU workstation
is sufficient. Qwen2.5-VL inference cells in the notebook require a GPU for
practical execution. The paper describes Stampede3 as a SLURM-managed
distributed GPU environment. The checked-in notebook also documents a Colab GPU
fallback/proxy workflow used when direct Stampede3 access was unavailable. Exact
Stampede3 hardware specifications are not available in this artifact.

The checked-in SLURM job provenance used one node, one task, four CPUs per task,
32 GB memory, and the `spr` partition. The logs report CPU execution for the
Qwen2.5-VL job.

## Software Requirements

The standalone figure-generation script requires Python 3 with NumPy, Pandas,
SciPy, Pillow, Matplotlib, and scikit-learn. Optional notebook cells for
Qwen2.5-VL require PyTorch, Transformers, Accelerate, and Safetensors.

Exact original package versions are not specified.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Experiment Workflow

1. Place UAV image folders under a root directory. Folder names containing
   `pre` are classified as pre-defoliation; folder names containing `post` are
   classified as post-defoliation.
2. Run `scripts/generate_publication_figures.py`.
3. The script builds `inventory_analysis_table.csv`, aggregates
   `stage_summary_table.csv`, generates a PCA plot, generates the pre/post
   grid, and generates the quantitative proxy panel.
4. Run `scripts/validate_results.py` to compare checked-in summaries to the
   paper Table II reference values.
5. For the GPU execution path, use the Colab notebook cells that write and run
   `LLM_colab_paper_fixed.py`. These cells run Qwen2.5-VL inference, collect
   latency measurements, and write Colab Drive outputs such as
   `paper_results.json` and `paper_results_table.csv`.
6. For the SLURM provenance path, inspect `slurm/submission.slurm`,
   `logs/slurm_3007292.log`, `logs/slurm_3007292.err`, and
   `logs/inference_rank0.log`. These files document submitted commands,
   environment packages, rank-0 execution, dataset inventory processing, and
   the time-limit termination of job `3007292`.

## Reproducibility Instructions

```bash
python3 scripts/generate_publication_figures.py \
  --root-dir "/path/to/TACC EXPERIMENTS" \
  --out-dir outputs/publication_figures \
  --sample-limit 80

python3 scripts/validate_results.py
```

## Expected Output

The checked-in artifact currently reports:

| Stage | Samples | Mean proxy | Mean white-region fraction |
|---|---:|---:|---:|
| post_defoliation | 265 | 9586.962264 | 0.031344693 |
| pre_defoliation | 160 | 4564.831250 | 0.017528029 |

These values support the qualitative trend but do not exactly reproduce the
paper Table II values, which report 80 samples per stage. Exact Table II and
Table III reproduction requires the exact split files and, for normalized
multi-GPU scaling, the parsed 4/8/16/32 output table used for the final paper.
