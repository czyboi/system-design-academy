---
name: source-research
description: Research System Design topics and build claim-level source evidence. Use before drafting when standards, algorithms, product behavior, or current vendor-version facts need verification.
---

# Source Research

Build an auditable evidence pack, not a generic essay.

1. Start from lesson outcomes and list claims that need evidence.
2. Use the System Design Primer for topic coverage and candidate references, not as sole authority.
3. Prefer standards/RFCs for protocol behavior, official vendor docs for product behavior, and original papers for foundational algorithms.
4. Open exact source pages and sections. Search snippets and model memory are discovery aids only.
5. Record publisher, exact URL/anchor, product/version, date checked, claim supported, limitations, and confidence.
6. Separate general principles from product-specific behavior. Never transfer PostgreSQL semantics to MySQL or MongoDB.
7. Identify disagreements, missing evidence, stale pages, and claims needing experiments.
8. Recommend Deep Research only for contested topics or synthesis across many independent sources; use normal search/direct docs for bounded questions.

## Output
Return a claim/source matrix with claim ID, exact proposed claim, source title/publisher/URL/section, version and date checked, scope supported/not supported, confidence (`verified`, `partial`, `unresolved`), and follow-up needed.

Do not write the lesson, invent citations, or claim a URL was checked if it was not opened.

## Reuse and bounded research

Reuse a pinned evidence snapshot when its revision, product/version and claimed scope still match. Preserve URL/section and date checked; re-open sources for new or changed claims and volatile behavior. Share a compact claim matrix and source locations, not an entire chat transcript. Technical reviewers independently inspect primary evidence even when using the same snapshot.
