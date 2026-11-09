# System Design Academy — Repository Instructions

## Project guardrails
- Work only on the explicitly requested module and lesson IDs.
- Prefer standards/RFCs and official vendor documentation. Record exact URL/section, product/version, and date checked.
- Treat System Design Primer as topic map and licensed source material, not sole technical authority. Do not translate it paragraph-by-paragraph or copy third-party assets without separate rights checks.
- Create original explanations, examples, diagrams, exercises, quizzes, and answer explanations.
- Keep generated lessons at `status: draft`. Never merge a PR or publish learner-facing content without explicit human approval.
- Never invent citations, benchmarks, guarantees, versions, licenses, or test results. Mark unresolved claims.
- Never commit credentials, API keys, tokens, learner data, or secrets.
- ChatGPT subscriptions do not include OpenAI API credits. Do not assume API access.

## Persistent task state — mandatory for multi-step work
- Before starting a multi-step task, search for an existing GitHub Issue and `.academy/state/tasks/<TASK-ID>.json`. Reuse the existing task when the goal is the same; do not create duplicate work.
- Read `.academy/state/README.md`, then run `python scripts/taskctl.py status <TASK-ID>` before doing task work.
- Treat `SKIP` as completed and reusable: do not repeat it. Treat `RESUME` as an interrupted step: read its checkpoint and continue. Treat `STALE` as changed inputs/outputs: inspect the diff and explicitly invalidate/re-run only what is affected. Treat `BLOCKED` as a dependency that must be resolved first.
- Call `taskctl start` before editing a step; checkpoint before handoff; commit declared outputs before `taskctl complete`.
- Never manually mark a step completed in JSON. `taskctl complete` verifies output files are tracked and clean, then records hashes and the commit SHA.
- Keep detailed progress in task JSON/JSONL; put only the owner, high-level status, links, blocker, and next action in the GitHub Issue.
- One active writer per task/lesson. Parallel reviewers must write to distinct report paths. The task state file is not a distributed lock.

## Skills and delegation
- Reusable procedures live in `.agents/skills/`. Use `task-intake` to create/claim work, `task-handoff` to resume across agents/providers, and `module-pipeline` for coordinated module generation.
- Specialist skills cover source research, curriculum design, lesson authoring, assessments, technical review, pedagogical review, and provenance review.
- Custom Codex subagent profiles live in `.codex/agents/`: `source_researcher`, `curriculum_designer`, `lesson_author`, `technical_reviewer`, `pedagogy_reviewer`, and `provenance_reviewer`.
- For a complete module task, delegate research and curriculum mapping in parallel; wait for both before authoring. After drafting, run technical, pedagogical, and provenance reviews in parallel; wait for all before revision.
- Give each agent exact inputs, output paths, and a stop condition. Never have two agents edit the same file. Parent owns shared files and final synthesis.
- Maximum two automated revision cycles. Stop for human judgment if critical disagreement remains.
- A role instruction such as "do not edit" is not a permission boundary. Custom subagent profiles inherit the parent session's permissions; set actual read-only access at the parent/host permission layer when needed.

## Content gates
- Every lesson needs outcomes, prerequisites, motivating problem, mechanism, worked example, trade-offs/failure modes, exercise, 5–8 knowledge checks with explanations, and direct references.
- Map every learning outcome to an assessment.
- Distinguish general principles from vendor-specific semantics.
- Use Deep Research only for multi-source synthesis or contested questions; use standard search and direct docs for bounded facts.
- Run `python scripts/validate_content.py`, `python -m unittest discover -s tests -v`, and `python scripts/taskctl.py validate`.
- Structural CI does not establish factual correctness, source reachability, legal rights, or teaching quality.
- Create a focused branch and draft PR. Never push generated lessons directly to `main`.