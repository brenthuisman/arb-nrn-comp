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
            go.Bar(
                x=clabels,
                y=[np.mean(data[cname]) / 10 for cname in cnames],
                error_y=dict(
                    type="data",
                    array=[np.std(data[cname]) / 10 for cname in cnames],
                ),
                textposition="auto",
                name=sim,
            )
            for sim, data in zip(("NEURON", "Arbor"), (nrn_data, arb_data))
        ],
        layout=dict(
            barmode="group",
            xaxis_title="Cell type",
            yaxis_title="Timestep duration (s<sub>wall</sub>/ms<sub>bio</sub>)",
            xaxis_tickangle=15,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.70),
        ),
    )
