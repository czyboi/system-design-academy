---
id: M03-EX1
status: draft
outcomes: [M03-S1]
---

# Service boundaries for catalogue publishing

A catalogue has an editor API, an item database and a preview renderer. In a hypothetical load test, a peak of 900 metadata requests and 30 preview requests per second saturates shared CPU and pushes metadata p99 from 120 ms to 430 ms. The metadata target is 200 ms p99. Editors can wait up to two minutes for previews and see their progress. Editors may update an item while its preview is rendering. Editors approve specific item versions. A public preview must match the current version and its approval.

For a modeled 60-second peak-load failure drill, hold item versions fixed. Test deliberate edits, revocations and supersession separately as correctness cases so legitimate cancellation does not count against the capacity SLO. In the stable-version load cohort, **at least 99% of original valid metadata requests** must succeed within one second of first submission; rejected, unresolved and timed-out requests fail this objective. The metadata p99 target of 200 ms applies separately to successful responses measured from their first submission, including waits and retries. **At least 99% of original valid preview submissions** must be durably accepted within one second, and **at least 99% of all original valid preview submissions** must produce an eligible completed preview within two minutes of original submission. Rejected, failed, expired, superseded-without-replacement or late submissions are misses in this drill; correctness tests must also prove no obsolete/unapproved preview is published. These are scenario targets to be verified, not automatic consequences of a capacity design.

Two mobile client versions coexist. Clients sometimes retry a create after losing the response. A renderer can accept work durably and then lose its reply. A rolling deploy can leave a stopped renderer in discovery results. For one dispatch cycle, assume a 300 ms total wait budget, a 120 ms first attempt, up to 30 ms of jittered delay and a healthy alternate that responds in 60 ms.

## M03-EX1

1. Compare a modular application with isolated renderer capacity, a separately deployed renderer, and a service per catalogue entity. Choose one and assign ownership of item version, publication state, rendering and retries. Identify the invariant and the transaction that protects it.
2. Define the editor-facing create and status interfaces and the renderer operation. Trace request and reply. Specify duplicate requests, compatibility and how a delayed result for an older version is handled.
3. Compare caller-side and intermediary-side endpoint selection for this workload. Trace the stopped renderer and a lost reply after acceptance. Specify remaining deadline, attempt ownership, bounded concurrency and behavior while discovery is unavailable.
4. Define pass criteria for original-request success, successful-response p99, original-preview completion and for correctness tests that force concurrent publication, edit and revocation in different orders. State which results would justify your split.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M03-S1

Choose a service boundary, trace its contract and defend the discovery and retry policy. Use [application boundaries](../lessons/M03-L01.md), [REST and RPC contracts](../lessons/M03-L02.md) and [service discovery](../lessons/M03-L03.md).
