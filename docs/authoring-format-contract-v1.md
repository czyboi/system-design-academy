# Authoring Format Contract v1 — authoring guidance

> Status: **connected to new lesson authoring on PR #43** (effective on `main` only after merge). No automatic authoring gate or changes to completed historical artifacts. Format checks remain user-triggered.

## Adoption, quality guardrails and agent delivery

For **newly claimed lesson tasks**, `.academy/state/task.template.json` declares `.agents/skills/content-format/SKILL.md` as an `author` input; Codex and Claude lesson-author adapters and the module-pipeline skill also reference it. Read this longer specification only if format details are unclear, to avoid unnecessary tokens. Historical completed authoring tasks remain completed and are never automatically invalidated.

**Precedence:** approved syllabus/outcomes → technical truth and complete mechanisms → pedagogy (worked examples, helpful visuals and reasoning) → format convenience. A required mathematical expression, architecture diagram or technical illustration must never be omitted or made less accurate just to fit a supported renderer. Flag a missing capability and extend the renderer/format by a separate reviewed task. No syntax quota, section length limit or diagram quota is imposed.

Technical/teaching reviews assess completeness, correctness and pedagogy **only when explicitly requested**. The deterministic format validator `scripts/validate_format.py` is implemented but is also run on demand, separately from automatic Python regression tests. Neither review nor validation is a default authoring dependency.

This integration does not add an LLM step. Reading a compact formatting skill **does consume a small amount of input tokens** in future authoring; the existing deterministic format validator has no LLM token cost. Avoid passing the entire specification in every agent brief when the compact instruction is sufficient.

## 1. Scope and authority

- This contract governs **representation and safe consumption**, not what to teach. Course depth, learning outcomes, technical accuracy, source provenance, exercises, and teaching quality remain governed by the approved curriculum, `modules/database/governance/content-guidelines.md`, `.agents/skills/lesson-authoring/SKILL.md`, and optional independent review.
- Applies to teaching lessons, companion assessments, and module integrated packages. Each artifact retains its own existing structure; no universal JSON rewriting or new required metadata is introduced here.
- Canonical artifact bytes and reviewed revisions remain immutable for the purpose of this rollout. A website-specific mapping, summary, or slug must live outside reviewed Markdown until separately approved.
- An accepted automated review (`ready-for-human-review`) is **not** human publication approval.

## 2. Existing front matter is the baseline

Lesson YAML front matter already carries `id`, `title`, `status`, `level`, `prerequisites`, `outcomes`, `assessment`, `source_review_date`, and `reviewer` on the inspected samples. Do not add a required `schema_version`, `kind`, `slug`, or `summary` to their source files as part of website integration.

- Keep IDs stable, including `Mxx-Lyy` lesson IDs and the explicit outcome IDs. Preserve the meaning of `assessment` as a repository-relative companion path.
- `prerequisites` is an array of strings, but some strings identify other lessons while others describe entry knowledge. Consumers **must not** treat every string as a lesson ID or infer semantics from natural language.
- Assessment front matter remains separate (`id`, `status`, `lesson`, `outcome_map`) and refers to actual teaching headings and assessment item IDs.
- Integrated package formats are distinct from lesson and companion formats; do not force them to carry lesson-only metadata.
- In the generation workflow, canonical content remains `status: draft`. Publication approval and version selection will have separate human-controlled records in a later website/release task; task-state progress uses no file hashes.

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
- Repository-wide content and format checks select the explicitly listed lesson/assessment paths from each module's `content-manifest.json`. If nested revisions exist without a selection manifest, content validation reports an error rather than guessing. Historical versions remain untouched.
- Review-ready drafts may be previewed in an access-controlled development environment; they must **not** be published publicly without independent human approval of the exact selected bytes.
- Missing selected assessments/assets or unsupported constructs must fail closed rather than silently choose another revision or omit content. Any future release-integrity hash is separate from the task lifecycle and does not enable automatic `STALE`.
- This contract does not itself define the public JSON API, approval record schema, or deployment process. Those are separate subsequent steps.

## 8. Compatibility and evolution

- **v1 compatibility promise:** the 13 selected MS01–MS02 lessons and companions must remain readable without editing their canonical bytes. Existing formatting variants are first-class fixtures.
- Changes to presentation tooling must not rewrite reviewed source. When reviewed teaching content changes materially, the author or owner explicitly marks the appropriate review scope `needs_review`; no automatic review invalidation or fingerprint-based task transitions occur.
- New syntax may be introduced once the web renderer and regression tests support it, with an explicit versioned capability note. Breaking changes require an explicit migration plan, not silent fallback.
- Contract version `v1` in this document is a **consumer-format specification**, not the schema version of any lesson front matter.

## 9. Implementation boundary

1. **Implemented:** deterministic format validation and synthetic regression fixtures using `markdown-it-py`; historical commit-pinned snapshot tests were intentionally removed.
2. **Future:** a thin website content loader honoring explicitly selected paths and preserving the Markdown body.
3. **Future:** independent human approval and publication controls, separate from authoring completion.
4. **Future:** website renderer plus visual QA for tables, code, diagrams, long lessons and assessments.

The compact format skill is a required input for new lesson tasks. CI runs Python regression tests automatically, but AI reviews and content/format validation remain opt-in.

## Reference specifications

- [GitHub Flavored Markdown spec](https://github.github.com/gfm/)
- [CommonMark spec](https://spec.commonmark.org/)
- [Mermaid security configuration](https://mermaid.js.org/config/usage.html)
- [Existing lesson/assessment workflow rules](workflow-contract.md)
- [MS01–MS02 compatibility audit](content-format-audit-ms01-ms02.md)
