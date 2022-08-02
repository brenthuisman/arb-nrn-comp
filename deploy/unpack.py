import os
import shutil
from pathlib import Path
from h5py import File
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from benchmarks import benchmarks

root_folder = Path(__file__).parent.parent
home_folder = Path(os.environ["HOME"])
net_folder = root_folder / "networks"
templ_folder = root_folder / "templates"
deploy_folder = home_folder / "arb-nrn-benchmarks-rdsea-2022"
model_folder = deploy_folder / "models"
job_folder = deploy_folder / "jobs"
cfg_folder = deploy_folder / "configs"
model_folder.mkdir(parents=True, exist_ok=True)
job_folder.mkdir(parents=True, exist_ok=True)
cfg_folder.mkdir(parents=True, exist_ok=True)

def reconfigure(h, cfg):
    with File(str(h), "a") as f:
        with open(cfg, "r") as g:
            f.attrs["configuration_string"] = g.read()

for benchmark in benchmarks:
    cfg_file = cfg_folder / f"{benchmark.name}.json"
    job_file = job_folder / f"{benchmark.name}.sh"
    net_file = net_folder / f"{benchmark.size}.hdf5"
    out_file = model_folder / f"{benchmark.name}.hdf5"
    print("Name:", benchmark.name)
    if benchmark.simulator == "neuron" and benchmark.coreneuron:
        print("Simulator:", "coreneuron")
    else:
        print("Simulator:", benchmark.simulator)
    print("GPU:", benchmark.gpu)
    if benchmark.distributed:
        print("Distr. scheme:")
        print(" ", benchmark.nodes, "nodes")
        print(" ", benchmark.mpi_per_node, "processes per node")
        print(" ", benchmark.threads, "threads per process")
    print("Creating", cfg_file)
    with open(cfg_file, "w") as c:
        with open(templ_folder / f"{benchmark.simulator}.json", "r") as t:
            c.write(benchmark.fill_in(t.read()))

    print("Creating", job_file)
    with open(job_file, "w") as j:
        with open(templ_folder / f"{benchmark.simulator}.sh", "r") as t:
            j.write(benchmark.fill_in(t.read()))

    print("Deploying", cfg_file)
    shutil.copy(net_file, out_file)
    reconfigure(out_file, cfg_file)
    print("---")
    print()
