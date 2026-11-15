---
name: lesson-authoring
description: Write concise, publication-ready, original System Design teaching lessons for experienced engineers using the approved curriculum and evidence pack.
---

# Lesson Authoring

## Inputs

Require the canonical task specification, selected approved curriculum, source research evidence, the declared `lesson-authoring`, `assessment-design` and `content-format` skills, `GOVERNANCE.md`, and exact canonical output paths. Module-specific templates and checklists may be consulted as examples, but are not mandatory new workflow inputs or substitutes for the current curriculum. The current approved baseline is `curriculum/revision-1/`. For Academy work, the current default learner is a middle/senior engineer studying system design, and learner-facing prose is English-only. Follow newer explicit user direction recorded in the task specification.

Do not start when the user has explicitly paused work, required source evidence is absent, or the lesson/assessment output paths are not separate. Review and validation are not drafting prerequisites unless the user specifically makes them part of this task.

## Publication-ready authoring standard

The `draft` front-matter status means **awaiting human approval**, not incomplete or demo-grade content. At handoff the lesson and companion must be educationally complete for publication: every assigned outcome is explained through causal mechanism and worked reasoning, with a precise trace, diagram or concrete interface when prose alone leaves a material gap. Do not pad for length or require universal diagram/code quotas. A learner must not depend on the answer key to understand missing lesson mechanisms.

For design exercises, independently check system capacity and **user-visible success**. State each important SLO's original-operation population, measurement window, start/end events, threshold and what rejected, failed, timed-out or late work counts as. Grade admitted/successful latency separately so excessive shedding cannot make a design look successful. Flag unresolved teaching or assessment gaps instead of deferring them to a post-merge phase. Apply these expectations through the existing self-check and independent reviews; add no agents or workflow stages.

## Progressive teaching and concept dependencies

For concepts with multi-step production hardening, teach the *causal progression*, not a checklist of technologies. Establish the concrete constraint and the smallest working model first; trace a normal operation, identify the failure or limit that motivates each added mechanism, then show how the hardened design changes the behavior and cost. End with the conditions for choosing or rejecting the added complexity. Preserve all required depth, but do not make production-only mechanisms appear necessary for every workload.

This is a reasoning order, **not** five mandatory headings, a length target, or a requirement to reteach standard backend knowledge. For each nontrivial concept needed to follow a central explanation, either explain its role at first use or link to the specific prerequisite where it is taught. Do not treat an unexplained term, source citation, assessment answer, or later worked solution as a substitute for the missing causal link. A compact trace, state transition or diagram is useful when prose alone leaves a material gap, never as a fixed quota.

In the existing author self-check, reconstruct the lesson's main decision from the lesson and declared prerequisites alone: the initial mechanism, its failure boundary, why the improvement works, and what it sacrifices. Repair only links that matter to an outcome; avoid padding correct, concise passages.

## Verified cross-module feedback

Before drafting, use the parent's relevant (maximum three) reviewer-confirmed prevention reminders selected from `.academy/knowledge/lessons-learned.json` by `scripts/learning_memory.py suggest --tags ... --role lesson_author`. They are hints for avoiding previously corrected mistakes, **not** technical sources or new constraints on teaching content. Verify claims against the current task evidence and curriculum; flag conflicts instead of copying a memory blindly. No additional AI step is required; do not load the entire memory file.

## Procedure

1. Confirm lesson ID, audience, prerequisites, status, scope, outcomes, and the exact lesson path.
2. Teach the engineering problem and decision before adding terminology. Assume common backend, SQL, and application fundamentals; explain them only when they are essential to the design decision.
3. Explain the mechanism causally: what changes in the system, why it changes, and which decision follows. Keep the exposition concise and remove repeated definitions, generic introductions, and material that does not support an outcome.
4. Use original, realistic examples and diagrams. Explain the important nodes and flows.
5. Teach relevant decision criteria, trade-offs, bottlenecks, failure modes, and operational effects. Distinguish general principles from version-specific vendor behavior.
6. Include a worked example that demonstrates the design reasoning. Keep the lesson file instructional: do not embed a quiz, knowledge-check bank, answer key, or assessment rubric.
7. Put the practical exercise, 5–8 knowledge checks, answers/explanations, rubric, and outcome-to-item map in the separately declared companion assessment artifact. Coordinate with assessment-design; do not use questions as a substitute for teaching.
8. Cite exact sources next to important or version-sensitive claims. Mark unresolved claims instead of guessing.
9. Before handoff, compare the finished explanation against every assigned Story topic, approved outcome and acceptance criterion. Confirm that each outcome is genuinely taught by worked reasoning, not merely named in a heading. Check numerical assumptions, trace mechanisms and document unresolved evidence. This is the author's responsibility, not an additional AI reviewer or validation stage.
10. Use `content-format` and the single data contract for front matter and Markdown; preserve attribution/adaptation notes. Choose headings to teach effectively, rather than satisfying an arbitrary section-name or link-count quota.

## Prohibited

- No paragraph-by-paragraph translation or close paraphrase of the Primer.
- No invented benchmarks, guarantees, product behavior, URLs, or version numbers.
- No unlicensed third-party assets.
- Do not call SQL or code tested unless it was executed in a declared environment.
- Do not pad a lesson with elementary material to meet a length target.

## Output

Write only the assigned canonical teaching lesson path. Write assessment content only at the separately declared canonical companion path; do not create `revision-N` copies or a content manifest. Report evidence gaps and unresolved claims separately.

## Substantive revisions and feedback

For edits to an existing lesson, follow authorized scope and record material user feedback. Flag changes to previously reviewed technical claims, assessments or explanations explicitly with `taskctl review-status TASK-ID --scope technical --state needs_review --reason "..."` (and/or the explicitly affected review scope). Cosmetic changes need not reset review status.

## Draft handoff

Write the lesson/assessment at their declared paths and record authoring completion. The **parent orchestrator**, not the author subagent, then invokes the single scoped `draft_handoff.py` validation-and-Git-delivery helper for the completed task or batch. Do not independently spawn a reviewer or start an autonomous correction loop; the **parent** may return located findings for at most two corrective rounds **on this lesson**. Make precise edits to the affected lesson/assessment, preserving correct material, and report what changed. The parent orchestrator triggers independent technical/provenance and coverage/pedagogy review **immediately after this lesson's draft handoff**, using Stage A of `module-quality-review`; the author does not self-review. A separate lightweight module synthesis review runs only when all lesson QA is ready and integration is drafted. After automatic QA, the parent may authorize bounded corrective edits from the reviewers' located findings and independent targeted re-review under `module-quality-review`. The user may request additional corrections/review or broader validation. Draft completion, quality review and successful Git delivery are not publish approval.
