# docs/spec.md

## Purpose
Build a convention-following Python project that computes and visualizes a structural trade study between:
- a strut-braced wing architecture, and
- a cantilever wing architecture,

for a commuter-class aircraft in the Cessna SkyCourier / Dornier 228 class.

The project must produce hard, decision-usable numbers that can confirm or disprove hypotheses about configuration efficiency.

## Primary outcomes
1. Reproducible low-to-medium fidelity structural analyses using TACS.
2. Gradient-enabled exploration using OpenMDAO/MPhys workflows.
3. Contour plots and summary tables of structural weight versus key design variables.
4. Clear comparison of benefits and drawbacks of strut-braced versus cantilever concepts.
5. Reproducible scripts and docs that allow a future contributor to rerun the headline study from a clean environment.

## Decision questions the project should answer
- Under the same load assumptions and constraints, which architecture reaches lower structural mass?
- Which constraints are typically active near the best feasible designs?
- How sensitive are the results to spar thickness, spar height scaling, strut attachment location, and strut sizing?
- Are any apparent advantages robust in the nearby design space, or are they narrow local effects?

## In scope
- Structural model of the wing primary load path using a box-beam spar abstraction.
- Two architectures: cantilever and strut-braced.
- Shared loading assumptions for both architectures.
- Parametric study plus gradient-enabled sweeps using OpenMDAO/MPhys and TACS.
- Structured outputs, contour plots, summary tables, and a comparative report.
- Repository scaffolding suitable for long-term team development.

## Non-goals for the initial release
- High-fidelity CFD-coupled aeroelastic design.
- Certification-level load envelopes.
- Detailed fastener, joint, or local FEA modeling.
- Manufacturing cost modeling beyond simple proxies.
- Full aircraft multidisciplinary optimization beyond the wing structural trade study.

## Modeling assumptions to make explicit and maintain
- The spar is modeled as a box beam with constant width in the initial release.
- Spar height follows the wing profile with bounded optimizer-adjustable scaling.
- Initial geometry and constraints come from `openmdao_semiwing_boxbeam_constraints.py`.
- Load cases are simplified but should be representative enough for concept comparison.
- Any fidelity limitation that could change the decision must be written in `docs/assumptions.md`.

## Architecture and implementation preferences
- Python 3.11+.
- `src/` layout with typed interfaces.
- Pydantic at the config boundary; dataclasses or similarly explicit typed objects internally.
- `ruff`, `black`, `mypy`, `pytest`, and pre-commit.
- Separate physics kernels from orchestration and postprocessing.
- Avoid hidden globals; pass configuration and state explicitly.
- Prefer package-native OpenMDAO, MPhys, and TACS patterns over custom abstractions.

## Target repository layout
```text
.
├─ pyproject.toml
├─ README.md
├─ AGENTS.md
├─ plan.md
├─ docs/
│  ├─ spec.md
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

## Core interfaces
1. Geometry API returns normalized, validated beam and station parameters.
2. Loads API returns named load cases with explicit units and sign conventions.
3. Analysis API accepts a validated config plus load case and returns mass, stresses, displacements, and derivatives when available.
4. Study API orchestrates sweeps or optimizations and writes machine-readable results.
5. Postprocess API produces contour figures, tables, and report artifacts from saved results.

## Initial design variables
- Spar wall thickness parameters, either station-based or piecewise.
- Spar height scale factors that remain bounded and profile-following.
- Strut attachment location and strut sizing parameters for the strut-braced case.
- Optional material choice or safety factor toggles for sensitivity studies.

## Initial constraints
- Stress allowables or failure index limits.
- Tip deflection or deformation limits.
- Buckling proxy constraints if available at the selected fidelity.
- Geometric bounds tied to manufacturability and packaging.

## Objectives
Primary objective:
- Minimize structural mass subject to constraints.

Secondary comparison metrics:
- Constraint robustness.
- Sensitivity smoothness and contour interpretability.
- Nearby feasible landscape quality, not just a single local optimum.

## Comparison protocol
- Use the same mission and load assumptions for both architectures.
- Use the same constraint set and allowable definitions.
- Use the same optimizer settings when comparisons are meaningful.
- Report both the best feasible point and the nearby landscape.

## Verification philosophy
- Verification is continuous, not deferred to the end.
- Cross-check simple cases against closed-form beam proxies where appropriate.
- Run derivative checks for OpenMDAO/MPhys integrations.
- Maintain regression tolerances for baseline metrics and representative contour samples.
- Treat any solver caveat or skipped integration test as a documented limitation, not as silent success.

## Reproducibility requirements
- Version all configs and assumptions.
- Save run metadata, including git SHA when available, dependency versions, timestamp, and machine info.
- Store artifacts under structured run directories.
- Provide single-command reproduction for headline results once the relevant milestones are complete.

## Seed file traceability requirement
`openmdao_semiwing_boxbeam_constraints.py` is the initial source of truth for geometry and constraint mapping. Preserve traceability by:
- recording imported parameter names,
- mapping them to internal schema fields,
- storing a machine-readable baseline snapshot,
- and documenting any assumptions or unit conversions introduced during import.

## Hard constraints on execution quality
- The project may use scaffolding and verification proxies early, but the final study results must come from the real TACS-backed path.
- If the environment cannot support TACS or MPhys, the repository should still make the blocker obvious and reproducible instead of pretending the study is complete.
