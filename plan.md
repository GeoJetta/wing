# plan.md — Wing Trade Study Execution Plan

## Purpose of this file
This file is the active execution plan for the repository.

Use:
- `AGENTS.md` for permanent repo rules and quality gates.
- `docs/spec.md` for the stable project objective, scope, and assumptions.
- `plan.md` for milestone order, current status, artifact expectations, validation commands, blockers, and next actions.

## Project objective
Build a reproducible structural trade study that answers this question with real solver-backed outputs:

**For the target commuter-aircraft wing, under the same loads and constraints, when is a strut-braced wing lighter or better-constrained than a cantilever wing?**

The project is only considered complete when it can:
1. Run a cantilever structural case from config to saved plots and machine-readable outputs.
2. Run a comparable strut-braced structural case from config to saved plots and machine-readable outputs.
3. Use the real TACS solve path for the reported structural results.
4. Use OpenMDAO/MPhys for the optimization and design-study layer after the structural baseline is verified.
5. Save contour plots, summary tables, and comparison artifacts that support a side-by-side decision.
6. Reproduce the headline results from documented commands in a clean environment.

## Execution strategy
The project will follow a **pyTACS-first, MPhys-second** workflow.

Why:
- TACS is the core solver risk, so the first job is proving that the structural environment is real and usable.
- pyTACS is the shortest path to a working shell-based structural baseline.
- MPhys and OpenMDAO should be added only after the cantilever shell model is running and producing trustworthy artifacts.
- The strut-braced case should be created by copying and extending the cantilever path, not by inventing a second unrelated stack.

This means the practical sequence is:
1. Bring up Python + TACS + pyTACS + OpenMDAO + MPhys.
2. Reproduce a known pyTACS shell cantilever example inside this repository.
3. Replace the example geometry with the project cantilever wing-box geometry.
4. Add project loads, design variables, and constraints.
5. Verify and lock a cantilever baseline.
6. Wrap that working case in OpenMDAO/MPhys.
7. Run the cantilever trade study.
8. Copy the cantilever case and extend it into the strut-braced case.
9. Run the strut trade study.
10. Compare both architectures.

## Non-goals for the first complete version
- No CFD or aeroelastic coupling beyond externally supplied structural loads.
- No certification-level load envelope.
- No detailed joint, fastener, or local failure FEA.
- No manufacturing or operating cost model beyond simple structural-weight comparison.
- No custom framework layered on top of TACS/OpenMDAO/MPhys.

## Starting assumptions and open dependencies
- The wing is modeled with shell-based wing-box structure from the start.
- The initial cantilever case is the reference model and template for the strut case.
- The strut can start as a simpler 1D structural member attached to the shell wing box.
- Loads begin with one useful static case and expand only after that case is verified.
- The repository must not report placeholder values as if they came from TACS.

### Important note on the seed file
`docs/spec.md` refers to `openmdao_semiwing_boxbeam_constraints.py` as the seed source for geometry and constraints.
The uploaded file currently available in the workspace is `openmdao_constraint.py`, which is only a small OpenMDAO constraint helper and **does not contain the geometry seed implied by the spec**.

Plan implication:
- treat the current uploaded constraint helper as useful for later OpenMDAO constraint registration,
- but do **not** treat it as the geometry source of truth,
- and keep the geometry-import milestone scoped so it can either consume the real seed script when provided or proceed from an explicit internal cantilever geometry definition.

## Standard artifact layout
All generated outputs should live under `artifacts/`.

```text
artifacts/
├─ env/
├─ cantilever_example/
├─ cantilever_repo_case/
├─ cantilever_geometry/
├─ cantilever_static/
├─ cantilever_verified/
├─ cantilever_trade/
├─ strut_geometry/
├─ strut_static/
├─ strut_trade/
└─ comparison/
```

Each run directory should contain, where applicable:
- the input config,
- a small machine-readable summary (`json`, `csv`, or `parquet`),
- generated plots,
- basic run metadata (timestamp, dependency versions, machine info, git SHA when available).

## Current status
- Current milestone: M0
- Overall status: blocked
- Last completed milestone: none
- Next recommended action: resolve the local build backend bootstrap so editable installs can run without external package index access
- Main execution choice: pyTACS shell baseline first, MPhys only after the cantilever baseline is verified
- Known dependency gap: the geometry seed file referenced in the spec is not present in the uploaded workspace

## Architecture summary

### Early execution path (before OpenMDAO/MPhys)
`config -> geometry definition -> shell mesh/BDF path -> pyTACS analysis -> artifacts -> verification`

### Later optimization path
`validated structural model -> MPhys/TacsBuilder -> OpenMDAO problem -> design variables/constraints/objective -> DOE/optimization -> contour plots/tables`

### Strut extension path
`validated cantilever geometry and loads -> add strut member + connection model -> verify static behavior -> wrap in MPhys/OpenMDAO -> run trade study`

### Module ownership by phase
- `config/`: validated user inputs and defaults
- `geometry/`: planform, wing-box parameterization, shell-model/BDF inputs
- `loads/`: static load cases and sign conventions
- `analysis/`: pyTACS setup and solve path first; MPhys builder later
- `postprocess/`: plots, summaries, artifact export
- `optimization/`: design variables, constraints, driver setup
- `studies/`: cantilever and strut study orchestration
- `cli/` and `scripts/`: reproducible command entry points

## Milestone checklist
- [ ] M0 - Bootstrap the Python environment and repo tooling
- [ ] M1 - Prove TACS, pyTACS, OpenMDAO, and MPhys imports in the repo environment
- [ ] M2 - Reproduce a documented pyTACS shell cantilever example inside the repo
- [ ] M3 - Turn the example into a stable repo-owned cantilever runner and artifact pipeline
- [ ] M4 - Implement the project cantilever wing-box geometry
- [ ] M5 - Map seed constraints/parameters into internal config and save a baseline snapshot
- [ ] M6 - Add the first project cantilever static load case and boundary conditions
- [ ] M7 - Add cantilever design variables and structural constraints
- [ ] M8 - Verify and lock the cantilever baseline outputs
- [ ] M9 - Wrap the validated cantilever case in OpenMDAO/MPhys and check derivatives
- [ ] M10 - Run the cantilever trade study and generate contour plots
- [ ] M11 - Create the strut-braced geometry from the cantilever template
- [ ] M12 - Add strut member modeling, loads, variables, and a static baseline solve
- [ ] M13 - Wrap the strut-braced case in OpenMDAO/MPhys and check derivatives
- [ ] M14 - Run the strut-braced trade study and generate contour plots
- [ ] M15 - Compare cantilever and strut-braced results and publish final artifacts

## Milestones

### M0 - Bootstrap the Python environment and repo tooling
Status: blocked

Goal:
Create the repository skeleton needed to support a real TACS project and make the developer workflow predictable.

Scope:
- Add or finalize `pyproject.toml`.
- Add `src/` layout, test layout, and minimal package entry points.
- Add dev tooling: `ruff`, `black`, `mypy`, `pytest`, pre-commit if appropriate.
- Add a lightweight `doctor` or smoke entry point scaffold.
- Add a short `README` section or `docs/verification.md` stub for environment setup.

Done when:
- Editable install works for the repo package.
- Lint, test, and type-check commands exist even if there are only minimal tests at first.
- The repo has a clear package entry point and test layout.

Validation commands:
- `python -m pip install -e ".[dev]"`
- `pytest -q`
- `ruff check .`
- `python -m wing_trade_study.cli.main doctor`

Artifacts:
- none required beyond repository files

Notes:
- This milestone is about repo scaffolding only, not solver verification.

### M1 - Prove TACS, pyTACS, OpenMDAO, and MPhys imports in the repo environment
Status: not started

Goal:
Make the solver stack real before any project modeling work begins.

Scope:
- Add environment instructions and any platform notes discovered during install.
- Add a smoke test that imports `tacs`, `openmdao`, and `mphys`.
- Record exact install blockers if they occur.
- Save a small environment report under `artifacts/env/`.

Done when:
- The documented environment can import `tacs`, `openmdao`, and `mphys`.
- A smoke test passes in the repo.
- Known platform or MPI requirements are documented.

Validation commands:
- `python -c "import tacs, openmdao, mphys; print('imports ok')"`
- `pytest -q tests/integration/test_environment_smoke.py`
- `python -m wing_trade_study.cli.main doctor --output artifacts/env`

Artifacts:
- `artifacts/env/` with a machine-readable dependency report or smoke summary

Blocker handling:
- If TACS or MPhys cannot import, record the exact command and error in `Blockers` and stop.

### M2 - Reproduce a documented pyTACS shell cantilever example inside the repo
Status: not started

Goal:
Run one known shell-based cantilever example before changing geometry, loads, or optimization structure.

Scope:
- Choose a documented pyTACS shell cantilever example or the closest shell-beam benchmark used in the TACS docs/examples.
- Bring the example into this repository in a traceable way.
- Run it without changing the underlying physical intent.
- Save all expected outputs to `artifacts/cantilever_example/`.
- Document the example source and any local adaptations.

Done when:
- The example runs from a repo command.
- The output directory contains the standard solver outputs plus a run summary.
- The example lineage is documented in code comments or docs.

Validation commands:
- `pytest -q tests/integration/test_cantilever_example.py`
- `python scripts/run_cantilever_example.py --output artifacts/cantilever_example`

Artifacts:
- `artifacts/cantilever_example/`

Notes:
- Prefer shell examples over beam-only examples because the project intends to use shells from the start.

### M3 - Turn the example into a stable repo-owned cantilever runner and artifact pipeline
Status: not started

Goal:
Refactor the reproduced example so it becomes a maintainable repository case instead of a one-off imported script.

Scope:
- Move the analysis path into the repository package structure.
- Separate configuration, analysis execution, and artifact export.
- Add a repeatable script or CLI entry point.
- Ensure outputs land in the standard artifact location.

Done when:
- The repository can run the example case through package-owned code.
- Output files are saved under `artifacts/cantilever_repo_case/`.
- The test path covers the repo-owned runner, not only the borrowed example.

Validation commands:
- `pytest -q tests/integration/test_cantilever_repo_case.py`
- `python scripts/run_cantilever_repo_case.py --output artifacts/cantilever_repo_case`

Artifacts:
- `artifacts/cantilever_repo_case/`

### M4 - Implement the project cantilever wing-box geometry
Status: not started

Goal:
Replace the borrowed example geometry with the project cantilever geometry while keeping the solve path as unchanged as possible.

Scope:
- Implement the commuter-class cantilever planform and wing-box geometry.
- Use shell geometry inputs appropriate for pyTACS/TACS.
- Keep geometry generation isolated from loads and optimization logic.
- Save geometry artifacts and a geometry-only run output.

Done when:
- The repository can build and run the cantilever case using the project geometry.
- Geometry parameters are explicit and testable.
- Geometry artifacts exist under `artifacts/cantilever_geometry/`.

Validation commands:
- `pytest -q tests/unit/test_cantilever_geometry.py`
- `pytest -q tests/integration/test_cantilever_geometry_smoke.py`
- `python scripts/run_cantilever_geometry.py --output artifacts/cantilever_geometry`

Artifacts:
- `artifacts/cantilever_geometry/`

Notes:
- If the real seed geometry file is later provided, this milestone may absorb its import path; otherwise geometry should be authored directly in the internal schema.

### M5 - Map seed constraints/parameters into internal config and save a baseline snapshot
Status: not started

Goal:
Preserve traceability from the external seed assumptions into repository-owned config objects.

Scope:
- Map available seed parameter names and constraint concepts into the internal config schema.
- Save a machine-readable baseline snapshot of the mapped values.
- Document any unit conversions or assumptions introduced during mapping.
- If the actual seed geometry file is still unavailable, limit this milestone to the available constraint/helper inputs and clearly record that gap.

Done when:
- The repository contains a traceable parameter/constraint mapping.
- A baseline snapshot exists for regression use.
- Gaps between the spec and the available seed file are documented.

Validation commands:
- `pytest -q tests/unit/test_seed_mapping.py`
- `python scripts/export_seed_snapshot.py --output artifacts/cantilever_geometry/seed_snapshot.json`

Artifacts:
- `artifacts/cantilever_geometry/seed_snapshot.json`

### M6 - Add the first project cantilever static load case and boundary conditions
Status: not started

Goal:
Create the first useful project-specific cantilever structural solve.

Scope:
- Define one representative static load case.
- Make sign conventions, units, and load bookkeeping explicit.
- Implement the cantilever boundary conditions.
- Save static results and load summaries.

Done when:
- One project cantilever static solve runs end to end.
- The load definition is machine-readable.
- Load totals and support assumptions are documented.

Validation commands:
- `pytest -q tests/unit/test_load_cases.py`
- `pytest -q tests/integration/test_cantilever_static_case.py`
- `python scripts/run_cantilever_static.py --output artifacts/cantilever_static`

Artifacts:
- `artifacts/cantilever_static/`

Notes:
- Start with the minimum load case needed to make the project meaningful; do not jump directly to a full envelope.

### M7 - Add cantilever design variables and structural constraints
Status: not started

Goal:
Expose the first real trade-study knobs on the cantilever model.

Scope:
- Add the initial design variables for the cantilever wing box and spar concept.
- Add structural constraints such as stress and tip deflection.
- Keep the implementation compatible with later OpenMDAO/MPhys integration.
- Ensure the static case still runs with the new parameterization.

Done when:
- Design variables can be changed without editing solver internals.
- Structural constraints are represented in a clear, testable way.
- A static run with those variables and constraints still produces artifacts.

Validation commands:
- `pytest -q tests/unit/test_design_vars.py`
- `pytest -q tests/unit/test_constraints.py`
- `pytest -q tests/integration/test_cantilever_parametric_static.py`
- `python scripts/run_cantilever_static.py --config examples/minimal_cantilever.yaml --output artifacts/cantilever_static`

Artifacts:
- updated `artifacts/cantilever_static/`

### M8 - Verify and lock the cantilever baseline outputs
Status: not started

Goal:
Promote the cantilever case from “runs” to “trusted enough to build on.”

Scope:
- Add baseline regression summaries for mass, representative stress outputs, and deflection outputs.
- Save standard plots and postprocessed summaries.
- Document what is trusted and what is still provisional.
- Freeze a baseline artifact set for later comparison.

Done when:
- The cantilever case has a repeatable baseline run.
- Baseline plots and machine-readable summaries exist under `artifacts/cantilever_verified/`.
- Regression tolerances are documented.

Validation commands:
- `pytest -q tests/regression/test_cantilever_baseline.py`
- `python scripts/export_cantilever_baseline.py --output artifacts/cantilever_verified`

Artifacts:
- `artifacts/cantilever_verified/`

### M9 - Wrap the validated cantilever case in OpenMDAO/MPhys and check derivatives
Status: not started

Goal:
Only after the cantilever baseline is trusted, add the optimization architecture layer.

Scope:
- Wrap the working cantilever structural model using MPhys/TacsBuilder and repository-owned OpenMDAO groups.
- Connect design variables, constraints, and objective.
- Add derivative checks and document acceptable tolerances.

Done when:
- The cantilever case runs through an OpenMDAO/MPhys path.
- `check_partials` or `check_totals` runs and the result is recorded.
- The repository has a stable optimization entry point for the cantilever case.

Validation commands:
- `pytest -q tests/integration/test_mphys_cantilever_setup.py`
- `python scripts/check_cantilever_derivatives.py --output artifacts/cantilever_verified/derivatives`

Artifacts:
- derivative report under `artifacts/cantilever_verified/derivatives/`

Notes:
- Do not add MPhys earlier than this milestone unless a blocker requires that change and the reason is recorded.

### M10 - Run the cantilever trade study and generate contour plots
Status: not started

Goal:
Produce the first decision-usable trade-space outputs for the cantilever architecture.

Scope:
- Implement the cantilever study driver.
- Run a grid or DOE over the primary cantilever variables.
- Generate contour plots for structural mass and key active constraints.
- Save machine-readable study outputs and figures.

Done when:
- The cantilever study can be launched from a repo command.
- At least one contour family is generated and saved.
- The outputs are sufficient to discuss trends rather than only a single optimum.

Validation commands:
- `pytest -q tests/integration/test_cantilever_trade_study.py`
- `python scripts/run_cantilever_trade.py --output artifacts/cantilever_trade`

Artifacts:
- `artifacts/cantilever_trade/`

### M11 - Create the strut-braced geometry from the cantilever template
Status: not started

Goal:
Build the strut-braced case by extending the validated cantilever case, not by starting over.

Scope:
- Copy the cantilever geometry path and extend it with strut geometry inputs.
- Define the initial strut representation and attachment locations.
- Keep the strut representation simple enough to debug.
- Save geometry outputs for the strut case.

Done when:
- The repository can build the strut-braced geometry using the cantilever case as its basis.
- Geometry artifacts exist under `artifacts/strut_geometry/`.
- The strut path is cleanly separated from the cantilever path without duplicating common code unnecessarily.

Validation commands:
- `pytest -q tests/unit/test_strut_geometry.py`
- `pytest -q tests/integration/test_strut_geometry_smoke.py`
- `python scripts/run_strut_geometry.py --output artifacts/strut_geometry`

Artifacts:
- `artifacts/strut_geometry/`

Notes:
- The first strut model may be a 1D member attached to the wing box if that is the most stable implementation path.

### M12 - Add strut member modeling, loads, variables, and a static baseline solve
Status: not started

Goal:
Make the strut-braced case physically meaningful enough for comparison.

Scope:
- Add the initial strut member behavior and connection assumptions.
- Add the matching load case and boundary conditions.
- Add strut-specific design variables and constraints.
- Run the first complete static strut baseline.

Done when:
- The strut-braced case runs statically from config to artifacts.
- The output summary makes the strut assumptions explicit.
- The result is suitable to use as a baseline before MPhys wrapping.

Validation commands:
- `pytest -q tests/integration/test_strut_static_case.py`
- `pytest -q tests/unit/test_strut_design_vars.py`
- `python scripts/run_strut_static.py --output artifacts/strut_static`

Artifacts:
- `artifacts/strut_static/`

### M13 - Wrap the strut-braced case in OpenMDAO/MPhys and check derivatives
Status: not started

Goal:
Bring the strut case up to the same optimization architecture level as the cantilever case.

Scope:
- Create the strut OpenMDAO/MPhys wrapper.
- Connect the strut variables, constraints, and objective.
- Run derivative checks and record tolerances.

Done when:
- The strut case runs through the OpenMDAO/MPhys path.
- Derivative checks are documented and artifacts are saved.

Validation commands:
- `pytest -q tests/integration/test_mphys_strut_setup.py`
- `python scripts/check_strut_derivatives.py --output artifacts/strut_static/derivatives`

Artifacts:
- derivative report under `artifacts/strut_static/derivatives/`

### M14 - Run the strut-braced trade study and generate contour plots
Status: not started

Goal:
Generate the same class of decision-usable outputs for the strut architecture.

Scope:
- Implement the strut trade-study driver.
- Run the selected study grid or DOE.
- Generate contour plots and summary tables.
- Save all outputs in the standard location.

Done when:
- The strut trade study runs from a documented repo command.
- At least one contour family is produced for the strut case.
- Results are organized for direct comparison with the cantilever outputs.

Validation commands:
- `pytest -q tests/integration/test_strut_trade_study.py`
- `python scripts/run_strut_trade.py --output artifacts/strut_trade`

Artifacts:
- `artifacts/strut_trade/`

### M15 - Compare cantilever and strut-braced results and publish final artifacts
Status: not started

Goal:
Turn two separate studies into a decision-ready comparison.

Scope:
- Create side-by-side summary tables.
- Compare best-feasible designs, active constraints, and sensitivity trends.
- Save a final comparison package and concise written interpretation.
- Document what is trusted, what is provisional, and what the next fidelity upgrade should be.

Done when:
- The repository produces a final comparison artifact set.
- The summary can answer the top-level project question with quantitative support.
- The final docs explain assumptions, limitations, and next steps.

Validation commands:
- `pytest -q tests/integration/test_final_comparison_artifacts.py`
- `python scripts/export_final_comparison.py --cantilever artifacts/cantilever_trade --strut artifacts/strut_trade --output artifacts/comparison`

Artifacts:
- `artifacts/comparison/`

## Decision log
- Added a lightweight top-level `wing_trade_study` package shim so `python -m wing_trade_study.cli.main ...` works from a source checkout before editable install succeeds.
- Kept solver dependency probing in `doctor` as an explicit availability check that returns machine-readable status and nonzero exit when the solver stack is unavailable.

## Blockers
- The geometry seed file referenced in `docs/spec.md` is not currently present in the uploaded workspace. Current uploaded file `openmdao_constraint.py` is only a minimal constraint helper.
- `python -m pip install -e ".[dev]"` fails in this environment because pip cannot reach the package index and cannot install build requirements (`setuptools>=68`).
- `python -m pip install -e ".[dev]" --no-build-isolation` also fails because the interpreter image does not have `setuptools` installed (`BackendUnavailable: Cannot import 'setuptools.build_meta'`).

## Rules for updating this file after each run
At the end of every Codex run:
1. Mark the milestone status accurately.
2. Update `Current status`.
3. Append any modeling or architecture choices to `Decision log`.
4. Record exact failing commands or missing dependencies in `Blockers`.
5. Set the next recommended action.
