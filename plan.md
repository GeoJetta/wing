# plan.md — Strut-Braced vs Cantilever Wing Trade Study (TACS + OpenMDAO/MPhys)

## 0) Purpose and success definition
Build a **large, convention-following Python project** that computes and visualizes a structural trade study between:
- a **strut-braced wing** architecture, and
- a **cantilever wing** architecture,

for a commuter-class aircraft in the Cessna SkyCourier / Dornier 228 class.

The project must produce **hard, decision-usable numbers** (e.g., structural mass trends, stress margins, displacement limits, and sensitivity-informed contour maps) that can confirm or disprove team hypotheses about configuration efficiency.

### Primary outcomes
1. Reproducible structural analyses at low-to-medium fidelity using TACS.
2. Gradient-based exploration using OpenMDAO/MPhys automatic differentiation workflows.
3. Contour plots and summary tables of structural weight vs key design variables.
4. Clear comparison of benefits and drawbacks of strut-braced vs cantilever concepts.

---

## 1) OpenAI-style plan quality requirements (must follow)
This plan and its execution should follow the spirit of a high-quality `plan.md`:

1. **Start with outcomes, not tasks**: define what “done” looks like in measurable terms.
2. **Be explicit about scope and non-goals**: avoid accidental project bloat.
3. **Use phased milestones**: each phase should produce tangible artifacts.
4. **Define interfaces early**: lock data contracts between geometry, analysis, optimization, and reporting.
5. **Prefer convention over novelty**: use package-native patterns from OpenMDAO, MPhys, and TACS.
6. **Make assumptions visible**: document fidelity limits, loads assumptions, and simplifications.
7. **Plan for verification continuously**: each phase must include checks/tests.
8. **Include risk register + mitigations**: identify likely blockers before implementation.
9. **Preserve reproducibility**: pinned dependencies, deterministic runs, and scripted workflows.
10. **Enable handoff**: docs, examples, and architecture notes for future contributors.

---

## 2) Scope, non-goals, and assumptions

### In scope
- Structural model of wing primary load path with box-beam spar abstraction.
- Two configurations (strut-braced and cantilever) under consistent loading assumptions.
- Parametric study + gradient-enabled sweeps with OpenMDAO/MPhys + TACS.
- Generation of contour plots and comparison metrics.
- Project scaffolding suitable for long-term team development.

### Non-goals (initial release)
- High-fidelity CFD-coupled aeroelastic design.
- Full certification-level load envelopes.
- Detailed fastener/joint local FEA.
- Manufacturing cost model beyond simple proxies.

### Core assumptions (initial, to validate)
- Spar is a box beam of constant width.
- Spar height follows wing profile with bounded optimizer-adjustable scaling.
- Initial geometry/constraints come from `openmdao_semiwing_boxbeam_constraints.py` (treat as source-of-truth seed).
- Load cases are simplified but representative for concept comparison.

---

## 3) Project conventions and architecture

## 3.1 Repository layout
```text
.
├─ pyproject.toml
├─ README.md
├─ plan.md
├─ docs/
│  ├─ architecture.md
│  ├─ assumptions.md
│  ├─ verification.md
│  └─ trade_study_protocol.md
├─ src/
│  └─ wing_trade_study/
│     ├─ __init__.py
│     ├─ config/
│     │  ├─ schema.py
│     │  └─ defaults/
│     ├─ geometry/
│     │  ├─ wing_planform.py
│     │  ├─ boxbeam_param.py
│     │  └─ importers.py
│     ├─ materials/
│     │  └─ materials_db.py
│     ├─ loads/
│     │  ├─ load_cases.py
│     │  └─ envelope.py
│     ├─ analysis/
│     │  ├─ tacs_model.py
│     │  ├─ mphys_builder.py
│     │  └─ openmdao_groups.py
│     ├─ optimization/
│     │  ├─ design_vars.py
│     │  ├─ constraints.py
│     │  └─ driver_setup.py
│     ├─ studies/
│     │  ├─ cantilever_baseline.py
│     │  ├─ strut_braced_baseline.py
│     │  └─ contour_runs.py
│     ├─ postprocess/
│     │  ├─ metrics.py
│     │  ├─ contour_plot.py
│     │  └─ report_tables.py
│     ├─ io/
│     │  ├─ config_loader.py
│     │  ├─ results_store.py
│     │  └─ logging.py
│     └─ cli/
│        └─ main.py
├─ scripts/
│  ├─ run_baselines.py
│  ├─ run_trade_grid.py
│  └─ export_report_artifacts.py
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  └─ regression/
└─ examples/
   ├─ minimal_cantilever.yaml
   └─ minimal_strut_braced.yaml
```

## 3.2 Coding conventions
- Python 3.11+.
- `src/` layout, typed interfaces, dataclass/pydantic configs.
- Tooling: `ruff`, `black`, `mypy`, `pytest`, pre-commit.
- Keep physics kernels and orchestration separated.
- Avoid hidden globals; pass config/state explicitly.

## 3.3 Interface contracts (critical)
1. **Geometry API** returns normalized, validated beam/station parameters.
2. **Loads API** returns named load cases with units and sign conventions.
3. **Analysis API** takes config + load case and returns mass, stresses, displacements, and derivatives.
4. **Study API** orchestrates sweeps/optimizations and stores machine-readable results.
5. **Postprocess API** produces contour figures and summary comparison artifacts.

---

## 4) Parameterization and trade-study definition

## 4.1 Design variables (initial)
- Spar wall thickness parameters (piecewise or station-based).
- Spar height scale factors (bounded, profile-following).
- Strut attachment location(s) and strut sizing (for strut-braced case).
- Optional material and safety factor toggles for sensitivity checks.

## 4.2 Constraints (initial)
- Stress allowables / failure index thresholds.
- Tip deflection / deformation constraints.
- Buckling proxy constraints (if available at fidelity level).
- Geometric bounds (manufacturability, packaging).

## 4.3 Objective options
- Minimize structural mass subject to constraints.
- Secondary comparisons: margin robustness and sensitivity smoothness.

## 4.4 Comparison protocol
- Same mission/load assumptions for both architectures.
- Same constraint set and allowable definitions.
- Same optimizer settings where meaningful.
- Report both local optimum and nearby sensitivity landscape.

---

## 5) Phased implementation plan

## Phase 1 — Project bootstrap and guardrails
**Deliverables**
- Packaging/tooling scaffold (`pyproject.toml`, linters, tests, CI stubs).
- Config schema with validation and units strategy.
- Documentation skeleton (`architecture.md`, `assumptions.md`).

**Verification**
- Lint/type/test checks run in CI and locally.
- Example config parses successfully.

## Phase 2 — Geometry and constraint ingestion
**Deliverables**
- Import path for `openmdao_semiwing_boxbeam_constraints.py`-derived setup.
- Internal geometry representation for both wing concepts.
- Constraint mapping into shared optimization interface.

**Verification**
- Geometry invariants tested (monotonic stations, bounds, units).
- Regression snapshot of imported baseline parameters.

## Phase 3 — TACS model integration
**Deliverables**
- TACS structural model for cantilever and strut-braced variants.
- Load case definition and application utilities.
- Basic run script yielding mass + stress + displacement outputs.

**Verification**
- Known-case sanity checks against hand calculations/proxies.
- Solver convergence checks and fail-fast diagnostics.

## Phase 4 — OpenMDAO/MPhys coupling and derivatives
**Deliverables**
- OpenMDAO groups/components wrapping TACS analyses via MPhys conventions.
- Design variable / constraint / objective plumbing.
- Total derivative checks at component/system levels.

**Verification**
- `check_partials`/`check_totals` thresholds documented and met.
- Consistent gradients across representative points.

## Phase 5 — Study execution and contour generation
**Deliverables**
- Scripted grid/DOE + gradient-informed refinement runs.
- Contour plots: mass vs key design-variable pairs.
- Structured outputs (CSV/Parquet/JSON + figures).

**Verification**
- Reproducibility check for repeated runs with fixed seeds/settings.
- Plot generation tests (file existence + schema checks).

## Phase 6 — Decision-ready reporting
**Deliverables**
- Comparative report with pros/cons and recommendation boundaries.
- Tables: best-feasible solutions, active constraints, sensitivity rankings.
- “What to trust / what to improve next” section.

**Verification**
- Review checklist satisfied.
- Team handoff walkthrough using docs + examples only.

---

## 6) Testing and quality strategy

### Unit tests
- Geometry transforms, bounds enforcement, units conversion.
- Config validation and defaults.

### Integration tests
- End-to-end run for minimal cantilever and strut-braced cases.
- OpenMDAO model setup and derivative pipelines.

### Regression tests
- Baseline metrics tolerance bands (mass, max stress, tip deflection).
- Contour-grid sample points remain stable across refactors.

### Performance checks
- Runtime budget per representative study.
- Memory usage bounds for medium grid runs.

---

## 7) Data management and reproducibility
- Version all input configs and assumptions.
- Save run metadata (git SHA, dependency lock, datetime, machine info).
- Store artifacts under structured run directories.
- Provide single-command reproduction for headline results.

---

## 8) Risk register and mitigations
1. **Derivative inconsistency in coupled setup**
   - Mitigation: derivative tests early; isolate offending components.
2. **Over-constrained optimization infeasibility**
   - Mitigation: staged constraint activation + feasibility diagnostics.
3. **Fidelity mismatch hides true trends**
   - Mitigation: assumptions log + targeted cross-check cases.
4. **Geometry import drift from seed script**
   - Mitigation: frozen baseline snapshots and import tests.
5. **Long run times for contour sweeps**
   - Mitigation: parallel sweep orchestration + caching + reduced-order pre-scan.

---

## 9) Immediate execution checklist for the implementing agent
1. Scaffold repository structure and tooling.
2. Add config schemas and minimal runnable examples.
3. Implement geometry importer compatible with seed constraint script.
4. Build minimal TACS solve returning mass/stress/displacement.
5. Wrap in OpenMDAO/MPhys with derivative checks.
6. Add sweep runner and contour plotting pipeline.
7. Produce first comparison package for team review.

---

## 10) Acceptance criteria (project “done”)
- Both architectures run from config to report through one CLI workflow.
- At least one validated contour family per architecture is generated.
- Comparative summary includes quantitative benefits/drawbacks with assumptions.
- Reproduction from clean environment works via documented commands.
- Tests, lint, and type checks pass in CI.

---

## 11) Notes on the provided seed file
Use `openmdao_semiwing_boxbeam_constraints.py` as the initial source for geometry and constraints mapping. Preserve traceability by:
- recording imported parameter names,
- mapping them to internal schema fields,
- and storing a machine-readable baseline snapshot for regression.
