# M03-L03 technical and provenance review

Reviewed 2026-11-13 against draft handoff `e02844a`. Scope covers the canonical lesson, companion assessment, evidence matrix and compatibility with the timed M03-L02 preview.

## Technical findings

| ID | Severity | Status | Location | Evidence and suggested correction |
| --- | --- | --- | --- | --- |
| DISC-T1 | major | open | `modules/m03/assessments/M03-L03.md:70` (Q6 explanation), `modules/m03/lessons/M03-L03.md:47` (worked example) | Q6 says “or a status lookup” resolves the unknown outcome. The lesson requires an authoritative lookup for the operation identity and correctly rejects a stale miss. Even an authoritative read can return absence while the original request is in flight and can still commit. A caller that treats that absence as rejection can issue a fresh key and create a duplicate charge. Align both passages with the EX-1 rubric at `modules/m03/assessments/M03-L03.md:74`. A committed record confirms the effect. An absent or pending result leaves it unknown. Require authoritative terminal evidence that the original attempt did not and cannot apply before issuing the same logical write under a fresh key. Preserve the alternative of reusing the same identity under a durable deduplication contract that covers the effect and the retry window. The need for terminal evidence follows from the possibility of a delayed write and the distinction between a transport failure and application effect. [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) · [Amazon Builders’ Library, Reducing client complexity and Late arriving requests](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) |

The discovery claims at lesson lines 25–35 and evidence rows DISC-1 and DISC-2 preserve the product boundaries. RFC 2782 assigns port and target and uses weight among records of the same priority. Consul exposes agent registration with optional health checks and a `passing` filter on the health endpoint, alongside its configuration KV API. etcd v3.6 removes keys attached to expired or revoked leases. ZooKeeper 3.9.4 removes ephemeral nodes when the creating session ends. These lifetimes and a consumer’s last refreshed view have separate failure boundaries. Kubernetes is scoped to a stable Service abstraction with changing backends. The lesson makes no claim that every Service type has a virtual IP or proxy. [RFC 2782, The format of the SRV RR](https://www.rfc-editor.org/rfc/rfc2782.html) · [Consul service registration](https://developer.hashicorp.com/consul/api-docs/agent/service#register-service) · [Consul health filter](https://developer.hashicorp.com/consul/api-docs/health#list-nodes-for-service) · [Consul KV API](https://developer.hashicorp.com/consul/api-docs/kv) · [etcd v3.6 Lease API](https://etcd.io/docs/v3.6/learning/api/#lease-api) · [ZooKeeper 3.9.4 Ephemeral Nodes](https://zookeeper.apache.org/doc/r3.9.4/zookeeperProgrammers.html#Ephemeral+Nodes) · [Kubernetes Service concepts](https://kubernetes.io/docs/concepts/services-networking/service/)

The trace at lesson lines 39–47 is consistent with the total deadline and the smaller per-attempt cap at line 37. Attempt one ends at 40 ms, the 20 ms delay brings attempt two to 60 ms with 240 ms remaining, and B answers at elapsed time 120 ms with 180 ms remaining. Two independent layers with two total attempts each can make up to four downstream attempts. The EX-1 calculation of six from three API attempts and two proxy attempts is the same upper-bound reasoning. Jitter, concurrency isolation and a maximum-staleness policy cover the overload and discovery-outage cases without assuming that a timeout cancels admitted work. [Amazon Builders’ Library, Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) · [gRPC Deadlines, Deadline Propagation](https://grpc.io/docs/guides/deadlines/#deadline-propagation)

The preview at `modules/m03/lessons/M03-L02.md:53` and related Q3 at `modules/m03/assessments/M03-L02.md:43–47` agree with the canonical trace’s inputs, chronology, and same-identity retry boundary. The preview can link to `M03-L03.md#worked-example-stale-endpoint-and-deadline-failure-trace` without changing its trace or assessment.

## Provenance and rights

The lesson attribution at line 68 identifies Donne Martin, the exact Primer revision and CC BY 4.0. The Primer’s service-discovery section supplies the topic scope, with the mechanism claims traceable to the official references at lesson lines 29–47 and evidence lines 7–9 and 16. The lesson and assessment use Academy examples and original calculations. The reviewed package contains no imported diagrams, code, or third-party exercise assets. No rights findings. [Primer at the pinned revision](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733#service-discovery) · [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

## Verdict

`revise`. DISC-T1 requires a bounded correction and targeted re-review.

## Round 1 targeted re-review

Reviewed 2026-11-13 against correction handoff `4a6dc6eb6d705ebeae58ea74f431ba46dae6dd7e`.

| ID | Status | Evidence |
| --- | --- | --- |
| DISC-T1 | resolved | https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ |

The worked example at `modules/m03/lessons/M03-L03.md:47` and Q6 and EX-1 at `modules/m03/assessments/M03-L03.md:70,74` now distinguish a committed record from absent, stale, or pending status. A fresh identity requires authoritative terminal evidence that the first attempt did not and cannot apply. This excludes the original delayed-commit case even if the status read was authoritative. The same-identity alternative remains conditional on a durable contract covering the operation. The EX-1 answer and rubric at lines 74–76 preserve the six-attempt upper bound and assess the stated discovery-ownership trade-off separately from the charge outcome. [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) · [Amazon Builders’ Library, Reducing client complexity and Late arriving requests](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

`ready-for-human-review`. No open blocker or major findings.
