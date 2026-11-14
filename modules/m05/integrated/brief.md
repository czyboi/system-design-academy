---
id: M05-EX1
status: draft
outcomes: [M05-S1]
---

# Pick storage for four access patterns

A connected marketplace offers token-based sessions, product pages and browse, device telemetry, and seller relationship suggestions. Its releases have one operations team. You may use more than one store, but each authority and derived representation needs an owner and recovery plan.

| Operation | Workload and invariant |
| --- | --- |
| Validate a session | Exact lookup by token. A validation whose authoritative check starts after acknowledged revocation must deny that token. An earlier overlapping check may succeed. Define what happens when the authority is unreachable and a cache still returns active. |
| Browse or edit a product | Browse active products by category and price, and fetch a product aggregate by ID. A price and its bounded variant display labels must change together. Browse may lag by 15 seconds under its target. Old clients still read the existing price field during the next release. |
| Read device telemetry | Read the last 30 minutes for one device. One device accounts for 40% of writes, and independent events can share a timestamp. Retain the original plus every accepted correction until at least 30 days after the original event time. The dashboard uses only the latest accepted correction. |
| Suggest relationships | Return unique second-hop sellers, excluding the seed and directly followed sellers. A supernode may need a remote lookup with tens of thousands of edges. The API must identify a partial result. |

Use two hypothetical drills. For the product freshness drill, track 200 original qualifying product commits in one ten-minute window. Each commit has an isolated fixed fixture in category `boots` with active products A at 60, target B at 72 and C at 75. The edit atomically changes B to 84 and updates its labels. Browse selects active boots with price below 80, ordered by price then product ID. The initial complete result is A, B, C and the expected result after the edit is A, C. Freeze all other changes to that fixture until its probe ends.

From each commit through its 15-second deadline, probe at one-second intervals, including both endpoints. Each probe must return the complete ordered browse result through the actual browse index and route, and the target's canonical revision through instrumentation reading the same database snapshot as that browse result. The fixture fits below the page limit. If a design uses pagination, read all pages from that same snapshot. Credit only A, C with the target at the committed revision or a newer known fixture state. Empty, partial, stale, cross-route or otherwise unproven results miss. The target is 99%. The candidate has 196 on-time proven commits, two late and two unavailable.

For the relationship drill, 100 original valid requests arrive in ten minutes. The 200 ms window runs from first arrival to response. The target is 95% complete and correct on time for this drill, with relevant graph edges held fixed. There are 91 full correct replies on time, four explicitly partial on time, three timed out and two full correct replies late. Count each original once and keep misses in the denominator.

## M05-EX1

1. Choose an access path, data model and transactional authority for each operation. Compare at least one alternative for each. Explain partitioning, query costs, maintenance and repair workload.
2. Trace a stale positive session cache after revocation, a product edit across the price boundary during rollout, two readings with equal event timestamps, and one bounded supernode traversal.
3. Score both drills under the stated contracts. Give tests that isolate freshness, version retention, lost state and partial traversal. For each of the four choices, give two questions that must be answered by exact product documentation or a controlled test.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M05-S1

Choose data models against the four access patterns and their invariants. Use [key-value and documents](../lessons/M05-L01.md), [wide-column and graphs](../lessons/M05-L02.md), and [distributed-store guarantees](../lessons/M05-L03.md).
