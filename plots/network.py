import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import dbbs_models
import time
import pickle

frozen = False

def plot():
    og = 40.3
    names = ["NEURON", "Arbor", "vectorization", "36 threads", "gpu"]
    data = [40.3, 10.57, 6.33, 0.27, 0.15]
    texts = [None, "x4", "x6", "x150", "x270"]
    return go.Figure(
        data=[
            go.Bar(
                x=names,
                y=data,
                text=texts,
                textposition="auto"
            )
        ],
        layout=dict(
            barmode="group",
            xaxis_title="Simulations",
            yaxis_title="Runtime [s/ms]"
        ),
    )
