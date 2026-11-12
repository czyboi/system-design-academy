# M01-L02 targeted technical and provenance re-review

## Findings

No open technical or provenance findings in the changed scope.

| Reference | Status | Evidence |
| --- | --- | --- |
| PR #55 comment 3 | resolved | [Same load, different p99](../../../../lessons/M01-L02.md#same-load-different-p99) compares two deterministic FIFO arrival traces at the same offered rate and CPU demand. [Owner feedback](https://github.com/czyboi/system-design-academy/pull/55#issuecomment-6820605428) |

## Technical and source checks

- Reviewed the M01-L02 changes from `e2158e2` to draft handoff `434dc63` on 2026-11-12. Both traces offer 115 requests in one second, consuming 920 ms of CPU work. The smooth spacing exceeds 8 ms, so every latency is 18 ms. The batched CPU completions are 8 through 96 ms in steps of 8 ms. With 10 ms added, the two largest latencies are 98 and 106 ms. The other 103 requests arrive when the slot is available and each takes 18 ms. Nearest-rank p99 uses sorted position 114, giving 18 ms and 98 ms. Only the smooth sample meets the 75 ms p99 target under the modeled assumptions. [Lesson trace and percentile](../../../../lessons/M01-L02.md#same-load-different-p99)
- The one-replica traces preserve the original 115 requests/s per B replica and the 8 ms service time. The earlier A fluid-model calculation of 60 queued requests and 0.75 s to drain remains separate. The added trace leaves companion Q2's one-second backlog and Q6's joint evaluation of p99 and failures intact. [Lesson burst model](../../../../lessons/M01-L02.md#trace-the-burst-and-the-queue) · [Companion knowledge checks](../../../../assessments/M01-L02.md#knowledge-checks)
- The trace inputs and output latencies are identified as hypothetical. The cited Google SRE section supports inspecting distributions because mean CPU utilization can conceal a slow tail. The example uses original tabulated arithmetic and introduces no third-party assets or product-version claims. [Google SRE, Worrying About Your Tail](https://sre.google/sre-book/monitoring-distributed-systems/#worrying-about-your-tail-or-instrumentation-and-performance)

**Verdict: ready-for-human-review.**
