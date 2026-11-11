---
name: content-format
description: Keep Academy lessons and assessments renderable without compromising learning quality; used only for newly claimed authoring tasks.
---

# Content Format (compact authoring instructions)

The canonical representation specification is `docs/authoring-format-contract-v1.md`; consult it when a syntax or exception is unclear. These rules apply to **new work only after this PR is merged**. Never rewrite or reopen completed reviewed artifacts solely for formatting.

- **Priority:** approved curriculum/outcomes, technical accuracy, pedagogy and adequate examples/diagrams **before** presentation convenience. Format is not a reason to omit, shorten, weaken, or simplify a necessary explanation, formula, diagram, or exercise. Flag missing renderer capability or escalate an extension instead.
- Keep existing Markdown + YAML front matter and the separate lesson/assessment pair. Do not add `slug`, SEO fields, schema version, or new required metadata to canonical files.
- Use normal CommonMark/GFM syntax (headings, paragraphs, lists, GFM tables, links, inline/fenced code). Retain flexible teaching headings. Prefer fenced code with a language when known; allow `text` for traces/diagrams-as-text.
- Diagrams are teaching-driven, **never quota-driven**. Mermaid fences are preferred only when they faithfully represent the mechanism; an appropriate original asset or future supported notation may be needed. Do not invent Mermaid syntax, fake a diagram, or drop a useful visual.
- Keep outcome IDs, paths, citations and source/license information valid; no executable embedded HTML/MDX/scripts. Images/assets require meaningful alt text and rights checks.
- Assessment answers may be plain `Answer:`/`Explanation:` or bold `**Answer:**`/`**Explanation:**`. Preserve mappings and rubrics; no assessment content in the teaching file.
- If a technically necessary format is not covered, **report the exact need and preserve the content requirement**; do not silently transform or delete it.

No new authoring agent, review stage or LLM build step is introduced. Format checks will be added as deterministic CI validation in a separate scoped task; model instructions alone cannot guarantee correctness.
