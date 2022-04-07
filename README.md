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
source $HOME/arbenv/bin/activate
```

3. Clone the arbor environment toolchain

```
cd arbenv
git clone git@github.com:Helveg/arbor --recurse-submodules
cd arbor && git checkout aba80a93b169bee93aa693c0d612bd7f66b7e5dc && cd ..
git clone git@github.com:dbbs-lab/arborize
cd arborize && git checkout 2ab8e26050782c5ce218114e50ceb550ad94b751 && cd ..
git clone git@github.com:Helveg/bsb-1 bsb
cd bsb && git checkout 1cf5a247927b52a54f870f3f2680cd9f947a8d3f && cd ..
git clone git@github.com:dbbs-lab/catalogue
cd catalogue && git checkout eb2eaee1d0563dfdca0692514ae2e25650578156 && cd ..
git clone git@github.com:dbbs-lab/glia
cd glia && git checkout 5442e9e1485cab643b4a422449f338e7c6e8b5b5 && cd ..
git clone git@github.com:dbbs-lab/models
cd models && git checkout 5174d0e41efcb44c605f8e08992a6002733740dd && cd ..
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

You can now replicate Arbor instructions.

5. Activate the NEURON environment

```
source $HOME/nrnenv/bin/activate
```

6. Install NEURON and the toolchain:

```
pip install -e $HOME/arbenv/bsb[neuron]
pip install NEURON==8.1 dbbs-models==1.5.0rc0 arborize==2.0.0b8
```

# Plotting

The plotting script can be called as follows (module_names optional, if left out all plots are generated):

```
python plot [module_name(s)]
python build <format: html, svg, png> [module_name(s)]
```

You can install the required dependencies as listed under step 6 above:
```
pip install NEURON==8.1 arborize==2.0.0b8 dbbs-models==1.5.0rc0 plotly pandas sklearn h5py arbor==0.6
```
pip install -e packages/bsb
pip install -e packages/models
pip install -e packages/catalogue
pip install -e packages/arborize
pip install -e packages/glia