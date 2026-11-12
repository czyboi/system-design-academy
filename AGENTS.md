# System Design Academy — Agent Instructions

## Boundaries
- Work only on the user-authorized task, module and lesson IDs. Never expand scope or generate other lessons implicitly.
- The official SDA-v1 plan is in `curriculum/revision-1/`; root-level course files are historical candidates. Use the chosen approved version at intake.
- Original English teaching content for middle/senior engineers; keep learner-facing lessons `status: draft`.
- Use exact primary-source references when making technical claims. Primer is a licensed topic map, not the sole factual authority; create original teaching, examples, diagrams and exercises.
- Do not fabricate citations, legal permissions, benchmarks or test results. Do not commit credentials or private learner data.
- Never publish, merge or claim human approval without an explicit user decision.

## Task memory and explicit state
- For a meaningful multi-step task, reuse or create a GitHub Issue, `.academy/specs/<TASK-ID>.json`, `.academy/state/tasks/<TASK-ID>.json`, and `.academy/state/worklog/<TASK-ID>.jsonl`.
- Read spec, state, worklog, relevant feedback and Git history before working. One active writer per task. The Issue coordinates ownership; the spec is authoritative.
- `python scripts/taskctl.py status TASK-ID` reads only recorded states. `SKIP` means explicitly completed, `READY` means eligible, `RESUME` means in progress, and `BLOCKED` means a dependency, hold or manual review gate requires attention.
- No automatic `STALE`, checksums, fingerprints or dependency invalidation. Editing files/specs never changes a completed step's status.
- Start only authorized pending/reopened work; `taskctl start` and `complete` record progress. Only `taskctl invalidate TASK-ID STEP-ID --reason "..."` reopens completed work. `--cascade` must be specifically requested; do not infer cascades.
- Explicitly flag meaningful changes to reviewed content with `taskctl review-status TASK-ID --scope technical --state needs_review --reason "..."` (or the affected scope). The default `general` scope does not certify technical, pedagogy or named review gates. Review status is not publication approval.
- Preserve old task/worklog/report history; legacy hashes are inert. Before cross-environment handoff, commit and push output, spec, task state and worklog, then run `taskctl handoff TASK-ID` to check Git-tracked/clean files and remote upstream sync. For agents sharing a checkout only, `handoff TASK-ID --local-only` skips remote verification. No checksums. A completed task with missing files shows a warning; its historical status remains unchanged.

## Default workflow
- `.academy/state/task.template.json`: research → author draft lesson + companion assessment. The author reads `.agents/skills/content-format/SKILL.md` for safe, renderable Markdown without reducing technical depth. `init` resolves all three output paths from the matching `delivery/backlog.json` Story (`proposed_task_id`), not by concatenating Task ID.
- `.academy/state/course.template.json`: draft a new versioned plan/inventory/matrix.
- `.academy/state/workflow.template.json`: implementation.
- After producing the requested draft, record completion and **stop**. Do not autonomously run AI reviewers, Python validation, tests, CI or a revision loop.
- On an explicit **review** request, invoke only the requested reviewer(s): technical/source rights, teaching/coverage/pedagogy, or comprehensive. Reviewer findings must be attributable to content locations; unresolved blocker/major findings cannot be declared clear.
- On an explicit **validation** request, run only the selected CLI checks. A review request is not implied permission to run validators, and a validation request is not implied permission to spawn AI reviewers.
- Keep teaching and assessment separate; outcomes must be taught and assessed. Read `.agents/skills/module-pipeline/SKILL.md` for details.
- User approval is required before publication, including when a draft has passed optional review and structural checks.

## Parallelism and permissions
- The parent orchestrator owns shared files and task state; delegate only bounded, non-overlapping outputs.
- One active writer per task. The task JSON is not a distributed lock.
- Agent instructions are not an access-control mechanism. Codex subagents inherit parent permissions; enforce boundaries in the actual host/sandbox.
- Stop at unresolved evidence or user-controlled decisions. Never spawn additional tasks to satisfy optional gates without authorization.
