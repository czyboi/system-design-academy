---
name: task-intake
description: Create or claim a well-scoped Academy task and prevent duplicate or conflicting work before agents start.
---

# Task Intake

1. Search GitHub Issues and `.academy/state/tasks/` for matching task IDs, lessons, goals, and output paths. Reuse equivalent work.
2. Confirm one active writer and a named owner before execution.
3. Initialize with:
   `python scripts/taskctl.py init <TASK-ID> --module <MODULE> --goal "..." --owner "@username" --template .academy/state/task.template.json`.
4. Edit `.academy/specs/<TASK-ID>.json` as the canonical source for goal, scope, constraints, Definition of Done, and acceptance criteria. Every requirement must have an ID and `applies_to` list. Remove all placeholders before starting.
5. Adjust state steps to exact inputs, outputs, definition versions, and dependencies. Each output path must have one owner.
6. Put links, owner, branch, dependencies, and a short summary in the GitHub Issue. Do not duplicate detailed scope/acceptance criteria; link the committed specification.
7. Commit specification, task state, and worklog before delegation.
8. Run `python scripts/taskctl.py status <TASK-ID>`; resolve stale/resume/blocked steps before assigning work.

Never invent completion records or mark a step completed from chat narrative. Use `taskctl complete` after verifiable committed outputs.
