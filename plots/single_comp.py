import plotly.graph_objs as go
import os

run_locally = False

def plot():
    if run_locally:
        # Run the remote script, locally
        os.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "remote"))
        # Importing the module runs the top level code, which rewrite the pickled data
        import single_comp_sim

    with open("single_comp.pkl", "rb") as f:
        (arb_mechs, arb_samples), (time, mechs) = pickle.load(f)
    return go.Figure(
        [
            *[
                go.Scatter(x=sample[:, 0], y=sample[:, 1], name="Arbor", legendgroup=mech, legendgrouptitle_text=mech)
                for mech, sample in zip(arb_mechs, arb_samples)
            ],
            *[
                go.Scatter(x=time, y=trace, name="NEURON", legendgroup=mech, legendgrouptitle_text=mech)
                for mech, trace in mechs.items()
            ]
        ]
    )
