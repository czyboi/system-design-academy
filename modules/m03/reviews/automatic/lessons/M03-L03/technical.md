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

## Human-feedback technical re-review, 2026-11-13

Reviewed `e805261..fdbe268` for M03-L03 in response to [issue #64](https://github.com/czyboi/system-design-academy/issues/64#issuecomment-6841513179). Scope covers the changed teaching, companion and canonical evidence.

| ID | Severity | Status | Location | Finding and correction | Evidence |
| --- | --- | --- | --- | --- | --- |
| MS02-H-T-DISC-1 | major | open | `modules/m03/assessments/M03-L03.md:18,74` and `modules/m03/lessons/M03-L03.md:55` | The exercise's capacity boundary is ambiguous. A proxy can free a slot on timeout while pricing still executes that request, and a retry can then exceed a backend work cap. Define 100 as proxy-tracked outstanding attempts, or add receiving-side admission or confirmed cancellation if 100 bounds actual work. Explicitly propagate the remaining deadline and clamp each 180 ms attempt to it. | [gRPC deadlines, server cancellation and propagation](https://grpc.io/docs/guides/deadlines/#deadlines-on-the-server) |

The nested worst case is six attempts. The new policy budgets 2 × 180 + 20 = 380 ms before other path work, and distinguishes the 30-second cache interval from the fallback cutoff measured from the last successful refresh. The charge path preserves its committed, unknown and terminal non-application distinctions. [AWS Builders' Library, retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) · [AWS Builders' Library, idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

The exercise and model are original illustrative material. No third-party asset was added. The prior attribution remains in the lesson.

**Human-feedback re-review verdict: `revise`.**

## Human-feedback correction re-review, 2026-11-13

Reviewed `fdbe268..31b2eb0` for the finding below and adjacent regressions.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| MS02-H-T-DISC-1 | resolved | `modules/m03/assessments/M03-L03.md:18,74–78`, `modules/m03/lessons/M03-L03.md:55`, and `modules/m03/evidence/M03-L03.md` distinguish the tier-wide 100 outstanding proxy attempts from active receiver work. The receiving service has its own admission control and safe cancellation. The model propagates the remaining deadline and clamps each attempt to the smaller of 180 ms and remaining time. Discovery age remains tied to the last successful refresh, and the charge still requires a covered same-key replay or authoritative terminal evidence before a new key. | [gRPC deadlines, server handling and propagation](https://grpc.io/docs/guides/deadlines/#deadlines-on-the-server) · [AWS Builders' Library, idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) |

**Correction re-review verdict: `ready-for-human-review`.**

## PR #66 original-call error budget technical review, 2026-11-13

Reviewed `99dd109..f1bda28` at PR head `f1bda28` (assessment change `00875c4`). Scope covers the EX-1 prompt, reference answer and rubric, with the lesson's deadline and concurrency controls as context.

| ID | Severity | Status | Location | Finding and suggested correction |
| --- | --- | --- | --- | --- |
| M03-L03-T-OVERLOAD-1 | major | open | `modules/m03/assessments/M03-L03.md:78`, against EX-1 at line 20 and the policy at lines 74 and 76 | The model answer assumes an average 200 ms occupancy for each outstanding proxy attempt while the same policy caps every upstream attempt at 180 ms or less. It defines no post-attempt slot retention that could account for the difference. The 500 attempts/s arithmetic is valid for a 200 ms mean, but its premise cannot support the example's feasibility decision. The model also leaves the observation window unspecified and does not quantify how the cache cutoff affects it. Use a consistent mean proxy slot hold, such as 160 ms during a saturated phase. At 100 slots this yields at most 625 attempts/s under the stated steady-state assumptions, before charging failures and retries against that throughput. A 95% target at 1,000 original calls/s needs 950 timely original successes/s. Define the cohort by first submissions over the full two-minute fault injection, track each original through its own 500 ms deadline, and quantify the separate failure bound. With a 60 s fail-closed phase and no eligible fallback, even perfect first-minute results give at most 50% timely success across the two minutes. [Little, 1961, theorem and assumptions](https://doi.org/10.1287/opre.9.3.383) · [Google SRE Workbook, What to Measure](https://sre.google/workbook/implementing-slos/#what-to-measure-using-slis) |

The prompt at `modules/m03/assessments/M03-L03.md:20` counts one eligible original call from first submission and requires a successful response by its original deadline. Shedding, rejections, timeouts, late responses and unresolved calls all consume the budget. This keeps the outcome denominator independent of attempt traffic and admitted-only latency. A production test can implement it with caller-side elapsed time and original-call identity, allowing each call's deadline to pass before finalizing the cohort. The 95% illustrative target allows 5% misses. At line 82 the ten-point rubric awards separate credit for bounded admission, quantitative user outcomes, and a failure test that checks both. [Google SRE Workbook, What to Measure](https://sre.google/workbook/implementing-slos/#what-to-measure-using-slis)

The changed answer preserves the technical distinction from `modules/m03/lessons/M03-L03.md:37,55`. The proxy limits outstanding attempts across the tier, and the receiver independently limits active execution. Remaining-time propagation keeps the deadline across retries. The arithmetic applies to proxy slot occupancy only. gRPC documents elapsed-time propagation and the application's responsibility for stopping work it spawned. The exercise makes no version-specific vendor claim. [gRPC deadlines, server handling and propagation](https://grpc.io/docs/guides/deadlines/#deadlines-on-the-server) · [AWS Builders’ Library, Retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

**PR #66 technical review verdict: `revise`.**

## PR #66 round 1 technical re-review, 2026-11-13

Reviewed `f1bda28..fefd326` at pushed head `fefd326`.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M03-L03-T-OVERLOAD-1 | resolved | `modules/m03/assessments/M03-L03.md:74,76,78–82` now models a 160 ms mean proxy slot hold, consistent with the 180 ms remaining-clamped attempt cap. Under the stated steady saturation, 100 / 0.160 gives approximately 625 attempt completions/s. Failures and retries consume the same attempt budget, so 625/s is an optimistic rate for original successes in that phase. The 95% target for the first-submission cohort `[0, 120 s)` at 1,000 originals/s requires 114,000 of 120,000 timely successes, equivalent to a window-average requirement of 950/s. Each original retains its own 500 ms deadline, including those whose deadlines extend past the cohort window. The separate no-fallback, no-continuation assumption makes the cache-cutoff bound valid independently of steady-state arithmetic. Even perfect first-minute results yield at most 60,000 / 120,000 timely successes, or 50%. | [Little, 1961, theorem and assumptions](https://doi.org/10.1287/opre.9.3.383) · [Google SRE Workbook, What to Measure](https://sre.google/workbook/implementing-slos/#what-to-measure-using-slis) · [gRPC Deadlines, server handling and propagation](https://grpc.io/docs/guides/deadlines/#deadlines-on-the-server) |

`modules/m03/lessons/M03-L03.md:55–59` now teaches original-call cohort accounting, how to observe deadlines after the window closes, and the conditions for translating occupancy into attempt throughput. The lesson and answer distinguish proxy slots from active receiver work. The assessment rubric at `modules/m03/assessments/M03-L03.md:86` retains the ten points and separate credit for a defensible original-call error budget and a production test that measures it.

**PR #66 round 1 technical verdict: `ready-for-human-review`.**
