# M03-L03 actual coverage and pedagogy review

## Scope and sources

Reviewed the draft lesson and assessment for middle and senior backend engineers against the approved SDA-v1 M03-L03 outline and both assigned inventory rows. Inspected [The System Design Primer, Service Discovery at the pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L791-L793). Prior M01-L02 feedback informs the transfer check below.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator, explanation and assessment |
| --- | --- | --- | --- |
| PR-H080 | Core concepts and mechanisms | taught | README.md#L791. Registration, registry and DNS resolution, eligibility, consumer refresh and client-versus-intermediary selection are explained. The stale endpoint example connects those mechanisms to a failed call. LO1 Q1 and Q3, LO2 Q5 and EX-1 apply the distinctions. |
| PR-BODY-R1-DISCOVERY-CONFIG | Registration, health and membership | taught | README.md#L793. Address and port records, health checks and lease/session expiration have distinct roles. Consul's registration, eligibility and configuration examples, etcd's leased keys and ZooKeeper's ephemeral nodes distinguish discovery primitives from settings such as a request limit. Q1 and EX-1 assess stale eligibility. |

The Academy additions include an explicit deadline, remaining budget, backoff, retry ownership, ambiguous writes and concurrency isolation. The trace follows one failed and one successful attempt through a stale client-side membership list.

## Pedagogy and language

LO1 has a concrete trace from selection through recovery. Q1–Q3 distinguish membership lag, time budgets and DNS record data. LO2 uses the ownership and failure controls subsection, then tests amplification, a routing trade-off and unknown write outcomes in Q4–Q6. The English lesson stays within the approved prerequisites and keeps its questions and rubric in the companion.

EX-1 changes the ownership from a client to a shared proxy, increases the nested budgets to three by two and adds a 30-second cached list and a 500 ms deadline. It asks for a charge variant with a lost response. The answer and rubric score the trace, safe retry policy and fallback, and allow an alternate client-side design. The exact worked numbers recur in Q2 and Q4 as reinforcement. The exercise independently tests both outcomes on changed inputs.

## Findings

- **M03-L03-P1 (minor).** The LO1 outcome map points to the worked trace, while Q3's SRV record fields are taught in **Registration, health and membership**. The trace supports LO1 as a whole and the fields are present in teaching. Add a subsection pointer near Q3 or in the lesson's trace to make that item easier to audit.
- **M03-L03-C1 (note).** **Registration, health and membership** could make the source example more concrete by showing an HTTP readiness probe and naming etcd's unleased configuration key as a counterpart to Consul KV. The lesson already explains endpoint eligibility, the three products' roles and why configuration and health serve separate purposes.

Verdict **ready-for-human-review**.
