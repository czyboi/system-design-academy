---
name: task-handoff
description: Resume an existing Academy task across agents, model providers, and sessions without repeating completed work.
---

# Task Handoff

## Intake
1. Read `AGENTS.md` and `.academy/state/README.md`.
2. Open the linked GitHub Issue; verify task ID, owner, branch, dependencies, and PR.
3. Read `.academy/specs/<TASK-ID>.json`, task state JSON, and JSONL worklog.
4. Inspect Git status, branch, recent commits, and PR.
5. Run `python scripts/taskctl.py status <TASK-ID>`.

## Decide whether to work
- `SKIP`: never repeat. Current spec slice, input fingerprint, output hashes, and Git integrity match.
- `RESUME`: inspect checkpoint and output state; use `start ... --resume` only if the spec/input snapshot is unchanged.
- `READY`: verify task owner and start the step before changing files.
- `STALE`: inspect differences and selectively rerun only the affected step/dependents.
- `BLOCKED`: resolve the prerequisite first.

## During work
- Follow the canonical specification; do not reinterpret Issue prose as acceptance criteria.
- Stay within assigned input/output paths; do not edit files owned by another agent.
- Commit start state before editing. Checkpoint and commit before provider/context handoff.
- Commit outputs before `complete`. For unchanged pre-existing artifacts, use explicit `--reuse-output PATH --reuse-reason "..."`; reuse is recorded.
- Never edit completion fields manually. Commit task JSON and worklog after each state transition.
- `automation_complete` is not approval. Do not mark work human-approved or published.

## Handoff report
Update the Issue with task/spec/state paths, branch/PR, last completed step, current step, blockers, and next action. Keep detailed progress in repository state and append-only worklog.
