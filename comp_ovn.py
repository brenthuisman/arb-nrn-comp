import dbbs_models as models
import sys
from patch import p
import plotly.graph_objs as go
import time

def run_nrn(setup, model, model_new, duration, v_init):
    if setup is not None:
        pass
    neuron_cell = model()
    neuron_cell.record_soma()
    neuron_cell_new = model_new()
    neuron_cell_new.record_soma()
    neuron_time = p.time
    p.dt = 0.025
    p.cvode.active(0)
    p.celsius = 32
    p.finitialize(v_init)
    p.continuerun(duration)
    return (neuron_time, neuron_cell.Vm), (neuron_time, neuron_cell_new.Vm)

if __name__ == "__main__":
    setups = {
        v: {"model": getattr(models, v), "new_model": getattr(models, v + "New")}
        for v in sys.argv
        if v.endswith("Cell")
    } or {
        name: {"model": model}
        for name, model in vars(models).items()
        if name.endswith("Cell")
    }
    for name, setup in setups.items():
        print(setup)
        model = setup["model"]
        model_new = setup["new_model"]
        print("Running", name)
        (nt, nv), (ot, ov) = run_nrn(None, model, model_new, 1000, -65)
        print("Setup", name, "finished")
        go.Figure(
            [
                go.Scatter(
                    x=nt,
                    y=nv,
                    name=f"{name} - NEURON"
                ),
                go.Scatter(
                    x=ot,
                    y=ov,
                    name=f"{name} - NEW"
                ),
            ]
        ).show()
