---
name: task-handoff
description: Resume or hand off an existing Academy task across agents, model providers, or conversation sessions without repeating completed work.
---

# Task Handoff

## Mandatory intake

1. Read root `AGENTS.md` and `.academy/state/README.md`.
2. Identify the GitHub Issue, task ID, owner, branch, and linked PR. Do not create a second task for the same goal.
3. Read `.academy/state/tasks/<TASK-ID>.json` and `.academy/state/worklog/<TASK-ID>.jsonl`.
4. Inspect `git status`, current branch, recent commits, and the linked PR.
5. Run `python scripts/taskctl.py status <TASK-ID>` and use its computed state as the execution guide.

## Decide whether to work

- `SKIP`: do not repeat the step. Its input fingerprint and output hashes match the recorded completion.
- `RESUME`: read the existing outputs and last checkpoint; call `start ... --resume` and continue from `next_action`.
- `READY`: check the Issue/branch owner, then call `start` before changing files.
- `STALE`: inspect input/output diffs. Do not overwrite automatically. Re-run only after confirming that the change requires it.
- `BLOCKED`: do not start until its dependency is current.

## During work

- Stay within the exact task and assigned output paths.
- Do not edit files owned by another step/agent.
- Save a checkpoint before context handoff or stopping. State what is done, what is not done, important evidence, open questions, and one concrete next action. Commit the updated task JSON and worklog to the active branch; an uncommitted checkpoint is invisible to another clone.
- If the task-specific prompt, acceptance criteria, or method changes, bump `definition_version` or add the changed spec as an `input_path`.
- Commit task JSON/worklog after every state mutation (`start`, `checkpoint`, `complete`, `invalidate`). Commit declared outputs before `taskctl complete`, then commit the updated state/worklog afterward.
- Do not mark a step complete by editing JSON manually. Use `taskctl complete` so the tool records hashes and commit SHA.

## Handoff report

Update the GitHub Issue with a short summary, state file path, branch/PR, last completed step, current step, blockers, and next action. Keep detailed step state in the JSON/JSONL files, not duplicated in the Issue body.