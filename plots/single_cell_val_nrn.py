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
    nrn_data = {}
    for name, model in vars(dbbs_models).items():
        if name.endswith("Cell"):
            print("Running", name)
            nrn_data[name] = []
            cell = model()
            t = time.time()
            dbbs_models.test.quick_test(cell, duration=1000)
            nrn_data[name] = list(cell.Vm)
