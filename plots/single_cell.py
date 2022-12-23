import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import time
import pickle

# You can toggle this flag to run the simulation scripts locally, note that this requires
# the setup of the full simulation environment with Arbor, NEURON and specific patches of
# the DBBS toolchain.
def plot(run_locally=False):
    if run_locally:
        # Run the remote script, locally
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "remote"))
        # Importing the module runs the top level code, which rewrite the pickled data
        import single_cell_time_arb, single_cell_time_nrn

    arb_data = {}
    with open("nrn_sc_time.pkl", "rb") as f:
        nrn_data = pickle.load(f)
    with open("arb_sc_time.pkl", "rb") as f:
        arb_data = pickle.load(f)
    # Change the bar mode
    cnames = ["GranuleCell", "GolgiCell", "PurkinjeCell", "BasketCell", "StellateCell"]
    clabels = ["Granule", "Golgi", "Purkinje", "Basket", "Stellate"]
    return go.Figure(
        data=[
            go.Scatter(
                x=clabels,
                y=[np.mean(nrn_data[cname]) / np.mean(arb_data[cname]) for cname in cnames],
                error_y=dict(
                    type="data",
                    array=[np.sqrt((np.mean(nrn_data[cname]) ** 2 / np.mean(arb_data[cname]) ** 2) * (np.var(nrn_data[cname]) ** 2 / np.mean(nrn_data[cname]) ** 2 + np.var(arb_data[cname]) ** 2 / np.mean(arb_data[cname]) ** 2)) for cname in cnames],
                    thickness=5,
                    width=15,
                ),
                marker=dict(color=f'rgb(255,127,14)', size=15),
                mode="markers",
                name="Speedup",
            )
        ],
        layout=dict(
            barmode="group",
            xaxis_title="Cell type",
            yaxis_title="Speedup factor",
            yaxis_rangemode="tozero",
            xaxis_tickangle=15,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.70),
        ),
    )
