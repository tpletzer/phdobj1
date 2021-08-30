#!/bin/bash -e
#SBATCH --profile task

#SBATCH --job-name=dailystats
#SBATCH --account=uoo03104
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=05:00:00
#SBATCH --hint=multithread
#SBATCH --mem=3G
#SBATCH --array=0-16

#SBATCH --output=test.%j.out
#SBATCH --error=test.%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tamara.pletzer@postgrad.otago.ac.nz


#conda activate xesmf_stable_env

NUMFILES=62
START=$(python -c "print($SLURM_ARRAY_TASK_ID * $NUMFILES)")
END=$(python -c "print($START + $NUMFILES)")

srun python /home/pleta922/phdobj1/daily_stats.py -s $START -e $END
