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
    col_ids = [1, 14, 19, 2, 13, 3, 4, 5]
    benches.loc[col_ids, "bench_name"] = (
        "NEURON 1-thread",
        "NEURON 18-thread",
        "NEURON 36-thread",
        "Arbor 1-thread",
        "Arbor 18-thread",
        "Arbor 36-thread",
        "Arbor 72-thread",
        "Arbor GPU",
    )
    return {
        cat: go.Figure(
            data=[
                go.Scatter(
                    x=benches["bench_name"].loc[col_ids],
                    y=benches[cat].loc[col_ids],
                    error_y=dict(
                        type="data",
                        array=benches_err[cat].loc[col_ids],
                        thickness=5,
                        width=15,
                        # color=[ #terrible plotly does not let you set colors per datapoints
                        #     "rgb(31, 119, 180)",
                        #     "rgb(255,127,14)",
                        #     "rgb(255,127,14)",
                        #     "rgb(255,127,14)",
                        #     "rgb(255,127,14)",
                        # ],
                    ),
                    mode="markers",
                    marker = dict(size = 15),
                    marker_color=[
                        "rgb(31, 119, 180)",
                        "rgb(31, 119, 180)",
                        "rgb(31, 119, 180)",
                        "rgb(255,127,14)",
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
