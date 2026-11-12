# Authoring Data Contract v1

AI generates **the same Markdown + YAML front-matter files the website will read**. Website code parses front matter and renders Markdown using standard libraries. There is no custom Thin Content Loader, adapter, section-to-JSON transform or second content format.

## Canonical files

- One teaching lesson: `modules/mXX/lessons/MXX-LYY.md`
- One companion assessment: `modules/mXX/assessments/MXX-LYY.md`
- Research evidence: `modules/mXX/evidence/MXX-LYY.md` (internal)

Use the exact paths in `delivery/backlog.json`. Git is the revision history; no nested lesson revisions, content manifests or duplicate lesson copies.

## Required metadata

Teaching lesson front matter:

```yaml
---
id: M01-L02
title: Example lesson
status: draft
level: intermediate
prerequisites: []
outcomes: [M01-L02-LO1]
assessment: modules/m01/assessments/M01-L02.md
source_review_date: 2026-11-12
---
```

Companion assessment front matter:

```yaml
---
id: M01-L02-assessment
status: draft
lesson: modules/m01/lessons/M01-L02.md
outcome_map:
  M01-L02-LO1:
    taught_in: Mechanism walkthrough
    items: [EX-1, Q1]
---
```

All fields shown are required; additional fields are optional. `prerequisites` and `outcomes` are arrays. Lesson filenames/IDs and companion paths must agree. The assessment maps every outcome to a real teaching heading and existing exercise/question IDs. `status: draft` does not mean publishable.

## Markdown

- Use free-form CommonMark/GFM headings, paragraphs, tables, lists, links, inline/fenced code, images and teaching-driven Mermaid diagrams.
- No fixed heading titles, section count, word count, minimum number of links or diagram quota. Stable `EX-1` and `Q1`–`Q8` labels support assessment outcome mapping.
- Do not use executable raw HTML/MDX, unsafe URL schemes or repository-escaping relative paths. Images require meaningful alt text and appropriate rights.
- If a necessary formula or diagram exceeds current rendering support, **preserve its educational requirement** and report the unsupported feature rather than deleting the explanation.

## Separation of responsibilities

**Format (this file):** metadata, paths, safe Markdown and mappings. **Teaching quality:** accuracy, evidence, causal mechanisms, worked examples, trade-offs, failures, exercises and licensing are controlled by `lesson-authoring`, `assessment-design`, approved curriculum and `GOVERNANCE.md`.

**On-demand validation:** `python scripts/validate_content.py --scope repo` checks metadata, canonical links and Markdown syntax/safety without rewriting files. It reuses `validate_format.py` internally. Python regression tests run automatically against isolated fixtures; AI reviews and checks of real lesson content remain manual.

**Website:** will parse this YAML/Markdown directly. Rendering security, solution visibility and human publication approval are future product concerns, not an additional content transformation pipeline.

References: [GFM](https://github.github.com/gfm/), [CommonMark](https://spec.commonmark.org/), [Mermaid security](https://mermaid.js.org/config/usage.html).
