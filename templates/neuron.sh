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
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/cray/pe/mpt/7.7.18/gni/mpich-crayclang/10.0/lib

## if: coreneuron and not gpu
## source $HOME/corenrn/bin/activate
## nrnivmodl -coreneuron $HOME/corenrn/dbbs-mod-collection/dbbs_mod_collection/mod
## if: coreneuron and gpu
## source $HOME/corenrn-gpu/bin/activate
## nrnivmodl -coreneuron -gpu $HOME/corenrn/dbbs-mod-collection/dbbs_mod_collection/mod
## if: coreneuron
## export GLIA_NOCOMPILE=TRUE
## export GLIA_NOLOAD=TRUE
## if: not coreneuron
## source $HOME/nrnenv/bin/activate

srun bsb -v 4 simulate @@name@@ --hdf5=$HOME/arb-nrn-benchmarks-rdsea-2022/models/@@name@@.hdf5
