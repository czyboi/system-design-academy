# Source evidence — M10 integrated design

Checked against approved SDA-v1 M10 outline and current canonical lesson source packs, 2026-11-16. All posts, workloads, page versions, cache sizes, deadlines and output thresholds are **original teaching assumptions**, not benchmarks.

| Integrated claim | Direct supporting evidence and limits |
| --- | --- |
| Canonical posts and graph-based home fan-out may have skew; ordinary/celebrity push/pull trade-off. | [M10-L02 evidence](../evidence/M10-L02.md) for historical TAO social-graph background. The 100k×200 = 20m writes/day and chosen hybrid policy belong to this exercise. |
| Durable page `u1:v2` may not yet be visible in old query index g17; versioned crawl/index publication must be checked separately. | [M10-L03 evidence](../evidence/M10-L03.md), with [M08-L03](../../m08/evidence/M08-L03.md) as unmerged prerequisite. Generation/source-cut gate is an **application-designed** invariant, not a named index vendor's automatic guarantee. |
| Query cache correctness depends on generation, rank model, scope and shard coverage, with explicit cold misses on node failure. | [M10-L06 evidence](../evidence/M10-L06.md), RFC 9111 and Redis/AWS caching docs. Cache-serving policy is a scenario contract. |
| Confirmed revocation must order with read authorization/content release; physical bytes and already-issued capabilities are separate. | [M10-L01 evidence](../evidence/M10-L01.md), [M10-L02 evidence](../evidence/M10-L02.md), [M10-L06 evidence](../evidence/M10-L06.md). The stronger serialized gate is a proposed **design**, requiring implementation and independent technical proof. |
| Other case-study invariants remain covered by individual lessons. | [M10-L04 evidence](../evidence/M10-L04.md), [M10-L05 evidence](../evidence/M10-L05.md), [M10-L07 evidence](../evidence/M10-L07.md), [M10-L08 evidence](../evidence/M10-L08.md). |

Original diagrams and narrative, no borrowed images or prose. Primer is the approved topic map, not reused case-solution text. No production client, crawler, index, cache or revocation test executed. Independent technical/source and pedagogy/coverage checks and upstream MS05 reconciliation pending.
