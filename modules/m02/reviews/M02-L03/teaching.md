# M02-L03 actual coverage and pedagogy review

## Scope and sources

Reviewed the lesson and companion at their declared paths against the SDA-v1 outline for middle and senior engineers. Checked the pinned [Primer README, load balancer and reverse proxy](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L660-L764), revision ae9bbd7b02d90b9866215de185217d33f39ab733, against the assigned inventory and matrix. Considered prior M01-L02 feedback on transfer and exact outcome evidence.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H067 | Routing and backend selection | taught | README.md#L660. Explains eligible backends, selecting one by transport or application information, and why probes can miss a failure. LO1 and LO2. |
| PR-H068 | Routing and backend selection | taught | README.md#L693. Address and port selection, NAT rewriting, and a distinct transport-proxy implementation. LO1 and LO2. |
| PR-H069 | Routing and backend selection | taught | README.md#L697. HTTP fields drive selection after termination, followed by independent upstream connections. LO1 and LO2. |
| PR-H070 | Proxy work and horizontal scaling | taught | README.md#L703. Adds web replicas, locates external state, and budgets pools as replica count increases. LO2. |
| PR-H071 | Proxy work and horizontal scaling | taught | README.md#L707. Shared state imposes another failure dependency, while a 12 × 20 example shows downstream connection growth. LO2. |
| PR-H072 | Trade-offs and failure modes | taught | README.md#L714. A single failed or saturated balancer can interrupt the whole path, and redundant instances may still share failure causes. LO2. |
| PR-H074 | Proxy work and horizontal scaling | taught | README.md#L730. Explains public request intake and forwarding, TLS, buffering, compression, caching, static serving, backend exposure and trusted client addressing. LO1 and LO2. |
| PR-H075 | Proxy work and horizontal scaling | taught | README.md#L755. Distinguishes balancing among eligible instances from accepting requests on behalf of a backend and explains how one component can do both. LO2. |
| PR-H076 | Trade-offs and failure modes | taught | README.md#L761. Explains why proxy-side resources and common failures can constrain availability and why cached data needs a freshness policy. LO2. |
| PR-B002 | Routing and backend selection | taught | README.md#L684. Contrasts random, round-robin, weighted, least-connection and cookie-based choices. LO2. |
| PR-BODY-R1-PROXY-COMPRESS | Proxy work and horizontal scaling | taught | README.md#L747. Explains bandwidth savings and proxy resource use, with TLS and compression CPU reinforced in the failure discussion. LO2. |
| PR-BODY-R1-PROXY-STATIC | Proxy work and horizontal scaling | taught | README.md#L749. Direct static serving shifts work from the application to proxy resources. LO2. |
| PR-BODY-R1-LB-ALGORITHMS | Routing and backend selection | taught | README.md#L684. Explains selection behavior, uneven work per connection and the capacity or availability risks of affinity. LO2. |
| PR-BODY-R1-LB-L4 | Routing and backend selection | taught | README.md#L695. Explains NAT rewriting and transport flow selection without reading an HTTP message. LO1 and LO2. |
| PR-BODY-R1-LB-L7 | Routing and backend selection | taught | README.md#L699. Explains message inspection, client-side termination and establishing or reusing upstream connections. LO1 and LO2. |
| PR-BODY-R1-SCALE-STATE | Proxy work and horizontal scaling | taught | README.md#L709. Connects interchangeable web processes, central sessions and replica-multiplied downstream pools. LO2. |

All 16 assigned topics have explanatory evidence. The lesson leaves CDN population and replacement to M02-L04 and uses M02-L02 transport semantics as a prerequisite.

## Pedagogy and assessment

The English lesson moves from a concrete ingress and session problem to selection, state placement, a request and failure trace, then decision criteria. It is concise for the declared audience. LO1 uses the catalogue failover trace and Q1–Q3 plus EX-1. LO2 uses the decision framework, Q4–Q6 and EX-1. The ticketing exercise transfers the mechanism to path and state choices under a new 165-connection web budget and an ambiguous purchase write. The answer derives 180 current connections and a maximum equal cap of 27. The rubric also accepts viable alternative designs that account for the two failures.

- **EDGE-P1, minor.** The companion maps all LO2 items to Decision framework, while the least-connections caveat behind Q5 and trusted forwarding for Q6 are specifically explained in Routing and backend selection and Proxy work and horizontal scaling. The prerequisite mechanisms are taught, and the capstone decision sequence remains aligned. Pointing those checks to their supporting sections would make the mapping more precise.

## Verdict

ready-for-human-review.
