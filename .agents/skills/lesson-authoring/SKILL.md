---
name: lesson-authoring
description: Write concise, original System Design teaching lessons for experienced engineers using the approved curriculum and evidence pack.
---

# Lesson Authoring

## Inputs

Require the canonical task specification, a coverage-reviewed curriculum map, lesson template, content guidelines, attribution policy, source-research evidence, and exact declared lesson output path. For Academy work, the current default learner is a middle/senior engineer studying system design, and learner-facing prose is English-only. Follow newer explicit user direction recorded in the task specification.

Do not start if the plan-stage coverage review blocks authoring, the lesson/assessment output paths are not separate, or a required source/review artifact is missing. Report the missing gate to the parent.

## Procedure

1. Confirm lesson ID, audience, prerequisites, status, scope, outcomes, and the exact lesson path.
2. Teach the engineering problem and decision before adding terminology. Assume common backend, SQL, and application fundamentals; explain them only when they are essential to the design decision.
3. Explain the mechanism causally: what changes in the system, why it changes, and which decision follows. Keep the exposition concise and remove repeated definitions, generic introductions, and material that does not support an outcome.
4. Use original, realistic examples and diagrams. Explain the important nodes and flows.
5. Teach relevant decision criteria, trade-offs, bottlenecks, failure modes, and operational effects. Distinguish general principles from version-specific vendor behavior.
6. Include a worked example that demonstrates the design reasoning. Keep the lesson file instructional: do not embed a quiz, knowledge-check bank, answer key, or assessment rubric.
7. Put the practical exercise, 5–8 knowledge checks, answers/explanations, rubric, and outcome-to-item map in the separately declared companion assessment artifact. Coordinate with assessment-design; do not use questions as a substitute for teaching.
8. Cite exact sources next to important or version-sensitive claims. Mark unresolved claims instead of guessing.
9. Add required front matter, attribution/adaptation notes, and `status: draft`.

## Prohibited

- No paragraph-by-paragraph translation or close paraphrase of the Primer.
- No invented benchmarks, guarantees, product behavior, URLs, or version numbers.
- No unlicensed third-party assets.
- Do not call SQL or code tested unless it was executed in a declared environment.
- Do not pad a lesson with elementary material to meet a length target.

## Output

Write only the assigned teaching lesson path. Write assessment content only when separately assigned that companion path. Report evidence gaps and unresolved claims separately.

## Substantive revisions and feedback

- For an existing lesson, map user and reviewer feedback to explicit task acceptance criteria and record each item as applied, deferred, or task-specific, with a reason.
- A substantive revision changes explanations, examples, technical claims, assessments, or learning sequence. Declare separate independent review outputs for pedagogy, source-topic coverage, and relevant technical/provenance/language areas after authoring; the author cannot count self-review as independent.
- If a required reviewer is unavailable, record the gap and leave that review gate unresolved. Do not describe the revised lesson as independently reviewed.

## Compact package handoff

Follow module-pipeline for the default two combined independent reviews: technical+provenance and actual coverage+pedagogy/language. Each dimension remains required, with distinct findings in its combined report. Write directly to the declared lesson/assessment paths; a passing candidate is handed off at those same paths. Do not create a second final copy or mandatory revision. Actual failed reviews require unique revised paths and fresh reviews under the two-cycle limit. This combined assignment satisfies the separate review-dimension requirement above without four separate reports.
