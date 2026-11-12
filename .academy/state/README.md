# Academy task memory — explicit lifecycle

The repository uses GitHub Issues for coordination, `.academy/specs/<TASK-ID>.json` for canonical requirements, `.academy/state/tasks/<TASK-ID>.json` for task state, and append-only `.academy/state/worklog/<TASK-ID>.jsonl` for history. Git holds the actual content and decisions.

There are **no automatic checksum/fingerprint comparisons** for task status. A completed step remains completed even if its inputs, outputs, spec, shared skills or dependency files are edited later. Previous hash metadata and historical worklogs remain as read-only history but are not evaluated.

## Lifecycle

- `pending` → `running` through `start`.
- `running` → `completed` through `complete`, after declared output files exist. Completion does not run validation or review; on historical/optional steps that declare `requires_reviews`, it rechecks the existing named review gate.
- `running` → `running` through `start ... --resume`; consult the checkpoint.
- `completed` → `invalidated` only through an explicit `invalidate` command. `invalidated` can then be started again.
- `blocked` and `execution_control` holds remain manual. A dependency is ready when its preceding step has explicitly completed. `invalidate --cascade` is opt-in, never inferred.
- Task aggregate `automation_status` is computed from these explicit step/hold states by user/agent commands, never from content changes. `status` issues read-only warnings for missing outputs of completed steps.

```bash
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT
python scripts/taskctl.py checkpoint TASK-ID STEP-ID --note "..." --next-action "..."
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT --resume
python scripts/taskctl.py complete TASK-ID STEP-ID --agent AGENT
python scripts/taskctl.py invalidate TASK-ID STEP-ID --reason "User asked to redo work"
python scripts/taskctl.py hold TASK-ID --state paused --reason "User paused"
python scripts/taskctl.py resume-task TASK-ID --reason "User resumed"
# For completed draft task(s), automatic scoped validation, commit, push and remote handoff:
python scripts/draft_handoff.py TASK-ID [TASK-ID ...]
# For non-draft tasks, after manual commit/push:
python scripts/taskctl.py handoff TASK-ID
# Only for a handoff inside the same checkout:
python scripts/taskctl.py handoff TASK-ID --local-only
```

## Separate review state

The `general` review state defaults to `not_reviewed`. Scoped decisions are recorded in `review_statuses` with a scope name, status and reason. Values: `not_reviewed`, `in_review`, `reviewed`, `needs_review`. Nothing is inferred from file edits.

```bash
python scripts/taskctl.py review-status TASK-ID --scope technical --state in_review --reason "User requested technical review"
python scripts/taskctl.py review-status TASK-ID --scope technical --state reviewed --reason "Technical review finished"
python scripts/taskctl.py review-status TASK-ID --scope pedagogy --state needs_review --reason "Updated exercise rubric"
# When a historic task explicitly requires a review step, use that step ID as --scope.
```

A formatting edit need not reset review status. A substantive edit should be flagged by the agent making the change or by the user. Because there are no hashes, omission of this update is an accepted manual-management risk. A review gate is accepted only if its review step is completed, its scoped `review-status` is explicitly `reviewed`, and the verdict is clear. Older historical tasks without any new review-status fields retain their recorded acceptance. `reviewed` does **not** authorize merge or publication.

## Manual checks

Task state transitions themselves do not launch AI reviews, Python test suites or revision loops. After completed lesson/integration drafts, the parent invokes `scripts/draft_handoff.py` for scoped deterministic format/data checks and feature-branch Git delivery. After the **whole module and integration** are complete, the parent invokes two independent reviewers following `.agents/skills/module-quality-review/SKILL.md`. Actionable findings return to the affected Author for **at most two targeted correction rounds**, each followed by independent re-review. `scripts/review_cycle.py` stores a separate, explicit QA cycle at `modules/mXX/reviews/automatic/cycle.json` (counter, verdict history, status), without adding a task-graph step or unbounded retry loop. Repository-wide validation, course coverage, task-schema checks and the regression suite remain on demand. GitHub Actions content validation uses `workflow_dispatch` only; Python regression tests run automatically on pull requests and pushes to `main`.

Use the two-step lesson template (including `assessment-design`, `content-format` and governance as declared author inputs), one-step course template or one-step tooling template for new tasks. The lessons/assessments use single canonical paths from the approved backlog; no nested lesson revisions or content manifests. Invalid task/spec initialization is rejected before persisting partial files. Historical six-step workflows and reports remain unchanged; do not silently restart or migrate them. For generated drafts, run `python scripts/draft_handoff.py TASK-ID [TASK-ID ...]` to validate, selectively commit/push outputs and task memory, and verify remote handoff. At module close, record independent verdicts via `python scripts/review_cycle.py record mXX --technical VERDICT --pedagogy VERDICT`. If findings remain, reserve a correction round via `python scripts/review_cycle.py begin-revision mXX` (up to two), then hand off changed drafts, re-review and record again. After the final verdict, pass `--review-report modules/mXX/reviews/automatic/technical.md --review-report modules/mXX/reviews/automatic/pedagogy.md` to hand off both reports and cycle state together. For other work, commit/push output/spec/state/worklog manually and then run `taskctl handoff TASK-ID`. The remote check verifies Git tracking, cleanliness and that local HEAD matches the advertised upstream (requires an accessible remote and configured upstream). Use `--local-only` only when the receiving agent shares this checkout. Remote verification happens only at explicit handoff, never during status/start/complete. `taskctl handoff` alone does not use checksums or run AI review/Python validation; the draft wrapper runs only scoped Python checks before it pushes. The parent orchestrator (not the Python wrapper) separately invokes reviewers once per completed module. Share checkpoints in the Issue when handing off.

Publication approval, PR merge and course release are human-controlled and separate from task progress.
