---
name: module-pipeline
description: Orchestrate Academy module creation with persistent task state, independent source-coverage gates, specialist reviews, and draft-only outputs.
---

# Module Pipeline

The parent orchestrates. Repository task state is durable memory; chat history is not.

## Mandatory intake and resume

1. Find or reuse the GitHub Issue and task ID.
2. Read the canonical `.academy/specs/<TASK-ID>.json`, state JSON, JSONL worklog, `.academy/state/README.md`, target-module governance, and relevant prior feedback.
3. Inspect branch, status, commits, and PR.
4. Run `python scripts/taskctl.py status <TASK-ID>`.
5. Respect statuses. Never repeat `SKIP`; resume unchanged `RESUME`; inspect `STALE`; wait on `BLOCKED`; start only `READY`.
6. If new, use task-intake. Complete the spec, freeze required inputs, and commit them before execution.

## Audience and deliverable contract

1. Record the target learner, entry knowledge, language, scope, learning outcomes, source revision, and current user direction in the canonical task spec. Current Academy defaults are middle/senior engineers learning system design and English-only learner-facing content; newer explicit user direction takes precedence over older documents.
2. Keep the teaching lesson concise and instructional: motivating engineering problem, relevant mechanisms, worked example, trade-offs/failure modes, outcomes, prerequisites, and direct references.
3. Put the practical exercise, 5–8 knowledge checks, answer explanations, rubric, and outcome mapping in a separately declared companion assessment artifact. A lesson title, citation, mention, or assessment question does not count as teaching.
4. Declare unique paths for lesson, companion assessment, evidence, curriculum map, every independent review, final artifacts, and validation records as applicable. Do not start authoring if the teaching and assessment paths are not separate.

## Workflow and mandatory coverage gates

1. Confirm the canonical scope, constraints, Definition of Done, and acceptance criteria are complete and mapped to task steps.
2. Start each step before editing; commit task JSON/worklog after state mutations. Run source research and curriculum mapping in parallel only when both are independent and READY.
3. **Plan coverage gate, before authoring:** assign the independent `curriculum-coverage-reviewer` to compare a pinned source repository's leaf topics with the curriculum map, lesson IDs, outcomes, prerequisites, and expected teaching depth. Require a disposition for every topic. The curriculum designer cannot self-approve this gate. If the reviewer reports `block` or `revise`, resolve material gaps or exclusions in the curriculum plan and repeat the audit before any author writes a lesson.
4. Author only after research, curriculum mapping, and the plan coverage gate are fresh and clear. Assign one author per lesson; keep the lesson teaching-only and assessments separate.
5. Run technical, provenance and source-coverage reviews independently with distinct report paths; run pedagogy afterward when it consumes the coverage report. Assign language checks explicitly to pedagogy. The post-authoring coverage review must inspect actual lesson teaching sections, not just the plan, and map every in-scope source topic to evidence. A quiz/check, reference, heading, or passing plan audit cannot establish that a topic was taught.
6. Consolidate findings and allow at most two automated revision cycles. Any material coverage gap or unsupported core outcome blocks completion; if a critical disagreement remains, stop for human judgment.
7. Commit declared outputs before `taskctl complete`. Checkpoint and commit before provider/context handoff.
8. Run `pip install -r requirements-dev.txt`, `python scripts/validate_content.py`, `python -m unittest discover -s tests -v`, and `python scripts/taskctl.py validate`. Record exact outcomes and distinguish structural checks from technical, legal, source-reachability, pedagogical, and human approval.
9. Prepare the run report, coverage matrix, unresolved claims, and draft PR only after gates are complete. Keep learner-facing content at `status: draft`.

A coverage report verdict of `ready-for-human-review` means only that the reviewer found no unresolved material source-to-course gaps for that review mode. It is not factual, legal, human, or publication approval.

## Explicit rejection and cleanup

- Record the user's rejection and its reason in the active task worklog with a disposition and follow-up. Promote reusable causes into the governing shared skill/checklist, not just the task record.
- When the user explicitly rejects generated outputs and directs deletion, enumerate exact generated files first, verify each target is inside the workspace and is an output rather than a source/policy/input, then delete only those exact files. Do not use broad recursive deletion.
- Preserve source material, curriculum plans needed for review, governance, immutable workflow inputs, task specifications/state/worklogs, and unrelated outputs unless the user explicitly includes them.
- After deletion, check the historical task states. Record them as stale/historical when their output hashes no longer match, and do not restart or reuse rejected artifacts as completed work.

## Idempotency rules

- Every step fingerprint includes input hashes, definition version, dependency fingerprints/output hashes, and its task-specification slice.
- DoD/acceptance criteria declare which step(s) they govern. A criterion change invalidates only affected steps and downstream dependents; global goal/scope/constraints change invalidates all steps.
- Start requires committed clean inputs/spec and records a start commit and input/output snapshots.
- Complete requires unchanged inputs/spec and verifiable committed output changes, unless explicit documented output reuse is requested.
- Do not overwrite stale work without inspecting it. Parent owns shared files and task-state transitions. One active writer per task/lesson; task JSON is not a distributed lock.

## Feedback and reusable learning

- At intake, read relevant prior task retrospectives, review reports, validation reports, and worklog entries. Carry forward applicable findings without reopening completed work outside the new task scope.
- Record explicit user corrections, reviewer findings, and validation/test failures with their source, affected step or artifact, disposition, and reason in the current task worklog or report.
- Before completing a material task, write a short retrospective linking feedback to the root cause, change made, and verification performed.
- Keep task-specific decisions in task artifacts. Promote reusable process feedback into the shared skill, QA checklist, or regression test that governs future work; include a regression check when practical.
- Keep provider profiles as role/configuration wrappers. Do not copy shared procedure into individual profiles, and do not claim an agent has learned unless the repository change is committed.

## Approval boundary and delegation

The CLI only reaches `automation_complete`. Human review, approval, PR merge, and publication are separate human-controlled gates. Never merge or publish. Give each agent bounded inputs, output paths, and stop conditions. Role instructions alone do not enforce permissions.

## Enforced gates and final revisions

Use the updated task template and the artifact-bound verdict format in `docs/workflow-contract.md`. An executed review can be completed with block/revise; authoring and final validation require clear designated reviews. Never relabel a negative review as accepted to unblock execution. Each revision writes new artifact paths so prior review evidence remains immutable. Recheck the final pair before validation. If no change is needed, the parent may copy the accepted candidate to final paths; record reuse/equivalence explicitly and verify the final hashes.

The template provides one revision and final rechecks. If a second revision is necessary, declare unique round-2 outputs and rechecks and repoint the final gate before starting; record revision_cycle 2. After two automated revisions, hold awaiting-human. Do not create further automated rounds by resetting cycle numbers. A user-authorized extra round requires a separately scoped task and preserved prior findings.

## Context and cost discipline

Parent owns state, Git commits and shared files. Dispatch only distinct outputs with a compact brief: task/step, relevant spec criteria, input paths, output paths and stop conditions. Prefer fresh bounded context for independent reviewers when the host supports it; do not copy the complete parent transcript by default. Keep the concurrency limit at four. Reuse immutable source snapshots with version checks; rechecks target changed claims plus affected dependencies. Record observed model/effort with start and runtime usage with complete when available; leave unavailable counters unknown, never estimate them as measured. Model settings in profiles are defaults, not evidence of the actual runtime used. Escalate only unresolved difficult claims to stronger review, preserving the initial findings.
