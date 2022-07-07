import plotly.graph_objs as go
import os
import dbbs_models
import arbor
import pickle


pkl_data = {}
for name, model in vars(dbbs_models).items():
    if name.endswith("Cell"):
        print("Running", name, flush=True)
        arb_model = arbor.single_cell_model(
            model.cable_cell(labels=arbor.label_dict({"midpoint": "(root)"}))
        )
        arb_model.properties.set_ion(
            ion="h", valence=1, int_con=1.0, ext_con=1.0, rev_pot=-34
        )
        arb_model.properties.set_property(Vm =-65, tempK=305.15, rL=35.4, cm=0.01)
        arb_model.properties.catalogue = model.get_catalogue()
        arb_model.probe("voltage", '"midpoint"', frequency=10)
        arb_model.run(1000, dt=0.025)
        pkl_data[name] = (arb_model.traces[0].time, arb_model.traces[0].value)
with open("arb_sc.pkl", "wb") as f:
    pickle.dump(pkl_data, f)
