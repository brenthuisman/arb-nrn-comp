from pathlib import Path
from glob import glob
import pandas as pd
import subprocess
import sys
import os
import re

success = re.compile("Submitted batch job (\d+)")
root_folder = Path(__file__).parent.parent
home_folder = Path(os.environ["HOME"])
deploy_folder = home_folder / "arb-nrn-benchmarks-rdsea-2022"
job_folder = deploy_folder / "jobs"

def get_jobscripts():
    return glob(str(job_folder / "*.sh"))

def get_re(*filters):
    print("pattern:", "^.*([^\/]*(" + ("|".join(filters)) + ")[^\/]*)\.sh$")
    return re.compile("^.*([^\/]*(" + ("|".join(filters)) + ")[^\/]*)\.sh$")

def get_process_id(pipes):
    out, err = pipes
    if err:
        return "ERR"
    else:
        return success.match(out).groups(1)[0]

def get_process_error(pipes):
    out, err = pipes
    return err

args = sys.argv.copy()
times = [int(x[1:]) for x in args if x.startswith("x")]
xtime = times[-1] if len(times) > 0 else 10
args = [x for x in args if not x.startswith("x")]
jobscripts = get_jobscripts()
pattern = get_re(*args[1:])
to_run = {m.groups(1)[0]: job for job in jobscripts if (m := pattern.match(job))}

print("Queue", xtime, "times")
print("\n".join(f" {x}" for x in to_run))

processes = {
    name: [
        subprocess.Popen(
            f"sbatch {script}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            encoding="utf-8"
        )
        for _ in range(xtime)
    ]
    for name, script in to_run.items()
}
blocks = []
while processes:
    name, proclist = next(iter(processes.items()))
    output = [proc.communicate() for proc in proclist]
    del processes[name]
    df = pd.DataFrame({"id": map(get_process_id, output), "name": [name] * xtime, "err": map(get_process_error, output)})
    blocks.append(df)
pd.concat(blocks).to_csv("jobids.csv", index=False)
