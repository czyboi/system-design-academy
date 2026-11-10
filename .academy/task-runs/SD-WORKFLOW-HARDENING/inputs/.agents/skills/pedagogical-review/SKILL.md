---
name: pedagogical-review
description: Review whether a concise System Design lesson teaches its outcomes to experienced learners and whether a separate companion assessment measures them.
---

# Pedagogical Review

## Inputs

Read the canonical task specification, user feedback, coverage-review report, teaching lesson, companion assessment, content guidelines, and target audience. The current Academy default is middle/senior engineers learning system design; learner-facing material is English-only unless a newer user decision is recorded.

## Procedure

1. Review the teaching lesson and companion assessment as a pair, while checking that they have distinct purposes and paths.
2. Trace the learner path in the lesson: motivating system problem → mechanism and decision criteria → worked example → trade-offs and failure modes.
3. Verify that each outcome is actually taught in the lesson and assessed in the companion artifact. Questions, answer keys, citations, and lesson titles do not count as instruction.
4. For middle/senior learners, flag elementary filler, repeated definitions, avoidable background, and long exposition that does not help the design decision. Do not penalize concise explanations that assume common backend and SQL fundamentals.
5. Flag unexplained jargon, reasoning jumps, missing prerequisite support, unclear diagrams, inconsistent examples, or material that is too dense to follow.
6. Check exercise scope, estimate, rubric clarity, multiple valid answers, and whether every question can be answered from taught content.
7. Flag quizzes, knowledge-check banks, answer keys, and assessment rubrics embedded in the teaching lesson. Confirm that the companion artifact contains the practical exercise and 5–8 checks with explanations.
8. Do not replace the independent curriculum-coverage review or technical/provenance review. Report only pedagogical evidence.
9. Suggest specific edits with locations; do not rewrite the whole lesson unless asked.

## Output

Return findings with artifact/location, learner impact, severity, and recommended change. End with `block`, `revise`, or `ready-for-human-review`. This is not source-coverage approval, technical approval, human approval, or publication authorization.
