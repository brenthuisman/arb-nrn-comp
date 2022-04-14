import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import pandas as pd


def plot():
    job_data = pd.read_csv("jobs.csv")
    benches = job_data.groupby(["bench_id"]).agg(
        {
            "bench_name": "first",
            "tts": "mean",
            "nodes": "first",
            "e": "mean",
            "spms": "mean",
            "nh": "mean",
        }
    )
    benches_err = job_data.groupby(["bench_id"]).agg(
        {
            "bench_name": "first",
            "tts": "std",
            "nodes": "first",
            "e": "std",
            "spms": "std",
            "nh": "std",
        }
    )
    benches["tts"] *= 10
    benches_err["tts"] *= 10
    benches.loc[1:5, "bench_name"] = (
        "NEURON",
        "Arb. single",
        "Arb. multithr.",
        "Arb. hyperthr.",
        "Arb. GPU",
    )
    return {
        cat: go.Figure(
            data=[
                go.Scatter(
                    x=benches["bench_name"].loc[1:5],
                    y=benches[cat].loc[1:5],
                    error_y=dict(
                        type="data",
                        array=benches_err[cat].loc[1:5],
                        thickness=5,
                        width=15,
                    ),
                    mode="markers",
                    marker = dict(size = 15),
                    marker_color=[
                        "rgb(31, 119, 180)",
                        "rgb(255,127,14)",
                        "rgb(255,127,14)",
                        "rgb(255,127,14)",
                        "rgb(255,127,14)",
                    ],
                )
            ],
            layout=dict(
                barmode="group",
                yaxis_title=title,
                yaxis_type="log",
                yaxis_dtick=1,
                yaxis_rangemode="tozero",
                xaxis_tickangle=30,
            ),
        )
        for cat, title in zip(
            (
                "tts",
                "spms",
                "e",
                "nh",
            ),
            (
                "Time-to-solution (s)",
                "Timestep duration (s<sub>wall</sub>/ms<sub>bio</sub>)",
                "Energy (kJ)",
                "Node hours (h)",
            ),
        )
    }
