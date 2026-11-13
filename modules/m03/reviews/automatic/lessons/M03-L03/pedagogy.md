# M03-L03 pedagogy and curriculum coverage review

Reviewed the canonical lesson and separate companion in lesson mode after draft handoff `e02844a`, against the [task specification](../../../../../../.academy/specs/SD-M03-L03.json), approved curriculum and coverage map. Audience: middle and senior engineers. Source scope is the [Service Discovery section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L791), pinned Primer revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Coverage

| Assigned topic and source locator | Status and instructional evidence | Assessment |
| --- | --- | --- |
| PR-H080, Service Discovery, README.md#L791 | taught: **Registration, health and membership** explains registry records, health, leases, stale membership, DNS and the distinct roles of Consul, etcd and ZooKeeper; **Ownership and failure controls** compares client and intermediary selection. The example traces a stale endpoint and recovery. | Q1–Q3, Q5 and EX-1 |
| PR-BODY-R1-DISCOVERY-CONFIG, registration, health checks and configuration KV, README.md#L793 | taught: the registration section relates address and port records, health checks and lease expiry to eligibility; it distinguishes configuration KV from membership and health. | Q1, Q3 and EX-1 |

The Academy additions—deadline, bounded retry, backoff and isolation—are explained in **Ownership and failure controls**, with amplification and unknown write outcomes in the worked example. The lesson's reporting workload and prerequisites lead naturally from M03-L02. Its preview matches the canonical trace: A fails at 40 ms, 20 ms backoff leaves 240 ms at 60 ms, and B responds at 120 ms. The archived link in M03-L02 remains an integration follow-up for the parent; the trace itself is consistent.

## Pedagogy and assessment

LO1's discovery, stale-membership and deadline trace is taught in the three headings named by both maps, and Q1, Q2, Q3 and EX-1 test its constituent actions. LO2's ownership and bounded retry choices are taught in the five headings named by both maps; Q4–Q6 test supporting decisions and EX-1 asks for their application to a stated workload. The front matter and narrative map agree on exact headings and item IDs. The six checks have explanations, the exercise permits multiple designs, and the worked arithmetic is consistent: 300 − 60 = 240 ms; 300 − 120 = 180 ms; two attempts at each of two layers yield four, and EX-1's three by two yields six.

## Findings

- **P-M03-L03-01 — Major, open — assessment, Answer key / rubric:** EX-1 explicitly requires choosing and defending discovery ownership, but its ten-point allocation scores the stale trace and arithmetic, deadline and retry ownership, refresh/outage policy, and charge handling without awarding points for the discovery ownership choice or its workload-specific rationale. Q5 asks generally when an intermediary helps, so it does not replace a graded defense for this workload. Allocate explicit rubric credit to a justified client-side or proxy discovery choice, including an appropriate trade-off, while retaining the ten-point total and credit for other required actions.
- **P-M03-L03-02 — Minor, open — assessment, Q6 explanation:** The phrase “or a status lookup” can suggest that any lookup resolves an unknown write, while the lesson and exercise key qualify the lookup as authoritative and warn that a stale miss leaves uncertainty. Add that qualification to the explanation so learners do not infer that a stale status result makes a retry safe.

**Verdict: revise.** Coverage is taught, but the assessment rubric needs the LO2 grading gap resolved. This is a pedagogy and assigned-coverage verdict, not technical or human approval.

## Round 1 targeted re-review

Reviewed the corrected companion handed off at `4a6dc6e` against the two findings above. The original verdict describes the initial review; this section records the current result.

| Finding | Status | Curriculum basis |
| --- | --- | --- |
| P-M03-L03-01 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md |
| P-M03-L03-02 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md |

The EX-1 rubric now awards two of ten points for a reasoned discovery ownership choice and its trade-off, accepts either client or intermediary ownership when justified, and retains credit for the other requested actions. The sample answer illustrates the proxy choice and its capacity and availability cost. Q6 now distinguishes an authoritative committed record from an absent, stale or pending status and explains the conditions for safe retry. These changes resolve both findings.

**Current verdict: ready-for-human-review.** This is a pedagogy and assigned-coverage verdict, not technical or human approval. The M03-L02 archived-link reconciliation remains an integration follow-up.
