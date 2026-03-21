# Environment setup (M0)

This project requires a Python 3.11+ environment with OpenMDAO, MPhys, and TACS importable from the same interpreter.

## Setup

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Verify

Run the direct import smoke check:

```bash
python -c "import openmdao; import mphys; import tacs; print('environment ok')"
```

Run the repository doctor command:

```bash
python -m wing_trade_study.cli.main doctor
```

The doctor command prints JSON and returns exit code `0` only when all required packages are available.

## Known failing tasks and potential solutions

When the following commands fail, use this checklist to triage quickly.

### 1) `python -m pip install -e ".[dev]"` fails during build dependencies

Observed failure pattern:
- proxy/index connectivity errors while resolving `setuptools`/`wheel` for the isolated build environment.

Potential solutions:
- Configure pip to use a reachable index or internal mirror (for example with `PIP_INDEX_URL` and `PIP_EXTRA_INDEX_URL`).
- Use a prebuilt wheelhouse for repeatable installs:
  1. build/download required wheels on a machine with index access,
  2. transfer wheel artifacts,
  3. install with `python -m pip install --no-index --find-links <wheelhouse> -e ".[dev]"`.
- In controlled environments where build requirements are already installed, use:
  - `python -m pip install --no-build-isolation -e ".[dev]"`.
  - This bypasses isolated-build dependency resolution and should only be used when the environment is managed intentionally.

### 2) `python -c "import openmdao; import mphys; import tacs"` fails

Observed failure pattern:
- missing `mphys` and/or `tacs` modules.

Potential solutions:
- Install OpenMDAO/MPhys from package index:
  - `python -m pip install openmdao mphys`
- Install TACS following its official installation guidance (compiler/MPI/system dependency prerequisites may be required before Python package installation).
- Re-run:
  - `python -m wing_trade_study.cli.main doctor`
  and confirm `all_available: true`.

### 3) `python -m wing_trade_study.cli.main doctor` returns non-zero

Interpretation:
- The command is functioning as intended; non-zero means at least one required package is not available as an installed distribution.

Potential solutions:
- Resolve missing packages using the steps above.
- If a same-named local folder exists (for example `openmdao/` in repo), keep using `doctor`; it verifies installed distribution metadata and avoids false-positive imports.
