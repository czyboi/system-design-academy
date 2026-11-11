---
name: module-pipeline
description: Run user-directed Academy draft work; review and validation are separate opt-in operations.
---

# Module pipeline — explicit steps only

## Intake
Read task-intake, current Issue, canonical spec, explicit state, worklog, Git status/commits and prior feedback. Respect holds and user scope. One writer per task. Choose the current approved curriculum baseline (SDA-v1: `curriculum/revision-1/`) unless the user expressly selects a different one.

## Default drafting (no automatic reviewers or validators)

**Course task:** one plan step creating a *new versioned* inventory, course plan and source-to-lesson coverage matrix. Use pinned Primer source and original educational material. Do not overwrite the approved SDA-v1 snapshot.

**Lesson task:** two steps.
1. `research` — gather source evidence for the assigned lesson. Reuse existing evidence when suitable. Do not refresh the whole Primer inventory per lesson.
2. `author` — write the original English draft lesson and separate companion assessment. Include prerequisites, outcomes, motivating problem, mechanism, worked example, decision criteria, failure modes, references, exercise, 5–8 checks with explanations and a rubric. Use the approved outline and assigned topics.

**Tooling task:** one `implementation` step with scoped outputs.

After the requested draft is produced, call `taskctl complete`, persist state and output, and **stop**. Do not automatically run Python validators, tests, reviewers, course gates, copy-to-final stages or revision loops. A draft need not have passed review or validation to have completed authoring.

## If the user requests review

Read the chosen reviewer skill(s); check only the specified content and review dimensions. Technical + provenance and teaching coverage + pedagogy are available combined review assignments, but neither pair is automatically launched. The user may request one dimension or a targeted section instead. Write the requested Markdown findings and, only when a review task declares it, a JSON verdict with `verdict` and `findings`; no artifact hashes. Reviewer independence matters when explicitly requested. Never claim release approval.

Explicitly update `review_status` (`in_review`, `reviewed` or `needs_review`) with a reason when authorized. If material changes are later made to reviewed content, mark `needs_review`. Cosmetic changes need not reset it. The system does not inspect hashes or infer review freshness.

## If the user requests validation

Run only the selected Python commands from `docs/workflow-contract.md`. Content validation, source coverage check, task schema check and tests are separate options. Validation is read-only for content and does not run AI reviews, create teaching text or publish anything.

## Revisions and handoff

Edit or redo only what the user requested. To reopen completed work, issue `taskctl invalidate TASK-ID STEP-ID --reason "..."`; `--cascade` only on an explicit instruction. Never repeat `SKIP` by interpreting an old report or changed spec as stale. One can perform small authorized edits within the current draft without reopening the historical authoring task; update review state if material.

Task state and JSONL worklog record decisions. Git records content; commit outputs and state together at a meaningful handoff. User authorization is required before PR merge, human approval or publication. Maximum two *automated* revision cycles when a user explicitly authorizes a revision workflow.
