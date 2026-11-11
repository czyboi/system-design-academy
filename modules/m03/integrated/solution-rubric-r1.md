---
id: M03-EX1-solution
status: draft
---

# Reference design and rubric

## Ownership and deployment

Keep items, approval and publication in the catalogue's transactional boundary. Give the renderer its own deployment and CPU capacity. It takes immutable input for an item version, owns rendering progress, and returns an output reference with the work ID and version. Keep current version, approval and public pointer on the same authoritative item row. Publish with one guarded row update that sets the pointer only if the row still has the rendered version and is approved. If an edit or revocation commits first, the guard rejects the old result. If publishing commits first, the edit or revocation clears the pointer in the same row update that changes version or approval. This preserves the invariant in both orders. Read the authoritative publication state when immediate revocation is required. A separate check followed by an unconditional write can race even inside a transaction. PostgreSQL 18 Read Committed is one implementation where a concurrent UPDATE rechecks the same target row after the competing update commits. [PostgreSQL 18 §13.2.1](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED)

A modular application with isolated worker capacity is viable if it meets both targets without separate release or data ownership. An entity-per-service split adds remote dependencies to metadata and moves a publication invariant across interfaces. For either viable option, compare metadata p99, CPU saturation and preview completion lag under peak demand and one unavailable worker. Confirm the renderer's concurrency cap still meets the two-minute target.

## Public and internal contracts

| Contract | Behavior |
| --- | --- |
| `POST /items/{item}/previews` | Authorize the editor, check the requested item version, and atomically persist the pending job and an idempotency record. Return `202 Accepted` with a link to the job status. Scope the key to the editor and operation, compare the item/version/options, and return the existing job for an identical retry within the documented window. Reject mismatched reuse. |
| `GET /preview-jobs/{id}` | Authorize access and return a private representation with `pending`, `ready`, `superseded` or `failed`. Expose a result link only when eligible. Add optional fields and preserve meanings that both client versions rely on. |
| `StartRender(work_id, item_version, input_ref, options)` | The dispatcher's stub marshals the operation. The transport carries it to the selected renderer, where the server stub decodes and dispatches it. The renderer atomically inserts a durable record under a unique work ID and returns that ID through the reverse path. All eligible endpoints share that acceptance store. Concurrent attempts with the same ID and matching immutable inputs return the existing record. A reused ID with changed inputs is rejected. An accept reply confirms a work record, while a later state change confirms completion. |

The catalogue dispatcher can rediscover and resume pending dispatch after a process restart. The renderer resumes accepted work from its durable state. Define deduplication retention to cover the full retry and recovery window, including dispatch across restarts. When a result is superseded, the catalogue can show that state and an editor can request a preview for the new version.

## Discovery and failure trace

For one catalogue caller, let its dispatcher select from a watched, locally cached renderer pool. Use registration, readiness, removal or expiry, and a maximum age for using the list during registry failure. An intermediary could instead centralize selection for several caller stacks. It adds another dependency to size and monitor. The retry owner and the discovery owner may be different components, but their deadline and attempt contracts must agree.

1. At 0 ms the dispatcher calls a renderer listed as ready. If the stopped instance never accepted the call, the alternate can create the job. If the first renderer accepted the work and its reply was lost, the alternate must reuse the committed record. In either case an unanswered attempt can consume the full 120 ms limit. The caller treats the outcome as unknown until it has an authoritative result.
2. Exclude the suspect endpoint for this retry. Wait at most 30 ms, then call a distinct eligible endpoint with the same work ID. At 150 ms there are 150 ms left. A 60 ms response arrives at 210 ms, leaving 90 ms. The receiver returns the existing record if acceptance happened on the first attempt.
3. The dispatcher owns a maximum of two attempts in this cycle. Disable independent retries in the intermediary or coordinate them within that cap. Bound in-flight dispatches. If discovery is unavailable and the cache exceeds its allowed age, or the cycle ends without a definitive reply, keep the durable job pending for bounded later dispatch with the same ID. Surface stalled jobs and apply the overall preview expiry policy.

The durable record covers acceptance of the logical job. If processing restarts, make the render output and completion handler repeat-safe for the same work ID. [AWS Builders' Library, making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

## Self-evaluation

Award 2 for complete reasoning, 1 for a correct but incomplete argument and 0 for a missing or contradictory argument.

| Criterion | Evidence for full credit |
| --- | --- |
| Boundary and invariant | Compare alternatives using the measured CPU constraint and the delay allowance. Name the state owner and show how the publication guard serializes with concurrent version changes and approval revocations. |
| Interface trace | Specify resource and operation semantics, stub path, private status, compatibility and durable duplicate handling. |
| Failure policy | Trace elapsed and remaining time, assign discovery and retry ownership, and preserve the same operation identity after a lost reply. |
| Verification | Propose load and worker-loss tests, including how to validate the maximum endpoint age and in-flight cap. Exercise both orderings of a render completion racing with an edit or revocation. |

Other choices earn credit if they protect the current-version invariant and bound work within the stated failure policies. A status check alone cannot make an ambiguous retry safe unless the status contract can resolve the prior effect.
