# System Design Academy

Source-grounded System Design course development for middle/senior engineers. Learner-facing content is English and remains draft until human approval.

## Current state

The previous learner outputs were removed at the user's request. No completed course is currently claimed. `CURRICULUM_MASTER.md` is the old proposed map; the earlier curriculum candidates have been removed; pinned source evidence remains as a historical input. The historical source-coverage recheck passed, but the pedagogy recheck requested revision and the user stopped finalization. Do not resume it implicitly.

This repository now defaults to a compact workflow. The workflow change does not regenerate curriculum, lessons, assessments or backlog.

## Start here

The shared [module-pipeline skill](.agents/skills/module-pipeline/SKILL.md) defines the process; [task-intake](.agents/skills/task-intake/SKILL.md) selects a bounded task.

| Work | Default steps | Template |
| --- | --- | --- |
| Course plan | Plan + full source inventory/matrix → independent coverage/pedagogy → validation | `.academy/state/course.template.json` |
| One lesson package | Research → reuse accepted plan gate → author → technical/source review + teaching/coverage review → validation | `.academy/state/task.template.json` |
| Workflow/code change | Implementation → verification | `.academy/state/workflow.template.json` |

Reviews are independent of the author. Revisions and rechecks happen only when needed, with at most two automated revision cycles. A passing first draft goes directly to handoff at the same reviewed paths. No mandatory final-copy stage.

## Full Primer coverage

One pinned course inventory and one topic-to-lesson matrix cover the full System Design Primer knowledge scope. Every topic needs a specific teaching location; optional tracks still count toward this requirement. Resource catalogs/translations/assets are classified separately with reasons. Missing or deferred knowledge blocks a claim of full coverage.

Plan coverage is distinct from actual teaching. The strict checker rejects omitted topic IDs, invalid mappings, missing lessons and stale teaching hashes. Independent reviewers verify that the inventory is complete and the explanations actually teach each topic. See [workflow contract](docs/workflow-contract.md) for commands and formats.

## Records and repository structure

- `.agents/skills/`: shared procedures; `.codex/agents/` and `.claude/agents/`: provider adapters.
- `.academy/specs/`: canonical task requirements; `.academy/state/`: task checkpoints, worklogs and templates.
- `.academy/task-runs/`: task evidence, reviews and one final report.
- `modules/`: draft teaching/assessment pairs and source references. Database pilot history is retained for reuse, not an active lesson inventory.
- `scripts/`: lifecycle, structural content and strict coverage checks; `tests/`: regression tests.

One Issue/spec/state/worklog per bounded task, not one per internal step. Fingerprints, artifact-bound review gates and holds remain in place to avoid repeating valid work. [Task protocol](.academy/state/README.md).

## Validation

```text
pip install -r requirements-dev.txt
python scripts/validate_content.py
python -m unittest discover -s tests -v
python scripts/taskctl.py validate
```

Run the selected lesson-pair or course-coverage checks as applicable. A workflow-only validation can pass with zero lessons; that is not proof of course completion. Automation never approves, merges or publishes learner content.
