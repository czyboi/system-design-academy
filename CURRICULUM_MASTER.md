# Master Curriculum — System Design Academy

**Status:** Proposed map; modules are not yet fully authored.

| Module | Topics | Learning outcome |
|---|---|---|
| 01. Fundamentals | Requirements, performance, scalability, latency, throughput, availability | Translate requirements into measurable system constraints |
| 02. Capacity estimation | QPS, concurrency, storage, bandwidth, peak load, headroom | Estimate workload and identify likely bottlenecks |
| 03. Networking & edge | DNS, HTTP, TCP/UDP, TLS, CDN, reverse proxy, load balancing | Explain request paths and edge-level design choices |
| 04. Application architecture | Monoliths, services, API design, service discovery, gateways | Choose service boundaries and communication patterns |
| 05. Databases | Modeling, indexing, transactions, replication, partitioning, sharding, recovery | Design a data layer against workload and consistency needs |
| 06. Caching | Cache patterns, eviction, invalidation, TTL, stampede, consistency | Design cache behavior and reason about stale data/failure |
| 07. Async processing | Queues, streams, delivery semantics, ordering, retries, idempotency, backpressure | Design reliable asynchronous workflows |
| 08. Distributed systems | CAP, consistency models, consensus concepts, coordination, clocks, failure detection | Reason about distributed behavior under partial failure |
| 09. Production systems | SLO/SLI, observability, resilience, security, DR, cost | Design systems that can be operated and recovered |
| 10. Case studies | URL shortener, feeds, crawler, notification, chat, scheduler, payment | Defend an end-to-end architecture through explicit trade-offs |

## Curriculum rules

- Dependencies must be explicit; do not teach a topic before its prerequisites without a short primer.
- Distinguish core curriculum from optional/vendor-specific deep dives.
- Every module must include an applied design exercise.
- Avoid duplicating the same explanation across modules; cross-reference shared concepts.
- Case studies should reuse concepts from earlier modules and introduce no hidden prerequisites.

## Database pilot

The current Database pilot is located at `modules/database/`. It is a structure and content-quality experiment, not yet a commercially approved module.
