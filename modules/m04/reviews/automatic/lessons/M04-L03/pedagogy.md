# M04-L03 pedagogy and curriculum coverage review

Reviewed the canonical lesson, companion assessment and evidence at draft handoff `ac46917` for middle and senior engineers. The scope is the [approved M04-L03 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l03), its assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the [pinned Primer federation and sharding section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L874-L935) and [consistent hashing reference](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1805), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Coverage

| Topic | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H091, federation | taught | **Split by domain or by row** separates billing and profile ownership. Q1 and EX-1 apply the split to a combined view. |
| PR-H092, federation disadvantages | taught | The same section explains cross-domain composition, freshness, partial states and transactions. Q1 and EX-1 ask about a combined dashboard. |
| PR-H094, sharding | taught | **Split by domain or by row**, **Choose the unit of routing** and **Move data with one writable owner** cover routing, key choice, hot tenants and migration. Q4 and EX-1 apply these mechanisms. |
| PR-H095, sharding disadvantages | taught | The routing and movement sections explain fan-out, skew, cross-shard invariants, stale routes and rollback. Q4–Q6 and EX-1 assess the trade-offs. |
| PR-B007, consistent hashing | taught | **Trace movement on a ring** gives the ownership interval convention, a join, wraparound and virtual tokens. Q2–Q3 and EX-1 assess token boundaries and changed ownership. |

## Pedagogy and assessment

The scenario contrasts a capability split with a hot tenant that remains concentrated after tenant hashing. The lesson then connects a more granular key to direct writes, fan-out on tenant-wide reads, and possible coordination for shared invariants. Its ring trace states the clockwise rule and endpoint convention before illustrating the changed interval. The assessment's ring answers correctly map 12 from B to D, leave 28 on B and wrap 90 to A. The migration sequence teaches snapshot and change capture, a fenced drain, verification, epoch switch and the separate rollback transition after destination writes.

LO1 is taught across the domain, routing, ring and movement sections and measured by Q1–Q3 and EX-1. LO2 is taught across the same decision sequence and measured by Q4–Q6 and EX-1. The separate companion has six explained checks and a practical design exercise with a point-bearing rubric. The sample solution reports partial dashboard results, direct ticket routing, tenant-list fan-out and stale-epoch handling. Equivalent designs are accepted when they meet the stated constraints.

## Findings

No open pedagogical or assigned-topic coverage findings.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the changed lesson and assessment at `21b3905`. **Move data with one writable owner** now teaches a durable plan with mutually exclusive conditional activation and abort, source fencing while a switch outcome is unknown, epoch checks at write admission, and a new fenced movement after destination writes. The revised EX-1 asks the learner to trace a lost switch reply and delayed activation. Its sample solution and migration rubric assess the corresponding taught behavior while retaining credit for alternative designs that meet the constraints.

The ring section identifies its inclusive-token rule as an example convention, and EX-1 explicitly adopts that convention. Its key calculations remain consistent with it. The two outcome maps and previously reviewed coverage dispositions remain supported by the lesson and companion.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.

## Round 2 targeted re-review

Reviewed the updated lesson and companion at `ec068f6`. **Move data with one writable owner** explains the durable closed-through epoch, atomic gate for opening and closing, draining admitted writes, and a delayed epoch-2 open rejected after the destination is fenced and source epoch 3 becomes active. EX-1 asks about delayed activation and rollback. Its sample solution and migration rubric assess the same floor and drain sequence, and retain acceptance of equivalent designs. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l03) includes partition movement and migration failure trade-offs.

Both outcome maps and the ring convention remain aligned with the teaching. No new pedagogical or assigned-topic coverage finding arose in the changed material.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.
