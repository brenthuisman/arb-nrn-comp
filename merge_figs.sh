#!/bin/bash
mkdir -p figures_paper
montage figures/mechanisms.png figures/mech_features_kde_max.png -tile 2x1 -geometry +0+0 figures_paper/mech.png
montage figures/network_single_tts.png figures/network_single_spms.png figures/network_single_e.png -tile 3x1 -geometry +0+0 figures_paper/network_single.png
montage figures/network_sock_tts.png figures/network_sock_spms.png figures/network_sock_e.png -tile 3x1 -geometry +0+0 figures_paper/network_sock.png
montage figures/network_distr_tts.png figures/network_distr_spms.png figures/network_distr_e.png -tile 3x1 -geometry +0+0 figures_paper/network_distr.png
montage figures/network_gpu_tts.png figures/network_gpu_spms.png figures/network_gpu_e.png -tile 3x1 -geometry +0+0 figures_paper/network_gpu.png
montage figures/single_cell.png figures/single_cell_isi.png figures/single_cell_vm.png -tile 3x1 -geometry +0+0 figures_paper/single_cell.png
