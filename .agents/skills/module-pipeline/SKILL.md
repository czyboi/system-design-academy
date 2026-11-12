---
name: module-pipeline
description: Run Academy drafts with scoped validation, safe Git handoff and independent automatic module-close reviews.
---

# Module pipeline — lightweight draft handoff and automatic module QA

## Intake
Read task-intake, current Issue, canonical spec, explicit state, worklog, Git status/commits and prior feedback. Respect holds and user scope. One writer per task. Choose the current approved curriculum baseline (SDA-v1: `curriculum/revision-1/`) unless the user selects another. For lesson tasks, `taskctl init` must resolve author/evidence output paths from that Story's `delivery/backlog.json` outputs, not the Task ID.

## Default drafting (author stays focused; parent owns module-close QA)

**Course task:** one plan step creating a *new versioned* inventory, course plan and source-to-lesson coverage matrix. Use pinned Primer source and original educational material. Do not overwrite the approved SDA-v1 snapshot.

**Lesson task:** two steps.
1. `research` — gather source evidence for the assigned lesson. Reuse existing evidence when suitable. Do not refresh the whole Primer inventory per lesson.
2. `author` — read the declared `lesson-authoring`, `assessment-design`, `content-format` and source governance instructions; write the original English draft lesson and separate companion assessment at their **single canonical paths**. Git records subsequent revisions. Include prerequisites, outcomes, motivating problem, mechanism, worked example, decision criteria, failure modes, references, exercise, 5–8 checks with explanations and a rubric. Use the approved outline and assigned topics.

**Tooling task:** one `implementation` step with scoped outputs.

After the requested lesson/integration draft is produced, call `taskctl complete` and persist state/output. Then the **parent orchestrator** (not each author subagent) must run `python scripts/draft_handoff.py TASK-ID [TASK-ID ...]` once for the finished task(s). For a multi-lesson batch, pass all completed draft Task IDs together to validate each lesson/assessment pair and integrated page, commit only declared outputs plus spec/state/worklog, and push once. The helper stays on an existing `codex/`, `feature/` or `feat/` branch or creates a new `codex/drafts-*` branch; it never pushes to `main`, force-pushes, opens a PR, merges or publishes. It runs scoped deterministic Python data/format checks only, not the full regression suite. On validation or Git failure, stop and report which step failed; preserve drafts and do not auto-correct or launch a revision loop. Draft authoring completion does **not** imply independent content review or publication approval. Course/tooling tasks retain manual Git handoff.

**Automatic module-close quality review:** After every lesson and the module-integration Story for an authorized module have completed and their drafts passed handoff, the parent MUST execute `.agents/skills/module-quality-review/SKILL.md`. Assign `technical_reviewer` and `pedagogy_reviewer` **independently** using existing model profiles, each reviewing every lesson/companion and the integrated design, then write module-scoped reports. Do this once per completed module, not after each lesson. Record scoped review decisions. If findings remain, follow `module-quality-review` to assign **only affected content** back to Author, then re-run both independent reviewers on changed work/dependencies. Persist the attempt with `scripts/review_cycle.py`; cap corrections at **two rounds per module**, then report unresolved issues and stop. Handoff both reports and cycle state with `draft_handoff.py --review-report`. An incomplete module does not trigger QA. Never call reviewer models from Python, run an unbounded repair loop or treat a reviewer verdict as human approval.

## Additional or targeted review on user request

Automatic **module-close** review follows the preceding rule and is already user-authorized. For separate or targeted review requests, read the chosen reviewer skill(s); check only the specified content and review dimensions. Technical + provenance and teaching coverage + pedagogy are available combined review assignments, but neither pair is automatically launched. The user may request one dimension or a targeted section instead. Write the requested Markdown findings and, only when a review task declares it, a JSON verdict with `verdict` and `findings`; no artifact hashes. Reviewer independence matters when explicitly requested. Never claim release approval.

Explicitly update `review-status --scope SCOPE` (`in_review`, `reviewed` or `needs_review`) with a reason; preserve separate technical, provenance, coverage and pedagogy decisions. For a named review gate, scope is the review step ID and its step must be completed with a clear verdict. If material changes are later made to reviewed content, mark `needs_review`. Cosmetic changes need not reset it. The system does not inspect hashes or infer review freshness.

## If the user requests validation

Run only the extra Python commands selected by the user from `docs/workflow-contract.md`. Repository-wide validation, course coverage, task schema checks and the test suite remain on demand; scoped draft checks are already run by `draft_handoff.py`. Validation is read-only for content and does not run AI reviews, create teaching text or publish anything.

## Revisions and handoff

Edit or redo only what the user requested. To reopen completed work, issue `taskctl invalidate TASK-ID STEP-ID --reason "..."`; `--cascade` only on an explicit instruction. Never repeat `SKIP` by interpreting an old report or changed spec as stale. One can perform small authorized edits within the current draft without reopening the historical authoring task; update review state if material.

Task state and JSONL worklog record decisions. Git records content. For default lesson/integration drafts use the automatic `draft_handoff.py` command above and, when the complete module reaches QA, the paired reviewer-report handoff described by `module-quality-review`; for other work commit/push explicitly and run `taskctl handoff TASK-ID`. Use `--local-only` solely when agents share a checkout; neither mode computes task hashes. Handoff never substitutes for independent content review. User authorization is required before PR merge, human approval or publication. The owner has authorized at most **two automatic corrective author rounds per completed module** after QA findings, as specified by `module-quality-review`; any additional revision requires new explicit user direction.
