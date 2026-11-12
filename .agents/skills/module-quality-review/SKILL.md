---
name: module-quality-review
description: Run independent technical and pedagogy reviews automatically once an authorized Academy module draft is complete.
---

# Automatic module quality review (parent orchestrator)

This is the owner's standing request for **automatic** qualitative QA after module completion; it does not create task-graph steps or authorize rewriting, merging, or publishing. Run **one module at a time**. For a milestone with multiple modules, review each completed module separately.

## When to launch

1. After drafting, scoped data/format validation and the usual feature-branch handoff of lesson/integration artifacts, read the selected module's Stories in `delivery/backlog.json`. A module is eligible only when **every lesson Story and its module-integration Story** in that module has completed the draft work and its declared files exist. Incomplete modules are not automatically reviewed. Do not claim a module is complete simply because the requested subset has been generated.
2. Check `modules/mXX/reviews/automatic/{technical,pedagogy}.md` and the latest meaningful edits. Skip a module already reviewed for its current completed draft unless a user specifically requests a fresh review or substantive content changes were explicitly flagged for re-review. Do not infer stale status from hashes or start new authoring tasks.
3. The **parent orchestrator** delegates exactly two independent review assignments for that module using existing profiles: `technical_reviewer` and `pedagogy_reviewer`. They must be separate from the authors and from each other. Keep the models and reasoning effort in the existing `.codex/agents/*-reviewer.toml` untouched. Reviewers may run in parallel if their output paths do not overlap. This is not a Python script that calls a model.

## Technical assignment

Read the module's canonical lesson/assessment pairs, integrated brief/solution/decision summary, relevant source evidence, task specs and approved curriculum. Apply `technical-review` plus its combined **provenance** procedure. Check correctness, important claims against primary sources, numeric reasoning, version-specific guarantees, diagrams, operational failure paths and assessment answers. Inspect *every* lesson and the integration, rather than a vague module-level impression.

Only write `modules/mXX/reviews/automatic/technical.md`. Give actionable, located findings (artifact, heading or line, severity, evidence link/section, proposed correction) and a separate per-artifact result. End with overall `block`, `revise` or `ready-for-human-review`. Unresolved blocker/major findings prohibit `ready-for-human-review`.

## Pedagogy assignment

Independently review the same complete module against the approved learning outcomes and topic mapping. Apply `pedagogical-review` with the combined **curriculum-coverage** procedure. Inspect the lesson/assessment pairs, worked examples, exercises, explanations, rubrics, prerequisites, knowledge progression, duplicate material and integration. Check each assigned outcome is genuinely taught and assessed; don't mistake a heading or keyword for instruction.

Only write `modules/mXX/reviews/automatic/pedagogy.md` with actionable, located findings, per-artifact results, any missing outcomes or sources, and a final `block`, `revise` or `ready-for-human-review`.

## Reporting, state and handoff

- The parent first confirms both reports exist, are substantial and clearly list all reviewed lesson IDs and the integration package. If a reviewer failed or a report is missing, mark module QA **incomplete**; preserve generated content and report the blocker without pretending the review succeeded.
- For each reviewed lesson/integration task, record the appropriate scoped `review-status` (`technical` and `pedagogy`) with a reason. For the relevant scope, use `reviewed` when that artifact has no open blocker/major finding, otherwise `needs_review`. Findings remain in the reports, not in the task's authoring step. An AI verdict never constitutes human approval.
- Handoff the two reports with the existing helper (no extra Git command or full test run): `python scripts/draft_handoff.py TASK-ID [TASK-ID ...] --review-report modules/mXX/reviews/automatic/technical.md --review-report modules/mXX/reviews/automatic/pedagogy.md`. This reruns only the inexpensive scoped validation, selectively commits task memory + reports and pushes to the existing feature branch. Make sure the task IDs include the reviewed module's completed packages. Report and stop on Git/validation failures.
- On `revise` or `block`, **do not** automatically launch authoring revisions, another review cycle, or new research. Record specific remediation and leave draft artifacts in Git. Revisions and a focused re-review require a new user direction. No PR merge or publication is authorized.
- Do not run automatic qualitative QA for course-planning or tooling tasks, or for a module that has not finished. If a user requests a standalone targeted review, use the existing explicit reviewer procedure.

This procedure adds **two reviewer invocations per completed module**, not two calls after each lesson; if a module is too large for a reviewer to read fully, report the capacity limitation instead of claiming all items reviewed.
