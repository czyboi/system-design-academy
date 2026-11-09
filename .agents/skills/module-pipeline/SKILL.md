---
name: module-pipeline
description: Orchestrate end-to-end creation or refresh of a System Design Academy module. Use for multi-lesson generation and coordination of research, authoring, reviews, and a GitHub PR.
---

# Module Pipeline

Act as lead orchestrator. Delegate bounded tasks to specialist subagents; do not do every specialist task in the main thread.

## Workflow
1. Read the target module curriculum, source registry, lesson template, content guidelines, attribution policy, and QA checklist.
2. Create a task manifest listing lesson IDs, dependencies, exact output paths, and states.
3. In parallel, ask `source_researcher` for claim/source evidence and `curriculum_designer` for prerequisites and outcome coverage. Both are read-only.
4. Reconcile their findings. Resolve conflicts or evidence gaps before writing.
5. Delegate lesson files to `lesson_author`. Assign unique lesson and report paths; the orchestrator owns shared files.
6. After drafts exist, run independent parallel reviews: `technical_reviewer`, `pedagogy_reviewer`, and `provenance_reviewer`.
7. Wait for all reviewers, consolidate actionable findings, and delegate corrections to the author. Maximum two revision cycles per lesson.
8. Run `python scripts/validate_content.py`.
9. Produce a run report with states, sources, verdicts, unresolved claims, and human actions.
10. Create a focused branch and draft PR. Never merge or publish learner-facing content.

## Delegation discipline
- Parallelize independent read-heavy research and reviews.
- Give each subagent a bounded question, exact inputs/output paths, and stop condition.
- Prefer read-only agents for research and review.
- Never let two agents edit the same file. Only the parent updates shared source registries/manifests.
- Keep the parent responsible for decisions and final synthesis.
- Stop if critical disagreement remains after two revision cycles.
- Subagents consume additional model/tool usage; parallelize only genuinely independent work.

## Required specialist skills
Use `source-research`, `curriculum-design`, `lesson-authoring`, `assessment-design`, `technical-review`, `pedagogical-review`, and `provenance-review` at their corresponding stages. Skills define procedures; custom agents define who performs them.
