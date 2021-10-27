import pesticide as pst
import pesticide.benches as bench
from mpi4py.MPI import COMM_WORLD as comm

seed_gen = bench.seed("dbbs")
bed = bench.Bed(seed_gen, bench.TreatmentGen(pst.Nursery))
bench = bench.Bench([bed])
bench.run_benchmarks("100", 100)
