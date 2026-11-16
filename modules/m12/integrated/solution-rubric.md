---
id: M12-EX1-solution
status: draft
---

# Reference — policy extension with one allocation authority

## Class and responsibility sketch

```text
ParkingLot --contains--> Level --contains--> Row --contains--> Spot
             delegates atomic admission + release to Level
Vehicle --describes requirements--> FitPolicy
AllocationPolicy --finds candidate--> row-local contiguous run
Allocation --records--> allocation_id, vehicle_id, spot_ids, revision, status
```

`Level` serializes mutations to its Spots and active Allocation map. `FitPolicy` knows if one spot supports a vehicle kind/capability; `AllocationPolicy` knows the required run length and adjacency requirements. Neither directly mutates shared physical ownership. The new `Truck` configuration specifies `required_large_run=3`, while `Bus` specifies 5. A stable `allocation_id` is the command result and release guard, not merely a convenient vehicle label.

## Trace an eligible allocation

A-L1/R1 free large runs [0,1], [3,4,5], [7] (the other spots 2,6 are occupied). Truck T1 may use [3,4,5] atomically. Bus B1 cannot use this row because there is no five-run. The all-free A-L1/R2 indexes [0,1,2,3,4] can accommodate B1 *if the two attempts coordinate on distinct rows*. If the row becomes partially occupied before commitment, the bus must retry scan or return no-fit without any partial change. B-L2/R3 has only four free consecutive spots and cannot accept B1. Total large free count across Level B or A is irrelevant to the five-*same-row* requirement.

At selection time, the Level validates all candidate spots under a version/lock, then writes their common allocation ID and registers `Allocation(T1,[3,4,5],active)` in one coherent transition. Increment/decrement available counts in that same transition. A concurrent C1 claim for spot4 must either commit first (T1 candidate rejected/replanned) or commit after T1 (C1 rejected for occupied spot). There is no legal interleaving where only 3 and 5 become T1-owned.

## Release and stale retries

`release(allocation_id=T1)` reads current active Allocation, checks all listed spots still refer to the same ID, atomically clears all three, updates counts and marks the allocation terminal. A duplicate identical release returns the prior release receipt or an explicit already-released outcome **without touching spots**. If C2 later claims spot4 under allocation C2, an old T1 release cannot release it because T1 is terminal and each spot's current allocation ID differs.

Maintain one nonnegative conservation equation per level/size: `free + occupied = physical_count`. Maintain per-allocation exact set correspondence: `{spot | spot.allocation_id == A.id} == A.spot_ids` for active A. No two active Allocation records share a spot. Counts alone cannot establish contiguity, ownership, or absence of ghost spots.

## Compare change strategies

A single `Lot` with `if vehicle.type...` scattered across search, assignment and release invites inconsistent updates. An injected `FitPolicy` and `AllocationPolicy` keep policy variation independent of Level's guarded ownership mechanism. New requirements such as EV charging can be expressed as capabilities rather than a combinatorial explosion of vehicle/spot subclasses. Scanning N spots on each row is O(N) in the level's size and can be sufficient for a moderate lot; a balanced indexed interval set may reduce candidate discovery but increases each spot-claim/release update and creates an additional correctness invariant. Never trust an index hit without checking authoritative spot state before commit.

## User-facing evaluation

All figures are synthetic. Parked-success by 250ms is 850/1000 = **85%**. A correct timely decision SLI may count the 80 legitimate no-fit results only if they are definitively returned before 250ms and policy-consistent, yielding 930/1000 = **93%** under that assumption. Timeouts, errors and late assignments remain counted as misses. Distinguish latency among accepted parkings from end-to-end outcomes.

Falsification tests: (1) truck valid three-run; (2) bus rejected by fragmented free set despite enough total; (3) car races truck revalidation; (4) two buses claim same five-run; (5) release three or five spots entirely; (6) duplicate release; (7) stale release after spot reuse; (8) charging policy without changing release; (9) free counts/index conservation after random operations; (10) crash/replay if deployed across processes.

## Rubric (12 points)

| Criterion | Pts | Full-credit evidence |
| --- | ---: | --- |
| Responsibility decomposition | 3 | Lot/Level/Row/Spot/Allocation/fit/allocation policies with single ownership |
| Allocation/release invariants | 4 | Exact row-local runs, atomic race handling, complete and stale-safe release |
| Extensibility and cost | 3 | Minimal truck rule extension, scan/index and composition trade-offs |
| Outcomes/verification | 2 | 85% parked-success, conditional decision SLI and six meaningful tests |

Accept alternative designs only when the invariants and failure ordering are as strong as claimed.
