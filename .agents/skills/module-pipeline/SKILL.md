---
name: module-pipeline
description: Orchestrate end-to-end creation or refresh of a System Design Academy module using persistent task state, specialist agents, independent reviews, and a draft PR.
---

# Module Pipeline

Act as lead orchestrator. Delegate bounded tasks to specialist subagents; do not do every specialist task in the main thread. The repository task state is durable memory. Never rely on chat history as the only progress record.

## Mandatory intake and resume

1. Find or reuse the matching GitHub Issue and task ID. Do not create a duplicate task for the same goal.
2. Read `.academy/state/README.md`, `.academy/state/tasks/<TASK-ID>.json`, and its JSONL worklog.
3. Inspect the current branch, `git status`, recent commits, and linked PR.
4. Run `python scripts/taskctl.py status <TASK-ID>` before delegating any step.
5. Respect the computed states: `SKIP` = do not repeat; `RESUME` = read checkpoint and continue; `READY` = eligible to start; `STALE` = inspect and selectively rerun; `BLOCKED` = resolve dependency first.
6. If no task exists, use `task-intake` to create one from `.academy/state/task.template.json`; adapt it to exact module/lesson scope and commit it before delegation.

## Workflow

1. Read the target module curriculum, source registry, lesson template, content guidelines, attribution policy, QA checklist, and task acceptance criteria.
2. Start each step with `python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT-NAME` before editing. Never execute a step marked `SKIP`.
3. Run source research and curriculum mapping in parallel when both are `READY`; wait for both before authoring.
4. Reconcile their findings. Resolve conflicts or evidence gaps before writing.
5. Delegate lesson files to `lesson_author`. Assign exactly one lesson file and unique output paths; the orchestrator owns shared files.
6. After drafts exist, run independent parallel reviews: `technical_reviewer`, `pedagogy_reviewer`, and `provenance_reviewer`, each writing to its declared report path.
7. Wait for all reviewers, consolidate actionable findings, and delegate corrections to the author. Maximum two revision cycles per lesson.
8. Commit the step's declared outputs, then run `python scripts/taskctl.py complete TASK-ID STEP-ID --agent AGENT-NAME`. Do not edit completion fields manually.
9. Before context handoff, save `taskctl checkpoint` with what is done, what remains, unresolved issues, and one concrete next action. Update the Issue with a short summary and state/PR links.
10. Run `python scripts/validate_content.py`, `python -m unittest discover -s tests -v`, and `python scripts/taskctl.py validate`.
11. Produce a run report with step states, sources, verdicts, unresolved claims, and human actions.
12. Create or update a focused draft PR. Never merge or publish learner-facing content.

## Idempotency rules

- A step's fingerprint covers declared input files, its `definition_version`, and dependency fingerprints/output hashes.
- `SKIP` is authoritative only while input fingerprint and committed output hashes still match.
- Add prompt/spec/skill/profile/template files to `input_paths`; bump `definition_version` if a material step definition changes.
- When an upstream step changes, allow its dependents to become blocked/stale; do not restart unrelated steps.
- Never overwrite old artifacts without inspecting the diff. Use `invalidate --cascade` only when deliberately choosing to rerun a step and its dependents.
- One active writer per task/lesson. Reviewers may run concurrently only with distinct report paths.

## Delegation discipline

- Give each subagent a bounded question, exact inputs/output paths, and stop condition.
- Role instructions are not security boundaries. Subagents inherit the parent session's permissions; enforce read-only access at the parent/host layer when required.
- No concurrent edits to the same file. Parent owns source registries, manifests, shared curriculum, and task-state transitions.
- Stop after two unsuccessful revision cycles or when evidence is insufficient.

## Research tiers

- Standard search: bounded factual lookup.
- Document analysis: read exact official documentation already identified.
- Deep Research: disputed topics or synthesis across many independent sources.