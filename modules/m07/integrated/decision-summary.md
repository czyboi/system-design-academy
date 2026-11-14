---
id: M07-decisions
status: draft
---

# Choose how deferred work completes

## Work a deferred completion decision

A newsroom accepts a video and produces a preview. Keep upload validation and cheap status reads on short request paths. Assign a stable job ID to each accepted preview, hand it off durably and complete by publishing a guarded status change. A timed-out response can leave an accepted job. A broker acknowledgement after the job commit can be retried without repeating the visible result. Bound waiting and active work and recheck the user's deadline before any retry.

A separate distribution event may need independent consumers and retained history. Store it in a log when replay and per-key ordering justify the added retention and lag management. Rebuilding a projection remains a distinct task from executing the preview job. Choose by consumer progress and effect semantics as well as by throughput.

## Compare completion, ordering and replay needs

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Caller needs a cheap result now | Synchronous call | Do bounded work on request path | Immediate outcome | Dependency latency consumes caller deadline | Timeouts under peak load | Work is lengthy and can be deferred | [M07-L01](../lessons/M07-L01.md) |
| One task needs an eligible worker | Message broker | Deliver, acknowledge, redeliver under a broker contract | Decoupled delivery | Visibility, acknowledgement and poison-message handling | Redelivery spikes or old pending jobs | Independent replay is central | [M07-L01](../lessons/M07-L01.md) |
| Deferrable job needs status and bounded execution | Task executor | Use a durable job, bounded claims, a retry budget and guarded result | Recoverable processing with client status | Job state and admission coordination | Queue age or retries exceed budgets | Caller requires immediate cheap completion | [M07-L01](../lessons/M07-L01.md), [M07-L02](../lessons/M07-L02.md) |
| Several consumers need independent replay | Partitioned retained log | Assign partitions and save a position per group and partition | Retained input for independent processors | Retention, checkpoints and hot-key limits | Saved cursor older than retained data | Only one bounded job should consume an item | [M07-L03](../lessons/M07-L03.md) |
