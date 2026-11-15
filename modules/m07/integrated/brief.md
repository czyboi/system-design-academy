---
id: M07-EX1
status: draft
outcomes: [M07-S1]
---

# Process media without losing accepted jobs

A media service generates a small preview from a durable, immutable upload. A client submits the upload version and a caller-scoped key and polls status. A matching retry uses the same identity and original deadline. A job may execute more than once. It may expose at most one immutable output reference. Invalid input is a permanent failure. Assume one SQS Standard queue with a configured destination URL, an authoritative job store and private attempt staging.

| Quantity | Assumed envelope |
| --- | --- |
| Offered burst | 80 original valid jobs/s for 5 s, then 35/s. At the start the fleet already runs at capacity and no job waits. |
| Baseline service | A homogeneous FIFO fluid model can start 50 jobs/s while busy. From start to usable result takes 1 s. For this model assume no retries or execution failures. |
| Deadline | Usable result by 3 s from first submission arrival. Set a separate waiting cap and cap total nonterminal work across all delivery locations. |
| Candidate increase | A measured dependency envelope can sustain 60 starts/s in a proposed configuration, with the same one-second duration. Test the remaining deadline and total capacity after the change. |

In a separate fault drill, measure 400 original valid submissions over the five-second burst window. Count each original once from first arrival to when its correct preview is usable through the client-facing status and retrieval path. Observe each original through its full three-second deadline. The target is 98% on time. The trial recorded 384 on-time, eight rejected without subsequent acceptance, five accepted but unfinished at the deadline and three terminal failures. Accepted-only latency is diagnostic.

## M07-EX1

1. Draw the admission, dispatch, execution and terminal states. Define the identity, durable acceptance point and conditions for acknowledging a delivery. Trace a lost acceptance reply and a worker crash after publication and before acknowledgement.
2. Compute the waiting and nonterminal limits, rejected originals, burst success and backlog drain at baseline. Defend the proposed change and test its admission and dispatch bounds. Set a deadline-aware retry policy with a shared dispatch limit.
3. Trace an unusable input, a live worker racing a DLQ observation, and an expired running claim whose delivery no longer exists. For the last case, test both an available waiting slot and a full waiting queue while the old execution may still be running. Score the fault drill and state what evidence would distinguish overload from lost work or duplicate effects.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M07-S1

Trace a duplicate-safe job lifecycle and defend its overload policy. [Queue lifecycle](../lessons/M07-L01.md) · [Back pressure and retries](../lessons/M07-L02.md).
