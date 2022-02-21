import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import math
from scipy.stats import gaussian_kde

xx = np.arange(0, 35, 0.01)
mechs = ["CaL13", "Ca", "Cav2_1", "Cav2_2", "Cav2_3", "Cav3_1", "Cav3_2", "Cav3_3", "cdp5", "cdp5_CAM", "cdp5_CAM_GoC", "cdp5_CR", "HCN1", "HCN1_golgi", "HCN2", "Kca1_1", "Kca2_2", "Kca3_1", "Kir2_3", "Km", "Kv1_1", "Kv1_5", "Kv2_2", "Kv3_3", "Kv3_4", "Kv4_3", "Kv7", "Leak", "Leak_GABA", "Na_granule_cell", "Na_granule_cell_FHF", "Nav1_1", "Nav1_6"]
groups = [0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1]
colors = ["rgba(100,100,100,0.2)", "rgba(130, 30, 0, 0.6)", "rgba(255, 0, 0, 1)"]
names = ["Regular", "RANGE vars", "Nonlinear"]
_shown = set()
# Use about the same amount of bins that plotly produces to normalize the numpy data, so
# that normalization yields about the same absolute units. (Not that the absolute count in
# a histogram matters much, but otherwise we have to display either no y-axes, or
# mismatched y-axes)
_plotly_bin_guess = 3750

def mech_pdf_scatter(jobs, speedup, mech, groups):
    relevant = speedup[[mech in job_mechs for job_mechs in jobs]]
    safe = relevant[~np.isnan(relevant)]
    kernel = gaussian_kde(safe)
    hist, edges = np.histogram(safe, bins=_plotly_bin_guess)
    pdf = kernel(xx)
    pdf = pdf * np.max(hist) / np.max(pdf)
    group = groups[mech]
    show = group not in _shown
    _shown.add(group)
    return go.Scatter(x=xx, y=pdf, name=names[group], legendgroup=group, marker_color=colors[group], showlegend=show)

def mech_group_scatter(jobs, speedup, group):
    groupmechs = [mech for mech, mech_group in zip(mechs, groups) if mech_group == group]
    res = []
    for mech in groupmechs:
        relevant = speedup[[mech in job_mechs for job_mechs in jobs]]
        safe = relevant[~np.isnan(relevant)]
        res.extend(safe)
    kernel = gaussian_kde(res)
    pdf = kernel(xx)
    pdf /= np.max(pdf)
    return go.Scatter(x=xx, y=pdf, name=names[group], legendgroup=group, marker_color=colors[group])

def mech_group_max(jobs, speedup, group):
    groupmechs = [mech for mech, mech_group in zip(mechs, groups) if mech_group == group]
    res = []
    for mech in groupmechs:
        relevant = speedup[[mech in job_mechs for job_mechs in jobs]]
        safe = relevant[~np.isnan(relevant)]
        res.append(max(safe))
    kernel = gaussian_kde(res)
    pdf = kernel(xx)
    return go.Scatter(x=xx, y=pdf, name=names[group], legendgroup=group, marker_color=colors[group])


def plot():
    mechgroups = dict(zip(mechs, groups))
    bigger_path = Path(__file__).parent.parent / "results" / "bigger_test"
    matrix_arb = np.load(str(bigger_path / "arbmatrix.npy"))
    mean_arb = np.where(np.isnan(matrix_arb[:, -1]), np.mean(matrix_arb[:, :-1], axis=1), np.mean(matrix_arb, axis=1))
    with open(str(bigger_path) + "/meta.txt", "r") as f:
        jobs = [l.split("mechanisms=")[1].split(" ") for l in f.read().split("morphology=")[1:]]

    matrix_nrn = np.load(str(bigger_path / "nrnmatrix.npy"))
    mean_nrn = np.where(np.isnan(matrix_nrn[:, -1]), np.mean(matrix_nrn[:, :-1], axis=1), np.mean(matrix_nrn, axis=1))
    speedup = mean_nrn / mean_arb
    fspeed = speedup[~np.isnan(speedup)]
    print("Lost", len(speedup) - len(fspeed), "jobs")
    hist, edges = np.histogram(fspeed, bins=_plotly_bin_guess)
    kernel = gaussian_kde(fspeed)
    envelop = kernel(xx)
    envelop_norm = envelop / np.max(envelop)
    envelop = envelop * np.max(hist) / np.max(envelop)
    return {
        "kde_raw": go.Figure(
            data=[
                go.Scatter(x=xx, y=envelop, name="All", line_color="rgb(255,127,14)"),
                *(mech_pdf_scatter(jobs, speedup, mech, mechgroups) for mech in mechs)
            ],
            layout=dict(
                xaxis_title="Speedup factor",
                xaxis_range=[0,20],
                yaxis_title="Count",
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=1
                ),
            ),
        ),
        "kde_grouped": go.Figure(
            data=[
                go.Scatter(x=xx, y=envelop_norm, name="All", line_color="rgb(255,127,14)"),
                *(mech_group_scatter(jobs, speedup, group) for group in range(3))
            ],
            layout=dict(
                xaxis_title="Speedup factor",
                xaxis_range=[1,20],
                yaxis_title="Probability density",
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=1
                ),
            )
        ),
        "kde_max": go.Figure(
            data=[
                *(mech_group_max(jobs, speedup, group) for group in range(3))
            ],
            layout=dict(
                xaxis_title="Maximum speedup factor",
                xaxis_range=[1,30],
                yaxis_title="Probability density",
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=1
                ),
            )
        )
    }
