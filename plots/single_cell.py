import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import os
os.environ["USING_NEURON"] = "TRUE"
import dbbs_models
import dbbs_models.test
import time
import pickle
from arbor import single_cell_model

def plot():
    arb_data = {}
    if not os.path.exists("nrn_single_cell.pkl"):
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

        with open("nrn_single_cell.pkl", "wb") as f:
            pickle.dump(nrn_data, f)
    else:
        with open("nrn_single_cell.pkl", "rb") as f:
            nrn_data = pickle.load(f)
    if not os.path.exists("arb_single_cell.pkl"):
        for name, model in vars(dbbs_models).items():
            if name.endswith("Cell"):
                print("Running", name)
                arb_model = single_cell_model(model.cable_cell())
                arb_model.catalogue = model.get_catalogue()
                arb_model.properties.set_ion(
                    ion="h", valence=1, int_con=1.0, ext_con=1.0, rev_pot=-34
                )
                arb_data[name] = []
                cell = model()
                for _ in range(20):
                    print("Run", _)
                    t = time.time()
                    arb_model.run(10, dt=0.025)
                    arb_data[name].append(time.time() - t)

        with open("arb_single_cell.pkl", "wb") as f:
            pickle.dump(arb_data, f)
    else:
        with open("arb_single_cell.pkl", "rb") as f:
            arb_data = pickle.load(f)
    # Change the bar mode
    cnames = ["GranuleCell", "GolgiCell", "PurkinjeCell", "BasketCell", "StellateCell"]
    return go.Figure(
        data=[
            go.Bar(
                x=cnames,
                y=[np.mean(data[cname]) / 10 for cname in cnames],
                error_y=dict(
                    type="data",
                    array=[np.std(data[cname]) / 10 for cname in cnames],
                ),
                text=["" if int(n) == 1 else f"x{int(n)}" for n in (np.mean(nrn_data[cname]) / np.mean(data[cname]) for cname in cnames)],
                textposition="auto",
                name=sim,
            )
            for sim, data in zip(("NEURON", "Arbor"), (nrn_data, arb_data))
        ],
        layout=dict(
            barmode="group",
            xaxis_title="Cell type",
            yaxis_title="Runtime [s/ms]",
        ),
    )
