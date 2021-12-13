import pandas
from pathlib import Path
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np

class Decompose:
    def __init__(self, columns, regression, speedup):
        self._coef = dict(zip(columns, regression.coef_))
        self._funcs = dict(zip(columns, (lambda v, c=c: c * v + regression.intercept_ for c in regression.coef_)))
        self._spd = speedup

    def only(self, vals, *cols):
        return 0

    def trendline(self, vals, col):
        return [0, 10], [1, 2]

def plot():
    mod_data = pandas.read_csv(Path(__file__).parent.parent / "nmodl.csv")
    mod_data.set_index("name")
    cols = ["ion_r", "ion_w", "range", "global", "state", "param", "assign"]
    features = mod_data[cols].to_numpy()
    ft_sum = np.sum(features, axis=1)
    speedup = mod_data["speedup"].to_numpy()
    regressor = LinearRegression().fit(features, speedup)
    regressor_simple = LinearRegression().fit(ft_sum.reshape(-1, 1), speedup)
    system_score = regressor.score(features, speedup)
    print("Regression score:", system_score)
    print("Simple regression score:", regressor_simple.score(ft_sum.reshape(-1, 1), speedup))
    decomp = Decompose(cols, regressor, speedup)
    param_decomp = decomp.only(features, "param")
    param_trend = decomp.trendline(features, "param")
    return go.Figure(go.Scatter(x=ft_sum, y=speedup, mode="markers"))
