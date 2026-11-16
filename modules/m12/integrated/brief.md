---
id: M12-EX1
status: draft
outcomes: [M12-S1]
---

# Extend a parking allocation policy without breaking ownership

A multi-level lot already supports motorcycle, compact and large spots. Cars take one compatible spot and buses need **five adjacent large spots in the same row**. The team wants to add a new rule: **a delivery truck needs three consecutive large spots**, while buses still need five. A quick patch adds a `Truck.park()` method that marks three neighboring spots in a loop, but a concurrent car can claim the middle spot during that loop. The result is a half-parked truck; the existing `release()` frees only its first spot.

This integrated assignment measures **M12-S1**: extend a parking fit/allocation rule while preserving allocation and release invariants. It transfers M12-L03-LO1 and M12-L03-LO2, not a summary verdict on all object-design models.

## Original domain contract

- Two levels, each containing row-local ordered spot indexes. Spot sizes are motorcycle, compact and large; a motorcycle fits any, a car fits compact/large, a bus needs five consecutive large, and the new truck needs three consecutive large in one row. Inputs valid.
- A Level coordinates physical spot ownership. One active Allocation contains exactly the set of occupied Spot IDs for one vehicle, with stable allocation ID, status and revision. Lot coordinates levels; FitPolicy evaluates compatibility; AllocationPolicy chooses a contiguous run.
- **At level A:** row R1 large spots 0–7. Index 2 is occupied and 6 is occupied: free runs [0,1], [3,4,5], [7]. Row R2 has large spots [0…4] all free.
- **At level B:** row R3 large spots [0…5], 0 occupied and 5 occupied: free run [1,2,3,4].
- One truck T1 and bus B1 request parking concurrently. A car C1 may claim one candidate spot between search and commit. A duplicate release of T1 can arrive after the spot has been reassigned.

## M12-EX1

1. Define `Lot`, `Level`, `Row`, `Spot`, `Vehicle`, `FitPolicy`, `AllocationPolicy` and `Allocation` responsibilities. Show a compact class/responsibility diagram, command contracts and who owns the **single authoritative spot state**. Avoid adding five unrelated `TruckSpot` subclasses.
2. Trace T1's successful three-spot selection and B1's valid five-spot selection, or explicitly explain when concurrency changes which succeeds. Demonstrate a failing bus candidate even when total free spots on a level exceed five but no qualifying run remains.
3. Design the atomic guard around candidate revalidation + all-or-nothing assignment. Trace C1 taking a candidate spot in between and show retry or failure without partial reservations. Specify how available counts and optional contiguous-run indexes remain coherent.
4. Release T1 completely. Trace an identical release retry, then a **delayed release** after another vehicle has occupied one former T1 spot. Prove that no new allocation is freed by T1's stale request.
5. Compare adding policy objects/composition against subclassing every vehicle/spot combination; contrast O(N) scans against indexed free runs, with failure and maintenance costs. List at least six invariant-oriented tests.
6. Define a five-minute cohort of 1,000 original vehicle arrival requests: 850 confirmed compatible parking assignments within 250ms, 80 legitimate no-fit results, 40 timeouts, 20 errors and 10 late assignments. Distinguish **parked-success** from a correct timely **decision** SLI and explain why available counts alone cannot prove safety.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## Synthesis boundary

The other five M12 lesson outcomes are independently assessed in their own companions. This integration's assignment and feedback must not be represented as a technical or pedagogy review of those separate packages. All content stays `draft` until independent QA and human approval.
