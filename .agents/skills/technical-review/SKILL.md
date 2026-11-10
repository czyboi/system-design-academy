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

When the task step declares `review`, write both assigned outputs: the explanatory Markdown report and verdict JSON following `docs/workflow-contract.md`. Record exact SHA-256 hashes for every declared reviewed artifact, verdict, and finding IDs with severity/status. An open blocker or major finding forbids `ready-for-human-review`. Do not infer a pass from another review. Rechecks inspect changed sections and their dependencies and bind the result to the complete current artifact set.
