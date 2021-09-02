from bsb.output import MorphologyRepository
import dbbs_models, itertools, h5py

c = "PurkinjeCell"
mr = MorphologyRepository("morphos.hdf5")
# mr.import_arbz_module(dbbs_models)
m = mr.get_morphology(c)

i = 10
print(m.branches[i]._full_labels)

exit()

with h5py.File("morphos.hdf5", "a") as f:
    del f[f"morphologies/{c}/branches/{i}/x"]
    f[f"morphologies/{c}/branches/{i}/x"] = [0, 0]
    del f[f"morphologies/{c}/branches/{i}/y"]
    f[f"morphologies/{c}/branches/{i}/y"] = [-333, -433]
    del f[f"morphologies/{c}/branches/{i}/z"]
    f[f"morphologies/{c}/branches/{i}/z"] = [0, 0]
    del f[f"morphologies/{c}/branches/{i}/radii"]
    f[f"morphologies/{c}/branches/{i}/radii"] = [0.365, 0.365]
