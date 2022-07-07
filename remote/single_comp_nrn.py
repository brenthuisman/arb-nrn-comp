import glia, glia.library
import pickle
from patch import p

def nrn_sim(pkg, t, dt):
    p.dt = dt
    p.celsius = 32
    time = p.time
    recorders = {}
    for mech in pkg.mods:
        s = p.Section()
        s.L = 4
        s.diam = 4
        try:
            s.insert(mech.mod_name)
        except ValueError:
            # The mod collection contains PointProcesses, skip those.
            continue
        print("inserted", mech.mod_name)
        mname = mech.asset_name
        # Match the NEURON display labels to the Arbor ones.
        if mech.variant != "0":
            mname += f"_{mech.variant}"
        if mname == "Km_granule_cell":
            mname = "Km"
        if mname == "Ca_granule_cell":
            mname = "Ca"
        recorders[mname] = p.record(s)

    p.finitialize()
    p.continuerun(t)

    return time, recorders

tSim = 1000
dt = 0.025
package = glia.package("dbbs_mod_collection")
time, mechs = nrn_sim(package, tSim, dt)
with open("single_comp_nrn.pkl", "wb") as f:
    pickle.dump((list(time), {mech: list(trace) for mech, trace in mechs.items()}), f)
