import dbbs_models as models
import sys
from patch import p
import plotly.graph_objs as go
import time


def run_nrn(models, duration, v_init):
    for model in models:
        model.record_soma()
    neuron_time = p.time
    p.dt = 0.025
    p.cvode.active(0)
    p.celsius = 32
    p.finitialize(v_init)
    p.continuerun(duration)
    return list(neuron_time)


if __name__ == "__main__":
    name = sys.argv[1]
    model = getattr(models, name)
    model_old = getattr(models, name + "Old")
    cell = model()
    cell_old = model_old()
    models = [cell, cell_old]
    print("Running", name)
    t = run_nrn(models, 100, -65)
    print("Finished", name)
    go.Figure(
        [
            go.Scatter(x=t, y=list(model.Vm), name=name)
            for name, model in zip(("NEW", "OLD"), models)
        ]
    ).show()
