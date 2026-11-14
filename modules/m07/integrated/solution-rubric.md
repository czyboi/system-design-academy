---
id: M07-EX1-solution
status: draft
---

# Reference design and rubric

## Reserve work and persist the handoff

Use an ingress record keyed by caller and submission key to retain the immutable upload version and first-seen arrival time across retries, including definite admission rejections. Keep it through the promised retry window. Verify matching input and derive the same absolute deadline for retries. If ingress cannot establish or read that record, fail admission until the original identity and deadline can be resolved. In one job-store transaction, atomically check that the caller/key does not already have an accepted job, reserve capacity, and create a `pending` job and outbox entry. Return the job ID after commitment. A definite capacity rejection reserves no job slot and produces no runnable intent. A caller that loses the response retries with the same key and resolves commitment before receiving an acceptance result. A committed retry receives its original job ID without another reservation. [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), [M07-L01](../lessons/M07-L01.md).

| Job transition | Durable guard and recovery |
| --- | --- |
| Original → pending | Persist admission and the corresponding outbox row together. |
| Pending → running | After a successful send to the configured queue the relay may retire that outbox row. It retains uncertain sends and retries the stable job ID. The worker checks the job's scheduled time and deadline, passes the dispatch controls and obtains a claim with an expiry and increasing attempt token before executing. A duplicate that finds a live claim can wait or become visible again. It cannot start another claim against the same job. |
| Running → pending | On retryable failure under the current claim or after an abandoned claim expires, fence that claim and schedule a durable retry intent with the same job ID and deadline when budgets permit. A worker can delete its delivery after a retry transition and runnable intent commit. Without that proof, leave the delivery recoverable. |
| Running → succeeded | Stage the preview as a readable, immutable private object. At the transition, require the current unexpired claim, eligible job state and remaining deadline. Commit the winning link, terminal status and reservation release together. |
| Pending or running → failed | Require permanent invalidity of the immutable input, the application deadline, or job-level attempt exhaustion after the last claim has failed or expired. Preserve an already committed terminal result and release its reservation only once. |

When redelivery follows a crash after publication, read terminal status and delete using the current receive's receipt handle. A former attempt cannot publish after its claim was superseded. Old handles can appear successful without deleting the message. A sweeper deletes a staged object only after confirming terminal status at the authority and excluding the immutable winning reference. A DLQ delivery is evidence about one message. An eligible live attempt may still succeed. Scan for aged pending jobs without a live claim even if no DLQ record exists. Atomically record one replacement outbox intent for the selected recovery generation and schedule it within the application budget. An older duplicate remains safe at claim time. If the job expires, commit guarded terminal failure. [SQS Standard delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html), [SQS DeleteMessage](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteMessage.html), [SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html).

## Size and trace the overload policy

The wait budget is 3 − 1 = 2 s, so baseline waiting capacity is 100 jobs. With 50 running, the total cap is 150. Count one accepted job across outbox, queue and delayed retry states, and separate waiting and in-flight limits. The burst would create `(80 − 50) × 5 = 150` waiting jobs without a cap. With the cap, at most 350 of 400 can be accepted and complete on time in the ideal no-retry model. The 50 rejected jobs make success 87.5%. At 35 later arrivals/s, 100 waiting jobs drain in `100/(50 − 35) ≈ 6.67 s`. That is the time until the backlog vanishes under continued arrivals.

The target needs at least 392 originals. With a 100-job waiting cap, the ideal minimum during the burst is `(392 − 100)/5 = 58.4` starts/s. At 60 starts/s, peak waiting is 100 jobs, or about 1.67 s. Running plus waiting need capacity for 160 jobs. All 400 can fit in the ideal model. This depends on the higher measured rate holding through the tail and on the model's execution and handoff times. Protect dependency starts with a separate dispatch cap, and enforce in-flight concurrency and admission as separate controls. When the measured dependency slows, reduce admission or shed before promising a deadline that the queue cannot meet. Existing jobs keep their reservations and deadlines.

Retry at one coordinating layer for transient errors. An illustrative policy allows one additional execution per job and at most five retry starts/s inside the shared 60 starts/s cap. Apply capped jitter and admit a retry only when estimated cooldown, queueing, execution and result visibility fit the original deadline. Recheck at dispatch. For example, if 900 ms remains and cooldown, waiting and completion are estimated at 150, 250 and 600 ms, a retry would exceed the remaining budget. A retry token cannot change that timing. Retry starts share the same dependency capacity. If five per second are used, at most 55 fresh starts/s remain, so the no-retry burst result cannot certify the target. Track queue age and retry demand to detect a loop where timeouts add more work to the same tight capacity. [M07-L02](../lessons/M07-L02.md), [Google SRE, Latency and Deadlines](https://sre.google/sre-book/addressing-cascading-failures/#latency-and-deadlines).

## Score the fault drill

384 / 400 = 96%, below 98% by eight successes. The reject, unfinished and failure categories remain in the denominator. Test a crash after idempotent acceptance, duplicate send after an uncertain response, expiry during a paused worker, stale worker publication, and delivery disappearance. Correlate each original key with acceptance, queue start, attempt claim, result commit and a successful client retrieval by the deadline. Compare first-attempt versus retry load and rejection against actual queue age. Invalid input should reach one terminal failure and consume no further starts. A late or unavailable result remains a miss even if capacity is within its envelope.

| Criterion | Points | Full credit |
| --- | ---: | --- |
| Durable acceptance and lifecycle | 3 | Gives one identity and one recoverable job, distinguishes queued/running/terminal states and handles arrival or acknowledgement uncertainty. |
| Effect and recovery | 3 | Fences stale and duplicate attempts, preserves the winning output and traces DLQ, invalid input and missing-delivery recovery. |
| Queue and retry budgets | 3 | Computes both cap types, rejection, model success and drain. Explains feasible scaling and retry time and rate controls. |
| Client outcome | 1 | Scores the all-original cohort and identifies usable-result evidence. |

Accept equivalent durable workflows and delivery choices that preserve the declared SQS and job contracts. Award partial credit for correct traces with incomplete justification.
