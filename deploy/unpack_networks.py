import os
import shutil
from pathlib import Path
from h5py import File

root = Path(__file__).parent.parent
cfg_folder = root / "configs"
net_folder = root / "networks"
home_folder = Path(os.environ["HOME"])

def reconfigure(h, cfg):
    with File(str(h), "a") as f:
        with open(cfg, "r") as g:
            f.attrs["configuration_string"] = g.read()

for cfg_file in cfg_folder.iterdir():
  cfg_file = cfg_folder / cfg_file
  if "large" in str(cfg_file):
    net_file = net_folder / "large.hdf5"
  else:
    net_file = net_folder / "small.hdf5"
  out_h5 = str(home_folder / Path(cfg_file).stem) + ".hdf5"
  print("Deploying", cfg_file, "to", out_h5, "[large]" if "large" in str(cfg_file) else "")
  shutil.copy(net_file, out_h5)
  reconfigure(out_h5, cfg_file)
