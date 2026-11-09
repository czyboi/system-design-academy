# AI Agent Instructions — System Design Academy

Read these files before making content changes:

1. `PROJECT_SPEC.md`
2. `GOVERNANCE.md`
3. `CURRICULUM_MASTER.md`
4. The target module's curriculum, content guidelines, attribution policy, QA checklist, source registry, and lesson template.

## Operating rules

- Work only on the explicitly requested module and lesson IDs. Do not expand scope silently.
- Treat `sources/source-registry.csv` as a discovery index, not proof that every claim is already verified.
- Prefer standards/RFCs and official vendor documentation for normative or version-specific behavior.
- Open the exact source page and cite the most specific relevant section. Search snippets are not evidence.
- Record the product, version/scope, date checked, and claim supported for version-sensitive facts.
- If a source is unavailable or does not support a claim, mark the claim `needs-human-verification`; do not guess.
- Use the System Design Primer for topic coverage and learning structure. Do not translate it paragraph-by-paragraph or copy third-party diagrams, images, notebooks, code, or flashcards.
- Create original explanations, examples, diagrams, exercises, quiz questions, answers, and rubrics.
- Keep generated material at `status: draft`. Never set `approved` or `published`.
- Do not publish learner-facing content, merge a PR, or make licensing/legal determinations.
- Do not add API keys, tokens, credentials, learner data, or other secrets to the repository.
- ChatGPT subscriptions do not include OpenAI API credits. Do not assume an API key or paid API access exists.

## Required workflow for each lesson

1. Read the module curriculum and identify prerequisites and learning outcomes.
2. Build a claim/source plan before drafting. Separate general principles from vendor-specific behavior.
3. Retrieve and inspect primary sources. Use ordinary search/document analysis for bounded questions; use Deep Research only for unresolved, multi-source synthesis.
4. Draft one lesson using the module's `workflow/lesson-template.md`.
5. Add editable Mermaid source when a diagram materially improves understanding; explain the diagram in prose.
6. Include a worked example, trade-offs, failure modes, exercise, 5–8 knowledge-check questions, and detailed answer explanations.
7. Map each learning outcome to at least one assessment item.
8. Perform a separate reviewer pass. The reviewer must list critical errors, weak/unsupported citations, version conflations, missing trade-offs, pedagogical gaps, and licensing concerns before suggesting edits.
9. Write a QA report. Do not hide unresolved concerns.
10. Run `python scripts/validate_content.py` and report its output.
11. Create a focused branch and pull request. Never push generated lesson content directly to `main`.
12. Stop at `ready-for-human-review`; request human approval for any publication decision.

## Pull request requirements

- Keep one PR focused on one lesson or a small, related set of lessons.
- Include changed lesson files, the corresponding QA report, and source-registry updates.
- PR description must summarize scope, sources checked, validation results, unresolved claims, and human actions required.
- If the same critical issue remains after two revision cycles, stop and request human judgment.
