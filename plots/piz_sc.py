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
    with open("arb_sc.pkl", "rb") as f:
        arb_data = pickle.load(f)
    with open("nrn_sc.pkl", "rb") as f:
        nrn_data = pickle.load(f)
    return {
        name: go.Figure([
            go.Scatter(
                x=(data := arb_data[name])[0],
                y=data[1],
                name="Arbor",
            ),
            go.Scatter(
                x=(data := nrn_data[name])[0],
                y=data[1],
                name="NEURON",
            ),
        ])
        for name in arb_data.keys()
    }
