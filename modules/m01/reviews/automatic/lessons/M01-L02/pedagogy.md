# M01-L02 targeted pedagogy and coverage review

Reviewed 2026-11-12 in lesson mode after the PR #55 revision. Scope is the new “Same load, different p99” explanation, its connection to the existing lesson and companion assessment, and the two source topics assigned to M01-L02. The audience is experienced middle and senior engineers. The prior [module review](../../pedagogy.md) supplies the recorded review context for unchanged material.

## Coverage

The approved [M01-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l02) assigns performance versus scalability, latency versus throughput, queueing and tail behavior. The source map is Donne Martin's *System Design Primer* at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

| Topic | Teaching evidence | Status |
| --- | --- | --- |
| PR-H032, performance versus scalability, `README.md#L412` | [Measure the request and the workload](../../../../lessons/M01-L02.md#measure-the-request-and-the-workload) distinguishes deployment performance under a stated workload from capacity gained with resources. The burst example compares the resulting choices. | taught |
| PR-H034, latency versus throughput, `README.md#L426` | The same measurement section defines request latency and completion throughput. [Same load, different p99](../../../../lessons/M01-L02.md#same-load-different-p99) connects arrival timing to the slow tail at a fixed offered workload. | taught |

## Pedagogy and assessment

The new example makes the comparison traceable. It fixes 115 arrivals, 8 ms of CPU work per request and a 10 ms remaining response path. The table contrasts a smooth schedule with a short group of simultaneous arrivals, then identifies the nearest-rank observation and compares it to the scenario's 75 ms target. The text labels the values hypothetical and directs learners to replay realistic bursts. This addresses the requested teaching improvement without presenting the illustrative samples as measured production behavior.

The existing [companion](../../../../assessments/M01-L02.md) remains answerable from the lesson. Q3 asks which measurement estimates p99, Q6 evaluates latency and errors together, and EX-1 asks the learner to evaluate a burst and propose a measurement plan. The existing outcome map retains Q1–Q3 for tracing and modeling, and Q4–Q6 plus EX-1 for decisions. No new assessment item is needed for the added illustration.

No actionable pedagogy or coverage findings arose in this targeted review.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and the assigned curriculum topics.
