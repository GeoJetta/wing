# TACS + MPhys Cantilever Strut Example

This repository contains a minimal **MPhys-integrated TACS** setup (not a custom pyTACS OpenMDAO component) for a cantilever wing beam with an optional strut.

## Environment installation

Recommended stack is a Linux machine (or WSL2 Ubuntu) with one conda env pinned to Python 3.10:

```bash
conda env create -f environment.yml
conda activate wingmdao
```

If you prefer command-by-command installation:

```bash
conda create -n wingmdao -c conda-forge python=3.10 mamba
conda activate wingmdao
mamba install -c conda-forge -c smdogroup tacs petsc4py mpi4py pynastran
pip install "openmdao[all]" mphys matplotlib numpy
```

## Run the model

```bash
python src/tacs_mphys_cantilever.py
```

Outputs:

- `outputs/cantilever_strut.bdf`: generated structural model passed into TACS via `TacsBuilder`
- `outputs/tacs_geometry.png`: 3D geometry view of the structure definition

## Notes

- Design constraints and variable bounds are in `src/constraints.py`.
- Geometry generation is done parametrically in-memory and written to a BDF file for TACS/MPhys consumption.
