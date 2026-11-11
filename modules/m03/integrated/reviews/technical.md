# Independent technical and provenance review — M03 synthesis

Reviewed 2026-11-11.

## Technical findings

- **M03-INT-TP1 · Major · Open.** Solution, **Ownership and deployment** and **Self-evaluation**; decision summary, transactional-owner row. The reference design checks version and approval “in the same transaction that updates the public pointer.” If a completion handler reads version 7 as approved, another transaction commits an edit or revocation, and the handler unconditionally updates the pointer, the now-ineligible preview can be published under ordinary Read Committed isolation. Require a guarded update on the authoritative item row that tests the current version and approval and publishes in a single atomic operation, or a locking/serialization design that coordinates with edits and revocations. Award full credit for a mechanism that closes this race. PostgreSQL 18 provides a concrete example of Read Committed statement snapshots and re-evaluation of a conditional update against a concurrently updated target row. [PostgreSQL 18 §13.2.1](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED)
- **M03-INT-TP2 · Minor · Open.** Solution, **Public and internal contracts**, `StartRender` row. The shared durable work ID and retention window correctly let another renderer resolve an accepted call. Explicitly use atomic create-if-absent or an equivalent uniqueness guarantee for the immutable input bound to that work ID so overlapping attempts cannot both create logical jobs. Return the existing compatible record after a conflict. [AWS Builders' Library, making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

The deployment alternatives are credible under the hypothetical CPU and latency inputs. The reference distinguishes HTTP acceptance, internal work acceptance and eventual completion, uses stable job identifiers across retry, and recognizes that an ambiguous timeout cannot prove an effect absent. At maximum jitter the second call starts at 120 + 30 = 150 ms, with 150 ms left. Its 60 ms response arrives at 210 ms, leaving 90 ms. A single attempt owner, a shared deadline, bounded concurrency, bounded later dispatch and an expiry policy address overload and stale discovery. [RFC 9110 §15.3.3](https://datatracker.ietf.org/doc/html/rfc9110#section-15.3.3) [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/) [AWS Builders' Library, bounded retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) [Azure microservices architecture](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)

## Provenance findings

No material provenance finding. The catalogue workload and request contracts are original exercise inputs. The evidence links primary documentation for architecture, protocols and retry guidance, and the exercise references the Academy lessons for mechanism context. No third-party diagrams, code, or other assets are reproduced.

## Verdict

`revise`
