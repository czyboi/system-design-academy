# M05 module synthesis pedagogy and coverage review

Reviewed the integrated package at `7f8154b` against the [approved M05 synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-integrated-package-plan), the canonical integration spec and the accepted per-lesson Stage A pedagogy reports. This review covers cross-lesson progression, the integrated exercise and rubric, and the topic and outcome reconciliation.

## Synthesis and assessment

M05-L01 supplies key-value and document access and revocation semantics. M05-L02 adds range locality, retained versions and graph traversal. M05-L03 connects model selection to operation-specific guarantees and coordinated invariants. The integrated exercise applies those lessons to sessions, product documents, telemetry and relationships. Its reference compares an alternative for each path, identifies the authority or derived representation, and supplies two product or test questions per choice.

The product drill counts 196 of 200 original commits within 15 seconds, yielding 98% against a 99% target. The relationship drill counts 91 of 100 original requests complete and correct within 200 ms, yielding 91% against a 95% target. Both use ten-minute arrival or commit cohorts. Partial, late, timed-out and unavailable outcomes remain in the applicable denominators. The rubric asks for both calculations and failure and repair tests.

The sample design traces a post-confirmation stale session cache, an atomic product edit with compatibility during rollout, same-timestamp telemetry events with distinct IDs, and an explicitly partial graph result. These are applications of accepted lesson mechanisms rather than an additional claim to assess all lesson outcomes. The one-team operating constraint informs the comparison of a shared stack with additional specialized stores.

## Coverage and outcome reconciliation

The topic ledger maps the assigned M05 topics and workload analogues to the same teaching sections reviewed in Stage A. The outcome portfolio retains the two separate outcomes and companion assessment items for each lesson. It maps M05-S1 to M05-L01-LO2, M05-L02-LO2 and M05-L03-LO2 and assigns M05-EX1 to that synthesis outcome, matching the approved plan. The decision table supplies the required trigger, option, mechanism, benefit, cost, failure signal, avoidance condition and lesson reference.

## Findings

No open module-synthesis pedagogical or assigned-topic coverage findings.

**Verdict: ready-for-human-review.** This verdict covers module synthesis pedagogy and curriculum coverage.

## Round 1 targeted synthesis re-review

Reviewed the revised brief and reference/rubric at `b188d79`. The product drill now supplies a fixed A/B/C fixture, complete ordered expected results, one-second probes through the 15-second deadline and same-snapshot revision evidence. The reference and rubric use that measurement and preserve the 196/200 cohort. The session reference distinguishes a post-acknowledgement revoked-state denial from fail-closed authority unavailability. The revised telemetry reference describes stable correction identities, a per-event revision authority, event-relative retention and latest-selection completeness.

| ID | Severity | Status | Location and learner impact | Suggested correction |
| --- | --- | --- | --- | --- |
| M05-SYN-P1 | major | open | [Brief, M05-EX1 items 2–3](../../integrated/brief.md#m05-ex1) asks learners to trace two events sharing a timestamp and propose tests for version retention and lost state. The [revised rubric](../../integrated/solution-rubric.md#rubric) additionally requires correction identity, latest selection, ambiguous retries, concurrent corrections and retention boundaries for full credit, while the brief does not specify that corrections can race or be retried after an ambiguous reply. A learner can answer the stated scenario yet miss substantial full-credit conditions. The [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-integrated-package-plan) requires a usable reference solution and self-evaluation of the four stated patterns. | State in the telemetry scenario that corrections can occur concurrently and their replies can be lost, then explicitly request identity, latest-selection and 30-day boundary traces or tests. Keep alternative mechanisms acceptable if they satisfy the stated contract. |

The 200-commit and 100-request cohorts and their 98% and 91% scores remain intact. The outcome portfolio and previously accepted topic dispositions are unchanged.

**Current verdict: revise.** This verdict covers targeted module synthesis pedagogy and curriculum coverage.

## Round 2 targeted synthesis re-review

Reviewed the revised brief and reference/rubric at `55afdc4`. The brief now explicitly asks for simultaneous corrections, a lost correction reply, audit reads at the 30-day boundary and a delayed correction or retry racing cleanup. The revised sample traces both competing conditional mutations and the closed-marker cleanup race. The original product and relationship drill cohorts and scoring remain intact.

| ID | Severity | Status | Evidence or remaining issue |
| --- | --- | --- | --- |
| M05-SYN-P1 | major | resolved | [Brief, M05-EX1 items 2–3](../../integrated/brief.md#m05-ex1) now requests the concurrent, ambiguous-retry and audit-boundary cases assessed in the [reference and rubric](../../integrated/solution-rubric.md#rubric). The [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-integrated-package-plan) requires self-evaluation of the four patterns. |
| M05-SYN-P2 | major | open | [Brief, M05-EX1 item 1](../../integrated/brief.md#m05-ex1) asks the learner to choose an access path and compare alternatives. The [Guarantees and failure traces rubric](../../integrated/solution-rubric.md#rubric) awards full credit only for binding each correction payload, receipt, identity and revision in **one authoritative event row** and requires a closed marker. That imposes the reference Bigtable representation on other designs, although the same artifact explicitly accepts alternative models. A relational transactional implementation or another equivalent design can preserve the requested audit, latest and cleanup guarantees without that physical representation. Grade the atomic identity, revision, retention and cleanup behavior by its observable guarantees, with the single-row and terminal-marker design as one acceptable implementation. |

**Current verdict: revise.** This verdict covers targeted module synthesis pedagogy and curriculum coverage.

## Owner-directed targeted follow-up

Reviewed the owner-authorized rubric correction at `0583ebb` after the two automatic correction rounds. The full-credit criterion now evaluates atomic correction acceptance, durable outcomes for identity and revision, complete or explicitly unavailable audit/latest reads, event-relative retention and protection against expired-data recreation. It permits equivalent representations that satisfy those observable guarantees. The single-row design remains a reference example.

| Finding | Status | Evidence |
| --- | --- | --- |
| M05-SYN-P2 | resolved | [Reference solution and rubric, Guarantees and failure traces](../../integrated/solution-rubric.md#rubric) and the [approved M05 synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-integrated-package-plan), which asks learners to compare data models. |

**Current verdict: ready-for-human-review.** This verdict covers the owner-directed targeted pedagogy and curriculum coverage follow-up.

## PR #77 targeted synthesis re-review

Reviewed the changed decision summary, brief, reference/rubric and outcome portfolio at `49210a1`. **Work a storage-to-guarantee decision** traces a parcel ID lookup, ordered tracking history and one-use pickup claim with a durable input-bound receipt. It compares access and operational criteria while keeping the strict claim at a coordinated authority. The M05-S1 portfolio names this worked section alongside the decision table.

The revised product drill permits either a shared database snapshot or reproducible correlation to the actual search-index serving view. The reference gives a concrete generation and per-required-shard evidence path for a separate index, while retaining complete ordered A, C results and proof of the committed revision by the 15-second deadline. The rubric grades the serving-view proof rather than requiring a database-only mechanism. The 200-commit cohort and 98% result remain intact. This targeted review found no new pedagogical or coverage issue against the [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-integrated-package-plan).

**Current verdict: ready-for-human-review.** This verdict covers the PR #77 targeted module synthesis pedagogy re-review.
