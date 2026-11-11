---
name: task-handoff
description: Resume explicit task state across AI agents, sessions and providers without repeating completed work.
---

# Task handoff

Read `AGENTS.md`, the selected Issue/PR, canonical spec, task JSON, JSONL worklog, relevant feedback, current branch/commits and Git status. Run `python scripts/taskctl.py status TASK-ID`.

- **SKIP:** completed by explicit action. Never rerun solely because files, spec, shared skills or dependencies changed.
- **RESUME:** interrupted work; use its checkpoint. `start ... --resume` does not inspect hashes.
- **READY:** pending or explicitly reopened and prerequisites completed; start only authorized scope.
- **BLOCKED:** a hold, manually blocked step, incomplete prerequisite or explicitly configured optional review gate.

No `STALE` state is computed. Never automatically invalidate completed steps; only use `invalidate` after an explicit instruction, with `--cascade` if expressly wanted.

Parent orchestrator owns task state and shared files. Subagents edit non-overlapping outputs only. Record checkpoints for long work, and commit artifacts/state/worklog together at task completion or provider handoff. Do not require a separate start-state commit, matched input snapshot or output checksum. Git and Issue ownership coordinate writers; task state is not a distributed lock.

Content-review status is independent: `not_reviewed`, `in_review`, `reviewed`, `needs_review`. A substantive edit to reviewed work must be flagged manually; cosmetic edits need not reset it. Never equate review status, a draft completion or a passing checker with approval to publish.

In the handoff report include task/spec/state paths, branch/PR, completed steps, current step, blockers, user-requested next action and unresolved feedback. Promote only genuinely reusable process lessons into shared skills. Never invent validations/reviews that were not run.
