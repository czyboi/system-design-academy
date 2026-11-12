# Academy task memory — explicit lifecycle

The repository uses GitHub Issues for coordination, `.academy/specs/<TASK-ID>.json` for canonical requirements, `.academy/state/tasks/<TASK-ID>.json` for task state, and append-only `.academy/state/worklog/<TASK-ID>.jsonl` for history. Git holds the actual content and decisions.

There are **no automatic checksum/fingerprint comparisons** for task status. A completed step remains completed even if its inputs, outputs, spec, shared skills or dependency files are edited later. Previous hash metadata and historical worklogs remain as read-only history but are not evaluated.

## Lifecycle

- `pending` → `running` through `start`.
- `running` → `completed` through `complete`, after declared output files exist. Completion does not run validation or review.
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
# After committing output + spec + state + worklog, manually verify handoff:
python scripts/taskctl.py handoff TASK-ID
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

No step implicitly launches an AI review, content validation, a Python test suite, or a revision loop. Select `scripts/validate_content.py`, `scripts/check_course_coverage.py`, `scripts/taskctl.py validate` or tests only when specifically requested. GitHub Actions content validation uses `workflow_dispatch` only; Python regression tests run automatically on pull requests and pushes to `main`.

Use the two-step lesson template, one-step course template or one-step tooling template for new tasks. Historical six-step workflows and reports remain unchanged; do not silently restart or migrate them. At handoff, commit output/spec/state/worklog together and run `taskctl handoff TASK-ID` (read-only Git tracking and dirty-file check, no checksums). The command does not run review or Python validation. Share checkpoints in the Issue when handing off.

Publication approval, PR merge and course release are human-controlled and separate from task progress.
