---
name: curriculum-design
description: Design a complete System Design curriculum from a pinned topic repository, with detailed teaching outlines and auditable topic coverage for experienced engineers.
---

# Curriculum Design

## Inputs

Read the canonical task specification, current user direction, relevant prior feedback, approved source repositories and their pinned revisions, and applicable Academy guidance. The default audience is middle/senior engineers learning System Design; learner-facing content is English-only. A newer explicit user decision takes precedence.

## Procedure

1. **Set the boundary.** State the audience's assumed experience, the capability the course should build, language, source revision, requested deliverables, and non-goals. Keep a plan-only request limited to curriculum artifacts; do not author lessons or assessments.
2. **Inventory the full declared source scope before sequencing.** Traverse the pinned repository's relevant topic hierarchy down to meaningful leaf topics. Inspect its study guide, appendices, under-development entries, in-repository solution examples, and other explicitly in-scope topic collections such as OOD. Inventory linked catalogs, translations, flashcards, assets, and tools as source resources; do not silently treat every link or asset as a teaching topic. Record exact paths, headings/anchors, and revision. Never claim repository-wide coverage from a README summary or a Database-only inventory.
3. **Give every source row a disposition.** Map it to an exact lesson and a specific outline item, or explicitly classify it as merged, optional, deferred, or outside the course with a short rationale. A topic name in a title, reference list, or general rationale is not coverage. For a merge, show where each constituent concept is taught. Flag incomplete or dated source topics for current technical research rather than omitting them.
4. **Build the sequence from engineering decisions.** Order modules and lessons from shared foundations through mechanisms and trade-offs to larger system compositions. Make prerequisites visible. Assume common backend, SQL, and application fundamentals for the default audience; avoid beginner filler and repeated long definitions. Mark material added beyond the pinned repository as an Academy addition and identify its evidence needs.
5. **Write a useful outline for every teaching lesson.** List the concepts in teaching order, the mechanism or design choice each explains, relevant decision criteria and trade-offs/failure modes, and the mapped source subtopics. Be specific enough that a later author can draft one lesson without guessing its scope. Keep the course itself teaching-focused; do not fill the outline with quizzes, exercises, answer keys, or assessment prompts unless explicitly requested.
6. **Separate later delivery work from course planning.** When a task requests an authoring backlog, create one module grouping (Epic) and one independently authorable lesson item (Story) per lesson. New draft lesson tasks default to research → author (lesson + assessment). Technical, coverage, pedagogy, validation and revision are separate optional user-triggered activities, not mandatory child work. Do not create external tracker issues unless requested.
7. **Review only when requested.** Prepare the complete inventory, matrix and proposed plan. If the user requests independent coverage review, give these to `curriculum-coverage-review` and request source re-enumeration; do not silently launch it during planning. An unreviewed draft must never be presented as independently verified.
8. **Check plan quality and persist learning.** Review prerequisites, sequence, audience fit, scope consistency, outline depth, and overlap. Record each user correction and reviewer finding with its disposition in the task worklog or review artifact. Promote reusable workflow corrections into this skill or the relevant shared QA skill; keep one-off decisions in task records.

## Planning outputs

Choose outputs that match the task, typically:

- An ordered course plan with module purpose, lesson IDs, prerequisites, and detailed teaching outlines.
- A pinned-source inventory and source-to-lesson matrix with exact locators, dispositions, and outline evidence.
- A lesson-sized authoring backlog only when requested; assessments remain separate and deferred until their companion lessons are accepted.
- Independent coverage and pedagogy review reports only when separately requested, including findings and their dispositions.

Do not claim independently verified complete coverage while topics lack dispositions, mappings lack concrete locations, or a user-requested independent review has not passed. A coverage pass establishes mapping quality, not technical correctness, source rights, human approval, or publication readiness.

## Compact full-course workflow

Use the three-step course template and module-pipeline. Produce one shared full-source inventory and matrix; do not regenerate them per lesson. Under a full-Primer requirement, every knowledge topic must map to a lesson/outline, including optional tracks. Deferred/outside-scope knowledge is an unresolved gap, not coverage. Distinguish non-teaching resources with justified classifications. Use the strict inventory and matrix formats in docs/workflow-contract.md. Existing evidence can be reused after checking revision and relevance; do not treat a historical coverage-only pass as course acceptance when pedagogy remains unresolved.

When the user requests a combined course review, one independent reviewer may cover full source enumeration and pedagogy, with separate results for each. Do not pre-schedule review rounds or revisions. Add bounded revisions only when expressly authorized. No learner content or external per-lesson Issue creation in a plan-only task.
