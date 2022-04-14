from arbor import single_cell_model
import dbbs_models
import pickle

for name, model in vars(dbbs_models).items():
    if name.endswith("Cell"):
        print("Running", name)
        arb_model = single_cell_model(model.cable_cell())
        arb_model.catalogue = model.get_catalogue()
        arb_model.properties.set_ion(
            ion="h", valence=1, int_con=1.0, ext_con=1.0, rev_pot=-34
        )
        arb_data[name] = []
        cell = model()
        for _ in range(20):
            print("Run", _)
            t = time.time()
            arb_model.run(10, dt=0.025)
            arb_data[name].append(time.time() - t)

with open("arb_single_cell.pkl", "wb") as f:
    pickle.dump(arb_data, f)
