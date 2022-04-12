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
    nodes: int = None

    def __post_init__(self):
        self.simulator = "neuron" if "nrn_" in self.name else "arbor"
        self.size = "large" if self.distributed else "small"
        if self.nodes is None:
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
    Benchmark("arb_small_st", False, 1, 1, False),
    Benchmark("arb_small_mpi", False, 36, 1, False),
    Benchmark("arb_small_mt", False, 1, 36, False),
    Benchmark("arb_small_ht", False, 1, 72, False),
    Benchmark("arb_small_gpu", False, 1, 12, True),
    Benchmark("arb_small_sock", False, 1, 18, True),

    Benchmark("arb_distr_mpi", True, 36, 1, False),
    Benchmark("arb_distr_mt", True, 2, 18, False),
    Benchmark("arb_distr_ht", True, 2, 36, False),
    Benchmark("arb_gpu_20", True, 2, 12, True),
    Benchmark("arb_gpu_16", True, 2, 12, True, nodes=16),
    Benchmark("arb_gpu_12", True, 2, 12, True, nodes=12),
    Benchmark("arb_gpu_10", True, 2, 12, True, nodes=10),
    Benchmark("arb_gpu_8", True, 2, 12, True, nodes=8),
    Benchmark("arb_gpu_6", True, 2, 12, True, nodes=6),
    Benchmark("arb_gpu_4", True, 2, 12, True, nodes=4),
    Benchmark("arb_gpu_2", True, 2, 12, True, nodes=2),
    Benchmark("arb_gpu_1", True, 2, 12, True, nodes=1),

    Benchmark("nrn_small", False, 1, 1, False),
    Benchmark("nrn_sock", False, 18, 1, False),
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
