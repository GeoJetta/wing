Read `AGENTS.md`, `docs/spec.md`, and `plan.md` before doing anything else.

Determine the first unchecked milestone in `plan.md` and work only on that milestone.

Before editing, state:
1. the active milestone ID and title,
2. the acceptance criteria you will satisfy,
3. the files you expect to modify,
4. the validation commands you will run.

Execution rules:
- Keep the diff tightly scoped to the active milestone.
- Follow repository conventions in `AGENTS.md`.
- Use convention over novelty.
- Do not invent TACS, OpenMDAO, or MPhys outputs.
- Analytic beam formulas are allowed only in verification utilities and tests.
- If a command fails, either fix the issue or record a concrete blocker in `plan.md` before stopping.
- If a required solver dependency is unavailable, document the exact failure and stop. Do not fake progress.
- Do not begin the next unchecked milestone.

At the end of the run:
1. run every validation command listed for the active milestone,
2. update `plan.md`:
   - mark milestone status,
   - update `Current Status`,
   - append any decisions made,
   - append any blockers encountered,
   - set the next recommended milestone,
3. summarize:
   - what changed,
   - what validations passed,
   - what remains risky or unresolved.

Definition of success for this run:
- exactly one milestone advanced in a truthful, validated way,
- or a precise blocker was documented with the smallest reproducible failing command.
