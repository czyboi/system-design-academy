---
name: module-quality-review
description: Independently review each completed Academy module, send findings to the appropriate author for up to two automatic corrective revisions, and re-review.
---

# Automatic module QA and bounded correction (parent orchestrator)

Standing user authorization: once a whole module is drafted, perform **Technical + provenance** and **Pedagogy + curriculum coverage** reviews. When actionable findings remain, automatically delegate **targeted corrections** to the existing author(s), then re-review. Do **not** modify shared agent prompts, model profiles, specs, approved curriculum or skill files to fix a content finding. Do not publish, merge, or change another module. Keep at most **two automatic corrective revision rounds per module**; the first review is round 0.

## Scope and triggering

1. Read the module's lesson and integration Stories in `delivery/backlog.json`. A module qualifies only if *every* lesson and integration Story has finished authoring, files exist, and the current drafts passed scoped validation and feature-branch handoff. A partially generated module is not considered reviewed.
2. Check `modules/mXX/reviews/automatic/cycle.json` through `python scripts/review_cycle.py status mXX`. If `ready` or `blocked`, do not restart automatically. If `revising`, **resume that existing round** from the task state/worklog; never spend another revision attempt for a restart. If no cycle record exists, run initial review.
3. The parent delegates two independent reviewer agents using the existing profiles **unchanged**: `technical_reviewer` (Sol High) and `pedagogy_reviewer` (Terra Medium). They cannot review their own authored fixes, edit lessons, or trigger the other agent. The parent can run them in parallel on separate output paths. Python scripts do **not** invoke LLMs.

## Initial review: each module artifact must be inspected

**Technical + provenance:** apply `technical-review` and `provenance-review` to all canonical lesson/assessment pairs and the integrated brief, solution and decision summary. Inspect primary sources, correctness, figures, assumptions, failure semantics, version boundaries, diagrams, and answer keys. Write only `modules/mXX/reviews/automatic/technical.md`.

**Pedagogy + coverage:** apply `pedagogical-review` and `curriculum-coverage-review` to all the same artifacts. Verify each outcome is actually taught and assessed, not merely named. Check examples, pacing, diagrams, exercises, rubrics, prerequisite progression, missing topics and duplication. Write only `modules/mXX/reviews/automatic/pedagogy.md`.

Both reports must enumerate every examined lesson ID and the integration, include **per-artifact verdicts**, and locate each finding by path, section/line, ID, severity (`blocker`, `major`, `minor`, `note`), evidence and concrete fix. The final verdict is `block`, `revise` or `ready-for-human-review`. An open blocker/major is never a clear verdict. Store reports even if they contain blockers.

## Automatic correction loop (maximum two author rounds)

1. Verify both reports are present and sufficiently specific; do not treat reviewer model silence or partial output as PASS. Record the two **actual** verdicts:
   `python scripts/review_cycle.py record mXX --technical VERDICT --pedagogy VERDICT`.
   This persists the module's review cycle, currently open findings and round count **without** inspecting content hashes. Reconcile per-artifact `taskctl.py review-status --scope technical|pedagogy` against the reviewers' findings; `needs_review` for open blocker/major or significant unresolved issues, `reviewed` only when the corresponding scope is clear. The final public status remains draft pending human approval.
2. If the recorded cycle is `ready`, stop the correction loop and hand off. If `needs_revision` and the findings are actionable, reserve a round **before** spawning Author:
   `python scripts/review_cycle.py begin-revision mXX`.
   The first call reserves revision 1, the second revision 2; a third is prohibited. **Do not regenerate an entire module by default.**
3. The parent builds a correction plan from the *open findings*, mapping each to affected canonical paths, Story Task IDs, exact sections, source-evidence gaps and linked assessment or integration impacts. Delegate to the original `lesson_author` for affected lesson/assessment pairs, or the integration author for integration artifacts. Give Author the quoted findings, verified evidence, and the current draft; instruct it to patch only implicated sections and their necessary dependencies. A fundamental error may warrant rewriting the **affected lesson**, not unrelated lessons. Reuse source research; invoke `source_researcher` only when the finding actually requires new verification. If evidence is unresolvable, copyright/rights unclear, reviewers contradict with no defensible resolution, or a safe correction cannot be justified, stop using `python scripts/review_cycle.py stop mXX --reason "..." ` and report for human action instead of guessing.
4. For affected completed author tasks, use the owner's standing rework authorization to explicitly `taskctl invalidate TASK-ID author --reason "Module reviewer finding IDs ..."` **without `--cascade`**, then `start` / `complete` that author step after the patch. For unusual historical task graphs use their declared author step rather than inventing one; do not alter completed research unless findings require it. Record which findings were addressed in the existing worklog. Flag material changes for both review scopes as `needs_review`. Do not edit models, skills or the approved curriculum to address teaching content.
5. Run `python scripts/draft_handoff.py` for **only changed completed draft Task IDs**. This reruns scoped deterministic validation, commits/pushes revised content and worklogs, and also persists the active `cycle.json` counter. If it fails, fix only deterministic representation errors in the affected files, then rerun the focused check; do not start a new author/reviewer round merely for validation formatting.
6. Reinvoke **both independent reviewers** in **targeted re-review mode**: verify every originally open finding is either resolved or still open, inspect corrected passages, companion assessment, nearby assumptions and downstream/integrated impacts; look for regressions introduced by changes. Reuse earlier evidence/reports; do not re-research untouched lessons. Each reviewer **updates its own original module report**, retaining finding IDs and history/locations; neither writes to the other's file. Parent records their new verdicts with `review_cycle.py record`. Continue only if cycle is `needs_revision` and the persisted counter permits one more round.
7. At `ready`, or `blocked` after two unsuccessful revisions, stop. The parent handoffs the reports and cycle state with
   `python scripts/draft_handoff.py TASK-ID [all completed module Task IDs] --review-report modules/mXX/reviews/automatic/technical.md --review-report modules/mXX/reviews/automatic/pedagogy.md`.
   This selectively commits/pushes the evidence of QA, does not merge and does not imply human publishing approval. Report unresolved findings and exhausted attempts explicitly.

**Hard stop conditions:** more than two corrective author rounds, missing independent review report, unverified critical claims, unsafe or speculative fixes, irreconcilable reviewer disagreements, or Git/validation failures. An interrupted `revising` cycle resumes its existing round rather than beginning a new one; a completed `ready` or `blocked` cycle requires new user direction to reopen. The module is never reported as ready when it still has open blocker/major findings.

The initial module QA costs **two model review calls**, plus two more per corrective round if needed. Re-review is scoped to changed content and dependencies to conserve tokens. No unbounded self-repair, repeated whole-module generation or additional AI reviewer roles.
