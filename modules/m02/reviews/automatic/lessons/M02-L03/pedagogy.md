# M02-L03 pedagogy and curriculum coverage review

Round 0, 2026-11-12. Reviewed the canonical lesson and companion for middle and senior engineers against the [approved M02-L03 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l03), [coverage matrix](../../../../../../curriculum/revision-1/coverage.csv), and [pinned Primer load-balancer and reverse-proxy sections](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L660-L764) at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. The archived teaching review in PR #38 supplied context.

## Findings

No open pedagogical or assigned-topic coverage findings.

## Coverage ledger

The section names below refer to the current [lesson](../../../../lessons/M02-L03.md).

| Topic ID | Teaching evidence | Disposition |
| --- | --- | --- |
| PR-H067 | Routing and backend selection explains eligible backends, selection and health-check delay. | taught |
| PR-H068 | Routing and backend selection distinguishes address/port decisions, NAT and transport proxying. | taught |
| PR-H069 | Routing and backend selection explains path and header inspection after TLS termination. | taught |
| PR-H070 | Proxy work and horizontal scaling explains adding interchangeable instances and placing shared state. | taught |
| PR-H071 | Proxy work and horizontal scaling explains shared-state failure and replica-multiplied connection pools. | taught |
| PR-H072 | Trade-offs and failure modes explains balancer saturation, failure and shared dependencies. | taught |
| PR-H074 | Proxy work and horizontal scaling explains forwarding and the assigned proxy responsibilities. | taught |
| PR-H075 | Proxy work and horizontal scaling distinguishes the distribution role from accepting requests on behalf of backends. | taught |
| PR-H076 | Trade-offs and failure modes explains proxy resource limits, shared failures and stale cache risk. | taught |
| PR-B002 | Routing and backend selection compares random, least connections, round robin, weights and affinity. | taught |
| PR-BODY-R1-PROXY-COMPRESS | Proxy work and horizontal scaling explains bandwidth savings and proxy CPU cost. | taught |
| PR-BODY-R1-PROXY-STATIC | Proxy work and horizontal scaling explains direct static-file serving and resource costs. | taught |
| PR-BODY-R1-LB-ALGORITHMS | Routing and backend selection explains the algorithms and uneven request cost. | taught |
| PR-BODY-R1-LB-L4 | Routing and backend selection explains transport-header selection and NAT rewriting. | taught |
| PR-BODY-R1-LB-L7 | Routing and backend selection explains application inspection, termination and backend connections. | taught |
| PR-BODY-R1-SCALE-STATE | Proxy work and horizontal scaling explains external sessions, shared dependencies and connection growth. | taught |

## Outcomes and assessment

LO1 is taught by the routing, proxy/state and worked-example sections. Q1–Q3 trace the retry, session location and unknown write outcome. EX-1 transfers the routing and failure trace to a ticket service. LO2 is taught in those mechanism sections, Trade-offs and failure modes, and Decision framework. Q4–Q6 assess the L7/TLS boundary, backend-load signal and trusted client identity. EX-1 assesses state placement, safe retry, connection budgeting and ingress recovery. Both front-matter entries match the companion's detailed outcome map and include the relevant teaching headings and items.

The worked example makes a backend failure observable and distinguishes the affinity cookie from shared session state. The companion contains six explained checks and a separate exercise with sample answer and rubric. The calculation gives 180 current web connections and an equal cap of 27 under the stated 165-connection allowance. The rubric accepts other designs that satisfy the stated constraints. M02-L02 is identified as the prerequisite.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.
