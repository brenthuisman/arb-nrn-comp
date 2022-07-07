import os
import shutil
from pathlib import Path
from h5py import File
from dataclasses import dataclass, field
import typing

@dataclass
class Benchmark:
    name: str
    distributed: bool
    mpi_per_node: int
    threads: int
    gpu: bool
    time: str = "10:00:00"
    nodes: int = None
    srun_args: typing.List[str] = field(default_factory=list)

    def __post_init__(self):
        self.simulator = "neuron" if "nrn_" in self.name else "arbor"
        self.size = "large" if self.distributed else "small"
        if self.nodes is None:
            self.nodes = 20 if self.distributed else 1
        self.constraint = "gpu" if self.gpu else "mc"
        self.coreneuron = "cnrn" in self.name
        if "ACCOUNT" in os.environ:
            self.account = os.environ["ACCOUNT"]
        elif self.gpu:
            self.account = os.environ["GPU_ACCOUNT"]
        else:
            self.account = os.environ["CPU_ACCOUNT"]
        if self.srun_args:
            self.srun_argstr = " " + " ".join(f"{arg}" for arg in srun_args)
        else:
            self.srun_argstr = ""

    def fill_in(self, content):
        for k, v in vars(self).items():
            content = content.replace(f"@@{k}@@", str(v).lower())
        content_lines = content.split("\n")
        parsed_ifs = []
        for i, line in enumerate(content_lines):
            if line.startswith("## if:"):
                parsed_ifs.append(self.parse_if(content_lines, i))
        for start, end, replace in reversed(parsed_ifs):
            content_lines[start:end] = replace
        return "\n".join(content_lines)

    def parse_if(self, lines, start):
        end = next(
            i for i in range(start + 1, len(lines))
            if lines[i].startswith("## if:") or not lines[i].startswith("## ")
        )
        if bool(eval(lines[start][6:], self.__dict__)):
            replace = [line[3:] for line in lines[start + 1 : end]]
        else:
            replace = []
        return start, end, replace



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
    Benchmark("nrn_small", False, 1, 1, False),
    Benchmark("nrn_small_mpi", False, 36, 1, False),
    Benchmark("nrn_small_hmpi", False, 72, 1, False, srun_args=["--oversubscribe"]),
    Benchmark("nrn_small_sock", False, 18, 1, False),
    Benchmark("nrn_distr", True, 36, 1, False),
    Benchmark("cnrn_small", False, 1, 1, False),
    Benchmark("cnrn_small_mpi", False, 36, 1, False),
    Benchmark("cnrn_small_mt", False, 1, 36, False),
    Benchmark("cnrn_small_gpu", False, 1, 12, True),
    Benchmark("cnrn_distr", True, 36, 1, False),
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
