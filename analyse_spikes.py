import h5py
from bsb.plotting import hdf5_plot_spike_raster

with h5py.File("results/results_arbor.hdf5", "a") as f, h5py.File(
    "results/results_nrn.hdf5", "r"
) as g:
    hdf5_plot_spike_raster(g["recorders/soma_spikes"])
    hdf5_plot_spike_raster(f["recorders/soma_spikes"])
