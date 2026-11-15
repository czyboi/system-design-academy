---
name: pedagogical-review
description: Review whether a concise System Design lesson teaches its outcomes to experienced learners and whether a separate companion assessment measures them.
---

# Pedagogical Review

Use up to three relevant, reviewer-confirmed prevention reminders selected by the parent with `learning_memory.py suggest --role pedagogy_reviewer` to watch for recurring teaching mistakes. They do not override the current curriculum, learner profile or independent evidence, and do not justify adding generic boilerplate.

## Select the assigned mode

- **Plan:** read the canonical scope, audience, curriculum outlines, prerequisites, source coverage report and prior findings. Check sequence, lesson boundaries, overlap, assumed entry knowledge and whether each outline can teach its stated capability. Do not require lesson or assessment files that have not been authored. Return location-specific findings on the plan only.
- **Lesson:** use the inputs and paired-artifact procedure below. If the coverage report is required, schedule this review after coverage; the reviewer still makes an independent pedagogical judgment.

## Inputs (lesson mode)

Read the canonical task specification, user feedback, coverage-review report, teaching lesson, companion assessment, content guidelines, and target audience. The current Academy default is middle/senior engineers learning system design; learner-facing material is English-only unless a newer user decision is recorded.

## Lesson-first comprehension pass

Read the teaching lesson **before** consulting its companion's answer key, sample solution or rubric. For each central outcome, attempt to reconstruct the intended reasoning using only the lesson and declared prerequisites: initial model → observable mechanism → limiting or failure condition → justified improvement → decision and cost. Locate the first unsupported transition if the chain breaks. A reader must not have to infer a missing mechanism from the assessment's model answer.

Check concept dependencies at their point of use: a crucial term or contract needs a sufficient in-lesson explanation or a precise earlier prerequisite, not just a citation. Check whether the sequence makes advanced hardening intelligible without assuming that every middle/senior engineer already knows this particular distributed-systems mechanism. Apply this test proportionately: a concise explanation can pass; do not demand fixed headings, diagrams, repeated definitions, or elementary background without a specific learner-impact finding.

## Calibrate teaching findings

- **Blocker:** a fundamental instructional contradiction or gap makes the core lesson unusable and cannot be safely interpreted from its stated prerequisites.
- **Major:** a missing causal step, essential concept dependency, or broken sequence prevents the intended learner from reconstructing a central mechanism or decision. Cite the exact first gap and show the reasoning it blocks.
- **Minor:** the mechanism and decision remain followable, but a localized explanation, transition or example would make them clearer.
- **Note:** optional presentation or stylistic preference; never block readiness solely for a preferred length, section split, or diagram.

Do not promote a minor or a stylistic preference to major to force a preferred rewrite. Assess the lesson independently of the companion first, then perform the existing paired-artifact and coverage checks. An open blocker or major prevents `ready-for-human-review` through the existing review gate; do not add an agent, extra pass, score, or revision round.

## Procedure

1. Review the teaching lesson and companion assessment as a pair, while checking that they have distinct purposes and paths.
2. Trace the learner path in the lesson: motivating system problem → mechanism and decision criteria → worked example → trade-offs and failure modes.
3. Verify that each outcome is actually taught in the lesson and assessed in the companion artifact. Questions, answer keys, citations, and lesson titles do not count as instruction.
4. For middle/senior learners, flag elementary filler, repeated definitions, avoidable background, and long exposition that does not help the design decision. Do not penalize concise explanations that assume common backend and SQL fundamentals.
5. Flag unexplained jargon, reasoning jumps, missing prerequisite support, unclear diagrams, inconsistent examples, or material that is too dense to follow.
6. Check exercise scope, rubric clarity, multiple valid answers, and whether every question can be answered from taught content.
7. Flag quizzes, knowledge-check banks, answer keys, and assessment rubrics embedded in the teaching lesson. Confirm that the companion artifact contains the practical exercise and 5–8 checks with explanations.
8. Do not replace the independent curriculum-coverage review or technical/provenance review. Report only pedagogical evidence.
9. Suggest specific edits with locations; do not rewrite the whole lesson unless asked.

## Output

Return findings with artifact/location, learner impact, severity, and recommended change. End with `block`, `revise`, or `ready-for-human-review`. This is not source-coverage approval, technical approval, human approval, or publication authorization.

## Machine-readable gate output

Run this reviewer for the owner's standing automatic **per-lesson and module-synthesis** QA requests through `module-quality-review`, or for an explicitly requested targeted/standalone review. For a declared review task, write the requested Markdown findings and optional JSON verdict using `docs/workflow-contract.md`; include finding IDs, severity and status, but no artifact checksums. An open blocker/major finding forbids `ready-for-human-review`. This reviewer cannot trigger code validation, self-revisions, or other reviewers; the parent separately coordinates the two independent reviewers. Record content-review status explicitly when authorized; this is not human publication approval.

## Combined review assignment

When module-pipeline explicitly assigns a combined teaching or course review, the same independent reviewer must also execute curriculum-coverage-review. Read actual source mappings and perform coverage first within that review; a separate coverage report is not required in this mode. Record distinct coverage and pedagogy findings in one report with one overall blocking verdict. This mode supersedes the separate-report input requirement above only for an explicit combined assignment; never infer coverage from pedagogical clarity. Check language here. The reviewer remains independent from the author and technical reviewer.
