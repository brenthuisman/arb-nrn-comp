Compares all DBBS models in Arbor and NEURON

# Replication

A no warranty list of steps to reproduce the findings in https://www.biorxiv.org/content/10.1101/2022.03.02.482285v1.full

These steps work on PizDaint, which uses [`slurm`](https://slurm.schedmd.com/documentation.html) for job management and [`modules`](http://modules.sourceforge.net/) for environment management.

1. Create separate environments for the Arbor and NEURON toolchains

```
cd $HOME
python -m venv arbenv
python -m venv nrnenv
```

2. Activate the Arbor venv:

```
source arbenv/bin/activate
```

3. Clone the arbor environment toolchain

```
cd arbenv
git clone git@github.com:arbor-sim/arbor --recurse-submodules
cd arbor && git checkout aba80a93b169bee93aa693c0d612bd7f66b7e5dc && git cd ..
git clone git@github.com:dbbs-lab/arborize
cd arborize && git checkout bcda075d4ea63bb5846d4edbff669c32a380bf1b && cd ..
git clone git@github.com:Helveg/bsb-1 bsb
cd bsb && git checkout 1bcfc0132b98455962dc0fea59a50b731d45971b && cd ..
git clone git@github.com:dbbs-lab/catalogue
cd catalogue && git checkout eb2eaee1d0563dfdca0692514ae2e25650578156 && cd ..
git clone git@github.com:dbbs-lab/glia
cd glia && git checkout 44adc91575f15a98813cd69a43a7e34d0a63b570 && cd ..
git clone git@github.com:dbbs-lab/models
cd models && git checkout 3931b4dd49577703179d9b083471be1c363fc10c && cd ..
```

3. Install the Python tools (in this order!)

```
CC=cc CXX=CC pip install mpi4py
pip install -e bsb
pip install -e models
pip install -e catalogue
pip install -e arborize
pip install -e glia
```

4. Build `arbor`:

```
mkdir arbor/build
cd arbor/build
module load daint-gpu cudatoolkit CMake gcc/9.3.0
module switch PrgEnv-cray PrgEnv-gnu
CC=cc CXX=CC cmake .. \
  -DARB_WITH_MPI=ON \
  -DARB_WITH_PROFILING=OFF \
  -DARB_GPU=cuda \
  -DARB_USE_BUNDLED_LIBS=ON \
  -DCMAKE_INSTALL_PREFIX=$HOME/arbenv \
  -DARB_WITH_PYTHON=ON \
  -DARB_VECTORIZE=ON
make install -j 8
cd $HOME
```

More details coming soon
