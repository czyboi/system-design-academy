---
id: M11-EX1
status: draft
outcomes: [M11-S1]
---

# One allocator and one limiter, two different invariants

An API platform deploys in two regions. It needs public object IDs and must also limit expensive tenant reports to a strict global cap. A teammate proposes “one central counter with a local cache in every region” for both services. The team needs to show why this is not automatically safe: **ID uniqueness is a non-reuse property over the object's lifetime**, while a strict rolling quota is a bounded-admission property **over a shared time interval**.

The approved module synthesis outcome **M11-S1** is to compare the unique-ID invariant of [M11-L05](../lessons/M11-L05.md) against the distributed rate-limit invariant of [M11-L06](../lessons/M11-L06.md), then defend distinct coordination and partition-failure choices. Other M11 domains remain assessed by their respective companions.

## Constraints and synthetic workload

| Property | Given workload / contract |
| --- | --- |
| ID allocation | 20,000 IDs/s globally across regions, each used once; IDs need uniqueness, not necessarily chronological ordering or secrecy |
| ID range leasing | Authority issues disjoint, epoch-associated ranges of 1,000 IDs; unused IDs may be skipped forever; no requirement for contiguous sequences |
| Global report quota | A tenant may initiate **at most 3 new original reports in any rolling 6-second interval**, across all gateways |
| Original operations | One input-bound request ID per intended report, reused on transport retries; a same-ID different payload is a conflict |
| Decision target | Correct durable admission or explicit rejection by 200 ms of first valid original request; avoid counting accepted-only latency as overall user success |
| Fault | Region A stops responding after receiving one unused ID range and a batch of quota grants; a partition may let its old processes resume |
| Success evidence | In a five-minute original-request cohort, count admitted, policy-rejected, timed-out, failed and late originals separately |

Do not assume network RTT, Redis write throughput or regional failover duration without a measured environment. Declare any needed parameters and keep them synthetic.

## M11-EX1 — Architecture comparison and failure drill

1. **Define identities and invariants.** Specify ID namespace, maximum lifetime/reuse rule, range authority, assignment epoch and persistence. Separately specify tenant/operation-class/revision quota key, rolling interval, original-operation receipt and exact acceptance boundary. Explain why a timestamp alone or per-gateway local counter does not prove either requirement.
2. **Draw the normal flow.** For each of two regions, show how the ID issuer and quota authority interact with gateways. Make it explicit where values become assigned, where an admission consumes quota and how a duplicate report request resolves. Include the data models or command contracts.
3. **Trace a partition and stale owner.** Region A has leased IDs 4000–4999, consumed through 4029, then loses connectivity. Its processes may resume. Region B needs more IDs and quota. Show what can be safely issued or stranded, why reclaiming uncertain IDs or quota is unsafe, and how a fenced epoch or non-overlapping grant prevents double use.
4. **Compare two credible alternatives per domain.** For IDs, contrast disjoint range leasing with random sufficiently large IDs plus a uniqueness guard or a centralized allocator. For quota, contrast one serializing shared counter/log with bounded nonoverlapping quota leases or an explicitly approximate local policy. State the cost of each in fairness, latency, availability and recovery.
5. **Verify end-user outcomes.** In a five-minute test of 1,000 original valid report attempts, assume 760 obtain durable accepted work and a client receipt within 200 ms; 140 receive legitimate quota rejection, 50 time out, 30 fail and 20 receive a late acceptance. Report accepted-work success and decision correctness as separate measures. Describe at least six falsification tests, including retry-after-lost-response and the two-region quota overshoot race.

Your answer must explicitly reject a design that treats a local cache copy of the global counter as exact admission authority. Identify when ID monotonicity, predictability and secrecy would **change** the choice.

[Reference design and rubric](solution-rubric.md) · [Decision table](decision-summary.md)

## Learning boundaries

This integration evaluates M11-L05-LO2 and M11-L06-LO2 together. It **does not certify** the nine lesson QA cycles or the other 16 lesson outcomes. Even an architecturally valid module-wide design cannot substitute for the per-lesson companion exercises or required independent reviews.
