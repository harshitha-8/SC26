#!/bin/bash
# Placeholder only.
# The paper reports 4/8/16/32 GPU normalized scaling, but the verified scripts
# and logs for those runs are not currently included in this artifact.

#SBATCH --job-name=sc26_scaling_placeholder
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --time=00:30:00
#SBATCH --output=logs/sc26_scaling_placeholder_%j.out
#SBATCH --error=logs/sc26_scaling_placeholder_%j.err

set -euo pipefail

echo "This placeholder does not reproduce Table III."
echo "Add verified 4/8/16/32 GPU scripts and logs before claiming scaling reproduction."
