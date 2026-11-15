---
id: M00-EX1-solution
status: draft
---

# Reference brief and rubric

## Reference brief

| Priority | Actor and action | Requirement or assumption |
|---|---|---|
| Must | Publisher uploads a signed PDF and grants access to a named employee. | Reject uploads over 2 MiB. Verify publisher role before writing the document and grant records. |
| Must | Signed-in reader follows the link to fetch the PDF. | Authorize by reader and document. Read the current grant before streaming bytes. |
| Must | Publisher revokes access and receives a confirmation. | Every authorization check started after confirmation denies that grant, absent a later grant. |
| Assumption | One office accepts a service interruption if the only app host is replaced. | Confirm tolerated outage duration and data recovery requirements with the owner before implementation. |
| Excluded | Public links, concurrent editing and retrieval of copies already delivered. | Retain these boundaries during the review. |

Treat the user counts and peak arrival rate as sizing assumptions. Confirm how long a host interruption is tolerable, how much data loss is acceptable, and how downloads cluster within a minute.

**Option A.** Use one application deployment and one durable relational store for metadata, grants and document bytes. The application accepts a publish request, stores the document and grant in one transaction, and reports success after commit. For each download it authenticates the employee, checks the grant and then streams the document. Revoke confirms after removing the grant in the store. Require grant changes and checks to observe the same per-grant order. A check started after revoke confirmation must deny the reader unless a later grant restores access. A protected HTTP response uses `Cache-Control: no-store` from the first download so a compliant cache cannot serve later requests without a new check. [Herlihy and Wing, §2.2](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf#page=7) · [RFC 9111 §5.2.2.5](https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2.2.5)

**Option B.** Put PDF bytes in private object storage and keep grants in the authoritative database. The app applies the same check and streams the object. This adds a storage call and an extra failure case. Upload objects before making them visible through committed metadata. If publication times out, reconcile the result using the upload identifier. Delete an object only when its publication attempt is terminal and authoritative metadata confirms that no committed document references it. Separate blob and grant storage lets each grow independently. A direct download link that remains usable after revocation would violate the stated rule. [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

Choose A while traffic is modest and the team accepts a host interruption. Fifty downloads of 2 MiB each represent 100 MiB of payload, or about 1.67 MiB/s averaged across a minute. Use a burst test to find short-interval resource limits. Check revocation by downloading once, revoking, waiting for confirmation and requesting the same link through the actual client path. Confirm that the second request is denied.

For the host-loss variant, remove the application host while load continues. At the modeled offered rate there are 250 original requests in five minutes, so at least 238 must return a complete PDF by the four-second client deadline. Track timeouts, failures, rejections and late bodies against the full offered count. Record survivor capacity and latency among completed downloads separately. An app host with no survivor cannot pass during a sustained outage. Test a redundant application path with enough surviving capacity and a reachable grant and document store. Separating PDF storage by itself leaves the app as a required dependency. [Google SRE Workbook, What to Measure Using SLIs](https://sre.google/workbook/implementing-slos/#what-to-measure-using-slis)

## Self-evaluation

Score each criterion from 0 to 2. Award 2 for clear reasoning with testable evidence, 1 for a correct but incomplete argument, and 0 for missing or contradictory reasoning.

| Criterion | Evidence for full credit |
|---|---|
| Scope | Prioritized actors and use cases, two measurable criteria, and named assumptions and exclusions. |
| Traceability | Clear request paths and a mechanism that enforces post-confirmation revocation. |
| Trade-off | Two feasible candidates with distinct costs and explicit effects on one required property. |
| Verification | A decision-changing observation and matching test. For the host-loss variant, count timely full downloads over all original authorized requests offered in the five-minute window. Report revoked-link checks separately. |

A proposed design can earn full credit with a different baseline if it honors the access constraint and explains its costs. M00-S1 uses both M00-L02 outcomes. Readiness is assessed in the [M00-L01 companion](../assessments/M00-L01.md).
