# M01 integrated design technical and provenance review

Checked 2026-11-11. Reviewed the brief, reference solution and rubric, decision summary, evidence, and pinned curriculum inputs recorded in the verdict.

## Technical findings

- **MI-T1 · minor · Solution rubric, Operation histories, fallback lag.** The brief explicitly assumes a conservative lag bound and declines fallback when it is unknown. Explain one source for such a bound, such as a source-certified timestamp through which all writes are represented in a locally applied contiguous prefix. The age of that proof, including clock uncertainty, can conservatively limit the duration of a degraded response after disconnection. The applied offset alone cannot establish time freshness. [Google SRE Workbook, A Worked Example, freshness and quality indicators](https://sre.google/workbook/implementing-slos/#a-worked-example).

The rates are 10 and 1 per second on average, 120 and 12 at peak, and 150 and 15 at the capacity test target. At peak the given payloads yield 1.92 Mbit/s read egress and 0.096 Mbit/s write ingress. Thirty days of writes total 2.592 GB logical and 7.776 GB for three full copies. The 200 ms critical-path allocations total correctly and the design calls for measured end-to-end p99. The decision summary conditions extra app capacity on app saturation and calls out shared storage and auth. The availability model uses an either-suffices branch success of 0.999999, combined with one mandatory authorization dependency for 0.9994990005 under the stated assumptions. The solution recognizes correlated outages and failure transitions. [Google SRE Workbook, Non-Abstract Large System Design](https://sre.google/workbook/non-abstract-design/) · [AWS Well-Architected Framework, REL11-BP05](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/rel_withstand_component_failures_static_stability.html).

Policy B changes only the customer display fallback. Writes and refund authorization stay on the authoritative path. The coordinated status check and refund authorization avoids a stale local read being used as authorization. The reference distinguishes client-visible recovery, latency, stale responses and request success. The values and eligibility rules are exercise assumptions with no implied production guarantees.

## Provenance findings

The source notes record sections, dates and scopes for the system design method, indicator choices and prepared capacity. The worksheet, policy histories, decision summary and arithmetic use original hypothetical inputs. The supporting publications are referenced for facts and methods. No third-party assets or implied endorsement were found.

Verdict: **ready-for-human-review**.
