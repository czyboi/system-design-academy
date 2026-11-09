# Content, Source, and Publication Governance

## Source hierarchy

1. Standards and RFCs for protocol/specification behavior.
2. Official vendor documentation for product-specific behavior.
3. Peer-reviewed papers and original research for foundational algorithms and systems.
4. Engineering blogs and conference talks for implementation case studies.
5. System Design Primer and curated educational material for topic discovery and learning structure.

A source's placement in this hierarchy does not guarantee its accuracy; check publication date, scope, version, and context.

## Claim-level provenance

For important claims, store: claim text, source URL, section/anchor, publisher, version/date checked, applicability, and confidence/verification status. Do not cite a landing page if a more specific page supports the claim. Search snippets are discovery aids, not final evidence.

## Technical accuracy

- Never generalize behavior from PostgreSQL to all SQL databases, or from one queue/database product to another.
- Record product/version boundaries where semantics differ.
- Mark unknown or unverified claims instead of guessing.
- Do not invent benchmarks, scale numbers, SLAs, or performance multipliers.
- Run SQL/code samples in a declared environment when presenting them as executable.
- Distinguish HA, replication, backup, and disaster recovery.

## Copyright and licensing

- Maintain a source/asset register.
- For CC BY 4.0 adaptations, retain author/title/source/license attribution and indicate changes.
- Do not assume images, diagrams, notebook code, flashcards, or linked third-party works inherit the license of a repository containing them.
- Prefer original diagrams, examples, datasets, and exercises.
- Link to third-party documentation rather than copying large portions.
- Escalate ambiguous rights or substantial adaptations for qualified legal review.

## AI use

- AI may research, summarize, draft, diagram, and create assessment materials.
- AI must preserve source traceability and label uncertainty.
- AI cannot approve its own output for publication.
- No external or learner-facing publication without human approval.

## Publication gate

Required: technical QA, pedagogical QA, source/citation QA, asset/license QA, and human approval. A draft cannot be labelled `approved` or `published` solely because an automated check passes.
