#!/bin/bash -e
#SBATCH --profile task

#SBATCH --job-name=dailystats
#SBATCH --account=uoo03104
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --hint=multithread
#SBATCH --mem=4G

#SBATCH --output=test.%j.out
#SBATCH --error=test.%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tamara.pletzer@postgrad.otago.ac.nz


#conda activate xesmf_stable_env

srun python /home/pleta922/phdobj1/daily_stats.py
