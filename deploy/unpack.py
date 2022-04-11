import os
import shutil
from pathlib import Path
from h5py import File
from dataclasses import dataclass

@dataclass
class Benchmark:
    name: str
    distributed: bool
    mpi_per_node: int
    threads: int
    gpu: bool
    time: str = "10:00:00"

    def __post_init__(self):
        self.simulator = "neuron" if "nrn_" in self.name else "arbor"
        self.size = "large" if self.distributed else "small"
        self.nodes = 20 if self.distributed else 1
        self.constraint = "gpu" if self.gpu else "mc"
        if "ACCOUNT" in os.environ:
            self.account = os.environ["ACCOUNT"]
        elif self.gpu:
            self.account = os.environ["GPU_ACCOUNT"]
        else:
            self.account = os.environ["CPU_ACCOUNT"]

    def fill_in(self, content):
        for k, v in vars(self).items():
            content = content.replace(f"@@{k}@@", str(v).lower())
        return content

benchmarks = [
    Benchmark("arb_small", False, 1, 1, False),
    Benchmark("nrn_small", False, 1, 1, False),
    Benchmark("nrn_distr", True, 36, 1, False),
]

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
