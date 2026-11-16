---
id: M12-decisions
status: draft
---

# Choose object responsibilities by change pressure

## One change reveals the ownership boundary

Adding a truck that needs three consecutive large spots is a *policy change*, not permission to modify partial spot state outside Level's guarded allocation. `FitPolicy` decides compatibility and `AllocationPolicy` chooses a row-local run. `Level` owns the consistent transition for all spots/Allocation records, including count/index updates. Releasing by stable allocation identity avoids accidentally freeing a newer occupant.

For M12-S1 use [M12-EX1](brief.md) and the [reference](solution-rubric.md). The other five lessons retain their companion assessments.

## Compare the six local object models

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Equality lookup collides | Chained hash map / ordered tree | Bucket chain keyed by equality, resize by load factor | Fast expected lookup | Collision and rehash cost | Silent lost colliding entry | Ordered/range query primary | [M12-L01](../lessons/M12-L01.md) |
| Recent cache entry needs quick eviction | Composed map+doubly linked list / ordered map | Map points to single recency node; tail eviction deletes key | Expected O(1) local LRU | Pointer invariants and locking | Map/list count diverges | Existing library fits production requirements | [M12-L02](../lessons/M12-L02.md) |
| Multi-spot vehicle and new fit rule | Composition + policies over authoritative Level | Compatible contiguous run committed as one Allocation | New rule without partial ownership | Scan/index update cost | Ghost spots/double release | One class mutates shared state outside Level | [M12-L03](../lessons/M12-L03.md) |
| Call escalates while employee frees | Versioned Assignment + DispatchPolicy | Single guarded call/employee transition | Safe reassignment | Queues and fairness complexity | Stale completion frees new owner | Rank subclasses own global queue state | [M12-L04](../lessons/M12-L04.md) |
| Game scoring changes across card games | Immutable Card + Deck + Hand + Scorer | Keep inventory and game rule separate | Reuse, deterministic testing | More explicit interfaces | Same card dealt twice / ace mis-score | Fixed ace value embedded in Card | [M12-L05](../lessons/M12-L05.md) |
| Membership changes while message sent | Distinct User, Relationship, Conversation and Message owners | Membership-at-write guard + stable receipt | Correct permissioned history | Coordination and policy cost | Removed member sends successfully | Client participant list treated as authority | [M12-L06](../lessons/M12-L06.md) |

## Synthesis outcome

**M12-S1:** extend parking fit/allocation with one new rule and demonstrate that allocate/fail/release preserve spot ownership. [M12-L03](../lessons/M12-L03.md) teaches the invariant; [M12-EX1](brief.md) measures transfer. This decision table is not independent QA of the other OOD models.
