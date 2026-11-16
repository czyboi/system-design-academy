---
id: M11-decisions
status: draft
---

# Choose the invariant before the product

## Work the cross-domain failure comparison

A public object identifier must not be assigned to two distinct objects in its defined namespace/lifetime. A strict global limiter must not admit more than a configured number of distinct originals during **any rolling window**, not just per gateway or per fixed bucket. Both use authority, but their **time semantics differ**. Disjoint ID ranges can remain unique with gaps and no full-time central counter, while quota grants must bound *spending time* as well as total quantity. Treat a resumed old owner as capable of acting until the durable acceptance resource rejects its epoch or the never-reissued allocation cannot conflict.

Use one committed identity per original operation, separate security/authorization from performance caches, and report accepted-work success independently from correctly denied attempts. The full comparison and failure trace are in [M11-EX1](brief.md) and its [reference](solution-rubric.md).

## Domain decision table

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Offline file edits and simultaneous collaboration differ | Versioned object sync vs operation-based editor | Immutable file revisions with conflicts vs ordered/convergent document operations | Match update granularity | Conflict UX or operation metadata | Divergent offline edits | Treating whole files as shared text ops | [M11-L01](../lessons/M11-L01.md) |
| Offline messaging and image publication | Durable message receipt and staged media version | Recipient progress plus guarded publish/visibility | Recoverable delivery | Retention, privacy, fan-out | Lost response or stale authorization | Assuming socket delivery means durable receipt | [M11-L02](../lessons/M11-L02.md) |
| Candidates and graph paths use stale projections | Authorized retrieval followed by scoring | Constrain eligible graph, then rank | Efficient discovery | Feature lag, expensive joins | Stale permission exposed | Ranking before permissions | [M11-L03](../lessons/M11-L03.md) |
| Many regions serve mutable protected content | CDN with validated object versions and data-owner policy | Origin/edge routing, guarded invalidation and region failover | Edge latency and origin shielding | Purge propagation and egress | Old fill wins after purge | Claiming edge cache is authorization authority | [M11-L04](../lessons/M11-L04.md) |
| Need globally unique IDs without gaps requirement | Fenced disjoint range leasing | Grant exclusive, durable namespaces/ranges | Local fast issue | Wasted ranges and epoch control | Old issuer reuses reserved ID | Sequential secrecy or cross-region monotonicity required | [M11-L05](../lessons/M11-L05.md) |
| Strict global per-tenant rolling quota | Serializing sliding-window authority | Atomic original receipt, count and durable intent | Exact quota semantics | Shared dependency, lower availability under partition | Two gateways admit beyond cap | Approximate global cap is adequate and latency dominates | [M11-L06](../lessons/M11-L06.md) |
| Shared turn or order-book sequencing | Per-game or per-instrument authoritative reducer | Canonical command order and fenced event log | Deterministic replay | Hot-owner serialization | Conflicting fills/turns | Cross-instrument risk left uncoordinated | [M11-L07](../lessons/M11-L07.md) |
| Unreachable cycles and pause spikes | Tracing stop-the-world or concurrent mark | Root reachability with barriers for mutation | Reclaims cycles | Pause versus CPU/headroom | Missed deadline or runaway live set | Replacing cache eviction policy with GC | [M11-L08](../lessons/M11-L08.md) |
| Cached state may be discarded, committed value cannot | Durable KV or disposable cache | Declared sync/replay vs refill/TTL/eviction | Appropriate availability/cost | Replica lag or origin stampede | Lost acked write or stale refill | Treating volatile cache as database | [M11-L09](../lessons/M11-L09.md) |

## Synthesis outcome

**M11-S1:** compare an ID-service invariant and an API-quota invariant; defend distinct coordination and failure policies. [M11-L05](../lessons/M11-L05.md) and [M11-L06](../lessons/M11-L06.md) teach the mechanisms; [M11-EX1](brief.md) assesses the transfer. The table links adjacent domain decisions but does not replace their own companion assessments.
