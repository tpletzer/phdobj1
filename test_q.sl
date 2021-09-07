#!/bin/bash -e
#SBATCH --profile task

#SBATCH --job-name=qtest94
#SBATCH --account=uoo03104
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=40:00:00
#SBATCH --hint=multithread
#SBATCH --mem=15G

#SBATCH --output=qtest94.%A_%a.out
#SBATCH --error=qtest94.%A_%a.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tamara.pletzer@postgrad.otago.ac.nz


#conda activate xesmf_stable_env
#JA=95+6 and numfiles=11-6
JA=94
NUMFILES=11
START=$(python -c "print($JA * $NUMFILES)")
END=$(python -c "print($START + $NUMFILES)")

cmd="srun python /home/pleta922/phdobj1/daily_q.py -s $START -e $END"

echo $cmd

$cmd
