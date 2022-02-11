import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import pandas as pd

def plot():
    job_data = pd.read_csv("jobs.csv")
    job_data["tts"] = pd.to_timedelta(job_data["tts"]).dt.total_seconds()
    benches = job_data.groupby(["bench_id"]).agg({
        "bench_name": "first",
        "tts": "mean",
        "nodes": "first",
        "e": "mean",
        "spms": "mean",
    })
    benches_err = job_data.groupby(["bench_id"]).agg({
        "bench_name": "first",
        "tts": "mean",
        "nodes": "first",
        "e": "mean",
        "spms": "mean",
    })
    benches.loc[6:9, "bench_name"] = ("NEURON", "Arbor", "Multithreaded", "Hyperthreaded")
    benches["nh"] = benches["tts"] * benches["nodes"]
    spacebar = (0, 6, 9, 10)
    return {
        cat: go.Figure(
            data=[
                go.Bar(
                    x=benches["bench_name"].loc[6:9],
                    y=benches[cat].loc[6:9],
                    # text=["" if int(n) == 1 else (" " * spacebar[len(str(int(n)))] + f"x{int(n)}") for n in round(benches[cat].loc[6] / benches[cat].loc[6:9])],
                    error_y=dict(
                        type="data",
                        array=np.log10(benches_err[cat].loc[6:9]),
                    ),
                    textposition="auto",
                    marker_color=["rgb(31, 119, 180)", "rgb(255,127,14)", "rgb(255,127,14)", "rgb(255,127,14)"],
                )
            ],
            layout=dict(
                barmode="group",
                yaxis_title=title,
                yaxis_type="log",
                xaxis_tickangle=30,
            ),
        )
        for cat, title in zip(("tts", "spms", "e"), ("Time-to-solution (s)", "Timestep duration (s<sub>wall</sub>/ms<sub>bio</sub>)", "Energy (kJ)"))
    }
