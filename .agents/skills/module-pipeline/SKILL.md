---
name: module-pipeline
description: Run a compact Academy workflow with reusable course coverage, two independent combined reviews, and draft-only outputs.
---

# Module Pipeline

## Intake and task size

Use task-intake. Read the canonical spec, state, worklog, issue, prior feedback and Git status; run taskctl status. Respect SKIP, STALE and execution holds. One Issue/spec/state/worklog per course-planning task, independently authorable lesson package, or scoped tooling change. Research and reviews are steps inside that task, not separate Issues. Parent owns task state and shared files. Commit before start, after state mutations, and before complete.

Use `.academy/state/course.template.json` for course planning (three steps), `task.template.json` for a lesson package (six steps), and `workflow.template.json` for tooling (two steps). Replace example paths with the exact assigned artifacts before starting. Do not reopen historical tasks just because shared skills changed.

## Course planning: plan → independent course review → validation

1. Reuse valid pinned-source evidence; inventory the entire System Design Primer at one full commit SHA. Include meaningful README leaves, study/approach material, appendices, under-development topics, system-design solution bodies, OOD examples and substantive additional prompts. Linked catalogs, translations, binary assets and tooling are inventoried as resources, not automatically crawled into unbounded scope.
2. Produce one plan, one inventory and one source-to-lesson matrix for the whole course. Give every knowledge topic an exact lesson and outline. Optional tracks still need teaching coverage; deferred/outside-scope knowledge cannot satisfy a full-Primer requirement. A resource classification needs a rationale and independent scrutiny. Do not regenerate the inventory for every lesson.
3. Assign an independent reviewer (not the planner) both curriculum-coverage-review and pedagogical-review in plan mode. Re-enumerate the pinned source to catch missing or misclassified inventory topics. Check sequencing and lesson boundaries. Write one report and one artifact-bound verdict; separately record `checks: {coverage: pass, pedagogy: pass}` only if both pass. Either material failure makes the overall verdict block/revise.
4. Run the strict coverage command documented in docs/workflow-contract.md with `--stage plan --review`. Only its accepted, unchanged plan/inventory/matrix/review can be reused at lesson intake. A historical prose-only pass or a coverage pass with unresolved pedagogy is not an accepted course gate.

## Lesson package: six normal steps

1. **research:** collect current primary-source evidence only for assigned lesson claims, with product/version, exact source section, date and unresolved claims. Reuse already valid evidence rather than re-searching unchanged general facts.
2. **plan-gate:** run the strict course check with the accepted shared verdict. Verify the lesson exists in that exact plan and all its assigned topics are in scope. When all hashes and both course checks pass, copy only the accepted verdict JSON to the task's plan-gate output; record provenance and explicit reuse in the worklog. This is gate reuse, not a new independent audit. No full planning/review agent run is needed. If missing, changed, negative or legacy-only, block authoring and resolve a bounded course-plan task first. Research and this read-only gate verification may run independently.
3. **author:** write the assigned draft teaching lesson and separate companion assessment directly to their declared paths. Include prerequisites, outcomes, problem, mechanism, worked example, decisions, trade-offs/failures and direct references. Companion contains an exercise, 5–8 checks with explanations, solution/rubric and outcome map. No learner output is authored in a workflow-only task.
4. **technical-review:** an independent reviewer uses technical-review plus provenance-review to check correctness, assumptions, sources, adaptations and asset rights. One report has separate technical and provenance findings; the overall artifact-bound verdict passes only when both dimensions pass.
5. **teaching-review:** a second independent reviewer uses curriculum-coverage-review plus pedagogical-review. Inspect every topic assigned to this lesson in the shared matrix against actual explanatory sections, then check learning sequence, assessment alignment, language and audience. One report records both coverage and pedagogy findings. Questions, titles and citations do not establish teaching. This reviewer is distinct from the author and technical reviewer; no wait for the technical report is necessary.
6. **validation:** require both accepted reviews bound to the exact lesson, assessment, evidence, plan, inventory and matrix. Run selected pair validation and required repository checks. Record results, unresolved minor findings and feedback disposition in one short report. Hand off the same reviewed paths; do not create a redundant final copy, duplicate coverage spreadsheet or separate retrospective file. Keep `status: draft` and human approval separate.

Combined reviews reduce handoffs, not checks. Add a separate specialist only for unresolved technical disputes, ambiguous asset rights, unusually complex assessment or evidence outside the assigned reviewers' competence. A missing required review dimension blocks acceptance.

## Conditional revisions, never a mandatory loop

If both reviews pass, finish without a revision or recheck. If either fails, preserve both reports and candidate; add a revision step with `revision_cycle: 1`, unique new pair paths, and direct dependencies on the reviews (not requires_reviews). Declare two new combined rechecks bound to the complete revised artifact set, including unchanged shared inputs, and repoint validation to those gates. Rechecks focus on changed claims and affected dependencies but verify the entire current hash set. No author self-approval or stale verdict reuse. A second necessary revision uses cycle 2 and new paths; after two unsuccessful cycles, hold awaiting-human. Never overwrite old reviewed artifacts or reset counters to bypass the limit. No copy of accepted content is required merely to call it final.

## Full-course completion

A lesson gate checks its assigned topics; it does not establish whole-course completion. Before claiming full Primer coverage, reconcile the one course matrix with real lesson paths, teaching headings and current SHA-256 values for every topic; run `check_course_coverage.py --stage taught`. Have an independent reviewer audit actual teaching depth across all topics, using fresh package reviews where valid and inspecting cross-lesson gaps. Bind a final course verdict to the complete artifact set and run again with `--review`. Missing, deferred, assessment-only, mention-only or stale evidence blocks full coverage. Also require current accepted technical/provenance and teaching reviews for every package. Structural success never replaces those judgments or human approval.

## Persistence, cleanup and cost

- Read relevant feedback before reuse; record user corrections and review/test failures with source, disposition and follow-up in the existing worklog/report. Promote reusable fixes into shared skills/tests through a scoped task.
- Delegate compact briefs and distinct outputs, not full transcripts. Parent owns Git/state; never have two writers for one artifact. Provider profiles remain thin role/configuration adapters. Use observed runtime/cost data only; no estimated savings presented as measured.
- User-requested resets affect only enumerated generated outputs. Verify exact paths stay inside the workspace, preserve pinned evidence, useful review history, task records and immutable inputs, and record deletions as historical/stale. Prefer retiring misleading entry points when deleting evidence would force expensive regeneration.
- Tooling changes do not trigger lesson creation, curriculum completion, historical-task resumption, a mass re-review, approval, merging or publication.
