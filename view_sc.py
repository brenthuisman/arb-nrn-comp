import pickle
import plotly.graph_objs as go

with open("arb_sc.pkl", "rb") as f, open("nrn_sc.pkl", "rb") as g:
    arb_sc = pickle.load(f)
    nrn_sc = pickle.load(g)

go.Figure([
    *(
        go.Scatter(
            x=data[0],
            y=data[1],
            name=name + " Arbor"
        )
        for name, data in arb_sc.items()
    ),
    *(
        go.Scatter(
            x=data[0],
            y=data[1],
            name=name + " NEURON"
        )
        for name, data in nrn_sc.items()
    ),
]).show()
