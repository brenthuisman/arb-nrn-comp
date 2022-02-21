import h5py
from bsb.config import get_result_config
from functools import reduce

with h5py.File("results/results_arbor.hdf5", "a") as f, h5py.File("results/results_nrn.hdf5", "r") as g:
    for k, v in g.attrs.items():
        f.attrs[k] = v
    attr_map = {n: gg.attrs for n, gg in g["recorders/soma_spikes"].items()}
    # Del previous results
    (res_f := f.require_group("recorders")).require_group("soma_spikes")
    del res_f["soma_spikes"]
    res_g = res_f.require_group("soma_spikes")
    demuxed = {}
    for id, t in f["all_spikes_dump"][()]:
        demuxed.setdefault(id, set()).add(t)
    for id, t_spikes in demuxed.items():
        n = str(int(id))
        ds = res_g.create_dataset(n, data=list(t_spikes))
        # Copy metadata for each cell from NEURON results
        for k, v in attr_map[n].items():
            ds.attrs[k] = v
