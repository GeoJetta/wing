#!/usr/bin/env bash
set -euo pipefail

conda create -y -n wingmdao -c conda-forge python=3.10 mamba
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate wingmdao
mamba install -y -c conda-forge -c smdogroup tacs petsc4py mpi4py pynastran
pip install "openmdao[all]" mphys matplotlib numpy

echo "Installed environment wingmdao"
