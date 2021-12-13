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
    benches["nh"] = benches["tts"] * benches["nodes"]
    return {
        cat: go.Figure(
            data=[
                go.Bar(
                    x=benches["bench_name"].loc[6:12],
                    y=benches[cat].loc[6:12],
                    text=["" if int(n) == 1 else f"x{int(n)}" for n in round(benches[cat].loc[6] / benches[cat].loc[6:12])],
                    textposition="auto",
                )
            ],
            layout=dict(
                barmode="group",
                yaxis_title=title,
                yaxis_type="log",
            ),
        )
        for cat, title in zip(("tts", "spms", "e"), ("Time-to-solution [s]", "Runtime [s/ms]", "Energy [kJ]"))
    }
