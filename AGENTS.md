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

## Skills and delegation
- Reusable procedures live in `.agents/skills/`. Use `module-pipeline` for module generation and specialist skills for research, curriculum design, authoring, assessments, and reviews.
- Custom Codex subagents live in `.codex/agents/`: `source_researcher`, `curriculum_designer`, `lesson_author`, `technical_reviewer`, `pedagogy_reviewer`, and `provenance_reviewer`.
- For a complete module task, delegate research and curriculum mapping in parallel; wait for both before authoring. After drafting, run technical, pedagogical, and provenance reviews in parallel; wait for all before revision.
- Give each agent exact inputs, output paths, and a stop condition. Never have two agents edit the same file. Parent owns shared files and final synthesis.
- Maximum two automated revision cycles. Stop for human judgment if critical disagreement remains.

## Content gates
- Every lesson needs outcomes, prerequisites, motivating problem, mechanism, worked example, trade-offs/failure modes, exercise, 5–8 knowledge checks with explanations, and direct references.
- Map every learning outcome to an assessment.
- Distinguish general principles from vendor-specific semantics.
- Use Deep Research only for multi-source synthesis or contested questions; use standard search and direct docs for bounded facts.
- Run `python scripts/validate_content.py`. It checks structure, not factual correctness, legal rights, or teaching quality.
- Create a focused branch and draft PR. Never push generated lessons directly to `main`.
