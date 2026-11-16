---
id: M11-EX1-solution
status: draft
---

# Reference design — disjoint allocation versus rolling admission

## 1. Name the invariants before choosing coordination

**ID invariant:** for each ID in the declared namespace and lifetime, there is at most one allocation to an actual object. An allocator may waste sequence values; the invariant is not “no gaps.” Range-grant ID and epoch must survive operator retry, and no uncertain portion can be granted to a different owner while the old holder may issue it. If IDs are user-facing security tokens, numerical uniqueness **does not** imply unguessability.

**Quota invariant:** for each `(tenant_id, operation_class, policy_revision)`, at most three **distinct new original operations** may be durably admitted in any rolling interval `(t−6,t]` across the global authority. Accepted retries with identical `original_id` and payload consume no new quota. Changed payload under the same ID is rejected as conflict. Denied attempts are counted separately and never applied asynchronously unless the API declares them queued. Client response loss must be reconciled against a durable receipt rather than recharged.

The quota invariant depends on *when* admissions happen, not merely total numbered tokens issued over the lifetime of a service. An ID range can be consumed at arbitrary times without a per-time fairness rule, while a leased quota grant needs a window/epoch budget and either exact admission-time coordination or a restricted, proven nonoverlap policy for the same rolling horizon.

## 2. Concrete independent authorities

```text
Region A gateway ----> ID issuer A (fenced epoch, disjoint range)
Region B gateway ----> ID issuer B (fenced epoch, disjoint range)
                    \-- central range allocator / durable grant ledger

Both region gateways --> global quota owner by tenant partition
                      --> atomic (original receipt lookup + rolling admission + durable intent)
                      --> report worker, idempotent by operation ID
```

**ID allocator model:** `grant_id, namespace, start, end, owner, epoch, committed`; issuer tracks `next_unissued` durably or reserves/consumes an entire range so after a crash it can safely skip uncertain values. Only the grant owner can issue its disjoint reserved range under an accepted epoch. Allocation of a range and publication of ownership require one consistent authority. If Region A held 4000–4999 and definitely handed out up to 4029, do **not** reassign 4030–4999 to B merely because A stopped responding: it may resume. Safest initial policy is permanently burn unproven remainder and issue B a **different** range, e.g. 5000–5999, at the cost of gaps and capacity. A more complex protocol can reclaim only if old issuance is fenced by a shared authority **at each issuance** or its lease guarantee is valid for the precise failure period; such coordination may defeat offline low-latency issuance. On reboot, issuer must not reissue IDs it might have previously returned.

**Quota authority model:** `tenant, operation_class, policy_revision, original_id, canonical_input, admission_time, status, intent_id`. In one appropriate serializable decision/transaction boundary, check existing receipt first; for a new original count previously **accepted** events in `(t−6,t]`, admit only if fewer than 3, then atomically charge and persist a recoverable report intent. Use an authoritative clock policy. Externally visible accepted work must be durable and runnable or recoverable—not an orphaned limiter token. A Redis script alone cannot atomically commit an unrelated SQL transaction and queue message.

## 3. Failure table

| Fault | IDs | Quota |
| --- | --- | --- |
| A loses connection | A may use only its nonoverlapping, valid fenced grant under the chosen contract; B receives distinct ranges | A must fail closed for strict global rolling limit unless its disjoint, time-bounded quota grant proves safety |
| Old A resumes after B takeover | Shared owner/fence rejects stale issuance; or no reissue of A's uncertain numbers | Old grant must be fenced at actual admission or permanently counted/reserved for its window; do not double-spend |
| API reply lost | Client retries stable allocation identity; a committed allocation receipt returns same ID | Client retries same original ID; receipt lookup returns existing admission without double charge |
| Store loses its latest acknowledged record | Can reuse an ID unless grant/revision/receipt survived at required durability level | Can overshoot quota or lose accepted report intent unless acceptance boundary is durable |
| Gateway uses local cached counter | Cannot safely allocate identical next counter values on multiple gateways | Both gateways may admit 3 each; the global 3-in-6-sec invariant is violated |

A bounded quota escrow design may reserve a fixed number of nonoverlapping permits for a known accounting interval, but for an **exact rolling** six-second window it must specify the timing and transfer mechanism proving that spending permits cannot violate **any** overlapping six-second interval. A simplistic “three per fixed window” lease fails at the window boundary (six admits around t=6). If that proof is too costly, choose a serializing authority with fail-closed partition behavior, or honestly weaken the product promise to approximate quotas.

## 4. Compare options

**IDs:** A central durable counter is conceptually simple but adds synchronous dependence and a throughput bottleneck. Disjoint ranges amortize coordination and tolerate a disconnected issuer at the price of holes, irrevocable uncertain ranges and stricter epoch/failover discipline. Large random IDs with an authoritative uniqueness guard avoid centralized number allocation, but the probability of collision is nonzero and the guard/retry semantics must be specified; random bytes do not establish monotonic order.

**Quota:** A per-tenant atomic serialized sliding log gives exact rolling semantics and simpler reasoning but adds latency and can fail closed under partition. Quota escrow lowers per-admission remote calls but complicates rolling-window guarantees, fairness and reclamation; a strict design may strand unused permits. Local counters are available but approximate; they must advertise error bounds and fail policy rather than claiming exact global compliance.

## 5. User-visible evidence and falsification

Under 1,000 originals, only 760 received correct accepted-work responses in the 200 ms limit: **accepted-work success = 760/1,000 = 76%**. A correct policy 429 is a *successful rate-limit decision* only if the metric contract explicitly evaluates correct classification; it is **not** a successfully admitted report. In a separate decision-response SLI, 760 timely acceptance receipts plus 140 timely correct 429 responses yield 900/1,000 = 90%, *assuming* those 140 actually arrived by the decision deadline. That response timing must be recorded, not inferred solely from a “rejected” count. Timeouts, failures, lateness and overload shedding remain in the original-attempt denominator.

Test (1) two gateways concurrently spending one tenant's last slot; (2) a fixed-window boundary burst; (3) duplicate original ID after lost response; (4) same ID with different payload; (5) old issuer resumes after region failover; (6) storage crash after grant/receipt acknowledgment before replication or fsync; (7) quota decision commit followed by report-intent crash; (8) clock rollback or cross-region skew; (9) allocation throughput with one hot issuer; (10) availability when the global quota owner partitions. Inspect durable grant and admission ledgers, not just gateway local counters.

## Rubric (12 points)

| Dimension | Pts | Full-credit evidence |
| --- | ---: | --- |
| Distinct invariants | 3 | Lifetime non-reuse versus exact rolling admission; stable retry receipts, key scope and clocks |
| Failure-safe architecture | 4 | Disjoint ID grants with old-owner fencing/non-reissue; serialized quota with coherent intent and strict fail policy |
| Alternatives and cost | 3 | Two defensible options each domain, justified trade-offs and rolling-window escrow warning |
| Outcomes and tests | 2 | Original-operation numerator/denominator, separate decision metric and six falsifying tests |

Full credit may use equivalent designs only if safety arguments cover the precise declared failure and timing boundaries. Reject ambiguous use of “exactly once,” “globally unique” or “highly available” without a corresponding evidence model.
