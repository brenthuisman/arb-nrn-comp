#!/bin/bash
mkdir -p figures_paper

montage figures/single_cell_vm.png figures/single_cell_isi.png -tile 1x2 -geometry +0+0 figures_paper/validation.png
montage figures/mechanisms.png figures/mech_features_kde_max.png figures/single_cell.png -tile 3x1 -geometry +0+0 figures_paper/perfcomp.png

montage figures/network_distr_tts.png figures/network_distr_spms.png figures/network_distr_e.png -tile 3x1 -geometry +0+0 figures_paper/network_distr.png
montage figures/network_undistr_tts.png figures/network_undistr_spms.png figures/network_undistr_e.png -tile 3x1 -geometry +0+0 figures_paper/network_undistr.png
montage figures/network_gpu_tts.jpg figures/network_gpu_spms.jpg figures/network_gpu_e.jpg -tile 3x1 -geometry +0+0 figures_paper/network_gpu.jpg
