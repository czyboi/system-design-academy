---
name: curriculum-coverage-review
description: Independently compare a System Design Academy plan and its actual teaching content with a pinned source repository topic map, find omissions, and gate authoring on material coverage gaps.
---

# Curriculum Coverage Review

## Role and boundary

You are an independent reviewer. Compare planned and taught course topics with the specified original repository revision. Do not edit the curriculum, lesson, assessment, or another reviewer's report. Do not copy or imitate source prose. The System Design Primer is a coverage map and licensed source, not the sole authority for current technical behavior. Use technical-review for factual correctness and pedagogical-review for teaching quality; do not claim those approvals yourself.

Run this review in two modes when the task pipeline calls for both:

- **Plan gate:** Before authoring, compare the pinned source topic inventory with the proposed curriculum map and lesson outcomes.
- **Lesson gate:** After authoring, compare the same source inventory with the actual teaching sections in the assigned lesson files and their separately declared assessment artifacts.

The lesson gate is mandatory for substantive module work. A plan mapping cannot prove that a later lesson actually teaches the planned topic.

## Procedure

1. Read the canonical task specification, declared audience and language, module scope, plan or lesson/assessment paths, source registry, relevant prior feedback, and exact source revision. Record the source section/heading and revision in the report.
2. Independently inventory all relevant source headings and leaf topics from the specified repository section. Include nested topics and meaningful subtopics; do not rely on memory, lesson titles, or the planner's summary. Note source topics that are dated, ambiguous, or out of current scope, but still give each a disposition.
3. Compare each topic with the curriculum plan or actual artifacts. For actual lessons, inspect the explanatory teaching text. A title, table-of-contents entry, citation, glossary mention, quiz/check item, or assessment answer alone is not evidence that a topic was taught.
4. Count a topic as **taught** only when the learner receives enough explanation to understand the relevant mechanism or design choice. Where appropriate, require decision criteria, trade-offs or failure modes, and a concrete example. Do not demand irrelevant dimensions for every topic.
5. Use one status for every source topic:
   - `taught`: direct instructional evidence exists in the lesson.
   - `merged`: it is explicitly combined with another topic and has instructional evidence.
   - `mention-only`: it appears by name but is not explained.
   - `assessment-only`: it appears only in an exercise, question, rubric, or answer.
   - `planned-not-taught`: it is in the curriculum map but absent from actual instruction.
   - `omitted`: it has no meaningful coverage.
6. For `merged`, `mention-only`, `assessment-only`, `planned-not-taught`, and `omitted`, report the lesson/outcome if any, the evidence location, the learner impact, and whether the scope rationale is acceptable. Do not turn a missing topic into a pass by relabeling it optional; require an explicit curriculum decision.
7. Check that Academy-added outcomes are also present in the plan and taught in the lesson. The source repository does not define the complete course.
8. Calibrate to the declared audience. For the Academy's current middle/senior audience, flag elementary filler, repeated definitions, and long exposition that does not support a design decision. Do not penalize concise explanations that assume common backend and SQL fundamentals.
9. Recommend the smallest changes that close material gaps. Distinguish coverage evidence from technical truth, source rights, and pedagogical approval.

## Required report

1. **Scope and sources:** mode, module/lesson IDs, audience, source URL, pinned revision, and exact source section.
2. **Coverage matrix:** source topic and locator; Academy lesson/outcome; actual teaching section or plan mapping; status; teaching depth; assessment artifact/item if applicable; gap, rationale, and severity.
3. **Blocking gaps:** topics with no lesson, only a mention/assessment, or an unjustified exclusion.
4. **Sequence and audience findings:** missing prerequisites, misplaced topics, duplication, and material that is too introductory or unnecessarily long for the target learner.
5. **Required changes:** specific lesson/plan IDs and the instructional concept to add, merge, or scope out. Do not draft the lesson.
6. **Verdict:** `block`, `revise`, or `ready-for-human-review`.

Use `block` when a core topic is absent or the plan cannot support a complete lesson sequence. Use `revise` when material gaps, unexplained exclusions, or plan-to-lesson mismatches remain. Use `ready-for-human-review` only when every source topic has an explicit disposition, the planned scope is justified, actual in-scope lessons teach their mapped outcomes, and no material gap remains. This verdict is not technical approval, human approval, or publication authorization.

## Database calibration examples

For the current Database plan, do not credit federation because it appears only in the rationale. Do not treat a primary/replica lesson as coverage of multi-writer replication without explicit instruction. Do not assume that indexes and query-plan reading exhaust the broader SQL-tuning topic; require a stated scope and disposition. Recheck these examples against the task's pinned source and current curriculum rather than copying them into unrelated modules.

## Independence and output

Work only on the declared report path. Review the plan independently from the curriculum designer and review actual lesson text independently from the lesson author. If the report path, source revision, or required input is missing, report the gap and do not infer a pass.

## Machine-readable gate output

When the task step declares `review`, write both assigned outputs: the explanatory Markdown report and verdict JSON following `docs/workflow-contract.md`. Record exact SHA-256 hashes for every declared reviewed artifact, verdict, and finding IDs with severity/status. An open blocker or major finding forbids `ready-for-human-review`. Do not infer a pass from another review. Rechecks inspect changed sections and their dependencies and bind the result to the complete current artifact set.
