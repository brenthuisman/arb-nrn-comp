import h5py
import numpy as np
from bsb.plotting import hdf5_plot_spike_raster
import itertools
from plotly.subplots import make_subplots

def plot():
    with h5py.File("results/results_arbenv.hdf5", "a") as f, h5py.File("results/results_nrnenv.hdf5", "r") as g:
        f.require_group("recorders/deduped")
        del f["recorders/deduped"]
        f.require_group("recorders/deduped")
        avg_arb = {}
        for k, spikes in f["recorders/soma_spikes"].items():
            # The spikes of each synapse were recorded instead of just the soma. This
            # means that all along the axon, duplicated spikes with slightly different
            # times are recorded; so we remove all duplicates that occur in rapid
            # succession of eachother.
            sort_order = np.argsort(spikes[()])
            nondupes = np.diff(spikes[()][sort_order]) > 3
            # Super optimized numpy code, please copy paste to all your own projects.
            ns = np.concatenate(([spikes[sort_order[0]]], spikes[()][sort_order[np.nonzero(nondupes)[0] + 1]]))
            avg_arb.setdefault(spikes.attrs["display_label"], []).append(len(ns))
            ds = f["recorders/deduped"].create_dataset(str(spikes.attrs['cell_id']), data=ns)
            for k,v in spikes.attrs.items():
                ds.attrs[k] = v
        avg_nrn = {}
        for spikes in g["recorders/soma_spikes"].values():
            avg_nrn.setdefault(spikes.attrs["display_label"], []).append(len(spikes))

        print("name,m_arb,s_arb,m_nrn,s_nrn")
        for k, v in avg_arb.items():
            print(f"{k},{np.mean(v)},{np.std(v)},{np.mean(avg_nrn[k])},{np.std(avg_nrn[k])}")
        nrn = hdf5_plot_spike_raster(g["recorders/soma_spikes"], show=False)
        arb = hdf5_plot_spike_raster(f["recorders/deduped"], show=False)
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Arbor", "NEURON"))
        nmap = {
            "golgi_cell": "Golgi cell",
            "basket_cell": "Basket cell",
            "stellate_cell": "Stellate cell",
            "purkinje_cell": "Purkinje cell",
            "granule_cell": "Granule cell",
        }
        for dat in itertools.chain(nrn.data, arb.data):
            dat.name = nmap[dat.name]
            dat.marker.size = 2
        for datum in arb.data:
            fig.add_trace(datum, row=1, col=1)
        for datum in nrn.data:
            datum.showlegend = False
            fig.add_trace(datum, row=1, col=2)
        fig.update_layout(
            xaxis_title="Time (ms)",
            yaxis_title="Cell (ID)",
            title_text="Raster plot",
            legend_itemsizing="constant",
        )
        return fig

def meta():
    return {"width": 1500, "height": 800}
