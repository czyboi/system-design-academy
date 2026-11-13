---
id: M03-EX1
status: draft
outcomes: [M03-S1]
---

# Service boundaries for catalogue publishing

A catalogue has an editor API, an item database and a preview renderer. In a hypothetical load test, a peak of 900 metadata requests and 30 preview requests per second saturates shared CPU and pushes metadata p99 from 120 ms to 430 ms. The metadata target is 200 ms p99. Editors can wait up to two minutes for previews and see their progress. Editors may update an item while its preview is rendering. Editors approve specific item versions. A public preview must match the current version and its approval.

For a 60-second peak-load failure drill, hold item versions and their approvals fixed. The cohort consists of original valid operations first submitted in [0, 60 seconds); retain that first timestamp and one identity across retries. Follow each operation through its own deadline, including the last preview through first submission plus 120 seconds. Measure four independent targets:

- At least 99% of original metadata operations receive a successful response within one second of first submission. Rejection, failure, timeout, a missing response and a late response are misses.
- The p99 elapsed time from first submission to response is at most 200 ms among metadata operations whose successful responses arrive within that one-second deadline. Include waits and retries; report this population and the success rate together.
- At least 99% of original preview submissions reach durable catalogue admission within one second of first submission. Admission means the catalogue has committed the job, identity and pending dispatch; separately report when the client receives its acknowledgement and status link.
- At least 99% of original preview submissions have a usable, authorized result for the submitted item and version through the catalogue status contract within 120 seconds of first submission. Worker completion alone does not meet this target.

Rejected, failed, expired, unexpectedly cancelled, unresolved and late preview submissions are misses for any target whose event did not occur by its deadline. A timely durable admission remains an admission success even if the job later fails readiness. Deliberate edits, revocations and supersession belong to separate correctness cases, not this stable-version cohort. The discovery outage crossing the cache-age limit is an operational fault drill. These are scenario targets to verify, not measured results.

Two mobile client versions coexist. Clients sometimes retry a create after losing the response. A renderer can accept work durably and then lose its reply. A rolling deploy can leave a stopped renderer in discovery results. For one dispatch cycle, assume a 300 ms total wait budget, a 120 ms first attempt, up to 30 ms of jittered delay and a healthy alternate that responds in 60 ms.

## M03-EX1

1. Compare a modular application with isolated renderer capacity, a separately deployed renderer, and a service per catalogue entity. Choose one and assign ownership of item version, publication state, rendering and retries. Identify the invariant and the transaction that protects it.
2. Define the editor-facing create and status interfaces and the renderer operation. Trace request and reply. Specify duplicate requests, compatibility and how a delayed result for an older version is handled.
3. Compare caller-side and intermediary-side endpoint selection for this workload. Trace the stopped renderer and a lost reply after acceptance. Specify remaining deadline, attempt ownership, bounded concurrency and behavior while discovery is unavailable.
4. Define and independently evaluate all four targets, including durable preview admission, using the stated event times and populations. Provide a reproducible actual test or explicitly labeled model with arrival pattern, capacity and service assumptions, fault onset and duration, observations and results; compare viable boundaries under the same schedule. Follow the cohort to each deadline and include an operational discovery outage that crosses your cache-age limit. Separately test cancellation and concurrent publication, edit and revocation in different orders. State which results justify your split.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M03-S1

Choose a service boundary, trace its contract and defend the discovery and retry policy. Use [application boundaries](../lessons/M03-L01.md), [REST and RPC contracts](../lessons/M03-L02.md) and [service discovery](../lessons/M03-L03.md).
