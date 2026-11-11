# Academy task memory — explicit lifecycle

The repository uses GitHub Issues for coordination, `.academy/specs/<TASK-ID>.json` for canonical requirements, `.academy/state/tasks/<TASK-ID>.json` for task state, and append-only `.academy/state/worklog/<TASK-ID>.jsonl` for history. Git holds the actual content and decisions.

There are **no automatic checksum/fingerprint comparisons** for task status. A completed step remains completed even if its inputs, outputs, spec, shared skills or dependency files are edited later. Previous hash metadata and historical worklogs remain as read-only history but are not evaluated.

## Lifecycle

- `pending` → `running` through `start`.
- `running` → `completed` through `complete`, after declared output files exist. Completion does not run validation or review.
- `running` → `running` through `start ... --resume`; consult the checkpoint.
- `completed` → `invalidated` only through an explicit `invalidate` command. `invalidated` can then be started again.
- `blocked` and `execution_control` holds remain manual. A dependency is ready when its preceding step has explicitly completed. `invalidate --cascade` is opt-in, never inferred.
- Task aggregate `automation_status` is computed from these explicit step/hold states by user/agent commands, never from content changes.

```bash
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT
python scripts/taskctl.py checkpoint TASK-ID STEP-ID --note "..." --next-action "..."
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT --resume
python scripts/taskctl.py complete TASK-ID STEP-ID --agent AGENT
python scripts/taskctl.py invalidate TASK-ID STEP-ID --reason "User asked to redo work"
python scripts/taskctl.py hold TASK-ID --state paused --reason "User paused"
python scripts/taskctl.py resume-task TASK-ID --reason "User resumed"
```

## Separate review state

`review_status` defaults to `not_reviewed`; allowed values: `not_reviewed`, `in_review`, `reviewed`, `needs_review`. It is updated **only explicitly**:

```bash
python scripts/taskctl.py review-status TASK-ID --state in_review --reason "User requested review"
python scripts/taskctl.py review-status TASK-ID --state reviewed --reason "Completed requested review"
python scripts/taskctl.py review-status TASK-ID --state needs_review --reason "Updated the lesson mechanism"
```

A formatting edit need not reset review status. A substantive edit should be flagged by the agent making the change or by the user. Because there are no hashes, omission of this update is an accepted manual-management risk. `reviewed` means content review was recorded, **not** authorization to merge or publish.

## Manual checks

No step implicitly launches an AI review, content validation, a Python test suite, or a revision loop. Select `scripts/validate_content.py`, `scripts/check_course_coverage.py`, `scripts/taskctl.py validate` or tests only when specifically requested. GitHub Actions validation uses `workflow_dispatch` only.

Use the two-step lesson template, one-step course template or one-step tooling template for new tasks. Historical six-step workflows and reports remain unchanged; do not silently restart or migrate them. Commit related output/state/worklog together for cross-agent continuity. Share checkpoints in the Issue when handing off.

Publication approval, PR merge and course release are human-controlled and separate from task progress.
