---
name: module-pipeline
description: Orchestrate Academy module creation with persistent task state, specialist agents, independent reviews, and a draft PR.
---

# Module Pipeline

The parent orchestrates. Repository task state is durable memory; chat history is not.

## Mandatory intake and resume
1. Find/reuse the GitHub Issue and task ID.
2. Read the canonical `.academy/specs/<TASK-ID>.json`, state JSON, JSONL worklog, `.academy/state/README.md`, and target module governance.
3. Inspect branch, status, commits, and PR.
4. Run `python scripts/taskctl.py status <TASK-ID>`.
5. Respect statuses. Never repeat `SKIP`; resume unchanged `RESUME`; inspect `STALE`; wait on `BLOCKED`; start only `READY`.
6. If new, use task-intake. Complete the spec and commit it before execution.

## Workflow
1. Confirm the spec scope, constraints, DoD, and acceptance criteria are complete and mapped to steps.
2. Start each step before editing; commit task JSON/worklog.
3. Run source research and curriculum mapping in parallel when both are independent and READY.
4. Reconcile findings; author only after dependencies are fresh.
5. Delegate one lesson to one author with distinct output paths.
6. Run technical, pedagogical, and provenance reviews in parallel with distinct report outputs.
7. Consolidate review findings; allow at most two revision cycles.
8. Commit outputs, then run `taskctl complete`; commit state/worklog after.
9. Checkpoint and commit before provider/context handoff.
10. Run content validation, integration tests, and task-state validation.
11. Prepare run report, source coverage, unresolved claims, and draft PR.

## Idempotency rules
- Every step fingerprint includes input hashes, definition version, dependency fingerprints/output hashes, and its task-specification slice.
- DoD/acceptance criteria declare which step(s) they govern. A criterion change invalidates only affected steps and downstream dependencies; global goal/scope/constraints change invalidates all steps.
- Start requires committed clean inputs/spec and records a start commit and input/output snapshots.
- Complete requires unchanged inputs/spec and verifiable committed output changes, unless explicit documented output reuse is requested.
- Do not overwrite stale work without inspecting it. Parent owns shared files and task-state transitions.
- One active writer per task/lesson. Task JSON is not a distributed lock.

## Approval boundary
The CLI only reaches `automation_complete`. Human review, approval, PR merge, and publication are separate human-controlled gates. Never merge or publish.

## Delegation
Give each agent bounded inputs, output paths, and stop conditions. Shared instructions live in `.agents/skills/`; provider-specific profiles should reference those skills rather than duplicate them. Role instructions alone do not enforce permissions.

## Feedback and reusable learning
- At intake, read relevant prior task retrospectives, review reports, validation reports, and worklog entries. Carry forward applicable findings without reopening completed work outside the new task scope.
- Record explicit user corrections, reviewer findings, and validation/test failures with their source, affected step or artifact, disposition, and reason in the current task worklog or report. Use clear dispositions such as applied, deferred, or task-specific.
- Before completing a material task, write a short retrospective linking feedback to the root cause, change made, and verification performed.
- Keep task-specific decisions in the task artifacts. Promote reusable process feedback into the shared skill, QA checklist, or regression test that governs future work; include a regression check when practical.
- Keep provider profiles as role/configuration wrappers. Do not copy shared procedure into individual agent profiles, and do not claim that an agent has learned unless the repository change is committed.
- For substantive lesson revisions that change explanations, examples, technical claims, assessments, or learning sequence, declare distinct independent review outputs for pedagogy and the relevant technical and provenance/language areas. The author must not label self-review as independent. If a reviewer is unavailable, record the gap and leave that gate unresolved.
