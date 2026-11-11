# M01-L02 technical and provenance review

Checked 2026-11-11. Reviewed the teaching draft, companion, evidence, and pinned curriculum inputs recorded in the verdict.

## Technical findings

- **L02-T1 · minor · Worked example and companion answer key, shared backend.** The upper bound of 30 queued requests/s or 300 over 10 seconds assumes the backend actually receives all 120 operations/s. The two balanced 65/s frontends can supply that rate in the modeled scenario if backend waits leave submission capacity available. The single 100/s frontend can shift some backlog upstream. Identify the scenario that yields the upper bound and distinguish offered demand from backend arrivals. [Microsoft Azure Architecture Center, Application design considerations](https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling#application-design-considerations) · [Google SRE, Queue Management](https://sre.google/sre-book/addressing-cascading-failures/#queue-management).
- **L02-T2 · minor · Core concepts and mechanisms, successful-request p99.** Use “about 99%” or define the percentile as a threshold containing at least 99% under a specified empirical quantile convention. A tied value can contain more observations. The distinction between successful requests and errors or timeouts is sound. [Google SRE, The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals).

The single server adds 200 requests and drains in 200 ÷ 30 ≈ 6.7 s under the fluid assumptions. The last burst arrivals face about 2 s of queue wait at 100 completions/s. The balanced pair receives 60/s each, a 70/30 split sends 84/s to one worker, and a survivor with capacity 65/s falls short of the 70/s normal arrival rate. Comparing useful throughput at matched targets, profiling dependencies, and accounting for state-placement and failure limits are supported. The modeled rates are not reported as measurements. [Vogels, A Word on Scalability](https://www.allthingsdistributed.com/2006/03/a_word_on_scalability.html) · [Dean and Barroso, The Tail at Scale, abstract](https://research.google/pubs/the-tail-at-scale/) · [Google SRE, Demand Forecasting and Capacity Planning](https://sre.google/sre-book/introduction/#demand-forecasting-and-capacity-planning).

## Provenance findings

The evidence traces substantive claims to the author's essay, research abstract, and official practice documents. The workload and queue arithmetic are original. Sources are cited for facts and guidance, with no copied figures, code, or other third-party assets. The Primer credit includes author, pinned revision, CC BY 4.0, and changes. No implied endorsement was found. [Primer license at pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt).

Verdict: **ready-for-human-review**.
