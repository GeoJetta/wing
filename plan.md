# plan.md

## Purpose of this file
This is the executable roadmap and status log for Codex runs.

Use:
- `AGENTS.md` for permanent operating rules.
- `docs/spec.md` for the stable project objective and architecture.
- `plan.md` for milestone order, exact scope, validation commands, status, blockers, and decisions.

## Core project objective
Build a reproducible Python project that performs a structural trade study between:
- a cantilever wing, and
- a strut-braced wing,

using TACS with OpenMDAO/MPhys where appropriate.

The project is complete when it can:
1. run a validated cantilever structural case,
2. evolve that case into a representative wing-box/spar model with design variables and constraints,
3. generate optimization-based contour plots and trend visualizations for the cantilever case,
4. implement and run the analogous strut-braced case,
5. generate comparable optimization outputs for the strut-braced case, and
6. compare structural weight and constraint behavior between the two architectures.

## Operating rules for the agent
- Complete at most one milestone per run.
- Treat the first unchecked milestone as the active milestone unless the prompt explicitly overrides this.
- Use the example-driven path first: reproduce a known working case before building custom geometry.
- Do not claim TACS/MPhys functionality unless it actually runs in the current environment.
- If a required dependency, example, input file, or solver setup is missing, record the exact blocker and stop.
- Update `Current Status`, `Decision Log`, and `Blockers` at the end of every run.

## Current Status
- Current milestone: M0
- Overall status: not started
- Last completed milestone: none
- Next recommended action: implement M0
- Latest summary: plan rewritten to follow an example-first build sequence focused on real solver setup, validated cantilever execution, then strut extension

## Milestone checklist
- [ ] M0 - Set up the Python environment, package scaffold, and quality gates
- [ ] M1 - Install and verify TACS / OpenMDAO / MPhys with a known working example
- [ ] M2 - Reproduce a cantilever example case and confirm expected outputs and plots
- [ ] M3 - Replace the example geometry with the target cantilever wing geometry
- [ ] M4 - Build the first representative wing-box / spar structural model for the cantilever case
- [ ] M5 - Add constraints, design variables, and a static cantilever analysis workflow
- [ ] M6 - Refine cantilever loads, verify outputs, and stabilize result/plot generation
- [ ] M7 - Add OpenMDAO/MPhys optimization plumbing for the cantilever case
- [ ] M8 - Run cantilever parameter sweeps and generate contour/trend plots
- [ ] M9 - Clone the cantilever case into a strut-braced structural model
- [ ] M10 - Add strut design variables, constraints, loads, and optimization plumbing
- [ ] M11 - Run strut-braced sweeps and generate contour/trend plots
- [ ] M12 - Compare cantilever vs strut-braced results and finalize deliverables

## Milestones

### M0 - Set up the Python environment, package scaffold, and quality gates
Status: not started

Why this milestone exists:
The project must have a stable package, CLI, tests, and reproducible install path before solver work begins.

Scope:
- Create or finalize `pyproject.toml`.
- Create `src/wing_trade_study/` package structure.
- Add `ruff`, `black`, `mypy`, `pytest`, and pre-commit configuration.
- Add minimal docs shell and CLI entry point.
- Add smoke tests for package import and CLI startup.

Out of scope:
- No TACS or MPhys integration yet.
- No study logic yet.

Done when:
- Editable install works.
- Static checks run.
- Minimal smoke tests pass.
- CLI help runs.

Validation commands:
- `python -m pip install -e ".[dev]"`
- `ruff check .`
- `black --check .`
- `mypy src`
- `pytest -q tests/unit/test_project_smoke.py`
- `python -m wing_trade_study.cli.main --help`

### M1 - Install and verify TACS / OpenMDAO / MPhys with a known working example
Status: not started

Why this milestone exists:
The main technical risk is environment and dependency setup. This must be resolved before custom model development.

Scope:
- Document exact installation steps for TACS, OpenMDAO, and MPhys.
- Verify imports in the project environment.
- Locate a known working structural example from the relevant docs/examples.
- Add a minimal environment verification script or test.

Out of scope:
- No custom wing geometry yet.
- No custom optimization setup yet.

Done when:
- TACS, OpenMDAO, and MPhys imports work in the project environment.
- A known example can at least be configured to run or is proven blocked with an exact reason.
- Environment/setup instructions are captured in docs.

Validation commands:
- `python -c "import openmdao; import mphys; import tacs; print('imports ok')"`
- `pytest -q tests/integration/test_environment_imports.py`

Blocker handling:
- If any dependency cannot be installed or imported, record the exact command, error, and environment state in `Blockers` and stop.

### M2 - Reproduce a cantilever example case and confirm expected outputs and plots
Status: not started

Why this milestone exists:
A working reference case is the safest starting point. The project should first prove that it can run an example and produce expected artifacts before changing the model.

Scope:
- Add a reproducible script or CLI path to run the chosen example.
- Store outputs in a consistent artifact directory.
- Confirm expected plots or result files appear in the correct folder.
- Record what “expected output” means for the chosen example.

Out of scope:
- No custom target geometry yet.
- No custom spar/wing-box parameterization yet.

Done when:
- The example cantilever case runs end-to-end.
- Output files and plots are produced in the expected directory.
- The run is documented well enough for repetition.

Validation commands:
- `pytest -q tests/integration/test_example_cantilever.py`
- `python scripts/run_example_case.py --case cantilever_example`

### M3 - Replace the example geometry with the target cantilever wing geometry
Status: not started

Why this milestone exists:
Once the example works, the next step is to move from tutorial geometry to the project’s target cantilever wing geometry.

Scope:
- Implement the specified cantilever planform and structural geometry inputs.
- Preserve as much of the known working example setup as possible.
- Add geometry validation checks.
- Ensure output folders and plots still work for the custom geometry case.

Out of scope:
- No full optimization yet.
- No strut geometry yet.

Done when:
- The example-based cantilever case is replaced by the specified project geometry.
- Geometry inputs are validated and documented.
- The case still runs and writes artifacts successfully.

Validation commands:
- `pytest -q tests/unit/test_cantilever_geometry.py`
- `pytest -q tests/integration/test_target_cantilever_case.py`
- `python scripts/run_baselines.py --config examples/minimal_cantilever.yaml`

### M4 - Build the first representative wing-box / spar structural model for the cantilever case
Status: not started

Why this milestone exists:
The project goal is not just to run a generic example; it needs a structural representation that reflects the intended wing concept.

Scope:
- Transition from the base cantilever example to a representative wing-box structure.
- Implement the initial spar or beam-style representation in the simplest credible form.
- Keep the model simple and explain assumptions clearly.
- Support the specified geometry and analysis path.

Out of scope:
- Do not add full optimization yet.
- Do not add the strut case yet.

Done when:
- The cantilever case uses the intended wing-box / spar representation.
- The structural model runs at least one static case.
- Assumptions are documented.

Validation commands:
- `pytest -q tests/unit/test_wingbox_parameterization.py`
- `pytest -q tests/integration/test_cantilever_wingbox_static.py`

### M5 - Add constraints, design variables, and a static cantilever analysis workflow
Status: not started

Why this milestone exists:
The project needs a meaningful design model, not just a fixed analysis. This milestone introduces the first real design-variable-driven cantilever case.

Scope:
- Implement the design constraints from the project inputs.
- Add the initial representative spar sizing variables.
- Add a static analysis path that reports mass, stress/failure metrics, and displacements.
- Keep the load model simple and explicit.

Out of scope:
- No full load refinement yet.
- No contour studies yet.

Done when:
- The cantilever case has explicit design variables.
- Constraints are represented in code.
- A static cantilever run produces key outputs for later studies.

Validation commands:
- `pytest -q tests/unit/test_design_variables.py`
- `pytest -q tests/unit/test_constraints.py`
- `pytest -q tests/integration/test_static_cantilever_design_case.py`

### M6 - Refine cantilever loads, verify outputs, and stabilize result/plot generation
Status: not started

Why this milestone exists:
Loads and result verification are likely to require multiple passes. This milestone stabilizes the cantilever workflow before optimization.

Scope:
- Improve or complete the load application logic.
- Verify that plots and result files match the intended artifact structure.
- Add checks on mass, stress trends, and displacements where reasonable.
- Add regression-style checks on artifact creation.

Out of scope:
- No optimizer-driven sweeps yet.
- No strut case yet.

Done when:
- The cantilever static workflow is stable and repeatable.
- Result files and plots are written in the correct locations.
- Verification checks exist for the output path and representative values or trends.

Validation commands:
- `pytest -q tests/integration/test_cantilever_results_and_plots.py`
- `python scripts/run_baselines.py --config examples/minimal_cantilever.yaml`

### M7 - Add OpenMDAO/MPhys optimization plumbing for the cantilever case
Status: not started

Why this milestone exists:
Once the cantilever analysis is stable, it can be wrapped for gradient-based study and optimization.

Scope:
- Build the OpenMDAO/MPhys cantilever analysis path.
- Register design variables, objective, and constraints.
- Add derivative checks where appropriate.
- Separate analysis setup from optimization driver setup.

Out of scope:
- No strut optimization yet.
- No large sweep studies yet.

Done when:
- The cantilever case runs through OpenMDAO/MPhys.
- Derivative checks are implemented and documented.
- The optimization plumbing is usable for parameter studies.

Validation commands:
- `pytest -q tests/integration/test_mphys_cantilever.py`

### M8 - Run cantilever parameter sweeps and generate contour/trend plots
Status: not started

Why this milestone exists:
The first decision-useful output is a cantilever study showing weight and constraint trends over the key design variables.

Scope:
- Run parameter sweeps or optimizer-supported studies for the cantilever case.
- Generate contour plots such as wing weight over spar width vs spar thickness.
- Add additional trend plots that expose constraint activity and structural behavior.
- Save machine-readable result artifacts.

Out of scope:
- No strut case yet.

Done when:
- At least one cantilever contour family is generated.
- Results are saved in a structured format.
- Plots clearly show design trends and are reproducible.

Validation commands:
- `pytest -q tests/integration/test_cantilever_trade_grid.py`
- `pytest -q tests/regression/test_cantilever_contours.py`
- `python scripts/run_trade_grid.py --config examples/minimal_cantilever.yaml --grid small`

### M9 - Clone the cantilever case into a strut-braced structural model
Status: not started

Why this milestone exists:
The strut case should build from the validated cantilever implementation rather than being developed independently from scratch.

Scope:
- Copy the cantilever case structure into a strut-braced branch of the model.
- Implement the strut geometry, attachment logic, and structural connectivity.
- Use the simplest credible representation for the strut, such as a 1D element, if appropriate.
- Preserve result schema and artifact structure.

Out of scope:
- No full strut optimization yet.
- No final comparison yet.

Done when:
- A strut-braced baseline structural case exists and runs.
- The strut geometry and connectivity are represented explicitly.
- Output fields are comparable to the cantilever outputs.

Validation commands:
- `pytest -q tests/unit/test_strut_geometry.py`
- `pytest -q tests/integration/test_strut_baseline_case.py`

### M10 - Add strut design variables, constraints, loads, and optimization plumbing
Status: not started

Why this milestone exists:
The strut-braced case needs its own design space and optimization wiring before meaningful comparison is possible.

Scope:
- Add strut-specific design variables.
- Add strut-related constraints, loads, and any connection logic needed for representative analysis.
- Add OpenMDAO/MPhys plumbing for the strut-braced case.
- Document architecture-specific assumptions.

Out of scope:
- No final comparison package yet.

Done when:
- The strut-braced case supports design variables and constraints.
- The strut-braced case runs through the optimization framework.
- The outputs remain comparable to the cantilever study outputs.

Validation commands:
- `pytest -q tests/integration/test_mphys_strut_braced.py`

### M11 - Run strut-braced sweeps and generate contour/trend plots
Status: not started

Why this milestone exists:
The strut case needs the same style of decision-useful outputs as the cantilever case.

Scope:
- Run parameter sweeps or optimization-supported studies for the strut-braced case.
- Generate contour plots and trend plots tailored to the larger strut design-variable set.
- Save structured result artifacts.

Out of scope:
- No final comparison narrative yet.

Done when:
- At least one strut-braced contour family is generated.
- Results are reproducible and saved consistently.
- The plots expose meaningful trends in weight and constraints.

Validation commands:
- `pytest -q tests/integration/test_strut_trade_grid.py`
- `pytest -q tests/regression/test_strut_contours.py`
- `python scripts/run_trade_grid.py --config examples/minimal_strut_braced.yaml --grid small`

### M12 - Compare cantilever vs strut-braced results and finalize deliverables
Status: not started

Why this milestone exists:
The project ends with a comparison, not just two independent analyses.

Scope:
- Compare cantilever and strut-braced mass results.
- Compare constraints, sensitivities, and dominant design trends.
- Produce summary tables, plots, and written conclusions.
- Finalize docs and reproduction instructions.

Out of scope:
- No new modeling fidelity beyond the established workflows.

Done when:
- Both architectures can be run from config to saved outputs.
- A comparison package clearly states where the strut helps, where it hurts, and under what assumptions.
- Reproduction steps work from a clean environment.
- The repository is handoff-ready.

Validation commands:
- `pytest -q`
- `python scripts/run_baselines.py --config examples/minimal_cantilever.yaml`
- `python scripts/run_baselines.py --config examples/minimal_strut_braced.yaml`
- `python scripts/run_trade_grid.py --config examples/minimal_cantilever.yaml --grid small`
- `python scripts/run_trade_grid.py --config examples/minimal_strut_braced.yaml --grid small`

## Decision Log
- 2026-03-21: Reworked the plan to follow a practical build order: environment first, working example second, custom cantilever development third, strut extension last.
- 2026-03-21: The project should not attempt the strut-braced case until the cantilever workflow is stable, validated, and producing usable plots.
- 2026-03-21: The strut may be represented initially with a simpler 1D structural element if that is the most robust path to a working comparative model.

## Blockers
- None recorded yet.

## Next Milestone Notes
M0 should focus only on package/install/test infrastructure.
M1 is the highest-risk milestone because solver environment issues may block the entire project.
Do not begin custom structural modeling until a known example has been reproduced successfully.