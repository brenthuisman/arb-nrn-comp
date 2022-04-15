import plotly.graph_objs as go
import os, sys
import pickle
import numpy as np
from scipy.signal import find_peaks
from plotly.subplots import make_subplots

# You can toggle this flag to run the simulation scripts locally, note that this requires
# the setup of the full simulation environment with Arbor, NEURON and specific patches of
# the DBBS toolchain.
def plot(run_locally=False):
    if run_locally:
        # Run the remote script, locally
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "remote"))
        # Importing the module runs the top level code, which rewrite the pickled data
        import single_cell_arb, single_cell_nrn

    with open("arb_sc.pkl", "rb") as f:
        arb_data = pickle.load(f)
    with open("nrn_sc.pkl", "rb") as f:
        nrn_data = pickle.load(f)

    figs = {}
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Stellate cell", "Basket cell", "Golgi cell", "Purkinje cell"),
        x_title="Spike pair",
        y_title="Interspike interval (ms)",
        specs=[
            [{"l":0.03, "t": 0.03}, {"t": 0.03}],
            [{"l":0.03, "b": 0.03}, {"b": 0.03}],
        ]
    )
    fig.update_layout(title="Single cell ISI")
    fig.update_annotations(font_size=35)
    ctr = 0
    for name, (nrn_t, nrn_v), (arb_t, arb_v) in ((name, nrn_data[name], arb_data[name]) for name in arb_data.keys()):
        if name == "GranuleCell":
            continue
        data = []
        for l, s, dt, c in (("NEURON", nrn_v, 0.025, "31,119,180"), ("Arbor", arb_v, 0.1, "255,127,14")):
            s = np.array(s)
            p, props = find_peaks(s, height=-10)
            isi = np.diff(p) * dt
            data.append(
                go.Scatter(
                    x=[*range(len(isi))],
                    y=isi,
                    name=l,
                    mode="lines+markers",
                    line=dict(color=f'rgb({c})'),
                    marker=dict(color=f'rgb({c})'),
                    legendgroup=l,
                    showlegend=not ctr
                ),
            )
        fig.add_traces(data, rows=(ctr // 2) + 1, cols=(ctr % 2) + 1)
        ctr += 1
        figs[name] = go.Figure(
            data=data,
            layout=dict(
                title_text=name,
                yaxis_title="Interspike interval (ms)",
                yaxis_rangemode="tozero",
                xaxis_title="Spike pair",
            ),
        )

    return fig
