---
name: task-intake
description: Create or claim a well-scoped Academy task and prevent duplicate or conflicting work before agents start.
---

# Task Intake

1. Search existing GitHub Issues and `.academy/state/tasks/` for the same lesson, module, goal, or output path before creating a task.
2. Reuse the existing task/Issue when the goal and acceptance criteria are the same. Create a new task only for distinct work or a separately reviewable deliverable.
3. Ensure the Issue states the goal, Definition of Done, dependencies, task ID, state-file path, owner, branch, and linked PR.
4. Create the repository state with `python scripts/taskctl.py init <TASK-ID> --module <MODULE> --goal "..." --template .academy/state/task.template.json`.
5. Adapt the template to the actual task: remove irrelevant stages; make every input and output path exact; ensure each output has one owner; ensure dependency links are accurate.
6. Confirm one active writer for each task/lesson. Give parallel reviewers distinct report paths. The JSON state file is not a distributed lock.
7. Commit the task state file and link it in the Issue before delegating work. After each state-mutating command, commit both task JSON and JSONL worklog; in particular, commit `start` before editing and commit each checkpoint before handoff.
8. Before assigning any step, run `python scripts/taskctl.py status <TASK-ID>` and resolve `STALE`, `RESUME`, and `BLOCKED` states first.

Do not create placeholder completion records, infer completion from a chat summary, or mark work complete before output artifacts are committed. After `complete`, commit the new task JSON/worklog so another clone can see the completion.