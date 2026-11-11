# Authoring Format Contract v1 — candidate (not enforced)

> Status: **proposed for human review**. This document does not add new authoring gates or alter accepted lesson artifacts. Its first implementation target is backward-compatible ingestion of SDA-MS01 and SDA-MS02.

## Adoption, quality guardrails and agent delivery

This is a **draft PR**: its rules are not active on `main` until merged. After adoption, **newly claimed content tasks** include both this document and the compact shared agent instruction `.agents/skills/content-format/SKILL.md` as declared author inputs; `.agents/skills/module-pipeline/SKILL.md` passes that instruction to the agent. Existing completed authoring tasks and their hash-bound artifacts are left alone.

**Precedence:** approved syllabus/outcomes → technical truth and complete mechanisms → pedagogy (worked examples, helpful visuals and reasoning) → format convenience. A required mathematical expression, architecture diagram or technical illustration must never be omitted or made less accurate just to fit a supported renderer. Flag a missing capability and extend the renderer/format by a separate reviewed task. No syntax quota, section length limit or diagram quota is imposed.

Before accepting newly generated output, the existing technical and teaching reviews still assess completeness, correctness and pedagogy. **These are qualitative review responsibilities, not machine-proof of no regression.** The deterministic format validator is a separate Step 2 and is not yet enforced by this PR.

This integration does not add an LLM step. Reading a compact formatting skill **does consume a small amount of input tokens** in future authoring; the later deterministic loader/validator has no LLM token cost. Avoid passing the entire specification in every agent brief when the compact instruction is sufficient.

## 1. Scope and authority

- This contract governs **representation and safe consumption**, not what to teach. Course depth, learning outcomes, technical accuracy, source provenance, exercises, and teaching quality remain governed by the approved curriculum, `modules/database/governance/content-guidelines.md`, `.agents/skills/lesson-authoring/SKILL.md`, and existing review gates.
- Applies to teaching lessons, companion assessments, and module integrated packages. Each artifact retains its own existing structure; no universal JSON rewriting or new required metadata is introduced here.
- Canonical artifact bytes and reviewed revisions remain immutable for the purpose of this rollout. A website-specific mapping, summary, or slug must live outside reviewed Markdown until separately approved.
- An accepted automated review (`ready-for-human-review`) is **not** human publication approval.

## 2. Existing front matter is the baseline

Lesson YAML front matter already carries `id`, `title`, `status`, `level`, `prerequisites`, `outcomes`, `assessment`, `source_review_date`, and `reviewer` on the inspected samples. Do not add a required `schema_version`, `kind`, `slug`, or `summary` to their source files as part of website integration.

- Keep IDs stable, including `Mxx-Lyy` lesson IDs and the explicit outcome IDs. Preserve the meaning of `assessment` as a repository-relative companion path.
- `prerequisites` is an array of strings, but some strings identify other lessons while others describe entry knowledge. Consumers **must not** treat every string as a lesson ID or infer semantics from natural language.
- Assessment front matter remains separate (`id`, `status`, `lesson`, `outcome_map`) and refers to actual teaching headings and assessment item IDs.
- Integrated package formats are distinct from lesson and companion formats; do not force them to carry lesson-only metadata.
- In the generation workflow, canonical content remains `status: draft`. Publication approval belongs to a separate, hash-bound decision record to be designed in a later step.

## 3. Markdown representation

- Treat the body as **Markdown**, using the CommonMark/GitHub Flavored Markdown (GFM) baseline, including paragraphs, headings, inline emphasis, ordered/unordered lists, blockquotes, links, tables, inline code, and fenced code blocks.
- A title heading and the teaching sections required by existing validation still apply. Supplemental heading titles and subsection counts may vary freely (e.g., `Worked example and historical architecture` is valid). **Do not split or discard educational content by matching a small fixed list of headings.**
- Retain the authored Markdown body and its meaningful order. Do not normalize it into a large collection of fixed sections or strip unknown blocks silently.
- Where an artifact cannot be rendered faithfully, report an explicit unsupported-format error at the consumption/build boundary instead of truncating the lesson. A rendering failure is not a reason to remove or simplify necessary teaching material.
- For new authored files, avoid executable inline HTML, MDX components, embedded scripts, and arbitrary iframes. This is a *consumer safety rule*, not a retrospective requirement to rewrite existing content.

## 4. Code and technical examples

- Fenced code blocks preserve all content literally. Prefer a language identifier when known; `text` and unlabeled fences remain allowed for diagrams-as-text, terminal output, traces, and examples whose language is unknown.
- Inline code is allowed. Do not execute code examples during rendering. Runtime verification or execution claims remain subject to existing technical review requirements.
- A future syntax-highlighter must provide safe plain-text fallback and must not modify code semantics.

## 5. Diagrams, images, and mathematics

- Diagrams are **optional and teaching-driven**. Prefer original Mermaid diagrams where useful and supported, using a fenced `mermaid` block. No per-lesson diagram quota is imposed.
- If Mermaid cannot express a mechanism clearly, keep the necessary explanation and escalate renderer support for an original, versioned asset or alternative format. Never simplify a technical concept merely to pass a diagram-format rule.
- Local assets, when introduced, need a stable repository-relative locator, meaningful text alternative, and separately reviewed provenance/license. Relative links resolve from the source artifact; consumers must reject repository traversal.
- LaTeX math delimiters and additional diagram formats are **extension candidates**, not proven v1 capabilities: add them only with an explicit render implementation and tests. Do not claim them supported solely because a parser accepts their text.
- Any Mermaid web renderer should retain a conservative security configuration (`securityLevel: strict`) and not allow content to enable unsafe click/HTML behavior. Rendered HTML must be sanitized.

## 6. Assessment-specific compatibility

- Continue separating exercise/questions/answers/rubrics from instructional lesson bodies.
- Both plain `Answer:` / `Explanation:` and emphasized `**Answer:**` / `**Explanation:**` occur in reviewed source. A future assessment parser must accept both, or preserve the Markdown whole; do **not** silently lose one style.
- Outcome mappings use the existing exact authored headings and item IDs (`Q1`...`Q8`, `EX-1`). Do not infer missing outcomes or auto-generate assessment answers.
- Public lesson output must not include private solution/rubric payload unless a separate product-level visibility decision allows it.

## 7. Revision selection, integrity, and publication

- A canonical lesson ID may have multiple versioned paths. Never choose a file solely by filename, modification time, directory order, or highest `revision-N` suffix.
- A consumer must use an explicit selected-artifact mapping backed by current teaching/technical review evidence and exact SHA-256 before treating the artifact as reviewed.
- Review-ready drafts may be previewed in an access-controlled development environment; they must **not** be published publicly without independent human approval of the exact selected bytes.
- Invalid hashes, missing assessments/assets, or unsupported constructs must fail closed rather than select another revision or silently omit content.
- This contract does not itself define the public JSON API, approval record schema, or deployment process. Those are separate subsequent steps.

## 8. Compatibility and evolution

- **v1 compatibility promise:** the 13 selected MS01–MS02 lessons and companions must remain readable without editing their canonical bytes. Existing formatting variants are first-class fixtures.
- Changes to presentation tooling must not invalidate completed content reviews by rewriting the original artifacts. Only modifications to reviewed source or authoritative specs should trigger the corresponding existing review/integrity logic.
- New syntax may be introduced once the web renderer and regression tests support it, with an explicit versioned capability note. Breaking changes require an explicit migration plan, not silent fallback.
- Contract version `v1` in this document is a **consumer-format specification**, not the schema version of any lesson front matter.

## 9. Implementation boundary (future, not part of this step)

1. Add non-mutating format validation and golden/negative tests against pinned MS01–MS02 fixtures. Prefer a standards-compliant Markdown parser over ad-hoc regex for understanding the body.
2. Implement a thin, deterministic content loader with selected-path/hash checking. Keep the Markdown body intact.
3. Add a separate publication gate for human-approved hashes.
4. Integrate the website renderer and perform visual QA on tables, code, diagrams, and long lessons.

No additional AI agent or LLM call is needed for deterministic build-time checks. The small format skill becomes a required authoring input for **new tasks after merge**, while deterministic renderer checks are still pending Step 2.

## Reference specifications

- [GitHub Flavored Markdown spec](https://github.github.com/gfm/)
- [CommonMark spec](https://spec.commonmark.org/)
- [Mermaid security configuration](https://mermaid.js.org/config/usage.html)
- [Existing lesson/assessment workflow rules](workflow-contract.md)
- [MS01–MS02 compatibility audit](content-format-audit-ms01-ms02.md)
