#!/bin/bash -e
#SBATCH --profile task

#SBATCH --job-name=quantile_j
#SBATCH --account=uoo03104
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --hint=multithread
#SBATCH --mem-per-cpu=1G
#SBATCH --array=10-100:10

#SBATCH --output=test.%j.out
#SBATCH --error=test.%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tamara.pletzer@postgrad.otago.ac.nz


# INDEX=$SLURM_ARRAY_TASK_ID
STEP=10

START=$(python -c "print($SLURM_ARRAY_TASK_ID - $STEP)")
END=$SLURM_ARRAY_TASK_ID

srun python /nesi/nobackup/uoo03104/quantile_alltest.py -s $START -e $END
