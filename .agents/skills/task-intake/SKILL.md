---
name: task-intake
description: Claim a bounded Academy task with explicit state and no automatic review or validation.
---

# Task intake

1. Search GitHub Issues and existing task state before creating anything. Read the matching spec/state/worklog, current user scope, feedback, Git status and PR. Do not duplicate completed work.
2. Declare exact task goal, scope, constraints, DoD and acceptance criteria in `.academy/specs/<TASK-ID>.json`. Issue coordinates ownership, dependencies, branch and links, not a second spec. Assign one active writer.
3. Choose the smallest template: `.academy/state/course.template.json` for a new versioned plan, `task.template.json` for lesson research + authoring, or `workflow.template.json` for one tooling implementation.
4. Select exact output paths from the matching backlog Story's `outputs` map (Task ID != Lesson ID), and the approved plan revision. For lesson content, the current baseline is `curriculum/revision-1/`. Never overwrite historical candidates, an approved plan or other tasks' output paths.
5. Declare only actual prerequisites/inputs; do not require automatic review, plan recheck, validators or extra final-copy steps. A task can finish its requested draft without any quality gate.
6. Initialize and verify spec/state; start eligible steps explicitly. When done, record completion, preserve evidence, commit output/spec/state/worklog together and explicitly run `taskctl handoff TASK-ID` before cross-agent handoff. Do not run checks except when the user separately asks.
7. If review or validation is expressly requested, select the specified review skills or commands. Set `review_status` manually for meaningful review decisions or substantive edits.
8. Use `taskctl invalidate` only at explicit direction; do not infer stale states from changed source/spec/output. Respect holds and the user's decision before any restart.

For provenance/technical publication concerns, disclose gaps; no automatic review or validator substitutes for human release approval.
