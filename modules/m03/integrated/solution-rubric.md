---
id: M03-EX1-solution
status: draft
---

# Reference design and rubric

## Ownership and deployment

Keep items, approval and publication in the catalogue's transactional boundary. Give the renderer its own deployment and CPU capacity. It takes immutable input for an item version, owns rendering progress, and returns an output reference with the work ID and version. The catalogue checks the current version and approval in the same transaction that updates the public pointer. A late result for a superseded version can finish rendering and cannot change that pointer.

A modular application with isolated worker capacity is viable if it meets both targets without separate release or data ownership. An entity-per-service split adds remote dependencies to metadata and moves a publication invariant across interfaces. For either viable option, compare metadata p99, CPU saturation and preview completion lag under peak demand and one unavailable worker. Confirm the renderer's concurrency cap still meets the two-minute target.

## Public and internal contracts

| Contract | Behavior |
| --- | --- |
| `POST /items/{item}/previews` | Authorize the editor, check the requested item version, and atomically persist the pending job and an idempotency record. Return `202 Accepted` with a link to the job status. Scope the key to the editor and operation, compare the item/version/options, and return the existing job for an identical retry within the documented window. Reject mismatched reuse. |
| `GET /preview-jobs/{id}` | Authorize access and return a private representation with `pending`, `ready`, `superseded` or `failed`. Expose a result link only when eligible. Add optional fields and preserve meanings that both client versions rely on. |
| `StartRender(work_id, item_version, input_ref, options)` | The dispatcher's stub marshals the operation. The transport carries it to the selected renderer, where the server stub decodes and dispatches it. The renderer records acceptance by work ID durably and returns that ID through the reverse path. Any eligible endpoint can resolve that same ID using the renderer owner's shared durable state. An accept reply confirms a work record, while a later state change confirms completion. |

The catalogue dispatcher can rediscover and resume pending dispatch after a process restart. The renderer resumes accepted work from its durable state. Define deduplication retention to cover the full retry and recovery window, including dispatch across restarts. When a result is superseded, the catalogue can show that state and an editor can request a preview for the new version.

## Discovery and failure trace

For one catalogue caller, let its dispatcher select from a watched, locally cached renderer pool. Use registration, readiness, removal or expiry, and a maximum age for using the list during registry failure. An intermediary could instead centralize selection for several caller stacks. It adds another dependency to size and monitor. The retry owner and the discovery owner may be different components, but their deadline and attempt contracts must agree.

1. At 0 ms the dispatcher calls a renderer listed as ready. Its attempt reaches the 120 ms limit without a reply. The renderer may have committed the work ID before the loss. Treat the result as unknown.
2. Exclude the suspect endpoint for this retry. Wait at most 30 ms, then call a distinct eligible endpoint with the same work ID. At 150 ms there are 150 ms left. A 60 ms response arrives at 210 ms, leaving 90 ms. The receiver returns the existing record if acceptance happened on the first attempt.
3. The dispatcher owns a maximum of two attempts in this cycle. Disable independent retries in the intermediary or coordinate them within that cap. Bound in-flight dispatches. If discovery is unavailable and the cache exceeds its allowed age, or the cycle ends without a definitive reply, keep the durable job pending for bounded later dispatch with the same ID. Surface stalled jobs and apply the overall preview expiry policy.

## Self-evaluation

Award 2 for complete reasoning, 1 for a correct but incomplete argument and 0 for a missing or contradictory argument.

| Criterion | Evidence for full credit |
| --- | --- |
| Boundary and invariant | Compare alternatives using the measured CPU constraint and the delay allowance. Name the state owner and atomic publication check. |
| Interface trace | Specify resource and operation semantics, stub path, private status, compatibility and durable duplicate handling. |
| Failure policy | Trace elapsed and remaining time, assign discovery and retry ownership, and preserve the same operation identity after a lost reply. |
| Verification | Propose observations for steady load, worker loss, stale discovery and preview lag. |

Other choices earn credit if they protect the current-version invariant and bound work within the stated failure policies. A status check alone cannot make an ambiguous retry safe unless the status contract can resolve the prior effect.
