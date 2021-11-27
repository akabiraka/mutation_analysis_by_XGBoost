#!/usr/bin/sh

## this must be run from directory where run.py exists.
## --workdir is not used in this file.

#SBATCH --job-name=mutation_analysis_by_XGBoost
#SBATCH --qos=csqos
#SBATCH --output=/scratch/akabir4/mutation_analysis_by_XGBoost/outputs/argo_logs/distributed_pssm_generator-%N-%j.output
#SBATCH --error=/scratch/akabir4/mutation_analysis_by_XGBoost/outputs/argo_logs/distributed_pssm_generator-%N-%j.error
#SBATCH --mail-user=<akabir4@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL

#SBATCH --partition=all-HiPri
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000MB

#SBATCH --array=2-208
##here total 209 unique proteins, where each may have multiple mutations
##the array task is set in the environment variable $SLURM_ARRAY_TASK_ID in python you
##can scrape it with ID = int(os.environ["SLURM_ARRAY_TASK_ID"])

python data_gen/distributed_pssm_generator.py
