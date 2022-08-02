import os
import sys
import pathlib
import pandas as pd

args = sys.argv[1:]
name = args[0]
ids_path = pathlib.Path(args[1]).parent
ids = pd.read_csv(args[1])
if len(args) > 2:
    log_dir = pathlib.Path(args[2])
else:
    log_dir = ids_path
home = pathlib.Path(os.getenv("HOME"))
batch_dir = home / "results" / name
batch_dir.mkdir(parents=True, exist_ok=False)

for line, row in ids.iterrows():
    print(row)
    id, name, err = row
    with open(log_dir / f"slurm-{id}.out", "r") as f:
        log = f.readlines()
    tms = [l for l in log if l.startswith("Simulated ")][-1]
    dline = next((i + 2 for i, l in enumerate(log) if l == "Job information (1/3)\n"), None)
    eline = next((i + 2 for i, l in enumerate(log) if l == "Job information (2/3)\n"), None)
    print(tms, dline, eline)
