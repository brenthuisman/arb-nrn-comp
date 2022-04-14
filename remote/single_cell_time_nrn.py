import os

os.environ["USING_NEURON"] = "TRUE"
import dbbs_models
import dbbs_models.test
import pickle

nrn_data = {}
for name, model in vars(dbbs_models).items():
    if name.endswith("Cell"):
        print("Running", name)
        nrn_data[name] = []
        cell = model()
        for _ in range(20):
            print("Run", _)
            t = time.time()
            dbbs_models.test.quick_test(cell, duration=10)
            nrn_data[name].append(time.time() - t)

with open("nrn_sc_time.pkl", "wb") as f:
    pickle.dump(nrn_data, f)
