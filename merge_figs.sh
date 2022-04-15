#!/bin/bash
mkdir -p figures_paper
montage figures/mechanisms.jpg figures/mech_features_kde_max.jpg -tile 2x1 -geometry +0+0 figures_paper/mech.jpg
montage figures/network_single_tts.jpg figures/network_single_spms.jpg figures/network_single_e.jpg -tile 3x1 -geometry +0+0 figures_paper/network_single.jpg
montage figures/network_sock_tts.jpg figures/network_sock_spms.jpg figures/network_sock_e.jpg -tile 3x1 -geometry +0+0 figures_paper/network_sock.jpg
montage figures/network_distr_tts.jpg figures/network_distr_spms.jpg figures/network_distr_e.jpg -tile 3x1 -geometry +0+0 figures_paper/network_distr.jpg
montage figures/network_gpu_tts.jpg figures/network_gpu_spms.jpg figures/network_gpu_e.jpg -tile 3x1 -geometry +0+0 figures_paper/network_gpu.jpg
montage figures/single_cell.jpg figures/single_cell_isi.jpg figures/single_cell_vm.jpg -tile 3x1 -geometry +0+0 figures_paper/single_cell.jpg
