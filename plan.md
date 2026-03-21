# plan.md — Wing Trade Study Execution Plan

## Purpose of this file
This is the executable roadmap and status log for Codex runs.

Use:
- `AGENTS.md` for permanent operating rules.
- `docs/spec.md` for the stable project objective and assumptions.
- `plan.md` for milestone order, status, validation commands, blockers, and next steps.

## What this project must accomplish
Build a reproducible structural trade study that answers a simple question with real analysis outputs:

**For the target commuter-aircraft wing, when do we get a lighter or better-constrained structure with a strut-braced wing than with a cantilever wing?**

The final project is successful only if it can:
1. Run a cantilever structural case from config to saved artifacts.
2. Run a comparable strut-braced structural case from config to saved artifacts.
3. Use TACS for the real structural solves.
4. Use OpenMDAO/MPhys for design variables, constraints, and optimization studies.
5. Save plots, contour maps, and summary tables that support a side-by-side comparison.
6. Reproduce the headline results from documented commands.

## Non-goals for the first complete version
- No CFD or aeroelastic coupling beyond what is needed for structural loads input.
- No certification-level load envelope.
- No local fastener/joint detail FEA.
- No manufacturing or operating cost model beyond simple structural-weight comparison.

## Working model assumptions for the first complete version
- The wing primary structure is represented as a wing box with an initial spar concept.
- The cantilever case is built first and becomes the template for the strut-braced case.
- The strut can initially be modeled as a simpler 1D member or equivalent structural element attached to the wing box.
- Load cases start simple and become more representative over time; they do not need to start comprehensive.
- The project must never report proxy or placeholder results as if they came from TACS.

## Standard output locations
All milestone work should save artifacts under `artifacts/` using a predictable layout.

```text
artifacts/
├─ env_smoke/
├─ cantilever_example/
├─ cantilever_geometry/
├─ cantilever_static/
├─ cantilever_verified/
├─ cantilever_trade/
├─ strut_geometry/
├─ strut_static/
├─ strut_trade/
└─ comparison/
```

Each saved run should include, where applicable:
- the input config,
- a small machine-readable summary (`json` or `csv`),
- generated plots,
- enough metadata to tell what code and settings produced the run.

## Operating rules for the agent
- Complete at most one milestone per run.
- Treat the first unchecked milestone as the active milestone unless the prompt explicitly overrides it.
- Prefer a small working step over a broad partial implementation.
- If TACS, MPhys, OpenMDAO, or required dependencies do not install or import, record the exact error in `Blockers` and stop.
- Do not claim that a result is valid unless the corresponding command actually ran.
- At the end of every run, update `Current Status`, `Decision Log`, and `Blockers`.

## Current Status
- Current milestone: M0
- Overall status: not started
- Last completed milestone: none
- Next recommended action: implement M0
- Latest summary: plan rewritten to follow the actual modeling path: environment first, then cantilever example, then project geometry, then loads/constraints/optimization, then the strut case, then comparison.

## Milestone checklist
- [ ] M0 - Bring up the TACS + OpenMDAO/MPhys environment and prove imports work
- [ ] M1 - Run a known cantilever example from the docs and save expected outputs
- [ ] M2 - Replace the example geometry with the project cantilever wing-box geometry
- [ ] M3 - Add project cantilever load cases and boundary conditions
- [ ] M4 - Add initial cantilever design variables and structural constraints
- [ ] M5 - Verify the cantilever case and lock a baseline set of plots/results
- [ ] M6 - Wrap the cantilever case in OpenMDAO/MPhys and verify derivatives
- [ ] M7 - Run the cantilever trade study and generate contour plots
- [ ] M8 - Create the strut-braced geometry using the cantilever case as the template
- [ ] M9 - Add strut connections, loads, variables, and a static baseline solve
- [ ] M10 - Wrap the strut-braced case in OpenMDAO/MPhys and verify derivatives
- [ ] M11 - Run the strut-braced trade study and generate contour plots
- [ ] M12 - Compare cantilever and strut-braced results and publish final artifacts

## Milestones

### M0 - Bring up the TACS + OpenMDAO/MPhys environment and prove imports work
Status: not started

Why this milestone exists:
Nothing else matters until the solver stack is real and reproducible.

Scope:
- Add or finalize the Python environment definition needed for this repo.
- Pin or document the required versions for Python, OpenMDAO, MPhys, TACS, and any plotting/mesh dependencies.
- Add a smoke-test path that proves the environment works.
- Add a short environment setup note under `docs/`.
- Add a CLI or script command that reports whether the required packages are available.

Out of scope:
- No project geometry yet.
- No study logic beyond environment verification.

Done when:
- A clean environment can be created using repo instructions.
- `openmdao`, `mphys`, and `tacs` import successfully from the repo environment.
- A smoke test or doctor command passes.
- Environment notes exist in the repo.

Validation commands:
- `python -m pip install -e ".[dev]"`
- `python -c "import openmdao; import mphys; import tacs; print('environment ok')"`
- `pytest -q tests/integration/test_environment_smoke.py`
- `python -m wing_trade_study.cli.main doctor`

Blocker handling:
- If TACS or MPhys cannot be installed in the chosen environment, record the exact failure, the platform details, and the next best workaround in `Blockers`, then stop.

### M1 - Run a known cantilever example from the docs and save expected outputs
Status: not started

Why this milestone exists:
Before changing physics or geometry, prove that a known example works inside this repository.

Scope:
- Choose the closest official or documented cantilever structural example from TACS/MPhys/OpenMDAO materials.
- Bring that example into this repo in a clear, traceable way.
- Run it without changing the underlying physics intent.
- Save the expected outputs to `artifacts/cantilever_example/`.
- Record the source of the example and any local adaptations.

Out of scope:
- No project-specific wing geometry yet.
- No project-specific design variables yet.

Done when:
- The example runs from a documented repo command.
- Expected output files exist in `artifacts/cantilever_example/`.
- At minimum, the output folder contains a run summary and the standard plots produced by the example.
- The lineage of the example is documented.

Validation commands:
- `pytest -q tests/integration/test_cantilever_example.py`
- `python scripts/run_cantilever_example.py --output artifacts/cantilever_example`

Notes:
- “Expected outputs” means the files and qualitative plot types that the documented example is supposed to generate, not hand-entered values.

### M2 - Replace the example geometry with the project cantilever wing-box geometry
Status: not started

Why this milestone exists:
Once the example works, the next step is to swap in the actual geometry we care about while keeping the problem simple enough to debug.

Scope:
- Implement the project cantilever wing planform and wing-box geometry.
- Use the seed file and project assumptions to define the geometry inputs.
- Keep the solve path as close to the working example as possible.
- Save geometry and run artifacts to `artifacts/cantilever_geometry/`.

Out of scope:
- No full load refinement yet.
- No optimization study yet.

Done when:
- The cantilever case runs using the project wing-box geometry.
- Geometry-related plots or exported representations are saved.
- The geometry path is separated cleanly from later load and optimization logic.

Validation commands:
- `pytest -q tests/unit/test_cantilever_geometry.py`
- `pytest -q tests/integration/test_cantilever_geometry_smoke.py`
- `python scripts/run_cantilever_geometry.py --output artifacts/cantilever_geometry`

### M3 - Add project cantilever load cases and boundary conditions
Status: not started

Why this milestone exists:
The project only becomes useful when the cantilever geometry is loaded in a way that reflects the intended study.

Scope:
- Implement the first project load cases for the cantilever wing.
- Define sign conventions, units, and boundary conditions explicitly.
- Start with the minimum useful static case and add load bookkeeping.
- Save load summaries and static outputs to `artifacts/cantilever_static/`.

Out of scope:
- No optimization yet.
- No strut-braced geometry yet.

Done when:
- At least one representative cantilever static case runs end to end.
- The load case definition is saved or reported in a machine-readable form.
- Force totals and boundary-condition assumptions are documented.

Validation commands:
- `pytest -q tests/unit/test_load_cases.py`
- `pytest -q tests/integration/test_cantilever_static_case.py`
- `python scripts/run_cantilever_static.py --output artifacts/cantilever_static`

Notes:
- If load implementation is too large for one run, split this milestone into smaller sub-steps in `Decision Log` before proceeding.

### M4 - Add initial cantilever design variables and structural constraints
Status: not started

Why this milestone exists:
The trade study needs a parameterized structural model, not just a fixed analysis case.

Scope:
- Add the first set of cantilever design variables.
- Start with the variables that matter most for the spar or wing-box study, such as spar width, spar thickness, and height scale.
- Implement the first structural constraints needed for a meaningful static sizing run.
- Support a static case where these variables can be changed through config or model inputs.

Out of scope:
- No full optimization study yet.
- No strut-specific variables yet.

Done when:
- The cantilever model exposes design variables for the initial sizing study.
- Static outputs include at least structural mass, a governing stress or failure measure, and a displacement measure.
- Constraint values are reported clearly for the baseline run.

Validation commands:
- `pytest -q tests/unit/test_cantilever_design_variables.py`
- `pytest -q tests/integration/test_cantilever_sizing_case.py`
- `python scripts/run_cantilever_sizing_case.py --output artifacts/cantilever_static`

### M5 - Verify the cantilever case and lock a baseline set of plots/results
Status: not started

Why this milestone exists:
Before optimizing anything, the baseline case needs a verification pass and a stable output package.

Scope:
- Review the baseline cantilever outputs for obvious errors or nonphysical behavior.
- Add the standard plots that should exist for every main case.
- Save a baseline package that later milestones can compare against.
- Add regression tolerances where practical.

Standard plots to generate:
- geometry or mesh view,
- deformed shape,
- stress or failure metric view,
- selected design-variable distribution,
- a compact summary plot or table for mass and deflection.

Out of scope:
- No gradient-based optimization yet.

Done when:
- `artifacts/cantilever_verified/` contains the baseline run package.
- The required plots are present.
- At least one regression or baseline check is added.

Validation commands:
- `pytest -q tests/regression/test_cantilever_baseline.py`
- `python scripts/export_cantilever_baseline.py --output artifacts/cantilever_verified`

### M6 - Wrap the cantilever case in OpenMDAO/MPhys and verify derivatives
Status: not started

Why this milestone exists:
The optimizer and contour studies need a working MPhys/OpenMDAO problem with trustworthy derivatives.

Scope:
- Build the cantilever OpenMDAO/MPhys model around the working TACS case.
- Register the initial design variables, objective, and constraints.
- Run derivative checks at the level that makes sense for the model.
- Keep the setup understandable and separate from study scripts.

Out of scope:
- No large parameter sweep yet.

Done when:
- The cantilever case runs through OpenMDAO/MPhys.
- Derivative checks execute and are recorded.
- The repo contains a clear run path for the cantilever optimization problem.

Validation commands:
- `pytest -q tests/integration/test_mphys_cantilever.py`
- `python scripts/check_cantilever_derivatives.py --output artifacts/cantilever_verified`
- `python scripts/run_cantilever_optimization.py --max-iter 3 --output artifacts/cantilever_verified`

### M7 - Run the cantilever trade study and generate contour plots
Status: not started

Why this milestone exists:
This is the first milestone that produces the decision-style plots the project is meant to deliver.

Scope:
- Run a cantilever trade study over selected design-variable pairs.
- Generate contour plots of structural weight and other key outputs.
- Include at least one plot family centered on spar width vs spar thickness.
- Add other useful views if they show meaningful trends, such as height scale vs thickness or stress margin vs mass.
- Save raw study outputs and plots to `artifacts/cantilever_trade/`.

Out of scope:
- No strut-braced case yet.

Done when:
- The repo can generate at least one informative contour family for the cantilever case.
- Saved outputs are sufficient to reproduce the plots without rerunning the solver logic by hand.
- Plot file names and folders are consistent.

Validation commands:
- `pytest -q tests/integration/test_cantilever_trade_study.py`
- `python scripts/run_cantilever_trade_study.py --output artifacts/cantilever_trade`

### M8 - Create the strut-braced geometry using the cantilever case as the template
Status: not started

Why this milestone exists:
The strut-braced model should reuse as much as possible from the working cantilever case rather than starting over.

Scope:
- Copy or extend the cantilever structural case into a strut-braced geometry path.
- Add the strut geometry and attachment definition.
- Represent the strut with a simple, explicit structural model first, such as a 1D member or equivalent element attached to the wing box.
- Save geometry artifacts to `artifacts/strut_geometry/`.

Out of scope:
- No full strut optimization yet.
- No final comparison yet.

Done when:
- The strut-braced geometry path is created and runs a geometry-level smoke test.
- The strut representation is documented clearly.
- Geometry outputs are saved in the expected folder.

Validation commands:
- `pytest -q tests/unit/test_strut_geometry.py`
- `pytest -q tests/integration/test_strut_geometry_smoke.py`
- `python scripts/run_strut_geometry.py --output artifacts/strut_geometry`

### M9 - Add strut connections, loads, variables, and a static baseline solve
Status: not started

Why this milestone exists:
The strut case becomes a real study case only after the connections, loads, and design variables are active.

Scope:
- Add the strut load path, connections, and boundary-condition handling.
- Implement the first strut-braced design variables.
- Reuse shared reporting outputs where possible so the strut case stays comparable to the cantilever case.
- Run a static baseline solve and save results to `artifacts/strut_static/`.

Out of scope:
- No strut optimization study yet.

Done when:
- A strut-braced static case runs end to end.
- The saved outputs include structural mass, stress or failure, and displacement metrics.
- The strut and cantilever result summaries are directly comparable.

Validation commands:
- `pytest -q tests/integration/test_strut_static_case.py`
- `python scripts/run_strut_static.py --output artifacts/strut_static`

### M10 - Wrap the strut-braced case in OpenMDAO/MPhys and verify derivatives
Status: not started

Why this milestone exists:
The strut case needs the same optimization and sensitivity path as the cantilever case before it can be studied fairly.

Scope:
- Build the OpenMDAO/MPhys path for the strut-braced case.
- Register its design variables, objective, and constraints.
- Run derivative checks for representative strut-braced points.
- Reuse shared optimization plumbing where practical.

Out of scope:
- No final contour sweep yet.

Done when:
- The strut-braced case runs through OpenMDAO/MPhys.
- Derivative checks execute and are documented.
- The strut optimization path mirrors the cantilever path closely enough for fair comparison.

Validation commands:
- `pytest -q tests/integration/test_mphys_strut.py`
- `python scripts/check_strut_derivatives.py --output artifacts/strut_static`
- `python scripts/run_strut_optimization.py --max-iter 3 --output artifacts/strut_static`

### M11 - Run the strut-braced trade study and generate contour plots
Status: not started

Why this milestone exists:
The strut-braced study needs the same style of output package as the cantilever study.

Scope:
- Run the strut-braced trade study.
- Generate contour plots and study outputs tailored to the strut case and its additional variables.
- Keep at least one contour family directly comparable to the cantilever study.
- Save outputs to `artifacts/strut_trade/`.

Out of scope:
- No final narrative comparison yet.

Done when:
- The repo can generate contour plots for the strut-braced case.
- At least one design-variable pair is directly comparable to the cantilever study.
- Additional strut-specific plots are included where they add insight.

Validation commands:
- `pytest -q tests/integration/test_strut_trade_study.py`
- `python scripts/run_strut_trade_study.py --output artifacts/strut_trade`

### M12 - Compare cantilever and strut-braced results and publish final artifacts
Status: not started

Why this milestone exists:
This is the point of the project: turn the two studies into a direct engineering comparison.

Scope:
- Gather the final cantilever and strut-braced results.
- Create tables and plots that compare structural weight, governing constraints, and sensitivity trends.
- State where the strut helps, where it hurts, and where the answer is still uncertain.
- Save the final comparison package to `artifacts/comparison/`.
- Document the commands needed to reproduce the headline results.

Out of scope:
- No new physics fidelity unless it is required to finish the comparison package.

Done when:
- The repo produces a direct cantilever vs strut comparison from saved study outputs.
- The comparison includes quantitative statements supported by saved artifacts.
- Reproduction commands are documented and tested.
- Another engineer can run the key study paths from the repo instructions.

Validation commands:
- `pytest -q`
- `python scripts/build_comparison_report.py --cantilever artifacts/cantilever_trade --strut artifacts/strut_trade --output artifacts/comparison`

## Decision Log
- 2026-03-21: Rewrote the plan so the milestones follow the actual engineering path: environment -> known cantilever example -> project cantilever model -> verification -> cantilever optimization/trade study -> strut model -> strut optimization/trade study -> comparison.
- 2026-03-21: The first trusted solver result must come from a reproduced known example before the project-specific geometry is introduced.
- 2026-03-21: The strut will initially be modeled with a simpler explicit structural representation rather than waiting for a high-fidelity strut model.
- 2026-03-21: Trade-study plots should be saved as artifacts, not rebuilt manually after the fact.

## Blockers
- None recorded yet.

## Next Milestone Notes
M0 should focus only on making the TACS + MPhys + OpenMDAO stack usable in this repo. Do not start project geometry or optimization work until the environment and imports are proven.
