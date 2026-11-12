---
name: task-intake
description: Claim bounded Academy work with explicit state; draft handoff validates and pushes safely without automatic AI review.
---

# Task intake

1. Search GitHub Issues and existing task state before creating anything. Read the matching spec/state/worklog, current user scope, feedback, Git status and PR. Do not duplicate completed work.
2. Declare exact task goal, scope, constraints, DoD and acceptance criteria in `.academy/specs/<TASK-ID>.json`. Issue coordinates ownership, dependencies, branch and links, not a second spec. Assign one active writer.
3. Choose the smallest template: `.academy/state/course.template.json` for a new versioned plan, `task.template.json` for lesson research + authoring, or `workflow.template.json` for one tooling implementation.
4. Select exact output paths from the matching backlog Story's `outputs` map (Task ID != Lesson ID), and the approved plan revision. For lesson content, the current baseline is `curriculum/revision-1/`. Never overwrite historical candidates, an approved plan or other tasks' output paths.
5. Declare only actual prerequisites/inputs; do not require automatic AI review, plan recheck or extra authoring/final-copy stages. A task can complete its draft before independent qualitative review; the parent runs the scoped format/data check during Git handoff.
6. Initialize and verify spec/state; start eligible steps explicitly. After lesson/integration draft completion, have the parent invoke `python scripts/draft_handoff.py TASK-ID [TASK-ID ...]`: scoped validation, selective commit/push to a feature branch, and remote handoff check. Batch multiple completed Task IDs to minimize pushes. Stop/report failures; do not repair automatically. For course/tooling work, continue manual Git handoff.
7. If independent review or additional validation is expressly requested, select only the specified review skills or commands. Set `review_status` manually for meaningful review decisions or substantive edits.
8. Use `taskctl invalidate` only at explicit direction; do not infer stale states from changed source/spec/output. Respect holds and the user's decision before any restart.

For provenance/technical publication concerns, disclose gaps; no automatic review or validator substitutes for human release approval.
