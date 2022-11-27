#!/bin/bash
#SBATCH --account=girirajan
#SBATCH --partition=girirajan
#SBATCH --job-name=noncoding
#SBATCH -o /data5/Saakshi/datafiles/logs/noncoding_%a.log
#SBATCH -e /data5/Saakshi/datafiles/logs/noncoding_%a.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=400:0:0
#SBATCH --mem-per-cpu=40G
#SBATCH --chdir /data5/Saakshi/datafiles
#SBATCH --exclude ramona,durga
#SBATCH --array 1-24

echo `date` started on $HOSTNAME 

a=$SLURM_ARRAY_TASK_ID

# Absolute path to the directory containing datafiles
dir = /data5/Saakshi/datafiles

# Mapping Family IDs, Relationship (p1 and s1) to Sample IDs
python $dir/mapping.py $dir/${a}.7_with_freq.tsv $dir/nygc_sfari_id_map.csv $dir/${a}.8_mapped.tsv

echo `date` finished on $HOSTNAME