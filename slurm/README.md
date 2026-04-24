# SLURM Templates

These files are templates for artifact users who want to adapt the workflow to
a SLURM-managed GPU cluster. They are **not** the original Stampede3 logs or the
verified 4/8/16/32 GPU scaling scripts used for the paper's Table III.

For exact Table III reproduction, the artifact still needs:

- original `sbatch` scripts for 4, 8, 16, and 32 GPU configurations;
- corresponding `.out` and `.err` logs;
- a normalized scaling CSV generated from those logs;
- the Figure 5 plotting script.
