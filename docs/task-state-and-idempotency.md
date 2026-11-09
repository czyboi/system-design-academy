# Task state, checkpoints, and idempotency

## Why this exists

Conversation memory is not a reliable project database. A new AI, model, provider, or coding session must be able to discover what was planned, what has already been completed, what evidence/artifacts were produced, and the next safe action without relying on the previous chat.

This repository uses a small hybrid:

1. GitHub Issues and PRs provide cross-agent task identity, owner, high-level status, and review history.
2. `.academy/state/tasks/<TASK-ID>.json` stores detailed step execution state.
3. `.academy/state/worklog/<TASK-ID>.jsonl` records append-only checkpoints/events.
4. Git commits store the actual deliverables and provide an immutable artifact trail.
5. GitHub Projects can later present Issues/PRs in a board/table/roadmap view; it must not become a competing task database.

## The anti-repeat guarantee

A step does not become reusable because an AI says "done". It becomes reusable only after:

- the declared outputs exist;
- the outputs are tracked by Git and have no uncommitted changes;
- the task state records their SHA-256 hashes and the commit SHA;
- the current input fingerprint is identical to the completion fingerprint.

The fingerprint includes each declared input file, the step's `definition_version`, and the fingerprints/output hashes of its dependencies. Thus, editing a source registry, lesson template, agent skill, agent profile, or upstream deliverable invalidates only the affected dependency chain. Independent steps remain reusable.

The output hash check catches manual edits to a completed deliverable even when no input changed.

## Status meanings

| CLI state | Meaning | Agent action |
|---|---|---|
| `SKIP` | Previous completion still matches current inputs and outputs | Do not rerun; move to next eligible step |
| `RESUME` | An interrupted step has the same active fingerprint | Read checkpoint and files; resume the same step |
| `READY` | Dependencies are current and the step has not been completed | Start and execute it |
| `STALE` | Inputs or outputs changed after the recorded run | Inspect the diff; re-run only this affected step after reconciling |
| `BLOCKED` | A dependency is incomplete or stale | Do not start; resolve the prerequisite first |

The tool never deletes stale files or automatically launches an agent. It exposes the next valid action and leaves overwrite/revision decisions to the orchestrator.

## Commit the state, not just the lesson

Every state-mutating `taskctl` command updates the task JSON and appends a worklog event. Commit both files to the active task branch after `init`/`add-step`, `start`, `checkpoint`, `complete`, or `invalidate`. Commit the `start` record before editing task outputs, and commit a checkpoint before switching AI/provider or ending the session. After outputs are committed and `complete` records their hashes, commit the updated task JSON/worklog too. An uncommitted checkpoint exists only in one clone and is invisible to another AI session working elsewhere.

## Cross-AI handoff protocol

The receiving AI should be able to follow these steps without access to prior chat history:

1. Open the GitHub Issue and read its goal, acceptance criteria, dependencies, owner, branch, and linked PR.
2. Read `AGENTS.md`, `.academy/state/README.md`, and `.academy/state/tasks/<TASK-ID>.json`.
3. Read the task's JSONL worklog and latest checkpoint.
4. Inspect `git status`, current branch, latest commit, and linked PR.
5. Run `python scripts/taskctl.py status <TASK-ID>`; trust the calculated `SKIP`/`READY`/`STALE`/`RESUME`/`BLOCKED` result over narrative status text.
6. Continue only a `READY` or unchanged `RESUME` step. Never repeat a `SKIP` step. If the task appears inconsistent, stop and reconcile state/artifacts rather than silently overwriting.
7. Checkpoint before switching models/providers or ending the context. Commit outputs before marking the step complete.

## Workflow ownership

The GitHub Issue is the ownership/coordination point: one active writer per task/lesson, a named owner, and one branch. Read-only reviewers can run concurrently if each writes to a distinct report path. The task JSON is not a distributed lock and does not prevent two separate clones from racing; ownership must be resolved in GitHub before a writer starts.

## Future extension

If the Academy later needs remote execution, automatic retries, or durable waits across distributed workers, an orchestrator such as LangGraph/Temporal can call this CLI/state format. Do not introduce that infrastructure until the file-based workflow becomes a real bottleneck.