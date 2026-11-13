---
id: M03-EX1
status: draft
outcomes: [M03-S1]
---

# Service boundaries for catalogue publishing

A catalogue has an editor API, an item database and a preview renderer. In a hypothetical load test, a peak of of 900 metadata requests and 30 preview requests per second saturates shared CPU and pushes metadata p99 from 120 ms to 430 ms. The metadata target is 200 ms p99. Editors can wait up to two minutes for previews and see their progress. Editors may update an item while its preview is rendering. Only a preview for the current, approved item version can be published.

Two mobile client versions coexist. Clients sometimes retry a create after losing the response. A renderer can accept work durably and then lose its reply. A rolling deploy can leave a stopped renderer in discovery results. For one dispatch cycle, assume a 300 ms total wait budget, a 120 ms first attempt, up to 30 ms of jittered delay and a healthy alternate that responds in 60 ms.

## M03-EX1

1. Compare a modular application with isolated renderer capacity, a separately deployed renderer, and a service per catalogue entity. Choose one and assign ownership of item version, publication state, rendering and retries. Identify the invariant and the transaction that protects it.
2. Define the editor-facing create and status interfaces and the renderer operation. Trace request and reply. Specify duplicate requests, compatibility and how a delayed result for an older version is handled.
3. Compare caller-side and intermediary-side endpoint selection for this workload. Trace the stopped renderer and a lost reply after acceptance. Specify remaining deadline, attempt ownership, bounded concurrency and behavior while discovery is unavailable. State which observations would justify your split.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M03-S1

Choose a service boundary, trace its contract and defend the discovery and retry policy. Use [application boundaries](../lessons/M03-L01.md), [REST and RPC contracts](../lessons/M03-L02.md) and [service discovery](../lessons/M03-L03.md).
