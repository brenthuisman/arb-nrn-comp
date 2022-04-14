import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * b / x

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
            "usage": "mean",
        }
    )
    benches["e"] = benches["e"] / 1000
    benches_err = job_data.groupby(["bench_id"]).agg(
        {
            "bench_name": "first",
            "tts": "std",
            "nodes": "first",
            "e": "std",
            "spms": "std",
            "nh": "std",
            "usage": "std",
        }
    )
    benches_err["e"] = benches_err["e"] / 1000
    loc_a = [10, 11, 12, 15, 16, 17, 18]
    loc_n = [6]
    benches.loc[loc_a, "bench_name"] = ("1", "2", "4", "8", "12", "16", "20")
    # Add a zero width space to NEURON's 20 label, so the bar doesn't group with the 20 of
    # Arbor, and messes up the layout.
    benches.loc[loc_n, "bench_name"] = ("\x2020",)
    return {
        cat: go.Figure(
            data=[
                go.Scatter(
                    x=benches["bench_name"].loc[loc_a],
                    y=benches[cat].loc[loc_a],
                    error_y=dict(
                        type="data",
                        array=benches_err[cat].loc[loc_a],
                        thickness=5,
                        width=15,
                    ),
                    mode="lines",
                    # marker = dict(size = 15),
                    # marker_color="rgb(255,127,14)",
                    line=dict(color='rgb(255,127,14)'),
                    name="Arbor 1 GPU/node",
                ),
                go.Scatter(
                    name='Arbor expected linearity',
                    x=benches["bench_name"].loc[loc_a],
                    # y=10**( -np.log10(np.array(benches[cat].loc[loc_a]).astype(float)[1])
                    #         /np.log10(np.array(benches[cat].loc[loc_a]).astype(float)[0])
                    #         *np.log10(np.array(benches["bench_name"].loc[loc_a]).astype(float))
                    #         +np.log10(np.array(benches[cat].loc[loc_a]).astype(float)[0])
                    #         ),
                    y = np.array(benches[cat].loc[loc_a]).astype(float)[0]
                        +(np.array(benches[cat].loc[loc_a]).astype(float)[1]
                        /np.array(benches[cat].loc[loc_a]).astype(float)[0])
                        /np.array(benches["bench_name"].loc[loc_a]).astype(float),
                    mode='lines',
                    line_color="black"
                ),
            ]
            + (
                [
                    go.Scatter(
                        x=benches["bench_name"].loc[loc_a][::-1],
                        y=benches[cat].loc[loc_n],
                        error_y=dict(
                            type="data",
                            array=benches_err[cat].loc[loc_n],
                            thickness=5,
                            width=15,
                        ),
                        mode="lines",
                        marker = dict(size = 15),
                        marker_color="rgb(31, 119, 180)",
                        name="NEURON 36 CPU/node",
                    ),
                ]
                if cat != "usage"
                else []
            ),
            layout=dict(
                barmode="group",
                yaxis_title=title,
                yaxis_type="log" if cat != "usage" else None,
                yaxis_dtick=1 if cat != "usage" else None,
                yaxis_rangemode="tozero",
                xaxis_title="Nodes",
                # xaxis_range=[-1.5, 8.5],
                legend=dict(
                    yanchor="top",
                    y=0.9,
                    xanchor="left",
                    x=0.05
                ),
                showlegend=False,
            ),
        )
        for cat, title in zip(
            ("tts", "spms", "e", "nh", "usage"),
            (
                "Time-to-solution (s)",
                "Timestep duration (s<sub>wall</sub>/ms<sub>bio</sub>)",
                "Energy (MJ)",
                "Node hours (h)",
                "GPU occupation (%)",
            ),
        )
    }
