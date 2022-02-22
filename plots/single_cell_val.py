import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import os
import time
import pickle
import dbbs_models
from arbor import single_cell_model

def plot():
    arb_data = {}
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
            arb_model.run(1000, dt=0.025)
            arb_data[name].append()
