---
id: M03-EX1-solution
status: draft
---

# Reference design and rubric

## Ownership and deployment

Keep items, approval and publication in the catalogue's transactional boundary. Give the renderer its own deployment and CPU capacity. It takes immutable input for an item version, owns rendering progress, and returns an output reference with the work ID and version. Keep current version, approved version and public pointer on the same authoritative item row. An approval records the reviewed version only if it is still current. Publish with one guarded row update that requires both versions to equal the rendered version. An edit advances the current version and clears the approval and pointer in the same update. A revocation clears the approval and pointer together. If either commits before publication, the guard rejects the result. If publication commits first, the edit or revocation clears the pointer when it commits. This preserves the invariant in both orders. When immediate revocation is required, keep preview objects private and gate each public fetch on the authoritative pointer. Avoid a public object URL or cached authorization that can outlive revocation. A separate check followed by an unconditional write can race even inside a transaction. PostgreSQL 18 Read Committed is one implementation where a concurrent UPDATE rechecks the same target row after the competing update commits. [PostgreSQL 18 §13.2.1](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED)

A modular application with isolated worker capacity is viable if it meets both targets without separate release or data ownership. An entity-per-service split adds remote dependencies to metadata and moves a publication invariant across interfaces. For either viable option, compare metadata p99, CPU saturation and preview completion lag under peak demand and one unavailable worker. Confirm the renderer's concurrency cap still meets the two-minute target.

## Public and internal contracts

| Contract | Behavior |
| --- | --- |
| `POST /items/{item}/previews` | Authorize the editor to access the item and scope the key to that editor and operation. Within the documented window, an identical retry returns the existing job link even if the item has since changed. Reject reuse with a different item, version or options. For a new key, check the requested version and atomically persist the pending job and its idempotency record. Return `202 Accepted` with a link to the job status. |
| `GET /preview-jobs/{id}` | Authorize access and return a private representation with `pending`, `ready`, `superseded` or `failed`. Expose a result link only when eligible. Add optional fields and preserve meanings that both client versions rely on. |
| `StartRender(work_id, item_version, input_ref, options)` | The dispatcher's stub marshals the operation. The transport carries it to the selected renderer, where the server stub decodes and dispatches it. The renderer atomically inserts a durable record under a unique work ID and returns that ID through the reverse path. All eligible endpoints share that acceptance store. Concurrent attempts with the same ID and matching immutable inputs return the existing record. A reused ID with changed inputs is rejected. An accept reply confirms a work record, while a later state change confirms completion. |

The catalogue dispatcher can rediscover and resume pending dispatch after a process restart. The renderer resumes accepted work from its durable state. Define deduplication retention to cover the full retry and recovery window, including dispatch across restarts. When a result is superseded, the catalogue can show that state and an editor can request a preview for the new version.

## Discovery and failure trace

For one catalogue caller, let its dispatcher select from a watched, locally cached renderer pool. Use registration, readiness, removal or expiry, and a maximum age for using the list during registry failure. An intermediary could instead centralize selection for several caller stacks. It adds another dependency to size and monitor. The retry owner and the discovery owner may be different components, but their deadline and attempt contracts must agree.

1. At 0 ms the dispatcher calls a renderer listed as ready. If the stopped instance never accepted the call, the alternate can create the job. If the first renderer accepted the work and its reply was lost, the alternate must reuse the committed record. In either case an unanswered attempt can consume the full 120 ms limit. The caller treats the outcome as unknown until it has an authoritative result.
2. Exclude the suspect endpoint for this retry. Wait at most 30 ms, then call a distinct eligible endpoint with the same work ID. At 150 ms there are 150 ms left. A 60 ms response arrives at 210 ms, leaving 90 ms. The receiver returns the existing record if acceptance happened on the first attempt.
3. The dispatcher owns a maximum of two attempts in this cycle. Disable independent retries in the intermediary or coordinate them within that cap. As an initial load-test setting, cap each dispatcher replica at 16 in-flight StartRender calls, including retries. A full cap leaves new work in the durable queue. During registry failure, use an eligible cached list for at most five seconds after the last successful refresh, then pause new sends until a fresh list arrives. On an expired list or a cycle without a definitive reply, keep the durable job pending and resume under the same work ID with backoff while its two-minute preview window remains. Surface stalled or expired jobs. Tune the limits using renderer capacity, retry rate and preview lag.

The durable record covers acceptance of the logical job. If processing restarts, make the render output and completion handler repeat-safe for the same work ID. [AWS Builders' Library, making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

## Self-evaluation

Score each criterion independently. Award 2 for the evidence in the table, 1 for a plausible but incomplete argument, and 0 for missing or contradictory reasoning. A proposal meets the design requirements only if it preserves publication eligibility under races, prevents duplicate logical work within the declared retry and recovery window, and bounds work during overload and discovery failure. A design that meets these requirements still needs the verification evidence for full credit.

| Criterion | Evidence for full credit |
| --- | --- |
| Boundary and invariant | Compare alternatives using the scenario’s CPU constraint and the delay allowance. Name the state owner and show how the publication guard serializes with concurrent version changes and approval revocations. |
| Interface trace | Specify resource and operation semantics, stub path, private status, compatibility and durable duplicate handling. |
| Failure policy | Trace elapsed and remaining time, justify discovery ownership, and give the retry owner a total attempt cap and a stable operation identity. State an in-flight cap and where work waits at saturation. Bound cache age during registry failure and specify how to defer, resume or expire work. |
| Verification | At the modeled peak, stop a worker and interrupt discovery. Check metadata p99 at or below 200 ms, queue age, retry rate, and the selected endpoint-age and in-flight caps. State the drill duration. Follow every preview accepted during the drill from durable acceptance through its two-minute deadline, and count expired, failed or late jobs as misses. Drop a reply after durable acceptance and check for one logical job. Force both orderings of publication racing an edit or revocation. After approving v1 and editing to v2, verify that v2 stays private until explicitly approved. Equivalent tests earn credit when they demonstrate the same constraints. |

Other choices earn credit if they protect the current-version invariant and bound work within the stated failure policies. An authoritative accepted record resolves whether the renderer accepted the work ID. An absent or pending record leaves room for an earlier attempt to apply. Preserve the covered work ID or require authoritative terminal evidence of non-application before assigning a fresh one.
