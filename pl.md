# plan.md

## Purpose of this file
This is the executable project roadmap and status log for Codex runs.

Use:
- `AGENTS.md` for permanent operating rules.
- `docs/spec.md` for stable project intent.
- `plan.md` for milestone order, scope boundaries, validation commands, status, blockers, and decisions.

## Operating rules for the agent
- Complete at most one milestone per run.
- Treat the first unchecked milestone as the active milestone unless the prompt explicitly overrides this.
- If a validation command fails, fix it or record a blocker before doing anything else.
- If TACS, MPhys, or other required solver dependencies are unavailable, document the exact failure and stop rather than faking results.
- Update `Current Status`, `Decision Log`, and `Blockers` at the end of every run.

## Current Status
- Current milestone: M0
- Overall status: not started
- Last completed milestone: none
- Next recommended action: implement M0
- Latest summary: initial plan converted into executable repo guidance; implementation has not started yet

## Milestone checklist
- [ ] M0 - Bootstrap package, tooling, docs shell, and CLI stubs
- [ ] M1 - Config schema, result schema, example YAMLs, and config validation path
- [ ] M2 - Seed importer and machine-readable baseline snapshot
- [ ] M3 - Geometry and load-case domain model for both architectures
- [ ] M4 - Solver-agnostic analysis interface plus analytic verification proxies
- [ ] M5 - TACS-backed cantilever baseline solve
- [ ] M6 - TACS-backed strut-braced baseline solve
- [ ] M7 - OpenMDAO/MPhys cantilever coupling and derivative checks
- [ ] M8 - OpenMDAO/MPhys strut-braced coupling, design vars, constraints, and objective plumbing
- [ ] M9 - Trade-grid execution, contour generation, and structured result storage
- [ ] M10 - Decision-ready comparison artifacts, documentation, and reproduction flow

## Milestones

### M0 - Bootstrap package, tooling, docs shell, and CLI stubs
Status: not started

Scope:
- Create `pyproject.toml` with project metadata and dev tooling.
- Create `src/wing_trade_study/` package skeleton.
- Add `ruff`, `black`, `mypy`, `pytest`, and pre-commit configuration.
- Add placeholder docs files: `docs/architecture.md`, `docs/assumptions.md`, `docs/verification.md`, `docs/trade_study_protocol.md`.
- Add CLI entry point with `--help` working.
- Add minimal smoke tests that prove the package imports and the CLI starts.

Out of scope:
- No solver integration.
- No study logic beyond package scaffolding.

Done when:
- Repository structure exists as described in `docs/spec.md`.
- `python -m pip install -e ".[dev]"` works.
- Static checks and initial smoke tests pass.
- CLI help works.

Validation commands:
- `python -m pip install -e ".[dev]"`
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/unit/test_project_smoke.py`
- `python -m wing_trade_study.cli.main --help`

### M1 - Config schema, result schema, example YAMLs, and config validation path
Status: not started

Scope:
- Implement external config schema under `wing_trade_study.config`.
- Implement result metadata schema for saved study outputs.
- Add `examples/minimal_cantilever.yaml` and `examples/minimal_strut_braced.yaml`.
- Add config loader and CLI command or script path that validates configs.

Out of scope:
- No seed import yet.
- No solver execution yet.

Done when:
- Both example YAML files parse and validate.
- Invalid configs fail with informative validation errors.
- Result metadata schema exists for future study outputs.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/unit/test_config_schema.py`
- `python -m wing_trade_study.cli.main validate-config examples/minimal_cantilever.yaml`
- `python -m wing_trade_study.cli.main validate-config examples/minimal_strut_braced.yaml`

### M2 - Seed importer and machine-readable baseline snapshot
Status: not started

Scope:
- Implement importer support for `openmdao_semiwing_boxbeam_constraints.py`.
- Map imported parameter names to internal schema fields.
- Write a machine-readable baseline snapshot suitable for regression tests.
- Document import assumptions and any unit conversions.

Out of scope:
- No TACS solve yet.
- No optimization plumbing yet.

Done when:
- The importer can read the seed file and produce a normalized internal representation or baseline snapshot.
- Imported fields are traceable back to original names.
- A regression test locks the imported baseline snapshot.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/unit/test_seed_import.py`
- `python -m wing_trade_study.cli.main import-seed --input openmdao_semiwing_boxbeam_constraints.py --output artifacts/baseline_snapshot.json`

Notes:
- If the seed file is not present at the repository root, locate it by filename, update the path in docs, and record the resolution in `Decision Log`.

### M3 - Geometry and load-case domain model for both architectures
Status: not started

Scope:
- Implement normalized geometry objects for cantilever and strut-braced variants.
- Implement load-case datamodels with explicit units and sign conventions.
- Add baseline builders that create valid analysis-ready inputs from imported and manual configs.
- Test geometry invariants and load-case invariants.

Out of scope:
- No real solver call yet.
- No derivative plumbing yet.

Done when:
- Both architectures can be built into normalized geometry representations.
- Geometry station ordering, bounds, and load sign conventions are tested.
- The code can build analysis-ready input data structures from example configs.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/unit/test_geometry.py`
- `pytest -q tests/unit/test_load_cases.py`

### M4 - Solver-agnostic analysis interface plus analytic verification proxies
Status: not started

Scope:
- Define the shared analysis input and output interfaces.
- Implement analytic beam verification utilities for simple cross-check cases.
- Add tests that compare simple proxy calculations against expected hand-derived behavior.
- Wire the analysis interface so later TACS integration plugs into a stable contract.

Out of scope:
- Do not present analytic proxy results as TACS results.
- No MPhys coupling yet.

Done when:
- A shared analysis contract exists and is used by baseline study code.
- Analytic verification proxies are clearly separated and documented as verification-only.
- Unit tests cover the proxy checks.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/unit/test_analysis_contract.py`
- `pytest -q tests/unit/test_beam_verification_proxies.py`

### M5 - TACS-backed cantilever baseline solve
Status: not started

Scope:
- Implement the minimal TACS-backed structural model for the cantilever case.
- Apply at least one representative named load case.
- Return structural mass, a governing stress or failure metric, and a key displacement metric.
- Add convergence diagnostics and fail-fast error handling.

Out of scope:
- No strut-braced solve yet.
- No OpenMDAO coupling yet.

Done when:
- A cantilever baseline solve runs from config through the real TACS path.
- The result is returned through the shared analysis interface.
- A targeted integration test covers the cantilever baseline path.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/integration/test_tacs_cantilever.py`
- `python scripts/run_baselines.py --config examples/minimal_cantilever.yaml`

Blocker handling:
- If TACS cannot be installed or imported in the environment, capture the exact install or runtime failure in `Blockers` and stop.

### M6 - TACS-backed strut-braced baseline solve
Status: not started

Scope:
- Extend the TACS-backed model to the strut-braced case.
- Implement the strut-specific geometry and sizing path needed for the baseline solve.
- Reuse the shared analysis interface and result schema.

Out of scope:
- No OpenMDAO coupling yet.
- No grid search or contours yet.

Done when:
- A strut-braced baseline solve runs from config through the real TACS path.
- Output fields are directly comparable to the cantilever baseline outputs.
- A targeted integration test covers the strut-braced baseline path.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/integration/test_tacs_strut_braced.py`
- `python scripts/run_baselines.py --config examples/minimal_strut_braced.yaml`

### M7 - OpenMDAO/MPhys cantilever coupling and derivative checks
Status: not started

Scope:
- Wrap the cantilever TACS analysis in OpenMDAO/MPhys conventions.
- Implement design variable, objective, and constraint plumbing needed for the cantilever case.
- Add derivative checks at the appropriate component or group level.

Out of scope:
- No strut-braced optimization plumbing yet.
- No final reporting yet.

Done when:
- The cantilever path is runnable through OpenMDAO/MPhys.
- Derivative tests execute and documented tolerances are met.
- The code clearly separates solver setup from optimization driver setup.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/integration/test_mphys_cantilever.py`

### M8 - OpenMDAO/MPhys strut-braced coupling, design vars, constraints, and objective plumbing
Status: not started

Scope:
- Extend the OpenMDAO/MPhys path to the strut-braced architecture.
- Implement shared design variable and constraint registration where appropriate.
- Ensure architecture-specific variables are isolated behind explicit interfaces.
- Add derivative checks for representative strut-braced points.

Out of scope:
- No grid or contour runs yet.
- No final report package yet.

Done when:
- The strut-braced path runs through OpenMDAO/MPhys.
- Derivative checks are implemented and documented.
- Both architectures share consistent objective and constraint definitions.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/integration/test_mphys_strut_braced.py`

### M9 - Trade-grid execution, contour generation, and structured result storage
Status: not started

Scope:
- Implement the scripted grid or DOE runners.
- Write structured result artifacts to disk.
- Generate contour plots for at least one validated variable pair per architecture.
- Add reproducibility metadata capture for study runs.

Out of scope:
- No final comparative narrative yet.

Done when:
- A small trade grid runs for each architecture from config.
- Machine-readable artifacts are written with run metadata.
- At least one contour family per architecture is generated from saved results.
- Plot generation is test-covered at a smoke-test level.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/integration/test_trade_grid_smoke.py`
- `pytest -q tests/regression/test_contour_artifacts.py`
- `python scripts/run_trade_grid.py --config examples/minimal_cantilever.yaml --grid small`
- `python scripts/run_trade_grid.py --config examples/minimal_strut_braced.yaml --grid small`

### M10 - Decision-ready comparison artifacts, documentation, and reproduction flow
Status: not started

Scope:
- Produce comparative tables and summary artifacts.
- Document what is trustworthy, what assumptions dominate the results, and what to improve next.
- Ensure headline results have single-command reproduction paths.
- Finalize docs for architecture, assumptions, verification, and trade-study protocol.

Out of scope:
- No new modeling fidelity beyond what earlier milestones established.

Done when:
- Both architectures run from config to saved report artifacts through documented commands.
- Comparative outputs include quantitative benefits and drawbacks with assumptions.
- Reproduction instructions work from a clean environment.
- The repo is handoff-ready for another engineer.

Validation commands:
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q`
- `python scripts/run_baselines.py --config examples/minimal_cantilever.yaml`
- `python scripts/run_baselines.py --config examples/minimal_strut_braced.yaml`
- `python scripts/run_trade_grid.py --config examples/minimal_cantilever.yaml --grid small`
- `python scripts/run_trade_grid.py --config examples/minimal_strut_braced.yaml --grid small`

## Decision Log
- 2026-03-20: The original single `plan.md` was split conceptually into `docs/spec.md` for stable specification and `plan.md` for executable milestone tracking.
- 2026-03-20: Config boundary will use Pydantic v2; internal domain objects may use dataclasses where helpful.
- 2026-03-20: Analytic beam models are allowed only as verification proxies and must never be reported as TACS results.
- 2026-03-20: Final study credibility depends on a real TACS-backed path; missing solver availability is a blocker, not a reason to fake outputs.

## Blockers
- None recorded yet.

## Next Milestone Notes
M0 should establish the package skeleton and quality gates first. Do not attempt solver integration before the package, config path, and docs shell exist.
