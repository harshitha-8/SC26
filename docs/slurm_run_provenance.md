# SLURM Run Provenance Notes

This repository includes the submitted SLURM script and logs supplied for the
SC26 artifact.

Verified files:

- `slurm/submission.slurm`
- `logs/slurm_3007292.log`
- `logs/slurm_3007292.err`
- `logs/inference_rank0.log`
- `results/dataset_inventory.json`
- `results/agrogpt_results_20260406_122646.json`

Verified execution details:

- job name: `agrogpt_deadline`
- allocation: `TG-AGR250027`
- partition: `spr`
- nodes: 1
- tasks per node: 1
- CPUs per task: 4
- memory: 32 GB
- model argument: `Qwen/Qwen2.5-VL-3B-Instruct`
- stage argument: `all`
- batch size: 1
- workers: 0
- feature source: `auto`
- generation: skipped
- per-stage limit in submitted command: 40

Observed log evidence:

- `inference_rank0.log` records `rank=0`, `world_size=1`, and `local_rank=0`.
- The April 6 run used demonstration mode and wrote
  `agrogpt_results_20260406_122646.json`.
- `dataset_inventory.json` reports 3,096 total images, with 1,358
  pre-defoliation and 1,738 post-defoliation images.
- `slurm_3007292.err` records model loading for Qwen2.5-VL on CPU and
  time-limit cancellation of job `3007292` on April 7, 2026.

Verification boundary:

These files demonstrate SLURM submission, environment/package availability,
rank-0 execution, dataset inventory, and a completed demonstration-mode
pre/post pass. They do not by themselves contain a parsed 4/8/16/32 normalized
multi-GPU scaling table. If the paper's final Table III reports normalized
multi-GPU values, that exact parsed table should also be checked in.
