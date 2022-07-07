import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import math


def plot():
    bigger_path = Path(__file__).parent.parent / "results"
    matrix = np.load(str(bigger_path / "arbmatrix.npy"))
    m = np.mean(matrix, axis=1)
    print(matrix.shape, m.shape)
    matrix = np.load(str(bigger_path / "nrnmatrix.npy"))
    m = np.mean(matrix, axis=1) / m
    return go.Figure(
        go.Histogram(x=m, marker_line_width=0, marker_color="rgb(255,127,14)"),
        layout=dict(
            xaxis_title="Speedup factor",
            xaxis_range=[0, 20],
            yaxis_title="Count",
            bargap=0.0,
            bargroupgap=0.0,
        ),
    )
