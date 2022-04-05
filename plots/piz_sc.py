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
    with open("arb_sc.pkl", "rb") as f:
        pkl_data = pickle.load(f)
    return {
        name: go.Figure(go.Scatter(x=data[0], y=data[1]))
        for name, data in pkl_data.items()
    }
