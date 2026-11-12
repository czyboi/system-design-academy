# Authoring Format Contract v1 — new canonical lessons

## Purpose and quality priority

Represent **new, original System Design lessons and their companion assessments** as safe, web-renderable Markdown without limiting what the course teaches. Apply the approved curriculum and outcomes first, then technical correctness and evidence, pedagogical clarity, and only then formatting convenience. Never remove a necessary example, formula, diagram, trade-off, or failure mode merely because a renderer cannot display it yet.

The default authoring graph remains **Research → Author → completed draft**. `content-format` is a compact input to the existing author step, not a new agent or review stage. Human-requested quality reviews and deterministic content/format validation stay separate and optional during drafting. Publication requires independent human approval.

## One canonical lesson per ID

- Create one lesson at `modules/mXX/lessons/MXX-LYY.md`, a separate assessment at `modules/mXX/assessments/MXX-LYY.md`, and evidence at `modules/mXX/evidence/MXX-LYY.md` (use the exact paths from `delivery/backlog.json`).
- **Git is the revision history.** Do not create `revision-1/`, `revision-2/` directories, alternative lesson copies or `content-manifest.json`. Revisions edit the canonical file, with explicit task-state/review decisions when appropriate.
- The approved curriculum version `curriculum/revision-1/` is a **syllabus snapshot**, not a version of lesson content; retain it. Old milestone lesson snapshots are not imported into the fresh authoring flow.
- Filenames, front-matter lesson IDs and companion references must agree. Do not infer website publication or reviewer approval from a draft's existence.

## Front matter and structured content

- Lesson front matter: `id`, `title`, `status: draft`, `level`, `prerequisites` (list), `outcomes` (list of stable outcome IDs), `assessment` (canonical relative path), `source_review_date`. Keep optional fields where useful, but do not require SEO, slug, schema-version or publication fields in the source.
- Companion assessment front matter: `id`, `status: draft`, `lesson` (canonical relative path), and `outcome_map` for **every** lesson outcome, mapping to a real teaching heading and existing assessment item IDs.
- Teach the motivating problem, core mechanism, worked reasoning, assumptions, trade-offs, failure modes, decision framework and grounded references. Additional sections are allowed; a fixed heading splitter must never discard unknown Markdown.
- Keep the practical exercise, 5–8 knowledge checks, answers with reasoning, worked solution and rubric in the **assessment file**, not in the lesson. Both `Answer:` / `Explanation:` and `**Answer:**` / `**Explanation:**` are valid.
- The source research evidence should provide specific authoritative URLs/sections, version/date scope and unresolved claims. Do not fabricate citation support, measured performance, product guarantees or asset rights.

## Markdown representation

- Use CommonMark/GFM headings, paragraphs, emphasis, lists, tables, code fences, inline code and links. Preserve the complete authored Markdown and its order; do not transform into fixed-size page blocks or silently drop unsupported constructs.
- Use fenced code blocks, with a language tag when useful; unlabeled or `text` fences remain allowed for traces and diagrams-as-text. Never execute embedded code in the renderer.
- Add diagrams when they clarify the mechanism; Mermaid is preferred only when accurate. Original assets need meaningful alt text and reviewed rights. No minimum/maximum diagram quota.
- Avoid executable raw HTML, MDX, scripts, unsafe URL schemes and path traversal. Website rendering must sanitize HTML and keep Mermaid security strict.
- Display-math delimiters and some advanced diagrams may not be supported by the current web-renderer plan. Preserve the technical requirement and flag unsupported presentation rather than weakening the lesson.

## Validation versus approval

- `scripts/validate_content.py` checks canonical paths, lesson-assessment linkage, outcomes and structural teaching/assessment requirements. `scripts/validate_format.py` checks Markdown/YAML syntax, links/assets and conservative Mermaid safety.
- Python **regression tests run automatically on PRs** using fixtures; they are not a substitute for reviewing real lessons. Content and format checks on authored files run **only when explicitly requested**, including through the manual GitHub Actions workflow.
- A passing deterministic validator does **not** prove correctness, source quality, legal rights, pedagogy or browser rendering fidelity. When the user requests a qualitative review, assess actual claims, explanations, examples, exercises, diagrams and risks.
- An edited reviewed lesson may require a manual `needs_review` status change. Neither file edits nor format changes auto-invalidate task progress; no task fingerprints/checksums or implicit review loops.
- The website loader, interactive exercise visibility, publication approval and deploy rules are **separate future product work**. Do not expose solutions publicly without an explicit visibility decision.

## References

- [GitHub Flavored Markdown spec](https://github.github.com/gfm/)
- [CommonMark spec](https://spec.commonmark.org/)
- [Mermaid security configuration](https://mermaid.js.org/config/usage.html)
- [Task and review workflow](workflow-contract.md)
- [Deterministic format validation](content-format-validation.md)
