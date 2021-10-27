import numpy as np
import plotly.graph_objs as go

dir = "bigger_test"
full_run = False

with (
    open(f"{dir}/arbmatrix.npy", "rb") as f,
    open(f"{dir}/nrnmatrix.npy", "rb") as g,
    open(f"{dir}/meta.txt", "r") as m
):
        arb = np.load(f)
        nrn = np.load(g)
        meta = np.array(m.read().split("morphology")[:-1], dtype=str)

print("Results:", arb.shape[0])
print("Reps:", arb.shape[1])
print("Arb NaNs: ", sum(np.isnan(arb[:, 0])))
print("NRN NaNs: ", sum(np.isnan(nrn[:, 0])))
print("time NaNs:", sum(np.isnan(nrn[:, 0] / arb[:, 0])))
times = nrn / arb
avg_time = np.mean(times[:, :-1], axis=1)
std_time = np.std(times[:, :-1], axis=1)
print("avg:", avg_time.shape)
winners = sum(avg_time > 1)
losers = sum(avg_time <= 1)
print("winners:", winners, "losers:", losers)
if full_run:
    go.Figure(go.Histogram(x=avg_time)).show()
print("humiliators:", sum(avg_time >= 14.8))
print("dead weight:", sum(avg_time <= 2.5))
sets = [k.split(" ") if (k := m.split("mechanisms=")[-1].rstrip("\n")) else [] for m in meta]
solo_sets = [len(s) == 1 for s in sets]
solo_set_names = [s[0] for s in sets if len(s) == 1]
print(next(zip(avg_time[solo_sets], std_time[solo_sets])))
solo_results = dict()
for solo, t, std in sorted(zip(solo_set_names, avg_time[solo_sets], std_time[solo_sets]), key=lambda x: x[1]):
    print("Mech:", solo.ljust(19, " "), f"{t:.4f}", "±", f"{std:.4f}")
