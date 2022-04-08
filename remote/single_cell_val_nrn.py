import os

os.environ["USING_NEURON"] = "TRUE"
import dbbs_models
import dbbs_models.test
import time
import pickle
from patch import p

pkl_data = {}
for name, model in vars(dbbs_models).items():
    if name.endswith("Cell"):
        print("Running", name, flush=True)
        cell = model()
        time = p.time
        dbbs_models.test.quick_test(cell, duration=1000)
        pkl_data[name] = (list(time), list(cell.Vm))
with open("nrn_sc.pkl", "wb") as f:
    pickle.dump(pkl_data, f)
