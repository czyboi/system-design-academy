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
| Read device telemetry | Read the last 30 minutes for one device. One device accounts for 40% of writes, and independent events can share a timestamp. Retain the original plus corrections for a 30-day audit and use only the latest version on the dashboard. |
| Suggest relationships | Return unique second-hop sellers, excluding the seed and directly followed sellers. A supernode may need a remote lookup with tens of thousands of edges. The API must identify a partial result. |

Use two hypothetical drills. For the product freshness drill, track 200 original qualifying product commits in one ten-minute window. A commit succeeds if browse can reflect its revision or a newer valid state for that product within 15 seconds of commit. Follow each through its deadline. A stale, wrong, late, unavailable or unobserved result misses. The target is 99%. The candidate returns 196 fresh on time, two late and two unavailable. For the relationship drill, 100 original valid requests arrive in ten minutes. The 200 ms window runs from first arrival to response. The target is 95% complete and correct on time for this drill, with relevant graph edges held fixed. There are 91 full correct replies on time, four explicitly partial on time, three timed out and two full correct replies late. Count each original once and keep misses in the denominator.

## M05-EX1

1. Choose an access path, data model and transactional authority for each operation. Compare at least one alternative for each. Explain partitioning, query costs, maintenance and repair workload.
2. Trace a stale positive session cache after revocation, a product edit across the price boundary during rollout, two readings with equal event timestamps, and one bounded supernode traversal.
3. Score both drills under the stated contracts. Give tests that isolate freshness, version retention, lost state and partial traversal. For each of the four choices, give two questions that must be answered by exact product documentation or a controlled test.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M05-S1

Choose data models against the four access patterns and their invariants. Use [key-value and documents](../lessons/M05-L01.md), [wide-column and graphs](../lessons/M05-L02.md), and [distributed-store guarantees](../lessons/M05-L03.md).
