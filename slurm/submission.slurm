#!/bin/bash
#SBATCH --job-name=agrogpt_deadline
#SBATCH --output=/work/10904/harshitha114488/LLM-test/Acess_HPC/output/slurm_%j.log
#SBATCH --error=/work/10904/harshitha114488/LLM-test/Acess_HPC/output/slurm_%j.err
#SBATCH --time=03:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=spr
#SBATCH --account=TG-AGR250027
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G

set -euo pipefail

PROJECT=/work/10904/harshitha114488/LLM-test
OUT=$PROJECT/Acess_HPC/output
CODE=$PROJECT/Acess_HPC/Files/LLM.py

mkdir -p "$OUT" "$PROJECT/.hf"

export HF_HOME=$PROJECT/.hf
export HUGGINGFACE_HUB_CACHE=$HF_HOME/hub
export TRANSFORMERS_CACHE=$HF_HOME/hub
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-4}

source $PROJECT/venv/bin/activate

python3 -m pip install -U accelerate transformers safetensors pillow numpy pandas matplotlib scikit-learn

srun python3 -u "$CODE" \
  --model-id Qwen/Qwen2.5-VL-3B-Instruct \
  --stage all \
  --batch-size 1 \
  --num-workers 0 \
  --feature-source auto \
  --skip-generation \
  --limit-per-stage 40