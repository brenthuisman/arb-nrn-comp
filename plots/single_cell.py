import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import dbbs_models
import time
import pickle

frozen = True

def plot():
    if frozen:
        with open("single_cell.pkl", "rb") as f:
            data = pickle.load(f)
    else:
        data = {}
        for name, model in vars(dbbs_models).items():
            if name.endswith("Cell"):
                data[name] = []
                cell = model()
                for _ in range(20):
                    t = time.time()
                    dbbs_models.quick_test(cell, duration=10)
                    data[name].append(time.time() - t)
        with open("single_cell.pkl", "wb") as f:
            pickle.dump(data, f)
    # Change the bar mode
    cnames = ["GranuleCell", "GolgiCell", "PurkinjeCell", "BasketCell", "StellateCell"]
    return go.Figure(
        data=[
            go.Bar(
                x=cnames,
                y=[np.mean(data[cname]) / spoof for cname in cnames],
                name=sim,
            )
            for sim, spoof in zip(("NEURON", "Arbor"), (10, 100))
        ],
        layout=dict(
            barmode="group",
            xaxis_title="Cell type",
            yaxis_title="Runtime [s/ms]",
        ),
    )
