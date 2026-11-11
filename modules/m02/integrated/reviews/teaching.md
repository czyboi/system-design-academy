# M02 module synthesis coverage and pedagogy review

## Scope and sources

Reviewed the integrated exercise, reference solution, decision summary, evidence and approved SDA-v1 outline for middle and senior engineers. Cross-checked the linked lesson mechanisms against the accepted M02 teaching artifacts. Their topic evidence uses [The System Design Primer, DNS through reverse proxy](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L581-L764) and [communication mechanisms](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1370-L1440), revision ae9bbd7b02d90b9866215de185217d33f39ab733. This is a synthesis review. The lesson companions retain their own assessment coverage.

## Synthesis coverage

| Approved input | Exercise evidence | Reference and rubric evidence |
|---|---|---|
| M02-L01-LO1 | M02-EX1 task 1 asks for the DNS-to-edge trace and R1/R2 selection at +60 s. Task 4 asks how to observe convergence. | DNS, connections and routing derives +90 s expiry for R1, traces R2's fresh lookup and names connection reuse, client caching and serve-stale as assumptions to recheck. DNS trace and Verification criteria. |
| M02-L03-LO2 | Task 2 requires protocol and TLS boundaries and a justified choice of L4 versus L7. | DNS, connections and routing traces separate encrypted legs, path selection, flow balancing across equivalent ingress replicas and redundant capacity. Request path criterion. |
| M02-L04-LO2 | Tasks 1 and 3 require hit/miss handling, media and private cache policy, origin load, replacement and outage behavior. Task 4 asks how to verify overload and freshness. | Cache behavior and origin capacity derives 200 and 2,160 fetches/s, gives the conditional 240 fetches/s coalescing result, and separates eligible stale public data, cold misses and private responses. Capacity and freshness and Verification criteria. |

The three approved inputs jointly support M02-S1, tracing DNS-to-origin delivery and justifying proxy and CDN choices. The exercise also applies transport knowledge and points to the accepted M02-L02 revision in both the brief and decision summary. The synthesis introduces no new assigned Primer topic; module validation will consolidate the accepted current lesson topic and outcome evidence.

## Pedagogy and assessment

The English brief provides a bounded, coherent workload, two independent incidents and new numerical assumptions, so the exercise requires transfer rather than reproduction of a lesson example. Each problem part has a corresponding rubric row with observable evidence. The reference solution checks the overloaded and mitigated origin rates against the stated capacity and conditions, then distinguishes the stale age of 110 s from the 300 s limit. It offers design choices and permits alternatives that preserve private isolation. The decision summary gives five engineering triggers with all requested fields and points to the current lesson path for each decision.

- **M02-SYN-P1, minor.** The Verification criterion expects an explicit freshness signal. The sample solution gives an age calculation and tells the learner to test old references, but does not name a concrete signal such as response Age interpreted against the configured freshness lifetime, an edge stale-serve indicator, or the served version recorded during a failure drill. The exercise, policy and grading criterion are already clear.

No material synthesis coverage, pedagogy or language finding identified.

## Verdict

ready-for-human-review.
