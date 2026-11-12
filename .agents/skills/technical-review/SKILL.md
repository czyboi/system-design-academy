---
name: technical-review
description: Independently audit a System Design lesson for correctness, assumptions, product-version scope, unsupported claims, trade-offs, and failure modes.
---

# Technical Review

Review first; do not rewrite.

1. Independently inspect cited primary sources.
2. Extract high-impact claims and verify the cited source supports each one.
3. Check definitions, causal explanations, assumptions, edge cases, capacity reasoning, failure modes, and trade-offs.
4. Detect vendor/version conflation; distinguish protocol behavior from implementation choice.
5. Check diagram arrows/labels against the described behavior.
6. Check SQL/code examples; if not executed in a declared environment, mark them untested.
7. Identify false absolutes, missing conditions, misleading simplifications, and unsupported numbers.
8. Do not treat another AI review as evidence.

## Severity
- blocker: materially false or likely to teach a wrong design decision;
- major: missing condition/trade-off likely to mislead;
- minor: imprecise or incomplete explanation;
- note: optional improvement.

## Output
Findings first, each with exact quote/location, severity, explanation, evidence URL/section, and suggested correction. End with `block`, `revise`, or `ready-for-human-review`. Never approve publication.

## Machine-readable gate output

Run this reviewer only when explicitly requested by the user. For a declared review task, write the requested Markdown findings and optional JSON verdict using `docs/workflow-contract.md`; include finding IDs, severity and status, but no artifact checksums. An open blocker/major finding forbids `ready-for-human-review`. No reviewer may trigger code validation or other reviewers automatically. Record content-review status explicitly when authorized; this is not human publication approval.

## Combined technical and provenance review

When the user explicitly requests a combined technical/source audit, this reviewer also executes provenance-review. Read and execute that shared skill, recording separate technical and source/rights findings in one report and one artifact-bound verdict. Either material failure blocks the combined verdict. The reviewer must be independent of the author and teaching reviewer. Request a separate specialist for ambiguous rights or unresolved claims beyond competence; do not waive checks because the handoff is combined.
