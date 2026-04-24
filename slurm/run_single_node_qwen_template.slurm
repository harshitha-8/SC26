#!/bin/bash
# Template only: adapt account, partition, paths, and modules for your cluster.
# This is not a verified Table III scaling script.

#SBATCH --job-name=sc26_qwen_single_node
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=02:00:00
#SBATCH --output=logs/sc26_qwen_%j.out
#SBATCH --error=logs/sc26_qwen_%j.err

set -euo pipefail

ROOT_DIR=${ROOT_DIR:-"/path/to/TACC EXPERIMENTS"}
OUT_DIR=${OUT_DIR:-"outputs/publication_figures"}

python3 -m pip install -r requirements.txt
python3 scripts/generate_publication_figures.py \
  --root-dir "$ROOT_DIR" \
  --out-dir "$OUT_DIR" \
  --sample-limit 80
