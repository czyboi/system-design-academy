# Explicit task state, handoff and completion

## Source of truth

One Git-tracked task specification: `.academy/specs/<TASK-ID>.json`, containing goal, scope, constraints, Definition of Done and acceptance criteria. GitHub Issue tracks ownership, branch, dependencies and links, not a competing full spec.

Current state is in `.academy/state/tasks/<TASK-ID>.json`. Append-only worklog records decisions, steps and handoff checkpoints. Completed steps are durable historical facts and are not recalculated from file bytes.

## Status contract

- `SKIP`: the step was explicitly marked completed. Never repeat without authorization.
- `READY`: the step is pending or was explicitly reopened and its prerequisite steps are completed.
- `RESUME`: explicitly running; inspect its checkpoint.
- `BLOCKED`: a hold, manually blocked step, unsatisfied dependency or an explicitly configured review gate.
- **No `STALE` computation.** No fingerprints, input hashes, output hashes or spec-slice hashes are used.

Start verifies the task spec and presence of declared inputs. Complete verifies that declared output paths exist, dependencies are still completed and any configured review gate remains satisfied; it records the explicit completion and appends a log entry. These commands do **not** run content validation, AI reviews or tests. Output files and state should be committed together for durable handoff; the CLI does not require an intermediate commit or an unchanged-output workaround.

Use `invalidate TASK-ID STEP-ID --reason "..."` to reopen intentionally. The optional `--cascade` reopens dependents only when specifically requested. File/spec changes alone do nothing to old task statuses.

## Review status and risk

`review_status` is independent of task execution: `not_reviewed`, `in_review`, `reviewed`, `needs_review`. Use `taskctl.py review-status` with an explicit reason. Review verdict files can record `block`, `revise` or `ready-for-human-review` and location-specific findings, but **do not need artifact checksums**. Legacy verdict hashes are ignored.

Without automated change detection, an edit that is not reported as needing review can leave the old review status visible. Whoever makes a substantive change must explicitly flag it. Git history remains available to inspect what changed. A content review never substitutes for human approval to publish.

## Cross-provider handoff

1. Read Issue, current spec, task state, worklog and relevant feedback.
2. Inspect branch/PR and `git status`; use `taskctl status`.
3. Do not rerun SKIP. Resume only authorized running work; start READY work only within user scope. Respect holds.
4. Record outputs and task state; for cross-environment handoff commit and push outputs/spec/state/worklog together, then run `taskctl handoff TASK-ID` (remote upstream sync check). Use `--local-only` only when both agents share the checkout. For long tasks, checkpoint with a next action.
5. Do not infer any approval from passing code checks or completed draft generation.

Git task state is not a distributed lock. Coordinate one active writer through GitHub ownership.
