# Rebuttal Evidence Notes

This note summarizes what the checked-in artifact can safely support during the
SC26 rebuttal.

## Verified From Notebook Metadata

- `notebooks/TACC_SC26.ipynb` records a GPU runtime with Colab metadata:
  `accelerator: GPU`, `machine_shape: hm`, and `gpuType: H100`.
- The notebook executes Qwen2.5-VL (`Qwen/Qwen2.5-VL-3B-Instruct`) on a small
  sample of UAV cotton images and saves qualitative model-comparison output.
- The generated `LLM_colab_paper_fixed.py` script selects CUDA when available
  and logs the CUDA device name, but the checked-in run metadata is single-rank:
  `rank=0`, `world_size=1`, `local_rank=0`.

## Verified From Slurm/Repository Files

- `slurm/submission.slurm` uses the `spr` partition, allocation
  `TG-AGR250027`, one node, one task per node, four CPUs per task, and 32 GB
  memory.
- `results/dataset_inventory.json` reports 3,096 total images and 16.52 GB of
  input imagery: 1,358 pre-defoliation images (7.20 GB) and 1,738
  post-defoliation images (9.32 GB).
- `results/stage_summary_table.csv` supports the qualitative result that
  post-defoliation imagery has higher candidate-center proxy values and higher
  white-region fraction than pre-defoliation imagery.

## Important Boundary

The notebook records an H100 validation/proxy path for the visual-language stage, and the checked-in Slurm files record the submitted rank-level provenance path. They do not contain a parsed 4/8/16/32
multi-GPU scaling table. In rebuttal language, describe this as local/proxy GPU
execution evidence, not as verified multi-GPU Stampede3 scaling evidence unless
the missing scaling logs are added.
