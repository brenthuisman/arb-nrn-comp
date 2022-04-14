import plotly.graph_objs as go
import os, sys
import pickle
import numpy as np
from scipy.signal import find_peaks

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
    for name, (nrn_t, nrn_v), (arb_t, arb_v) in ((name, nrn_data[name], arb_data[name]) for name in arb_data.keys()):
        data = []
        for l, s, dt in (("arbor", arb_v, 0.1), ("neuron", nrn_v, 0.025)):
            s = np.array(s)
            p, props = find_peaks(s, height=-10)
            isi = np.diff(p) * dt
            data.append(
                go.Scatter(
                    x=[*range(len(isi))],
                    y=isi,
                    name=l,
                    mode="lines+markers",
                ),
            )
        figs[name] = go.Figure(
            data=data,
            layout=dict(
                title_text=name,
                yaxis_title="Interspike interval (ms)",
                yaxis_rangemode="tozero",
                xaxis_title="Spike pair",
            ),
        )

    return figs
