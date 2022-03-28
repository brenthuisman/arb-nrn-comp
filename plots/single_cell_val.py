import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import os
import time
import pickle
import dbbs_models
import arbor
from arbor import single_cell_model
import pickle


def plot():
    arb_data = {}
    pkl_data = {}
    for name, model in vars(dbbs_models).items():
        if name.endswith("Cell"):
            print("Running", name, flush=True)
            arb_model = single_cell_model(
                model.cable_cell(labels=arbor.label_dict({"midpoint": "(root)"}))
            )
            arb_model.properties.set_ion(
                ion="h", valence=1, int_con=1.0, ext_con=1.0, rev_pot=-34
            )
            arb_model.properties.catalogue = model.get_catalogue()
            arb_model.probe("voltage", '"midpoint"', frequency=10)
            arb_model.run(1000, dt=0.025)
            arb_data[name] = go.Figure(
                go.Scatter(x=arb_model.traces[0].time, y=arb_model.traces[0].value)
            )
            pkl_data[name] = (arb_model.traces[0].time, arb_model.traces[0].value)
    with open("arb_sc.pkl", "wb") as f:
        pickle.dump(pkl_data, f)
    return arb_data
