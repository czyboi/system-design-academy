---
name: provenance-review
description: Audit source traceability, citations, attribution, adaptations, and third-party asset rights in System Design Academy content.
---

# Provenance and License Review

1. Identify claims relying on external sources and check whether the exact source is cited.
2. Distinguish topic inspiration, factual reference, quotation, translation, adaptation, and original material.
3. For adaptations of System Design Primer, record Donne Martin, title, source URL, CC BY 4.0 link, and changes made.
4. Never assume images, diagrams, notebook code, flashcards, or links inside Primer inherit its license.
5. For each third-party asset, record creator, source, terms/license, and permission status. If unclear, replace with original material or seek permission.
6. Flag fabricated, overly broad, or unrelated citations.
7. Check that no endorsement, certification, or affiliation is implied.
8. Do not provide a definitive legal opinion; escalate ambiguous rights or substantial adaptations to qualified counsel.

## Output
Return an asset/source ledger and findings with severity blocker / major / minor / note. End with `block`, `revise`, or `ready-for-human-review`; never declare legal approval.

## Machine-readable gate output

Run this reviewer only when explicitly requested by the user. For a declared review task, write the requested Markdown findings and optional JSON verdict using `docs/workflow-contract.md`; include finding IDs, severity and status, but no artifact checksums. An open blocker/major finding forbids `ready-for-human-review`. No reviewer may trigger code validation or other reviewers automatically. Record content-review status explicitly when authorized; this is not human publication approval.

## Combined review assignment

When assigned alongside technical-review, contribute the source/asset ledger and distinct provenance findings to the same review report and overall verdict. Do not require a duplicate ledger when the existing evidence already records the relevant sources/assets. Any unresolved material rights or attribution issue blocks acceptance or requires a scoped specialist; combining roles is not legal approval.
