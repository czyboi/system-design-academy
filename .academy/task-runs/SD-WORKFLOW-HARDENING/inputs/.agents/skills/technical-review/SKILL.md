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
