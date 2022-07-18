import plotly.graph_objs as go
import os, sys
import pickle

# You can toggle this flag to run the simulation scripts locally, note that this requires
# the setup of the full simulation environment with Arbor, NEURON and specific patches of
# the DBBS toolchain.
def plot(run_locally=False):
    if run_locally:
        # Run the remote script, locally
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "remote"))
        # Importing the module runs the top level code, which rewrite the pickled data
        import single_cell_val_arb, single_cell_val_nrn

    with open("arb_sc.pkl", "rb") as f:
        arb_data = pickle.load(f)
    with open("nrn_sc.pkl", "rb") as f:
        nrn_data = pickle.load(f)
    fig = go.Figure().set_subplots(
        rows=1,
        cols=4,
        subplot_titles=("Stellate cell", "Basket cell", "Golgi cell", "Purkinje cell"),
        y_title="Vm (mV)",
        x_title="Time (ms)",
        specs=[[{"l": 0.01, "b": 0.05}, {"b": 0.05}, {"b": 0.05}, {"b": 0.05}]]
    )
    fig.update_layout(title="Single cell Vm")
    fig.update_annotations(font_size=35)
    ctr = 0
    for name in arb_data.keys():
        if name == "GranuleCell":
            continue
        fig.add_traces(
            [
                go.Scatter(
                    x=(data := nrn_data[name])[0],
                    y=data[1],
                    name="NEURON",
                    line=dict(color=f'rgb(31,119,180)', width=1),
                    marker=dict(color=f'rgb(31,119,180)'),
                    legendgroup="n",
                    showlegend=not ctr
                ),
                go.Scatter(
                    x=(data := arb_data[name])[0],
                    y=data[1],
                    name="Arbor",
                    line=dict(color=f'rgb(255,127,14)', width=1),
                    marker=dict(color=f'rgb(255,127,14)'),
                    legendgroup="a",
                    showlegend=not ctr
                ),
            ],
            rows=1, cols=ctr + 1
        )
        ctr += 1

    # fig.update_yaxes(range=[-75, 55])
    # for i in range(2, 5):
    #     fig.update_yaxes(showticklabels=False, row=1, col=i)

    return fig

def meta():
    return {"width": 700 * 4, "height": 800}
