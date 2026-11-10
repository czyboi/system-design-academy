# Workflow hardening verification

Task: SD-WORKFLOW-HARDENING; Issue #7; owner @czyboi.
Implementation commit: 6233187c9e3e. Date checked: 2026-11-10.

## Changes and feedback disposition

| User-approved finding | Resolution | Evidence |
| --- | --- | --- |
| Template lacks coverage gates and companion outputs | Added plan coverage before authoring, distinct lesson/assessment outputs, four reviews and four final rechecks; pedagogy depends on coverage | WorkflowTemplateTests |
| Validator and guidelines demand quizzes inside lessons | Updated paired templates, guidelines and validator; outcome map links items to existing teaching headings | ContentContractTests |
| Completed negative review can unlock acceptance | Added review JSON contract, exact artifact hashes, finding severity/status and requires_reviews acceptance boundaries | Negative, clear, stale and invalid review integration tests |
| Revision is not checked after editing | Final validation requires rechecks bound to final artifacts; two tagged revision starts maximum | Template and revision budget tests |
| Status inspection mutates task records | Status is read-only; reconcile explicitly persists aggregate changes | Byte-for-byte state/worklog test |
| Stop decisions lack executable controls | Added paused/awaiting-human controls, explicit resume-task, blocking start/resume/complete | Hold integration test |
| Pedagogy skill assumes lesson inputs for plan review | Added explicit plan and lesson modes in shared skill and thin provider wrappers | Profile adapter checks and source inspection |
| All agents inherit expensive parent settings | Sol/high default; Astra/high technical reviewer; Terra/medium pedagogy; Sol/medium provenance | TOML checks; runtime tool catalog reflected configured role models |
| Repeated context/research and absent cost measurements | Added bounded briefs, source snapshot reuse rules, targeted rechecks, observed runtime/usage recording; resume preserves run ID | Runtime metadata and resume tests |
| Validator is tied to deleted Database pilot outputs | Added workflow/curriculum/lesson scopes and explicit active package manifests; retired pilot inventory remains historical | Missing selected artifact, empty repo and curriculum mapping tests |

## Validation results

Checks ran on the implementation content committed as 6233187c9e3e; no code changed afterward.

- `pip install -r requirements-dev.txt`: exit 0; dependencies already installed. Pip reported sandbox temporary-directory cleanup warnings; installation did not fail.
- `python scripts/validate_content.py`: exit 0; 0 current lessons, 20 source rows, 11 skills, 7 custom agents. An empty authoring inventory is intentional after the earlier user-directed reset, not evidence that lesson content was reviewed.
- `python scripts/validate_content.py --scope workflow`: exit 0.
- `python -m unittest discover -s tests -v`: exit 0; 32 tests passed in 47.667 seconds, no failures or skips. Earlier run had 31 tests passing before the final revision-budget regression was added.
- `python scripts/taskctl.py validate`: exit 0; all historical and current task schemas readable.
- `git diff --check`: exit 0 before implementation commit.

Tests cover gates with block/clear verdicts, stale and mismatched artifact hashes, false clear verdicts with open material findings, revision budget, task holds, read-only status versus reconcile, runtime metadata, resume identity, scoped curriculum mapping and lesson/assessment structure.

## Limits and migration

- No learner content or curriculum was authored, resumed, approved or published. Existing historical task outputs and their recorded decisions were preserved.
- New gate/control fields are additive. Historical tasks retain their old graph semantics until explicitly migrated; a recorded old user stop decision still governs even if execution_control is absent. Read the worklog before any legacy task execution.
- Review JSON validates structure, verdict consistency and artifact identity; it cannot prove technical truth, reviewer independence or human authorization. Human review remains required.
- Runtime metadata and counters are supplied from observed host usage; collection is not automatic. No real token savings or model benchmark is claimed. Current session model need not change when project defaults change.
- Two-run revision enforcement applies to steps tagged revision_cycle. Intake must classify revisions accurately. Holds do not terminate an external worker process; the parent must stop it.
- Scope-specific artifact validation is required for new run artifacts outside canonical lesson directories. Existing global checks exclude immutable inputs/historical runs; explicitly selected artifacts still receive applicable checks.
- Independent specialist review of this workflow code was not performed; verification consists of code inspection and regression/integration tests.

## Retrospective

The underlying failure was drift between shared instructions and executable contracts: skill changes added teaching separation and review requirements without updating scaffolding or validation. This task aligns those layers and adds regressions at the CLI and template boundaries. Model selection alone would not have fixed the repeated work caused by this drift.

During setup, PowerShell treated an unquoted @czyboi argument as syntax, so the initial init command failed before creating task state. Quoting the owner fixed intake. A first patch-format attempt was rejected without changing the target; it was reapplied as an update. These were tooling failures, not passing validations. No unresolved test failure remains.
