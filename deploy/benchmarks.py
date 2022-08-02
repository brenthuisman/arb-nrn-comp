from dataclasses import dataclass, field
import typing, os

@dataclass
class Benchmark:
    id: int
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
            self.srun_argstr = " " + " ".join(f"{arg}" for arg in self.srun_args)
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
    Benchmark(2, "arb_small_st", False, 1, 1, False),
    Benchmark(28, "arb_small_mpi", False, 36, 1, False),
    Benchmark(3, "arb_small_mt", False, 1, 36, False),
    Benchmark(4, "arb_small_ht", False, 1, 72, False),
    Benchmark(5, "arb_small_gpu", False, 1, 1, True),
    Benchmark(13, "arb_small_sock", False, 1, 18, True),

    Benchmark(7, "arb_distr_mpi", True, 36, 1, False),
    Benchmark(8, "arb_distr_mt", True, 2, 18, False),
    Benchmark(9, "arb_distr_ht", True, 2, 36, False),
    Benchmark(18, "arb_gpu_20", True, 1, 12, True),
    Benchmark(17, "arb_gpu_16", True, 1, 12, True, nodes=16),
    Benchmark(16, "arb_gpu_12", True, 1, 12, True, nodes=12),
    Benchmark(21, "arb_gpu_10", True, 1, 12, True, nodes=10),
    Benchmark(15, "arb_gpu_8", True, 1, 12, True, nodes=8),
    Benchmark(22, "arb_gpu_6", True, 1, 12, True, nodes=6),
    Benchmark(12, "arb_gpu_4", True, 1, 12, True, nodes=4),
    Benchmark(11, "arb_gpu_2", True, 1, 12, True, nodes=2),
    Benchmark(10, "arb_gpu_1", True, 1, 12, True, nodes=1),

    Benchmark(1, "nrn_small", False, 1, 1, False),
    Benchmark(19, "nrn_small_mpi", False, 36, 1, False),
    Benchmark(20, "nrn_small_hmpi", False, 72, 1, False, srun_args=["--oversubscribe"]),
    Benchmark(14, "nrn_small_sock", False, 18, 1, False),
    Benchmark(6, "nrn_distr", True, 36, 1, False),
    Benchmark(23, "cnrn_small", False, 1, 1, False),
    Benchmark(24, "cnrn_small_mpi", False, 36, 1, False),
    Benchmark(25, "cnrn_small_mt", False, 1, 36, False),
    Benchmark(26, "cnrn_small_gpu", False, 1, 12, True),
    Benchmark(27, "cnrn_distr", True, 36, 1, False),
]
