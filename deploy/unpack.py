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
        self.nodes = 20 if self.distributed else 1

    def fill_in(self, content):
        for k, v in vars(self).items():
            content = content.replace(f"@@{k}@@", v)
        return content

benchmarks = [
    Benchmark("arb_small", False, 1, 1, False)
]

root = Path(__file__).parent.parent
home_folder = Path(os.environ["HOME"])
net_folder = root / "networks"
jobs_folder = root / "jobs"
cfg_folder = root / "configs"
jobs_folder.mkdir(parents=True, exist_ok=True)
cfg_folder.mkdir(parents=True, exist_ok=True)

def reconfigure(h, cfg):
    with File(str(h), "a") as f:
        with open(cfg, "r") as g:
            f.attrs["configuration_string"] = g.read()

for benchmark in benchmarks:
  cfg_file = cfg_folder / (benchmark.name + ".json")
  net_file = net_folder / f"{benchmark.size}.hdf5"
  out_h5 = home_folder / f"{benchmark.name}.hdf5"
  print("Name:", benchmark.name)
  print("Simulator:", benchmark.simulator)
  print("GPU:", benchmark.gpu)
  if benchmark.distributed:
      print("Distr. scheme:")
      print(" ", benchmark.nodes, "nodes")
      print(" ", benchmark.mpi_per_node, "processes per node")
      print(" ", benchmark.threads, "threads per process")
  print("Deploying", cfg_file)
  shutil.copy(net_file, out_h5)
  reconfigure(out_h5, cfg_file)
