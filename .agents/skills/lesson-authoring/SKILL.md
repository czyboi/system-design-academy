---
name: lesson-authoring
description: Write concise, original System Design teaching lessons for experienced engineers using the approved curriculum and evidence pack.
---

# Lesson Authoring

## Inputs

Require the canonical task specification, selected approved curriculum, source research evidence, the declared `lesson-authoring`, `assessment-design` and `content-format` skills, `GOVERNANCE.md`, and exact canonical output paths. Module-specific templates and checklists may be consulted as examples, but are not mandatory new workflow inputs or substitutes for the current curriculum. The current approved baseline is `curriculum/revision-1/`. For Academy work, the current default learner is a middle/senior engineer studying system design, and learner-facing prose is English-only. Follow newer explicit user direction recorded in the task specification.

Do not start when the user has explicitly paused work, required source evidence is absent, or the lesson/assessment output paths are not separate. Review and validation are not drafting prerequisites unless the user specifically makes them part of this task.

## Procedure

1. Confirm lesson ID, audience, prerequisites, status, scope, outcomes, and the exact lesson path.
2. Teach the engineering problem and decision before adding terminology. Assume common backend, SQL, and application fundamentals; explain them only when they are essential to the design decision.
3. Explain the mechanism causally: what changes in the system, why it changes, and which decision follows. Keep the exposition concise and remove repeated definitions, generic introductions, and material that does not support an outcome.
4. Use original, realistic examples and diagrams. Explain the important nodes and flows.
5. Teach relevant decision criteria, trade-offs, bottlenecks, failure modes, and operational effects. Distinguish general principles from version-specific vendor behavior.
6. Include a worked example that demonstrates the design reasoning. Keep the lesson file instructional: do not embed a quiz, knowledge-check bank, answer key, or assessment rubric.
7. Put the practical exercise, 5–8 knowledge checks, answers/explanations, rubric, and outcome-to-item map in the separately declared companion assessment artifact. Coordinate with assessment-design; do not use questions as a substitute for teaching.
8. Cite exact sources next to important or version-sensitive claims. Mark unresolved claims instead of guessing.
9. Use `content-format` and the single data contract for front matter and Markdown; preserve attribution/adaptation notes. Choose headings to teach effectively, rather than satisfying an arbitrary section-name or link-count quota.

## Prohibited

- No paragraph-by-paragraph translation or close paraphrase of the Primer.
- No invented benchmarks, guarantees, product behavior, URLs, or version numbers.
- No unlicensed third-party assets.
- Do not call SQL or code tested unless it was executed in a declared environment.
- Do not pad a lesson with elementary material to meet a length target.

## Output

Write only the assigned canonical teaching lesson path. Write assessment content only at the separately declared canonical companion path; do not create `revision-N` copies or a content manifest. Report evidence gaps and unresolved claims separately.

## Substantive revisions and feedback

For edits to an existing lesson, follow authorized scope and record material user feedback. Flag changes to previously reviewed technical claims, assessments or explanations explicitly with `taskctl review-status TASK-ID --state needs_review --reason "..."`. Cosmetic changes need not reset review status.

## Draft handoff

Write the lesson/assessment at their declared paths, record authoring completion and stop. **Do not launch independent AI reviewers, Python validation, or a revision loop automatically.** The user can later request technical/provenance review, actual coverage/pedagogy review, targeted corrections or validation independently. No duplicate final-copy step is needed, and draft completion is not publish approval.
