import os
import sys
import pathlib

args = sys.argv[1:]
name = args[0]
ids_path = pathlib.Path(args[1]).parent
ids = pandas.read_csv(args[1])
if len(args) > 2:
    log_dir = pathlib.Path(args[2])
else:
    log_dir = ids_path.copy()
home = pathlib.Path(os.getenv("HOME"))
batch_dir = home / "results" / name
batch_dir.mkdir(parents=True, exist_ok=False)

for id in ids:
    print(id)
