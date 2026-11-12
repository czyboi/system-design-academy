---
name: content-format
description: Compact authoring guidance for directly usable YAML and Markdown content.
---

# Content format

The **single format authority** is `docs/authoring-format-contract-v1.md`; use it for required fields and supported syntax. Do not define a separate format or add a conversion layer.

- Write the canonical lesson and companion assessment paths directly as YAML front matter plus Markdown; Git stores revisions.
- Preserve exact IDs, outcome maps and companion references. Use GFM with free-form headings, code, tables and teaching-driven diagrams.
- No fixed heading names, length, link-count or diagram quota. Avoid raw HTML/MDX, unsafe links, missing image alt text and unlicensed assets.
- Never weaken a necessary explanation, formula or example solely to fit renderer capabilities; report the limitation.

Teaching and assessment quality remain governed by the approved curriculum, `lesson-authoring`, `assessment-design` and `GOVERNANCE.md`. Use `scripts/validate_content.py` only when validation is requested; no extra AI or adapter stage.
