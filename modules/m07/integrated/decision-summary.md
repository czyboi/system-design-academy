---
id: M07-decisions
status: draft
---

# Choose how deferred work completes

## Work a deferred completion decision

A newsroom accepts a video and produces a preview. Keep upload validation and cheap status reads on short request paths. Assign a stable job ID to each accepted preview, hand it off durably and complete by publishing a guarded status change. A timed-out response can leave an accepted job. The job and outbox intent commit before any broker send. The relay retires intent only after SQS `SendMessage` succeeds for the configured queue; uncertain sends retry the same job ID. A worker deletes a delivery using that receive’s receipt handle only after observing terminal state or committing a retry transition and its runnable intent.

An independent reconciler scans due pending jobs and expired running claims, including when the delivery is missing. It conditionally fences the current token and atomically reserves a waiting slot and one retry intent, subject to deadline and attempt budgets. If the waiting cap is full, it commits terminal overload instead of creating an extra waiter. A recovery generation, due time and bounded cooldown prevent repeated scans from flooding the queue. The stale worker cannot publish, but its physical execution permit remains occupied until it actually stops; any replacement needs a separate permit and shares the dispatch cap. Preserve the original identity and deadline, release the job reservation once at terminal state, and stage a durable readable immutable object before guarded publication. This is one acceptable recovery design; equivalent guarded workflows can satisfy the same contract.

A separate distribution event may need independent consumers and retained history. Store it in a log when replay and per-key ordering justify the added retention and lag management. Rebuilding a projection remains a distinct task from executing the preview job. Choose by consumer progress and effect semantics as well as by throughput.

## Compare completion, ordering and replay needs

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Caller needs a cheap result now | Synchronous call | Do bounded work on request path | Immediate outcome | Dependency latency consumes caller deadline | Timeouts under peak load | Work is lengthy and can be deferred | [M07-L01](../lessons/M07-L01.md) |
| One task needs an eligible worker | Message broker | Deliver, acknowledge, redeliver under a broker contract | Decoupled delivery | Visibility, acknowledgement and poison-message handling | Redelivery spikes or old pending jobs | Independent replay is central | [M07-L01](../lessons/M07-L01.md) |
| Deferrable job needs status and bounded execution | Task executor | Use a durable job, bounded claims, a retry budget and guarded result | Recoverable processing with client status | Job state and admission coordination | Queue age or retries exceed budgets | Caller requires immediate cheap completion | [M07-L01](../lessons/M07-L01.md), [M07-L02](../lessons/M07-L02.md) |
| Several consumers need independent replay | Partitioned retained log | Assign partitions and save a position per group and partition | Retained input for independent processors | Retention, checkpoints and hot-key limits | Saved cursor older than retained data | Only one bounded job should consume an item | [M07-L03](../lessons/M07-L03.md) |
