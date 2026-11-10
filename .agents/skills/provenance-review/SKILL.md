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

When the task step declares `review`, write both assigned outputs: the explanatory Markdown report and verdict JSON following `docs/workflow-contract.md`. Record exact SHA-256 hashes for every declared reviewed artifact, verdict, and finding IDs with severity/status. An open blocker or major finding forbids `ready-for-human-review`. Do not infer a pass from another review. Rechecks inspect changed sections and their dependencies and bind the result to the complete current artifact set.

## Combined review assignment

When assigned alongside technical-review, contribute the source/asset ledger and distinct provenance findings to the same review report and overall verdict. Do not require a duplicate ledger when the existing evidence already records the relevant sources/assets. Any unresolved material rights or attribution issue blocks acceptance or requires a scoped specialist; combining roles is not legal approval.
