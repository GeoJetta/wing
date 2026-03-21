# AGENTS.md

## Read this first
Before changing code, read these files in order:

1. `AGENTS.md`
2. `docs/spec.md`
3. `plan.md`

Use them this way:
- `AGENTS.md` defines permanent operating rules.
- `docs/spec.md` defines the stable project specification and non-goals.
- `plan.md` defines the current executable milestone, status, decisions, and blockers.

If they conflict, follow:
1. `AGENTS.md` for operating behavior,
2. `docs/spec.md` for project intent,
3. `plan.md` for the active implementation slice.

## Working mode
- Complete at most one milestone per run unless the prompt explicitly overrides this.
- Keep diffs narrowly scoped to the active milestone in `plan.md`.
- Make the smallest change that satisfies the milestone and its validation commands.
- Prefer convention over novelty. Use familiar OpenMDAO, MPhys, and TACS patterns instead of custom frameworks.
- When runtime code changes, update tests and docs in the same run.
- Do not start speculative refactors or "while I am here" cleanups.

## Project goal
Build a reproducible Python project that compares strut-braced and cantilever wing structural concepts for a commuter-class aircraft using TACS plus OpenMDAO/MPhys workflows. The project must produce decision-usable structural outputs: mass trends, stress margins, displacement limits, and sensitivity-informed contour plots.

## Non-negotiable engineering rules
- Do not invent TACS, OpenMDAO, or MPhys outputs.
- Do not silently replace unavailable solver behavior with fabricated values.
- Analytic beam equations are allowed only for verification utilities, smoke checks, and unit tests. They must be clearly labeled as verification proxies and must never be reported as TACS results.
- Keep both architectures on the same units, loads, constraint definitions, and report conventions unless the spec explicitly says otherwise.
- Preserve traceability from `openmdao_semiwing_boxbeam_constraints.py` into internal schema fields and a machine-readable baseline snapshot.
- Keep physics kernels, orchestration, and postprocessing separate.
- Keep inputs and outputs machine-readable. Avoid burying essential data only in prose logs.
- If a solver dependency is unavailable or broken, document the exact blocker and stop. Do not fake completion.

## Repository conventions
- Python version: 3.11 or newer.
- Use `src/` layout.
- Use typed interfaces throughout the package.
- Use Pydantic v2 models for external config parsing and validation.
- Use dataclasses for internal domain objects where they improve clarity.
- Persist units explicitly and prefer SI units at the config boundary. If imported seed values are not in SI units, convert them and record the original source values in the imported snapshot.
- Keep side effects at the edges: CLI, scripts, and IO layers.
- Avoid hidden global state; pass config and state explicitly.

## Expected repository layout
- `src/wing_trade_study/`: package code
- `tests/unit/`: pure logic tests
- `tests/integration/`: multi-module and solver-coupled tests
- `tests/regression/`: tolerance-based baseline checks
- `examples/`: minimal runnable YAML configs
- `docs/`: architecture, assumptions, verification, and study protocol
- `scripts/`: reproducible entry points for baselines, trade grids, and report exports

## Required commands
These commands should exist and remain valid as the repository matures.

Environment install:
- `python -m pip install -U pip`
- `python -m pip install -e ".[dev]"`

Formatting and static checks:
- `ruff check .`
- `black --check .`
- `mypy src`

Test entry points:
- `pytest -q`
- `pytest -q tests/unit`
- `pytest -q tests/integration`
- `pytest -q tests/regression`

Smoke commands:
- `python -m wing_trade_study.cli.main --help`
- `python scripts/run_baselines.py --help`
- `python scripts/run_trade_grid.py --help`

Expected study commands by the time the relevant milestones are complete:
- `python scripts/run_baselines.py --config examples/minimal_cantilever.yaml`
- `python scripts/run_baselines.py --config examples/minimal_strut_braced.yaml`
- `python scripts/run_trade_grid.py --config examples/minimal_cantilever.yaml --grid small`
- `python scripts/run_trade_grid.py --config examples/minimal_strut_braced.yaml --grid small`

## Validation policy
When you change code, run the smallest validation set that still proves the milestone is correct.

Minimum expectations:
- Docs-only changes: no code validation required.
- Changes under `src/`, `scripts/`, or `tests/`: run `ruff check .`, `black --check .`, `mypy src`, and the targeted `pytest` subset for the changed area.
- Changes that affect CLI wiring: also run `python -m wing_trade_study.cli.main --help`.
- Changes that affect examples or config parsing: run config-related unit tests and validate both minimal example YAML files.
- Changes that affect TACS or MPhys plumbing: run the targeted integration tests for that path and record any environment limitation in `plan.md`.
- Do not mark a milestone complete until every listed validation command for that milestone passes, or a concrete blocker is recorded.

## Data and interface contracts
Honor these contracts unless the active milestone explicitly changes them and the docs are updated in the same run.

### Config boundary
- External study inputs come from YAML files.
- Config parsing belongs under `wing_trade_study.config` and `wing_trade_study.io`.
- Parsed configs must validate architecture type, geometry parameters, load cases, material selections, bounds, and output settings.

### Geometry API
- Geometry functions return normalized and validated station-wise parameters.
- Geometry must expose both cantilever and strut-braced variants through a shared interface.

### Loads API
- Loads must be named, unit-explicit, and sign-convention-explicit.
- Load cases must be reusable across both architectures.

### Analysis API
- Analysis entry points accept a validated config plus a named load case.
- Analysis results must expose at least structural mass, governing stress metric or failure index, key displacement metrics, and enough metadata to trace the run and solver settings.
- Derivative-related outputs must be explicit when available; do not imply gradients exist if they do not.

### Study API
- Studies orchestrate sweeps and optimizations and write machine-readable results.
- Results storage must capture run metadata: git SHA when available, dependency versions when available, config path, timestamp, and machine info.

### Postprocess API
- Postprocessing must be deterministic for a fixed input result set.
- Figures and tables must be reproducible from saved results without rerunning the full solver when possible.

## Dependency and environment rules
- Pin direct dependencies in `pyproject.toml`.
- Prefer extras for optional heavy dependencies when that improves developer ergonomics, but do not split the real solver path behind a fake implementation.
- If TACS or MPhys need system packages or MPI-related setup, document the exact requirements in `README.md` and `docs/verification.md` as soon as they are discovered.
- Do not add a dependency unless it is clearly justified by the active milestone.

## Documentation update rules
When a milestone changes behavior or interfaces, update the relevant docs in the same run:
- `docs/architecture.md` for structure and boundaries
- `docs/assumptions.md` for modeling assumptions and fidelity limits
- `docs/verification.md` for checks, tolerances, and solver caveats
- `docs/trade_study_protocol.md` for how the comparison is executed

## Blocker protocol
If you hit a blocker:
1. Reduce it to the smallest failing command or failing test.
2. Record the exact command, observed error, and likely cause in `plan.md`.
3. Note whether the blocker is environmental, dependency-related, data-related, or design-related.
4. Stop after leaving the repository in a clean, coherent state.

## Completion checklist for any milestone
Before declaring a milestone complete:
- The milestone scope in `plan.md` is satisfied.
- The milestone validation commands were run and passed.
- Relevant tests were added or updated.
- Relevant docs were added or updated.
- `plan.md` was updated with status, decisions, blockers, and the next recommended milestone.

## Things to avoid
- Do not hardcode one-off paths if a stable config or interface belongs instead.
- Do not build a custom meta-framework around OpenMDAO or TACS.
- Do not mix study orchestration with plotting or report generation logic.
- Do not edit `.codex/` files unless the prompt explicitly asks for it.
- Do not perform Git history mutation or remote operations unless explicitly asked.
