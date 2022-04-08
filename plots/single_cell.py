import plotly.graph_objs as go
import os
import pickle

# You can toggle this flag to run the simulation scripts locally, note that this requires
# the setup of the full simulation environment with Arbor, NEURON and specific patches of
# the DBBS toolchain.
run_locally = False

def plot():
    if run_locally:
        # Run the remote script, locally
        os.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "remote"))
        # Importing the module runs the top level code, which rewrite the pickled data
        import single_cell_val_arb, single_cell_val_nrn

    with open("arb_sc.pkl", "rb") as f:
        arb_data = pickle.load(f)
    with open("nrn_sc.pkl", "rb") as f:
        nrn_data = pickle.load(f)
    return {
        name: go.Figure([
            go.Scatter(
                x=(data := arb_data[name])[0],
                y=data[1],
                name="Arbor",
            ),
            go.Scatter(
                x=(data := nrn_data[name])[0],
                y=data[1],
                name="NEURON",
            ),
        ])
        for name in arb_data.keys()
    }
