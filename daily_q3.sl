#!/bin/bash -e
#SBATCH --profile task

#SBATCH --job-name=qstats3
#SBATCH --account=uoo03104
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --hint=multithread
#SBATCH --mem=15G


#SBATCH --output=qstatsall2.1000.out
#SBATCH --error=qstatsall2.1000.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tamara.pletzer@postgrad.otago.ac.nz


#conda activate xesmf_stable_env

NUMFILES=1000
START=$(python -c "print($NUMFILES)")
END=$(python -c "print($NUMFILES + 1)")

cmd=srun python /home/pleta922/phdobj1/daily_q.py -s $START -e $END

echo $cmd

$cmd
