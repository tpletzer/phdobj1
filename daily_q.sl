#!/bin/bash -e
#SBATCH --profile task

#SBATCH --job-name=qstats
#SBATCH --account=uoo03104
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=40:00:00
#SBATCH --hint=multithread
#SBATCH --mem=15G
#SBATCH --array=0-47

#SBATCH --output=qstatsall.%A_%a.out
#SBATCH --error=qstatsall.%A_%a.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tamara.pletzer@postgrad.otago.ac.nz


#conda activate xesmf_stable_env

NUMFILES=11
START=$(python -c "print($SLURM_ARRAY_TASK_ID * $NUMFILES)")
END=$(python -c "print($START + $NUMFILES)")

cmd=srun python /home/pleta922/phdobj1/daily_q.py -s $START -e $END

echo $cmd

$cmd
