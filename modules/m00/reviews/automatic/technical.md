# M00 technical and provenance synthesis

Round 0, 2026-11-15. Scope covers the [integrated brief](../../integrated/brief.md), [reference solution and rubric](../../integrated/solution-rubric.md), [decision summary](../../integrated/decision-summary.md), [claim evidence](../../integrated/evidence.md) and their connections to the accepted lesson packages. This synthesis reuses the Stage A results for [M00-L01](lessons/M00-L01/technical.md) and [M00-L02](lessons/M00-L02/technical.md).

## Finding disposition

| Finding | Disposition | Verified correction |
|---|---|---|
| M00-INT-T1 | resolved | In [Reference brief, Option B](../../integrated/solution-rubric.md#reference-brief), a timeout leads to reconciliation by upload identifier. Cleanup requires a terminal publication attempt and confirmation from authoritative metadata that no committed document references the object. This addresses the ambiguous metadata commit in the archived report. The RFC supports the ambiguous-response premise, while the reconciliation and deletion rules are part of the example design. [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2). |

## Cross-lesson and integrated checks

- The transaction decision in the [summary](../../integrated/decision-summary.md) preserves the two failure timings taught in M00-L01. Option B applies the same distinction to publishing, where a lost response leaves commit status to reconcile. This creates a transfer from the readiness trace to a design decision.
- The brief establishes a post-confirmation authorization-check boundary. The solution checks the current grant before releasing bytes, confirms the revoke after the authoritative change, orders grant changes and checks on the same grant, and allows a subsequent regrant. The client trace tests a repeated URL after confirmation. The example distinguishes private object storage from direct download links that remain usable and uses the compliant-cache protection from M00-L02. [Herlihy and Wing, §2.2](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf#page=7) · [RFC 9111 §5.2.2.5](https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2.2.5).
- Peak payload is 50 × 2 MiB = 100 MiB, about 1.67 MiB/s averaged over the minute. Burst testing measures shorter intervals. The five-minute variant at 50 downloads per minute has 250 original authorized attempts, and 238 is the smallest whole number meeting the 95% target. The four-second client-send-to-complete-body criterion counts rejected, failed, timed-out and late attempts against the full offered count. Survivor capacity, latency of completed requests and revoked-link probes are separate checks. The rubric makes the client population explicit. Like M00-L02, the variant requires a reachable state path as well as a surviving application path. [Google SRE Workbook, Implementing SLOs](https://sre.google/workbook/implementing-slos/#what-to-measure-using-slis).
- The summary's test-and-revise row is consistent with the lesson and reference solution. Selecting the simpler starting option depends on office scope, estimated demand and tolerance of a host interruption. The host-loss target changes the topology decision, and the solution calls for a test before claiming the design meets it. [Google SRE Workbook, Design Process](https://sre.google/workbook/non-abstract-design/#design-process).

## Provenance

The integrated evidence distinguishes the external consistency, caching and measurement claims from the hypothetical document-sharing workload and application policies. The linked primary passages support those bounded claims. The brief, reference alternatives, numbers and scoring criteria are original Academy material. The package consists of Markdown, YAML and local evidence, with citations to external sources and zero embedded third-party assets.

**Verdict: ready-for-human-review.**
