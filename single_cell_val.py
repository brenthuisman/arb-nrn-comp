from pathlib import Path
import numpy as np
import os
import time
import pickle
import arborize
import dbbs_models
import arbor
import glia
from arbor import single_cell_model
import pickle
import plotly.graph_objs as go

arb_data = {}
pkl_data = {}
for name, model in vars(dbbs_models).items():
    if name.endswith("Cell"):
        print("Running", name, f"on {arborize.__version__}", flush=True)
        if arborize.__version__ == "2.0.3":
            cc = model.cable_cell(labels=arbor.label_dict({"midpoint": "(root)"}))
            cat = model.get_catalogue()
        else:
            cc = model.cable_cell(Vm=-65)
            cat = arbor.default_catalogue()
            cat.extend(glia.catalogue("dbbs"), "")
        arbor.write_component(cc, f"{name}.acc")
        arb_model = single_cell_model(cc)
        arb_model.properties.set_property(Vm=-65, tempK=305.15)
        arb_model.properties.set_ion(
            ion="h", valence=1, int_con=1.0, ext_con=1.0, rev_pot=-34
        )
        arb_model.properties.set_ion(
            ion="cal",
            int_con=0.00005,
            ext_con=2.0,
            rev_pot=132.5,
            valence=2,
        )
        arb_model.properties.catalogue = cat
        arb_model.probe("voltage", '"midpoint"', frequency=10)
        arb_model.run(1000, dt=0.025)
        pkl_data[name] = (arb_model.traces[0].time, arb_model.traces[0].value)

go.Figure(
    [go.Scatter(name=name, x=v[0], y=v[1]) for name, v in pkl_data.items()]
).show()
with open("arb_sc.pkl", "wb") as f:
    pickle.dump(pkl_data, f)
