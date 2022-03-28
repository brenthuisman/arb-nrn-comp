import dbbs_models as models
import sys
from patch import p
import plotly.graph_objs as go
import time
import numpy as np


def run_nrn(setup, model, model_old, duration, v_init):
    if setup is not None:
        pass
    neuron_cell = model()
    rv = [
        p.record(neuron_cell.sections[sroi])
        for sroi in range(len(neuron_cell.sections))
    ]
    for s in neuron_cell.sections:
        syn = p.ExpSyn(s)
        syn.stimulate(start=10, number=1)
    neuron_cell_old = model_old()
    for s in neuron_cell_old.sections:
        syn = p.ExpSyn(s)
        syn.stimulate(start=10, number=1)
    rv2 = [
        p.record(neuron_cell.sections[sroi])
        for sroi in range(len(neuron_cell_old.sections))
    ]
    neuron_time = p.time
    p.dt = 0.025
    p.cvode.active(0)
    p.celsius = 32
    p.finitialize(v_init)
    p.continuerun(duration)
    return (neuron_time, [np.array(x) - np.array(x2) for x, x2 in zip(rv, rv2)])


if __name__ == "__main__":
    setups = {
        v: {"model": getattr(models, v), "model_old": getattr(models, v + "Old")}
        for v in sys.argv
        if v.endswith("Cell")
    } or {
        name: {"model": model}
        for name, model in vars(models).items()
        if name.endswith("Cell")
    }
    sroi = 1
    for name, setup in setups.items():
        print(setup)
        model = setup["model"]
        model_old = setup["model_old"]
        print("Running", name)
        t, dvs = run_nrn(None, model, model_old, 100, -65)
        print("Setup", name, "finished")
        go.Figure(
            [go.Scatter(x=t, y=dv, name=f"diff {sroi}") for sroi, dv in enumerate(dvs)]
        ).show()
