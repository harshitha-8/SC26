# SLURM Scripts and Templates

This directory contains the submitted SLURM script supplied with the artifact
and additional templates for adapting the workflow to a SLURM-managed cluster.

Included script:

- `submission.slurm`: submitted single-node, single-task Qwen2.5-VL run using
  the `spr` partition and `TG-AGR250027` allocation.

Template scripts:

- `run_single_node_qwen_template.slurm`
- `run_scaling_placeholder.slurm`

Related logs are checked in under `logs/`.

For exact normalized Table III reproduction, the artifact still needs the
parsed 4/8/16/32 scaling table if those final values are reported:

- original `sbatch` scripts for 4, 8, 16, and 32 GPU configurations;
- corresponding `.out` and `.err` logs;
- a normalized scaling CSV generated from those logs;
- the Figure 5 plotting script.
