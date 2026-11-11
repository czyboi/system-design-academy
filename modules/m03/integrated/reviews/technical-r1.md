# Independent technical and provenance recheck — M03 synthesis

Reviewed 2026-11-11.

## Technical findings

- **M03-INT-TP1 · Major · Resolved.** The revised **Ownership and deployment** solution keeps version, approval and public pointer on one authoritative row. The pointer update itself checks version and approval. An edit or revocation that wins the race causes the guarded update to fail. If publication wins, the subsequent edit or revocation clears the pointer atomically. The decision summary describes the same mechanism and the rubric checks both orderings. The PostgreSQL example scopes predicate re-evaluation to a concurrent update of the same target row under Read Committed. [PostgreSQL 18 §13.2.1](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED)
- **M03-INT-TP2 · Minor · Resolved.** The revised `StartRender` contract uses a unique durable work ID, an atomic insert in state shared by eligible endpoints, and a compatibility check on immutable inputs. Concurrent matching attempts resolve the same accepted job. A mismatched reuse is rejected. The render output and completion handler remain repeat-safe when processing itself restarts. [AWS Builders' Library, making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

The revised discovery trace distinguishes an endpoint that accepted no work from acceptance followed by a lost reply. Both can consume the 120 ms attempt limit from the dispatcher's perspective. With the full 30 ms backoff, 150 ms remains for the second attempt. A 60 ms response leaves 90 ms. The dispatcher retains the same work ID, owns at most two attempts per cycle, limits concurrency and defers within an overall expiry policy when it cannot safely choose a destination or obtain a definitive response. The unchanged brief is consistent with both branches. [gRPC deadline guidance](https://grpc.io/docs/guides/deadlines/) [AWS Builders' Library, bounded retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

## Provenance findings

No material provenance finding. The revised solution links the PostgreSQL concurrency behavior to the exact version and section and cites AWS for the general retry design. The reference trace and data model remain original. The current brief, solution, summary and evidence reproduce no third-party assets.

## Verdict

`ready-for-human-review`
