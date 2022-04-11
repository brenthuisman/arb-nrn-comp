#!/bin/bash -l
#SBATCH --job-name="@@name@@"
#SBATCH --account="@@account@@"
#SBATCH --time=@@time@@
#SBATCH --nodes=@@nodes@@
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=@@mpi_per_node@@
#SBATCH --cpus-per-task=@@threads@@
#SBATCH --partition=normal
#SBATCH --constraint=@@constraint@@
#SBATCH --hint=nomultithread

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export HDF5_USE_FILE_LOCKING=FALSE
source $HOME/nrnenv/bin/activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/cray/pe/mpt/7.7.18/gni/mpich-crayclang/10.0/lib

srun bsb -v 4 simulate @@name@@ --hdf5=$HOME/arb-nrn-benchmarks-rdsea-2022/models/@@name@@.hdf5
