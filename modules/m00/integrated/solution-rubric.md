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

**Option A.** Use one application deployment and one durable relational store for metadata, grants and document bytes. The application accepts a publish request, stores the document and grant in one transaction, and reports success after commit. For a download it authenticates the employee, checks the grant against the authoritative store, then streams the document through the application. Revocation removes the grant in the authoritative store and acknowledges after commit. The service must perform a fresh check on each download. A cache of allow decisions or an old grant snapshot would violate the post-revocation rule.

**Option B.** Put PDF bytes in private object storage and keep grants in an authoritative database. The app checks the grant on every download and streams the object. This adds a storage call and an extra failure case. Upload objects before making them visible through committed metadata, and clean up objects left behind by failed metadata writes. Publish and download can scale their storage needs independently. A direct download link that stays usable after revocation would miss the stated rule.

Choose A while the low traffic and host-replacement assumption hold. Peak document payload is at most about 1.67 MiB/s if 50 maximum-size downloads arrive within one minute and bytes are evenly served over that minute. Use a burst test to find the actual transfer and database saturation limits. Check post-revocation requests under concurrent read traffic and simulate loss of the host. If serving through one host loss becomes mandatory, validate redundant app capacity and a state path that can still authorize requests. Moving PDFs to object storage alone leaves the app as a required dependency.

## Self-evaluation

Score each criterion from 0 to 2. Award 2 for clear reasoning with testable evidence, 1 for a correct but incomplete argument, and 0 for missing or contradictory reasoning.

| Criterion | Evidence for full credit |
|---|---|
| Scope | Prioritized actors and use cases, two measurable criteria, and named assumptions and exclusions. |
| Traceability | Clear request paths and a mechanism that enforces post-confirmation revocation. |
| Trade-off | Two feasible candidates with distinct costs and explicit effects on one required property. |
| Verification | One decision-changing observation, a matching test and a clear rule for reconsidering the choice. |

A proposed design can earn full credit with a different baseline if it honors the access constraint and explains its costs. M00-S1 uses both M00-L02 outcomes. Readiness is assessed in the [M00-L01 companion](../assessments/M00-L01.md).
