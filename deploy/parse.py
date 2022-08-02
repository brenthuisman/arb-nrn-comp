import re
import os
import sys
import pathlib
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from benchmarks import benchmarks
import csv
import shutil

args = sys.argv[1:]
name = args[0]
ids_path = pathlib.Path(args[1]).parent
ids = pd.read_csv(args[1])
if len(args) > 2:
    log_dir = pathlib.Path(args[2])
else:
    log_dir = ids_path
home = pathlib.Path(os.getenv("HOME"))
batch_dir = pathlib.Path(__file__).parent.parent / "results" / name
batch_dir.mkdir(parents=True, exist_ok=False)
out = [["job_id","bench_name","bench_id","nodes","tts","spms","e","nh","usage"]]

float_pat = re.compile(r"([\d\.]+)")

for line, row in ids.iterrows():
    id, name, err = row
    bench = next((b for b in benchmarks if b.name == name), None)
    if bench is None:
        print(f"Unknown benchmark `{name}`")
        continue
    with open(log_dir / f"slurm-{id}.out", "r") as f:
        log = f.readlines()
    try:
        tms = [l for l in log if l.startswith("Simulated ")][-1]
    except IndexError:
        logged = False
    else:
        logged = True
    dline = next((i + 4 for i, l in enumerate(log) if l == "Job information (1/3)\n"), None)
    eline = next((i + 4 for i, l in enumerate(log) if l == "Job information (2/3)\n"), None)
    tail = not (dline is None or eline is None)
    if logged and tail:
        spms = float(float_pat.search(tms.split("tick")[-1])[0])
        to_sec = lambda ts: sum(int(x) * 60 ** i for i, x in enumerate(reversed(ts.split(':'))))
        tts = to_sec([l for l in log[dline][:-1].split(" ") if l][-2])
        e = float([l for l in log[eline][:-1].split(" ") if l][-2])
        out.append([id, name, bench.id, bench.nodes, tts, spms, e, bench.nodes * tts / 3600])
    else:
        print(id, "errored")

with open(batch_dir / "jobs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(out)

for line, row in ids.iterrows():
    shutil.move(log_dir / f"slurm-{row[0]}.out", batch_dir)

print(len(ids), "logfiles parsed and moved to '{batch_dir}'")
