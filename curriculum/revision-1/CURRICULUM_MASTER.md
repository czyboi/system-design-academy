---
id: SD-COURSE-OUTLINE
status: draft
language: en
source_revision: ae9bbd7b02d90b9866215de185217d33f39ab733
---

# System Design Academy — full-course outline

This is a proposed teaching plan for human review. Independent source coverage and pedagogy review is required; this file does not certify coverage, technical correctness, approval or publication readiness. No lesson text, quiz answers, reference solutions or delivery backlog is authored here.

## Audience, entry knowledge and learning route

For middle/senior engineers who can implement a backend service, use SQL joins/transactions, trace an HTTP request, and reason about hash tables, queues, graphs and asymptotic cost. M00-L01 diagnoses gaps and prescribes a short repair route before dependent work. No cloud-vendor experience is assumed. Course and later learner-facing artifacts use English.

Target capability: turn workload and invariants into an explainable design; estimate capacity; trace failure states; compare alternatives; and revise using evidence. All tracks in this plan contribute to the requested full Primer scope, including OOD and additional domains; none is an excluded optional topic. A learner can postpone a track for pacing, but has not completed the full course until it is covered.

Study order: M00 → M01 → M02 → M03 → M04 → M05 → M06 → M07 → M08 → M09 → M10 → M11 → M12 → M13 → CP-01. M12 may be studied after its listed lesson prerequisites; the linear path avoids forward dependencies. Review each worked example before attempting the separate companion exercise; return to decision criteria after feedback.

## Source boundary and evidence needs

Pinned topic map: [System Design Primer at ae9bbd7b02d90b9866215de185217d33f39ab733](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), inspected 2026-11-10. `curriculum/revision-1/source-inventory.json` classifies all tracked files and enumerates knowledge leaves. `curriculum/revision-1/coverage.csv` maps each topic to an exact lesson and instructional outline item. Locators with #L refer to line numbers at this pinned revision; repeated headings remain unambiguous.

Primer is the topic map, not the sole technical authority. Later lesson research must record primary-source URL/section, date, product/version and unresolved claims. In particular verify old SQL type/query-cache advice, database transaction and consistency semantics, AWS roles/guarantees, transport versions, broker delivery guarantees, security controls, historic latency tables and incomplete/incorrect sample code. Dynamo the paper and DynamoDB the service must remain distinct. No existing source prose or assets are copied into lessons by this outline.

Academy additions include AAAA/TXT DNS records, CSRF controls and URL-safe Base64 comparison. Academy additions needed to make the Primer topics teachable: deadlines/retry budgets/idempotency, tail latency, cache stampedes, outbox/reconciliation, event-time handling, backup/recovery objectives, fencing, file-sync/collaboration mechanisms, rate-limit algorithms, exchange ordering and GC details. These are planned teaching scope; primary evidence is still required before drafting claims.

## Course and module package contract

Each module has a motivating problem, measurable capability, prerequisites, ordered teaching lessons, an integrated design exercise, a separate reference-solution/self-evaluation package, and a decision summary. Each lesson follows problem → mechanism → worked example → trade-offs and when to use/avoid → quick understanding checks. The entries below specify that scope without drafting the lessons or assessment items.

For each lesson, LO1 is to trace/model its named mechanisms in the worked scenario; LO2 is to select/reject an alternative using its decision criteria and failure modes. The future companion assessment maps LO1 to Q1–Q3 and the relevant EX-1 mechanism/flow criterion, LO2 to Q4–Q6 and EX-1 decision/failure criteria. Checks may expand to Q7–Q8 if a distinct outcome needs evidence. Each answer needs an explanation; rubric and explicit outcome map are separate from teaching text. Each module exercise measures its explicit synthesis subset below. The complete per-lesson companion portfolio covers all lesson outcomes; CP-01 assesses the separately named cross-module transfer outcomes.

## Course map

| Module | Capability | Lessons | Prerequisites |
|---|---|---:|---|
| M00 Learning guide and design method | Frame a bounded design, identify evidence gaps, and use feedback to improve it. | 2 | Backend coding, SQL CRUD/joins/transactions, HTTP request handling, basic data structures and asymptotic cost. |
| M01 Workload, performance and distributed guarantees | Quantify workload and express latency, consistency and availability decisions. | 4 | M00 |
| M02 Networking, routing and delivery | Choose the request path and delivery protocol for a concrete service. | 4 | M01 |
| M03 Application boundaries and communication | Design component boundaries, APIs and discovery with explicit failure handling. | 3 | M02 |
| M04 Relational data and scaling | Choose a relational data path and justify each scaling change. | 5 | M03, M01-L03 |
| M05 Storage models beyond relational tables | Match access patterns and invariants to data models and distributed-store mechanisms. | 3 | M04 |
| M06 Caching and memory budgets | Design cache placement, coherence, eviction and distribution for explicit freshness goals. | 3 | M05 |
| M07 Queues, jobs and overload control | Design asynchronous processing with explicit delivery, retry and overload semantics. | 3 | M06, M03-L03 |
| M08 Distributed processing and retrieval mechanisms | Design batch/stream aggregation and scatter-gather retrieval with bounded costs. | 3 | M07, M05 |
| M09 Security, observability and coordination | Build a threat model, evidence loop and coordination boundary into the architecture. | 3 | M08, M01-L04 |
| M10 Worked system compositions | Build and critique complete designs from requirements through failures and scaling. | 8 | M00–M09 |
| M11 Additional design domains | Apply shared mechanisms to every substantive additional Primer prompt. | 9 | M10 |
| M12 Object-oriented design and local invariants | Model responsibilities, invariants and extensible behaviour in all six Primer OOD examples. | 6 | M00-L01, M06-L03; M11-L02 for chat context |
| M13 Architecture reading and synthesis | Extract transferable decisions while identifying dated, missing and unsupported claims. | 1 | M10–M12 |

## M00 — Learning guide and design method

**Problem to solve:** A plausible diagram can hide unstated requirements and missing skills.

**Expected output:** Frame a bounded design, identify evidence gaps, and use feedback to improve it.

**Prerequisites:** Backend coding, SQL CRUD/joins/transactions, HTTP request handling, basic data structures and asymptotic cost.

### M00-L01 — How to learn and check readiness

**Prerequisites:** Entry assumptions

**Outcomes:** M00-L01-LO1: trace/model the mechanisms below in the worked scenario. M00-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Diagnostic: trace an HTTP request, SQL transaction, hash lookup and queue consumer.
2. Study routes: prerequisite repair, first pass, deliberate practice and spaced retrieval; adjust breadth/depth and some/many/most practice to short/medium/long timelines and experience.
3. Evaluate diagrams by decisions and failure evidence; use historical architectures as context.

**Worked-example plan:** Plan a study route after discovering a gap in transaction reasoning.

**Trade-offs and when to use/avoid:** Select repair material by observed gaps; avoid memorising technology menus or copying reference diagrams.

**Quick-check focus:** Explain which prerequisite gap would prevent reasoning about a repeated payment request. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M00-L02 — From requirements to a defensible design

**Prerequisites:** M00-L01

**Outcomes:** M00-L02-LO1: trace/model the mechanisms below in the worked scenario. M00-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Clarify actors, use cases, constraints, assumptions and explicit non-goals.
2. High-level components, interfaces and data flow before a targeted core-component deep dive.
3. Scale iteratively: estimate, load-test, profile, change one bottleneck and reassess.
4. Communicate alternatives, unresolved risks and evidence in a time-bounded design review.

**Worked-example plan:** Take a small link-sharing service from requirements to an initial read/write path.

**Trade-offs and when to use/avoid:** Spend detail on constraints that change architecture; do not introduce infrastructure without a measured or estimated need.

**Quick-check focus:** Identify the requirement that would make the initial single-node design unacceptable. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M00 integrated package plan

**Integrated design exercise:** Produce a one-page design brief for a document-sharing service.

**Reference solution and self-evaluation:** Reference package: assumptions register, prioritised use cases, two architecture alternatives, explicit unknowns; assess traceability and justified scope.

**Synthesis outcome map:** M00-S1: frame the brief and defend its scope; readiness diagnosis belongs to M00-L01’s companion. M00-EX1 measures this synthesis outcome using M00-L02-LO1 and M00-L02-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose study route by demonstrated prerequisites, then use the same requirements-to-decision method in every module. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M01 — Workload, performance and distributed guarantees

**Problem to solve:** Systems fail when estimates and guarantees use incompatible assumptions.

**Expected output:** Quantify workload and express latency, consistency and availability decisions.

**Prerequisites:** M00

### M01-L01 — Capacity and latency budgets

**Prerequisites:** M00-L02

**Outcomes:** M01-L01-LO1: trace/model the mechanisms below in the worked scenario. M01-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Convert daily/monthly activity to average and peak requests, storage, bandwidth and working set.
2. Powers of two, bytes versus bits, retention and replication overhead.
3. Latency orders of magnitude, serial round trips, sequential versus random access; dated numbers require measurement.

**Worked-example plan:** Budget traffic and storage for a 30-day activity feed using original hypothetical inputs.

**Trade-offs and when to use/avoid:** Use ranges and peak/headroom assumptions; historical latency tables are intuition, not current benchmarks.

**Quick-check focus:** Find the missing multiplier in a storage estimate with replicas and retention. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M01-L02 — Performance versus scalability

**Prerequisites:** M01-L01

**Outcomes:** M01-L02-LO1: trace/model the mechanisms below in the worked scenario. M01-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Performance versus scalability and latency versus throughput.
2. Vertical and horizontal scaling, state placement and limiting resources.
3. Queueing, saturation, tail latency and benchmark/profile feedback.

**Worked-example plan:** Compare a faster server with two slower servers under a bursty workload.

**Trade-offs and when to use/avoid:** Scale the constrained resource; reject claims that more nodes automatically reduce request latency.

**Quick-check focus:** Explain why throughput rises while tail latency worsens near saturation. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M01-L03 — Consistency and partition decisions

**Prerequisites:** M01-L02

**Outcomes:** M01-L03-LO1: trace/model the mechanisms below in the worked scenario. M01-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Weak, eventual and strong consistency through observable read/write histories.
2. CAP consistency and availability during a partition; CP and AP policies by operation.
3. Convergence, conflict handling and read-your-writes requirements; BASE terminology with product-specific limits.

**Worked-example plan:** Trace a profile update and a balance check during a network partition.

**Trade-offs and when to use/avoid:** Choose per-operation semantics; avoid treating CAP as a normal-operation three-way menu.

**Quick-check focus:** Classify a stale read and explain which guarantee was violated. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M01-L04 — Availability and failover budgets

**Prerequisites:** M01-L03

**Outcomes:** M01-L04-LO1: trace/model the mechanisms below in the worked scenario. M01-L04-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Active-passive versus active-active failover, heartbeat detection, hot/cold standby startup, promotion and split-brain risk.
2. Replication for availability versus backups for recovery.
3. Availability in numbers: three/four nines and downtime windows.
4. Serial and parallel dependency availability with independence and common-cause assumptions.

**Worked-example plan:** Draw a failover timeline for a two-region read service.

**Trade-offs and when to use/avoid:** Balance recovery time, data loss, write conflicts and operational complexity; calculations require stated assumptions.

**Quick-check focus:** Explain why adding a standby does not guarantee the computed parallel availability. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M01 integrated package plan

**Integrated design exercise:** Estimate a regional order-status service and compare two failure policies.

**Reference solution and self-evaluation:** Reference package: units and peak assumptions, bottleneck budget, read/write histories, availability dependency model; assess correct assumptions rather than a single numeric answer.

**Synthesis outcome map:** M01-S1: connect a workload estimate to operation-level consistency and failover choices. M01-EX1 measures this synthesis outcome using M01-L01-LO1, M01-L03-LO2 and M01-L04-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Compare throughput, latency, cost, consistency and failure tolerance under one explicit workload. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M02 — Networking, routing and delivery

**Problem to solve:** Each extra network layer changes latency, failure handling and cache behaviour.

**Expected output:** Choose the request path and delivery protocol for a concrete service.

**Prerequisites:** M01

### M02-L01 — DNS and endpoint discovery

**Prerequisites:** M01-L04

**Outcomes:** M02-L01-LO1: trace/model the mechanisms below in the worked scenario. M02-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Recursive and authoritative resolution, NS/MX/A/CNAME record roles and TTL caching; AAAA/TXT are Academy extensions.
2. DNS weighted-round-robin, latency-based and geolocation routing; maintenance, cluster-size/A-B traffic allocation, failover and propagation delays.
3. Endpoint changes, stale answers and resolver/control-plane failures.

**Worked-example plan:** Trace a regional endpoint change while clients retain cached records.

**Trade-offs and when to use/avoid:** Use DNS for coarse endpoint selection; account for caches when setting recovery expectations.

**Quick-check focus:** Predict which clients still reach the old endpoint after a record change. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M02-L02 — TCP, UDP and HTTP

**Prerequisites:** M02-L01

**Outcomes:** M02-L02-LO1: trace/model the mechanisms below in the worked scenario. M02-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. TCP setup/teardown, sequence/checksum/acknowledgement/retransmission and ordered-byte-stream limits; distinguish flow control from congestion control, head-of-line effects and connection-pool memory budgets.
2. UDP datagrams, loss/reordering, broadcast/DHCP use, application-owned error correction and congestion control; late-data-versus-loss trade-offs.
3. HTTP request/response, headers, connections and GET/POST/PUT/PATCH/DELETE method semantics; distinguish safety, idempotence and cacheability and verify source-era table details against the selected protocol version.

**Worked-example plan:** Compare a file download with a latency-sensitive game update.

**Trade-offs and when to use/avoid:** Choose semantics before transport; verify current HTTP/TLS behaviour from standards during authoring.

**Quick-check focus:** Explain why a UDP application may still need acknowledgements. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M02-L03 — Load balancing and reverse proxies

**Prerequisites:** M02-L02

**Outcomes:** M02-L03-LO1: trace/model the mechanisms below in the worked scenario. M02-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. L4 transport-header/NAT versus L7 application-header/message routing, health checks, random/least-load/round-robin/weighted algorithms and cookie session affinity.
2. Reverse-proxy responsibilities: TLS termination, response compression, direct static-content serving, buffering, caching, backend hiding and per-client connection/IP controls; compare CPU and freshness costs.
3. Horizontal web scaling, stateless requests, central session storage, downstream connection budgets and redundant load balancers.
4. Load balancer versus reverse proxy roles, bottlenecks and failure domains.

**Worked-example plan:** Trace retries and session state when a backend fails behind a proxy.

**Trade-offs and when to use/avoid:** Choose routing information, connection cost and failure behaviour; avoid a single ingress failure point.

**Quick-check focus:** Select L4 or L7 for routing by HTTP path and justify the choice. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M02-L04 — CDN push, pull and cache control

**Prerequisites:** M02-L03

**Outcomes:** M02-L04-LO1: trace/model the mechanisms below in the worked scenario. M02-L04-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Push versus pull CDN population and origin load.
2. Cache keys, TTLs, versioned URLs, invalidation and private content boundaries.
3. Edge placement, cache misses, origin failure and cost/freshness trade-offs.

**Worked-example plan:** Model a viral image with a cold edge and a later content replacement.

**Trade-offs and when to use/avoid:** Use a CDN for distributable content; reject unsafe shared caching for personalised responses.

**Quick-check focus:** Explain how a cache-key omission can return one user another user’s content. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M02 integrated package plan

**Integrated design exercise:** Design the public request path for a global image catalogue.

**Reference solution and self-evaluation:** Reference package: DNS-to-origin sequence, protocol choice, L4/L7 comparison, origin-failure and stale-content scenarios; assess correct layer boundaries.

**Synthesis outcome map:** M02-S1: trace DNS-to-origin delivery and justify proxy/CDN choices. M02-EX1 measures this synthesis outcome using M02-L01-LO1, M02-L03-LO2 and M02-L04-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Select routing and delivery mechanisms by payload, connection lifetime, freshness, geography and failure policy. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M03 — Application boundaries and communication

**Problem to solve:** Service decomposition moves local calls and shared state into distributed failure paths.

**Expected output:** Design component boundaries, APIs and discovery with explicit failure handling.

**Prerequisites:** M02

### M03-L01 — Application layers and microservices

**Prerequisites:** M02-L03

**Outcomes:** M03-L01-LO1: trace/model the mechanisms below in the worked scenario. M03-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Separate web, application and data responsibilities.
2. Modular monolith versus microservices, domain ownership and independent scaling.
3. Service boundaries, network overhead, distributed transactions and deployment/operability costs.

**Worked-example plan:** Compare separating media processing with splitting every entity into a service.

**Trade-offs and when to use/avoid:** Decompose for justified ownership or scaling needs; avoid distributing tightly coupled invariants.

**Quick-check focus:** Identify a boundary that creates unnecessary synchronous fan-out. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M03-L02 — REST, RPC and interface contracts

**Prerequisites:** M02-L02, M03-L01

**Outcomes:** M03-L02-LO1: trace/model the mechanisms below in the worked scenario. M03-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. REST resource identity, representation-based manipulation, self-descriptive messages and hypermedia as uniform-interface constraints; client/server, stateless/cache/layer constraints and their actual scope require primary-source research.
2. RPC request/return path: client call → stub marshals procedure/arguments → transport → server stub unmarshals and dispatches → result returns in reverse; schemas, coupling, SDK/platform choices and debugging/cache limitations.
3. Compare REST and RPC calls for public/internal APIs: operation versus resource interfaces, nested-resource round trips, payload growth, event-like queries and client compatibility.
4. Compatibility, pagination, deadlines and idempotent retries as Academy additions.

5. Compose public REST/HTTP, internal RPC and service discovery; choose interface style and endpoint-discovery ownership together using M03-L03 failure traces.

**Worked-example plan:** Design resource and operation interfaces for exporting a report.

**Trade-offs and when to use/avoid:** Compare interoperability, tooling, streaming and compatibility; no universal REST/RPC performance claim.

**Quick-check focus:** Explain how a retried create call can produce duplicate work. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M03-L03 — Service discovery and resilient calls

**Prerequisites:** M03-L02, M02-L01

**Outcomes:** M03-L03-LO1: trace/model the mechanisms below in the worked scenario. M03-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Registry and DNS discovery, registration/address/port records, health endpoints, leases and stale membership; Consul/etcd/ZooKeeper role comparison and configuration key-value scope.
2. Client-side versus server-side discovery and load balancing.
3. Deadlines, bounded retries, backoff and failure isolation as Academy additions.

**Worked-example plan:** Trace a request to a terminated worker still present in discovery.

**Trade-offs and when to use/avoid:** Choose discovery ownership and failure policy; bound retry amplification and avoid depending on discovery on every hot request.

**Quick-check focus:** Find the amplification caused by retries at multiple call layers. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M03 integrated package plan

**Integrated design exercise:** Split a growing catalogue application into justified deployment boundaries.

**Reference solution and self-evaluation:** Reference package: ownership boundaries, API contracts, discovery lifecycle and timeout/retry sequence; assess whether decomposition solves a real constraint.

**Synthesis outcome map:** M03-S1: choose a service boundary, trace its contract and defend discovery/retry policy. M03-EX1 measures this synthesis outcome using M03-L01-LO2, M03-L02-LO1 and M03-L03-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose modular monolith or services, then REST or RPC, by ownership, coupling, compatibility and operational cost. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M04 — Relational data and scaling

**Problem to solve:** Indexes, replicas and partitions solve different bottlenecks and create different consistency costs.

**Expected output:** Choose a relational data path and justify each scaling change.

**Prerequisites:** M03, M01-L03

### M04-L01 — Relational invariants and query-driven models

**Prerequisites:** M03-L02

**Outcomes:** M04-L01-LO1: trace/model the mechanisms below in the worked scenario. M04-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. RDBMS tables, constraints, joins and ACID as prerequisites applied to design.
2. Model entities and access paths around transaction boundaries.
3. Choose normalisation and object/blob references for an order workload.

**Worked-example plan:** Define the boundary that prevents an order from referring to a missing customer.

**Trade-offs and when to use/avoid:** Prefer explicit invariants and query requirements; treat storage-engine and isolation details as vendor-scoped research.

**Quick-check focus:** Identify which multi-row invariant needs a transaction. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M04-L02 — Single-leader and multi-writer replication

**Prerequisites:** M04-L01, M01-L04

**Outcomes:** M04-L02-LO1: trace/model the mechanisms below in the worked scenario. M04-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Single-leader log replication, read replicas, replication lag and read routing.
2. Promotion, fencing, acknowledged-write loss and recovery.
3. Multi-writer replication, conflict detection/resolution and coordination latency.
4. Replication cost, replay bottlenecks and consistency choices.

**Worked-example plan:** Trace concurrent profile edits at two writers and a stale read after promotion.

**Trade-offs and when to use/avoid:** Choose write authority, lag tolerance and conflict policy explicitly; replicas do not remove all write bottlenecks.

**Quick-check focus:** Explain what can be lost if a leader acknowledges before replication. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M04-L03 — Federation, sharding and consistent hashing

**Prerequisites:** M04-L02

**Outcomes:** M04-L03-LO1: trace/model the mechanisms below in the worked scenario. M04-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Federation: functional partitioning and cross-domain joins/transactions.
2. Sharding: partition-key choice, routing, hot spots, rebalancing and cross-shard queries.
3. Hash/range partitioning, consistent-hash ring and virtual nodes.
4. Partition movement, membership changes and skew; a ring alone does not ensure balanced load.

**Worked-example plan:** Compare separating billing from profiles with sharding profiles by tenant.

**Trade-offs and when to use/avoid:** Select functional split versus horizontal split by workload; include migration, hot keys and scatter costs.

**Quick-check focus:** Predict which keys move when a node joins a consistent-hash ring. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M04-L04 — Denormalisation and derived views

**Prerequisites:** M04-L03

**Outcomes:** M04-L04-LO1: trace/model the mechanisms below in the worked scenario. M04-L04-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Duplicate data to replace joins with precomputed access paths.
2. Materialized views, update propagation and source-of-truth ownership.
3. Write amplification, stale views and repair/rebuild strategies.

**Worked-example plan:** Build a customer-order summary and trace a partial update.

**Trade-offs and when to use/avoid:** Trade read latency against write complexity and repair cost; keep authoritative data identifiable.

**Quick-check focus:** Locate the stale projection after one of two writes fails. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M04-L05 — SQL tuning as an evidence loop

**Prerequisites:** M04-L04

**Outcomes:** M04-L05-LO1: trace/model the mechanisms below in the worked scenario. M04-L05-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Benchmark and profile before changes; query plans and slow-query evidence.
2. Tighten schema: type/range/precision, nullability, CHAR/VARCHAR/TEXT, decimal money and external blobs.
3. B-tree and composite-index access, read/write/memory trade-offs and bulk load/rebuild.
4. Expensive joins, partition pruning/hot tables and query-shape changes.
5. Query-cache tuning as historical product behaviour; verify version and distinguish application caching.

6. Compare read replicas, federation, sharding, denormalisation and query tuning by the measured read/write/storage bottleneck and affected transaction boundary.

**Worked-example plan:** Compare two query plans and a schema/index change under the same workload.

**Trade-offs and when to use/avoid:** Choose measured improvements; source-era type and query-cache advice must be verified, corrected or explicitly historical.

**Quick-check focus:** Explain why an index or partition can increase cost for this workload. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M04 integrated package plan

**Integrated design exercise:** Evolve an order database under read growth, write growth and a hot tenant.

**Reference solution and self-evaluation:** Reference package: query workload, schema/index changes, replica policy, partition routing and migration risks; assess invariants and benchmark plan.

**Synthesis outcome map:** M04-S1: select a scaling change and show the query/replication evidence that justifies it. M04-EX1 measures this synthesis outcome using M04-L02-LO2, M04-L03-LO2 and M04-L05-LO1. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Compare tuning, replicas, federation, sharding and denormalisation by the constrained resource and affected invariants. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M05 — Storage models beyond relational tables

**Problem to solve:** A database category does not determine the guarantees of an actual product.

**Expected output:** Match access patterns and invariants to data models and distributed-store mechanisms.

**Prerequisites:** M04

### M05-L01 — Key-value and document stores

**Prerequisites:** M04-L03

**Outcomes:** M05-L01-LO1: trace/model the mechanisms below in the worked scenario. M05-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Key-value operations, hash/ordered access and application-owned relationships.
2. Documents, nested aggregates, indexes and schema evolution.
3. Redis, Memcached, MongoDB and DynamoDB as distinct research cases; BASE is not a product guarantee.

**Worked-example plan:** Compare storing a session token with a product aggregate queried by attributes.

**Trade-offs and when to use/avoid:** Use key-value for known-key access; use documents when aggregate retrieval and indexed fields fit; verify transaction scope.

**Quick-check focus:** Explain why arbitrary attribute search changes a key-value design. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M05-L02 — Wide-column and graph stores

**Prerequisites:** M05-L01

**Outcomes:** M05-L02-LO1: trace/model the mechanisms below in the worked scenario. M05-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Wide-column row keys, column families, sparse values and timestamped value versions; access-pattern-driven range/lexicographic locality and product-specific retention/conflict semantics.
2. Graph vertices, edges, adjacency traversal and indexing.
3. Bigtable/HBase and Cassandra comparison scope; graph partitioning and supernodes.

**Worked-example plan:** Design time-series access and a friends-of-friends query.

**Trade-offs and when to use/avoid:** Choose partition locality and query shape; graph representation does not eliminate distributed traversal cost.

**Quick-check focus:** Identify a hot partition caused by a time-series row key. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M05-L03 — SQL versus NoSQL and distributed-store guarantees

**Prerequisites:** M05-L02, M01-L03

**Outcomes:** M05-L03-LO1: trace/model the mechanisms below in the worked scenario. M05-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Compare relational, key-value, document, wide-column and graph workloads using schema/joins/transaction/throughput/ecosystem criteria and clickstream/log, leaderboard, basket, hot-table and metadata cases.
2. ACID, BASE, consistency and availability: separate model from actual implementation.
3. Dynamo-style replication/quorums/conflict repair versus coordinated/global transactions.
4. Dynamo paper versus DynamoDB product naming; Spanner as a contrasting research case.

**Worked-example plan:** Choose storage for a basket, inventory reservation and reporting projection.

**Trade-offs and when to use/avoid:** Specify invariants and operation semantics before products; verify contemporary guarantees and cost.

**Quick-check focus:** Reject a SQL/NoSQL recommendation based only on traffic volume. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M05 integrated package plan

**Integrated design exercise:** Choose storage for sessions, product documents, time series and relationship traversal.

**Reference solution and self-evaluation:** Reference package: query/invariant table, model comparison and two product evidence questions per option; assess workload fit and guarantee precision.

**Synthesis outcome map:** M05-S1: choose data models against the four stated access patterns and invariants. M05-EX1 measures this synthesis outcome using M05-L01-LO2, M05-L02-LO2 and M05-L03-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Compare query expressiveness, partition model, consistency, transactions, operational cost and repair requirements. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M06 — Caching and memory budgets

**Problem to solve:** A fast cache can serve stale data, amplify misses or lose writes.

**Expected output:** Design cache placement, coherence, eviction and distribution for explicit freshness goals.

**Prerequisites:** M05

### M06-L01 — Where and what to cache

**Prerequisites:** M05-L01, M02-L04

**Outcomes:** M06-L01-LO1: trace/model the mechanisms below in the worked scenario. M06-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Client, CDN, web-server, database and application cache boundaries; internal DB cache tuning versus external RAM cache, and Redis persistence/list/sorted-set features as version-scoped comparison.
2. Cache granularity: database rows, query results, serializable objects and fully rendered HTML; query-key hashing/dependency invalidation versus object assembly/invalidation, working-set and hit-rate budgets.
3. TTL, eviction, hot keys, cold starts and stampedes; file-local cache state complicates cloning/autoscaling and must be externalised, shared or safely disposable.

4. Compose where-to-cache, row/query/object/HTML granularity and when-to-update policies; choose among cache-aside, write-through, write-behind and refresh-ahead using the M06-L02 failure traces.

**Worked-example plan:** Compute a bounded query-cache working set and trace a miss to the origin.

**Trade-offs and when to use/avoid:** Cache expensive reusable work; reject unauthorised sharing or a working set with negligible reuse.

**Quick-check focus:** Choose object or query caching after one object participates in many queries. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M06-L02 — Cache update and coherence policies

**Prerequisites:** M06-L01

**Outcomes:** M06-L02-LO1: trace/model the mechanisms below in the worked scenario. M06-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Cache-aside and invalidation ordering; read-through as an Academy comparison.
2. Write-through, write-behind and refresh-ahead state transitions.
3. Failure windows, stale reads, lost dirty data, cache-aside miss/round-trip costs, write-through cold starts and never-read entries, refresh misprediction and repair.

**Worked-example plan:** Trace a concurrent read/write and a cache crash under each policy.

**Trade-offs and when to use/avoid:** Select bounded staleness versus write latency/durability; reject absolute freshness claims without assumptions.

**Quick-check focus:** Identify the write-behind loss window and a suitable mitigation. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M06-L03 — Bounded LRU and distributed query cache

**Prerequisites:** M06-L02, M04-L03

**Outcomes:** M06-L03-LO1: trace/model the mechanisms below in the worked scenario. M06-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Hash lookup plus linked recency list, get/set invariants and capacity eviction.
2. Query API hit/miss flow, query/content/ranking change invalidation.
3. Independent, replicated and sharded cache-cluster layouts; consistent-hash routing.
4. Partial failures, hot shards and memory/replication cost; Memcached and Redis comparison questions.

**Worked-example plan:** Walk through five accesses to a capacity-three cache, then remove one cluster node.

**Trade-offs and when to use/avoid:** Use LRU when recency predicts reuse; compare eviction policy and cluster topology with observed access skew.

**Quick-check focus:** Find a cache/list invariant broken by updating an existing key. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M06 integrated package plan

**Integrated design exercise:** Design a query-result cache under a hot query and a node failure.

**Reference solution and self-evaluation:** Reference package: cache keys, size budget, read/write traces, eviction and invalidation strategy, shard failover; assess stale-data and origin-overload risks.

**Synthesis outcome map:** M06-S1: connect cache granularity, a coherence trace and distributed layout. M06-EX1 measures this synthesis outcome using M06-L01-LO2, M06-L02-LO1 and M06-L03-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose cache location, object/query granularity, update policy, eviction and sharding together. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M07 — Queues, jobs and overload control

**Problem to solve:** Deferring work changes where latency and failures appear.

**Expected output:** Design asynchronous processing with explicit delivery, retry and overload semantics.

**Prerequisites:** M06, M03-L03

### M07-L01 — Message queues and task queues

**Prerequisites:** M03-L03

**Outcomes:** M07-L01-LO1: trace/model the mechanisms below in the worked scenario. M07-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Enqueue, acknowledge, execute and report asynchronous completion.
2. Message broker versus task scheduler/executor responsibilities.
3. Delivery duplication/loss, idempotent processing and poison-job handling.
4. Redis, RabbitMQ/AMQP, SQS and Celery as version-scoped evidence cases.

5. Compose message/task queues, bounded back pressure and microservice boundaries; compare synchronous work with deferred execution and use M03-L01/M07-L02 for the detailed ownership and overload mechanisms.

**Worked-example plan:** Trace a worker crash between side effect and acknowledgement.

**Trade-offs and when to use/avoid:** Use background work for deferrable operations; cheap synchronous work may not justify queue latency and operations.

**Quick-check focus:** Explain why delivery at least once needs a duplicate side-effect policy. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M07-L02 — Back pressure, bounded work and retry control

**Prerequisites:** M07-L01, M01-L02

**Outcomes:** M07-L02-LO1: trace/model the mechanisms below in the worked scenario. M07-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Queue depth, arrival/service rates, Little’s law assumptions and waiting-time budget.
2. Bounded queues, admission rejection, rate limits and load shedding.
3. Exponential backoff, jitter, retry budgets and overload feedback.

**Worked-example plan:** Model a burst that arrives faster than a fixed worker pool can drain it.

**Trade-offs and when to use/avoid:** Reject excess work before unbounded delay; compare adding workers with reducing admitted work.

**Quick-check focus:** Compute whether a backlog can drain while arrivals continue. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M07-L03 — Event logs, ordering and replay

**Prerequisites:** M07-L02

**Outcomes:** M07-L03-LO1: trace/model the mechanisms below in the worked scenario. M07-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Queue versus partitioned pub/sub log; consumer groups and offsets.
2. Per-key ordering, replay, retention and state reconstruction.
3. Kafka as a historical architecture and current product research case.
4. Event propagation and outbox/reconciliation as Academy additions.

**Worked-example plan:** Rebuild a search projection from an activity log after an indexing outage.

**Trade-offs and when to use/avoid:** Choose replay and ordering scope explicitly; partition count, retention and hot keys create constraints.

**Quick-check focus:** Explain why increasing consumers cannot parallelise one ordered key indefinitely. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M07 integrated package plan

**Integrated design exercise:** Design asynchronous media processing with status, retries and overload admission.

**Reference solution and self-evaluation:** Reference package: state machine, acknowledgement/retry points, idempotency record, queue budget and recovery; assess duplicate/loss handling.

**Synthesis outcome map:** M07-S1: trace a duplicate-safe job lifecycle and defend overload policy; log replay remains in M07-L03’s companion. M07-EX1 measures this synthesis outcome using M07-L01-LO1 and M07-L02-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose synchronous calls, message brokers, task execution or logs by completion semantics, ordering and replay needs. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M08 — Distributed processing and retrieval mechanisms

**Problem to solve:** Parallel processing adds shuffle, skew and partial-result decisions.

**Expected output:** Design batch/stream aggregation and scatter-gather retrieval with bounded costs.

**Prerequisites:** M07, M05

### M08-L01 — MapReduce and distributed file storage

**Prerequisites:** M07-L03

**Outcomes:** M08-L01-LO1: trace/model the mechanisms below in the worked scenario. M08-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Map, partition, shuffle, reduce and multi-stage sorting.
2. Retryable tasks, duplicate-safe outputs, data locality and skew.
3. GFS/HDFS chunk/block replication and metadata roles.
4. MapReduce versus Spark execution and memory/recomputation trade-offs.

**Worked-example plan:** Aggregate product sales by category, then sort category totals with original sample records.

**Trade-offs and when to use/avoid:** Use batch for large replayable datasets; compare shuffle cost and skew with simpler database aggregation.

**Quick-check focus:** Trace one key through mapper, shuffle and reducer after a task retry. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M08-L02 — Streaming aggregation, trends and top-k

**Prerequisites:** M08-L01

**Outcomes:** M08-L02-LO1: trace/model the mechanisms below in the worked scenario. M08-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Batch versus stream freshness and event-time windows.
2. Late/duplicate events, state retention and recomputation.
3. Exact versus approximate top-k and trend/baseline comparison.
4. Storm and Spark as processing architecture cases, not interchangeable guarantees.

**Worked-example plan:** Compute hourly top products and compare a bursty topic against a baseline.

**Trade-offs and when to use/avoid:** Choose accuracy, lateness and memory limits explicitly; prevent counting retries as new events.

**Quick-check focus:** Explain why lifetime popularity and trending are different queries. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M08-L03 — Indexes and scatter-gather search

**Prerequisites:** M05-L02, M07-L03

**Outcomes:** M08-L03-LO1: trace/model the mechanisms below in the worked scenario. M08-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Document versus inverted index, tokenisation, normalisation, boolean terms and ranking inputs.
2. Partition index/query work, scatter requests and merge/rank results.
3. Fan-out latency, deadlines, partial failures and result completeness.
4. Search freshness and index rebuild/repair as asynchronous projections.

**Worked-example plan:** Trace a two-term query across three shards including a timed-out shard.

**Trade-offs and when to use/avoid:** Choose partitioning and partial-result policy by relevance and freshness requirements; keep retrieval mechanics separate from crawler/feed composition.

**Quick-check focus:** Explain what a timeout means for a globally ranked result. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M08 integrated package plan

**Integrated design exercise:** Compute ranked category totals and query a sharded index under one slow shard.

**Reference solution and self-evaluation:** Reference package: map/shuffle/reduce records, event-time policy, index layout, deadlines and merge rules; assess skew and incomplete-result semantics.

**Synthesis outcome map:** M08-S1: trace ranking records and defend freshness and partial-search-result policy. M08-EX1 measures this synthesis outcome using M08-L01-LO1, M08-L02-LO2 and M08-L03-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose batch versus streaming and full versus partial results by freshness, correctness and tail-latency goals. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M09 — Security, observability and coordination

**Problem to solve:** A design must protect data and remain diagnosable while components fail.

**Expected output:** Build a threat model, evidence loop and coordination boundary into the architecture.

**Prerequisites:** M08, M01-L04

### M09-L01 — Security by trust boundary

**Prerequisites:** M03-L02, M02-L03

**Outcomes:** M09-L01-LO1: trace/model the mechanisms below in the worked scenario. M09-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Authentication versus authorisation, least privilege and network segmentation.
2. HTTPS/TLS, encryption at rest, credentials and secret handling.
3. Validate input, parameterised SQL, injection/XSS/CSRF and output handling.
4. Protect APIs and sensitive financial data; current standards and vendor scopes required.

5. Apply encryption in transit/at rest, least privilege, input/output controls and parameterised SQL together at a concrete service trust boundary.

**Worked-example plan:** Trace an authenticated user requesting another tenant’s financial record.

**Trade-offs and when to use/avoid:** Prioritise confidentiality/integrity threats by asset and trust boundary; encryption alone does not enforce access.

**Quick-check focus:** Identify the authorisation decision missing from a valid-token request. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M09-L02 — Measure, trace and recover

**Prerequisites:** M09-L01, M01-L04

**Outcomes:** M09-L02-LO1: trace/model the mechanisms below in the worked scenario. M09-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. CPU, memory, IO, network and queue metrics tied to workload hypotheses.
2. Logs, metrics and distributed traces; Dapper trace propagation/sampling case.
3. Load testing, profiling and iterative bottleneck diagnosis.
4. Recovery objectives, backup/restore and failure drills as Academy additions.

**Worked-example plan:** Diagnose a slow request through edge, application, queue and database spans.

**Trade-offs and when to use/avoid:** Collect evidence for a decision; account for telemetry cost, sampling and sensitive data.

**Quick-check focus:** Distinguish a downstream bottleneck from time waiting for a worker. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M09-L03 — Coordination and multi-data-centre control

**Prerequisites:** M09-L02, M05-L03

**Outcomes:** M09-L03-LO1: trace/model the mechanisms below in the worked scenario. M09-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Membership, leader election, leases, fencing and distributed locks.
2. Chubby and ZooKeeper roles and failure boundaries.
3. Cross-data-centre latency, quorum/failover placement and common-cause risk.
4. Clock assumptions and global transaction comparison with Spanner.

**Worked-example plan:** Trace a lease holder paused beyond expiry while a replacement starts writing.

**Trade-offs and when to use/avoid:** Use coordination for a defined invariant; stale clients need fencing and partitions require an explicit policy.

**Quick-check focus:** Explain why a lock lease alone may not prevent a stale owner writing. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M09 integrated package plan

**Integrated design exercise:** Review a multi-service design for data exposure, correlated failures and diagnosis gaps.

**Reference solution and self-evaluation:** Reference package: trust-boundary diagram, controls, trace/metric plan, failover and coordination scenarios; assess specific risks and evidence.

**Synthesis outcome map:** M09-S1: justify controls, identify diagnostic evidence and defend coordination under a stale owner. M09-EX1 measures this synthesis outcome using M09-L01-LO2, M09-L02-LO1 and M09-L03-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose controls, telemetry and coordination by threat, operational question and invariant. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M10 — Worked system compositions

**Problem to solve:** Knowing components does not prove one can compose and evolve a full system.

**Expected output:** Build and critique complete designs from requirements through failures and scaling.

**Prerequisites:** M00–M09

### M10-L01 — Paste storage, short links and expiry

**Prerequisites:** M06-L03, M09-L01

**Outcomes:** M10-L01-LO1: trace/model the mechanisms below in the worked scenario. M10-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope anonymous paste/short-link creation and retrieval; estimate reads, writes and retention.
2. Identifier namespace and creation flow: hash input/truncation, Base62 digits versus standard Base64 URL characters, collision detection/retry and uniqueness metadata; source-era MD5 claims require correction and URL-safe Base64 is an Academy comparison.
3. Read path resolves metadata to object content; monthly URL-hit analytics maps (year-month, URL) to counts then reduces totals; expiry/deletion and index-assisted cleanup must invalidate cached reads.
4. Scale hot links with cache/read replicas, split analytics into warehouse and raw content into object storage, address write bottlenecks; protect unguessable/private data and evaluate source-era hash advice.

**Worked-example plan:** Design a paste service and derive the difference when the value is a long URL.

**Trade-offs and when to use/avoid:** Separate uniqueness from secrecy; compare random IDs and allocated IDs, cache TTL and deletion deadlines.

**Quick-check focus:** Trace a deleted paste still served from a cache. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10-L02 — Social feed publication and timelines

**Prerequisites:** M10-L01, M07-L03

**Outcomes:** M10-L02-LO1: trace/model the mechanisms below in the worked scenario. M10-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope posts, home/user timelines and media; derive fan-out/storage estimates.
2. Durable author posts and user-timeline reads, follower-graph lookup, media object storage, asynchronous notifications and home-timeline materialisation.
3. Fan-out-on-write/read/hybrid, celebrity skew, inactive-user rebuild, bounded active-user/tweet retention, reply ordering and batched tweet/user hydration.
4. Keyword-search integration delegates tokenisation/index/shard retrieval to M08-L03.

**Worked-example plan:** Trace one post from an ordinary author and one from a celebrity into two home timelines.

**Trade-offs and when to use/avoid:** Choose fan-out strategy by follower distribution, write amplification and freshness; search mechanics remain owned by M08-L03.

**Quick-check focus:** Explain a missing/reordered reply caused by delayed fan-out. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10-L03 — Crawler and web-search composition

**Prerequisites:** M08-L03, M10-L02

**Outcomes:** M10-L03-LO1: trace/model the mechanisms below in the worked scenario. M10-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope crawl and search; derive frontier, page-storage and index sizes.
2. Frontier priorities and visited-URL lifecycle, cycle prevention and signature-based content deduplication; compare Jaccard/cosine similarity, exact URL grouping and false equivalence.
3. Recrawl timestamps and adaptive freshness, robots controls and their protocol limits; document/title/snippet and inverted-index queues, crawl-store consistency and content-change propagation.
4. Query serving composes M08-L03 retrieval with titles/snippets and crawl freshness.
5. Critique unique-only MapReduce filtering versus emitting one copy per repeated URL; scale crawl/index partitions and query caches, DNS caches, pooled connections and bandwidth budgets; do not switch HTTP transport to UDP without a supported protocol.

**Worked-example plan:** Trace two URLs with the same content and a changed page through frontier, crawl store and index.

**Trade-offs and when to use/avoid:** Choose freshness and crawl breadth under bandwidth/host limits; avoid removing every occurrence of a repeated URL.

**Quick-check focus:** Explain why a stale index can persist after a successful recrawl. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10-L04 — Financial aggregation and budgeting

**Prerequisites:** M08-L01, M09-L01

**Outcomes:** M10-L04-LO1: trace/model the mechanisms below in the worked scenario. M10-L04-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope account connection, transaction extraction and budget recommendations; estimate write-heavy load.
2. Account connector/authentication and account metadata; first-link/manual/active-user scheduled refresh, extraction queue, raw transaction object logs, category/aggregate SQL updates and completion/budget notifications; deduplication and source credential-hash design need explicit verification.
3. Category selection: seeded seller dictionary and crowd/manual override ranking; budget templates by income tier, sparse per-user category overrides and recomputation after category changes.
4. Monthly spending map/reduce by period/category and budget-notification side effects; compare OLTP recent transactions, warehouse aggregates and raw object-store retention, cache/read/write bottlenecks and sensitive-data boundaries.

**Worked-example plan:** Trace an account refresh replay and a monthly category-budget calculation.

**Trade-offs and when to use/avoid:** Choose asynchronous refresh versus immediate consistency; avoid duplicate transactions and unsupported financial guarantees.

**Quick-check focus:** Explain how retrying extraction can double count spending. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10-L05 — Distributed social-graph traversal

**Prerequisites:** M05-L02, M09-L03

**Outcomes:** M10-L05-LO1: trace/model the mechanisms below in the worked scenario. M10-L05-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope shortest relationship path and estimate graph/lookup cost.
2. BFS, bidirectional search and visited/frontier state.
3. Person-ID lookup, partitioned person servers and batched same-server adjacent-node fetches; traversal caches/offline precomputation and location-aware placement.
4. Cross-server traversal, skew, visibility controls and time/hop search limits; high-degree search heuristics versus shortest-path correctness, graph-store alternatives and the source’s GraphQL/graph-query conflation to correct.

**Worked-example plan:** Find a short path across three partitions and trace batched frontier expansion.

**Trade-offs and when to use/avoid:** Choose graph placement and search limits by traversal locality; distinguish reachability from reconstructing a shortest path.

**Quick-check focus:** Explain why a shared visited set across independent searches can corrupt results. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10-L06 — Search query cache at service scale

**Prerequisites:** M06-L03, M08-L03

**Outcomes:** M10-L06-LO1: trace/model the mechanisms below in the worked scenario. M10-L06-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope hit/miss behaviour and estimate bounded query-result memory.
2. Query API, LRU map/list and cache-fill flow; apply M06-L03 invariants.
3. Invalidate for content, URL set and ranking changes.
4. Scale independent/replicated/sharded caches with routing, hot keys and failover.

**Worked-example plan:** Design an original service-scale cache for search results with a node loss.

**Trade-offs and when to use/avoid:** Compare duplicated memory, hit ratio, sharding complexity and acceptable staleness; do not reteach the LRU algorithm.

**Quick-check focus:** Explain which ranking change requires invalidating a cached query. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10-L07 — Category sales ranking

**Prerequisites:** M08-L02, M10-L04

**Outcomes:** M10-L07-LO1: trace/model the mechanisms below in the worked scenario. M10-L07-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope weekly category ranking, hourly refresh and read-heavy workload.
2. Filter window, aggregate category/product quantities and distributed sort.
3. Materialise ranking, serve reads and cache stable results.
4. Handle multi-category products, boundary timestamps, replays and hot categories.

**Worked-example plan:** Trace original sales records through two MapReduce stages into a ranking table.

**Trade-offs and when to use/avoid:** Choose batch versus incremental ranking by freshness and correction requirements.

**Quick-check focus:** Explain why a retried sales record changes ranking without deduplication. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10-L08 — Iteratively scaling a cloud application

**Prerequisites:** M09-L02, M10-L07

**Outcomes:** M10-L08-LO1: trace/model the mechanisms below in the worked scenario. M10-L08-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Scope and estimate the read/write workload, relational-data need, user-content growth and peak uncertainty.
2. Initial EC2 web/SQL box and request flow, vertical scaling/host profiling, SQL-versus-NoSQL choice, static public IP and Route 53 DNS; source port/egress rules need contemporary security review.
3. Users+ separates S3 objects and RDS/database, introduces public/private subnets, allowed ports and encryption boundaries for independent scaling.
4. Users++ introduces redundant ELB/ingress and web/application tiers across availability zones, SQL failover, TLS termination and CloudFront delivery.
5. Users+++ compares database-cache tuning with external memory caching, central sessions, read/write routing and MySQL read replicas/load distribution.
6. Users++++ automates provisioning/configuration and autoscaling with min/max bounds, metrics or time triggers, multi-AZ groups and scale-up delay; host/aggregate/log/external/incident/error telemetry.
7. Users+++++ addresses retention/warehouse split, cache-miss and writer bottlenecks with federation/sharding/denormalisation/tuning or appropriate NoSQL, plus asynchronous thumbnail queues/workers.
8. Compare historical EC2/static IP/Route 53/S3/RDS/ELB/CloudFront/ElastiCache/CloudWatch/Redshift/SQS/EC2-Lambda worker roles with current AWS documentation; no old scale threshold or guarantee is inherited.

**Worked-example plan:** Evolve an original read-heavy service in five stages, identifying the trigger for each change.

**Trade-offs and when to use/avoid:** Choose managed versus self-managed components by cost and recovery requirements; source diagrams are historical patterns.

**Quick-check focus:** Explain why web autoscaling cannot fix a saturated database writer. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M10 integrated package plan

**Integrated design exercise:** Compare two full designs for a content platform, then change one dominant constraint.

**Reference solution and self-evaluation:** Reference package: each case includes requirements/estimates, first viable architecture, core read/write flows, bottleneck-driven evolution and failure analysis; assess consistency with assumptions.

**Synthesis outcome map:** M10-S1: compare a feed/search content platform, trace crawl-to-query flow and defend its query-cache strategy; the other five case studies remain assessed in their companions. M10-EX1 measures this synthesis outcome using M10-L02-LO2, M10-L03-LO1 and M10-L06-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose compositions by workload and invariants; shared fundamentals are applied here rather than redefined. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M11 — Additional design domains

**Problem to solve:** New domains expose invariants that a familiar feed or URL shortener does not cover.

**Expected output:** Apply shared mechanisms to every substantive additional Primer prompt.

**Prerequisites:** M10

### M11-L01 — File synchronisation and collaborative documents

**Prerequisites:** M10-L03

**Outcomes:** M11-L01-LO1: trace/model the mechanisms below in the worked scenario. M11-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. File sync: metadata, chunks, change detection, versions, offline updates and conflict handling.
2. Collaborative editing: operation propagation, convergence and concurrent edits.
3. Contrast whole-file/version sync with OT/CRDT-style operation models; authoring needs primary evidence.

**Worked-example plan:** Trace concurrent offline file edits and simultaneous document insertions.

**Trade-offs and when to use/avoid:** Choose conflict granularity, ordering and convergence semantics; file sync and collaborative editing have distinct invariants.

**Quick-check focus:** Explain why last-write-wins can lose a user’s edit. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L02 — Messaging and media sharing

**Prerequisites:** M10-L02

**Outcomes:** M11-L02-LO1: trace/model the mechanisms below in the worked scenario. M11-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Chat: connection/presence routing, offline delivery, message IDs and receipts.
2. Photo sharing: upload metadata, object storage, transformations, moderation and CDN.
3. Integrate feed/timeline and group membership while preserving access boundaries.

**Worked-example plan:** Trace an offline group recipient and a private photo becoming public.

**Trade-offs and when to use/avoid:** Choose acknowledgement meaning, history retention and cache privacy; distinguish accepted, stored and delivered.

**Quick-check focus:** Explain why server acceptance is not proof that a recipient saw a message. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L03 — Recommendation and graph search

**Prerequisites:** M10-L05, M08-L03

**Outcomes:** M11-L03-LO1: trace/model the mechanisms below in the worked scenario. M11-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Recommendations: event collection, candidates, scoring, serving and feedback.
2. Graph search: entity/edge constraints, traversal/index combination and ranking.
3. Offline feature freshness, online latency, permissions and cold starts.

**Worked-example plan:** Compare related-product recommendations with a friends-in-a-city query.

**Trade-offs and when to use/avoid:** Choose precomputation versus online computation; preserve permissions and distinguish relevance from traversal correctness.

**Quick-check focus:** Explain how stale features and stale permissions create different failures. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L04 — CDN as a service and global data serving

**Prerequisites:** M10-L08, M09-L03

**Outcomes:** M11-L04-LO1: trace/model the mechanisms below in the worked scenario. M11-L04-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. CDN service: origin registration, edge routing, cache population/purge and origin protection.
2. Multi-data-centre data serving: regional placement, replication and failover.
3. Compare latency, staleness, egress cost and failover capacity.

**Worked-example plan:** Trace a regional outage while an origin changes a widely cached object.

**Trade-offs and when to use/avoid:** Choose global replication versus edge caching by data mutability and operation semantics.

**Quick-check focus:** Explain why routing users elsewhere is insufficient without spare regional capacity. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L05 — Unique-ID service

**Prerequisites:** M10-L01, M09-L03

**Outcomes:** M11-L05-LO1: trace the named mechanism and its state transitions in the worked scenario. M11-L05-LO2: choose an alternative and defend its invariant/failure trade-offs.

**Teaching sequence:**
1. Random IDs, namespace size, collision probability/handling and uniqueness enforcement; distinguish unique, unguessable and ordered IDs.
2. Coordinated allocation versus time/worker/sequence IDs, throughput and coordination cost.
3. Clock rollback, sequence exhaustion, worker-identity reuse and restart/failover invariants.

**Worked-example plan:** Trace allocation across two workers, a sequence overflow and a clock rollback.

**Trade-offs and when to use/avoid:** Choose uniqueness, secrecy and order separately; coordination, random collisions and clock assumptions create different costs.

**Quick-check focus:** Explain how reusing a worker identity after restart can create an ID collision. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L06 — Distributed API rate limiter

**Prerequisites:** M07-L02, M11-L05

**Outcomes:** M11-L06-LO1: trace the named mechanism and its state transitions in the worked scenario. M11-L06-LO2: choose an alternative and defend its invariant/failure trade-offs.

**Teaching sequence:**
1. Fixed and sliding-window counters: boundary bursts, exactness, memory and atomic update scope.
2. Token and leaky buckets: refill/drain state, burst allowance and queue versus reject semantics.
3. Distributed quota partitioning, shared counters, key scope, fairness and fail-open/fail-closed policy under storage failure.

**Worked-example plan:** Apply all four algorithms to one original burst trace, then lose the shared quota store.

**Trade-offs and when to use/avoid:** Choose algorithm by fairness, allowed burst and accuracy; choose admission failure policy by service objective.

**Quick-check focus:** Explain why a per-gateway counter can violate a global quota. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L07 — Multiplayer card games and exchange order books

**Prerequisites:** M11-L06, M09-L03

**Outcomes:** M11-L07-LO1: trace/model the mechanisms below in the worked scenario. M11-L07-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Multiplayer game: authoritative state, turns, reconnects and client validation.
2. Exchange: order entry, price/time priority, matching, cancellation and replay.
3. Compare per-game and per-instrument serialisation, deterministic logs and failover.

**Comparison limit:** Teach authoritative sequencing and replay through one turn-based card game and one single-instrument price/time order book; exclude game physics, exchange networking/regulation and market microstructure. Trace each domain’s duplicate/reordering failure separately.

**Worked-example plan:** Trace a duplicate game action and an order/cancel race.

**Trade-offs and when to use/avoid:** Choose authoritative ordering and recovery before transport; trading policies require an explicit domain contract.

**Quick-check focus:** Explain which operation order changes the accepted outcome. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L08 — Memory reclamation

**Prerequisites:** Entry graph/reference knowledge diagnosed by M00-L01; M11-L07

**Outcomes:** M11-L08-LO1: trace the named mechanism and its state transitions in the worked scenario. M11-L08-LO2: choose an alternative and defend its invariant/failure trade-offs.

**Teaching sequence:**
1. Reachability roots, object graph, marking, sweep and unreachable reference cycles.
2. Stop-the-world pause and live-set/heap/memory-pressure trade-offs.
3. Concurrent mutation/reclamation boundary and barriers as an explicitly bounded extension; no full collector implementation is implied.

**Worked-example plan:** Mark and sweep an original object graph containing a reference cycle; compare pause cost for two live-set sizes.

**Trade-offs and when to use/avoid:** Use tracing reclamation for managed object lifecycles; distinguish reachability from cache eviction and bound concurrent-collector scope.

**Quick-check focus:** Explain why a cycle can be unreachable even when each object has a nonzero reference count. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11-L09 — Key-value store and disposable cache composition

**Prerequisites:** M10-L06, M11-L08

**Outcomes:** M11-L09-LO1: trace the named mechanism and its state transitions in the worked scenario. M11-L09-LO2: choose an alternative and defend its invariant/failure trade-offs.

**Teaching sequence:**
1. Design a Redis-like key-value service: key/command model, expiry, partition routing and bounded memory.
2. Design a Memcached-like disposable cache: eviction, misses, cache refill and node replacement.
3. Compare durable acknowledgement, persistence/replay, replication and recovery with disposable cached state; contemporary products need version-scoped evidence.

**Worked-example plan:** Trace an expiry, a memory-pressure eviction and a restart after acknowledged writes under both service contracts.

**Trade-offs and when to use/avoid:** Choose durable store versus disposable cache semantics before products; compare replay cost, staleness and data-loss tolerance.

**Quick-check focus:** Identify which acknowledged values may be discarded by the chosen contract. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M11 integrated package plan

**Integrated design exercise:** Compare a unique-ID service with a distributed API rate limiter and explain why their invariants require different coordination and failure policies.

**Reference solution and self-evaluation:** Reference package: domain-specific flows, data model, estimate, one failure trace and two alternatives per variant; assess transfer of principles and explicit invariants.

**Synthesis outcome map:** M11-S1: compare an ID-service invariant and an API-quota invariant, then defend their distinct coordination/failure policies; every other domain remains assessed in its companion. M11-EX1 measures this synthesis outcome using M11-L05-LO2 and M11-L06-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Compare designs by delivery, ordering, synchronisation, durability, ranking, geographic and lifecycle requirements. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M12 — Object-oriented design and local invariants

**Problem to solve:** Distributed architecture still depends on correct local state transitions and interfaces.

**Expected output:** Model responsibilities, invariants and extensible behaviour in all six Primer OOD examples.

**Prerequisites:** M00-L01, M06-L03; M11-L02 for chat context

### M12-L01 — Hash-table contracts and collisions

**Prerequisites:** M00-L01

**Outcomes:** M12-L01-LO1: trace/model the mechanisms below in the worked scenario. M12-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Source contract: integer keys, fixed-size in-memory table, chaining and assumed-valid inputs; key/value items, deterministic bucket indexing and collision chains.
2. Set/update/get/remove semantics, missing keys and equality/hash contract.
3. Capacity/load-factor and resizing as a required extension beyond the fixed-size source.

**Worked-example plan:** Trace collisions and removal of the middle item in a bucket.

**Trade-offs and when to use/avoid:** Choose hash table versus ordered index by access needs; expected constant time depends on assumptions.

**Quick-check focus:** Explain why replacing a colliding bucket loses unrelated keys. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M12-L02 — LRU object collaboration

**Prerequisites:** M12-L01, M06-L03

**Outcomes:** M12-L02-LO1: trace/model the mechanisms below in the worked scenario. M12-L02-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Source contract: valid web-query inputs and an in-memory cache; node ownership, lookup/list consistency and recency updates.
2. Get, existing-key update, capacity eviction and zero-capacity boundary.
3. Repair incomplete source stubs and accidental attributes through explicit contracts.

**Worked-example plan:** Design original map/list interfaces and trace remove-tail then update.

**Trade-offs and when to use/avoid:** Choose a data structure that supports required complexity; this lesson owns local class contracts, M06 owns cache policy.

**Quick-check focus:** Locate the missing key/back-pointer that prevents safe lookup eviction. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M12-L03 — Parking allocation and contiguous resources

**Prerequisites:** M12-L01

**Outcomes:** M12-L03-LO1: trace/model the mechanisms below in the worked scenario. M12-L03-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Source contract: multiple levels and motorcycle/compact/large spots; motorcycle/car fit policies and a bus requiring five consecutive large spots on one row.
2. Parking lot, level and spot responsibilities.
3. Allocate contiguous compatible spots, release all vehicle spots and maintain availability counts.

**Worked-example plan:** Trace a bus allocation that must span several adjacent spots on one row.

**Trade-offs and when to use/avoid:** Use polymorphism for fit rules and composition for containment; avoid partial allocation on failure.

**Quick-check focus:** Explain the invariant broken when freeing only one spot of a multi-spot vehicle. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M12-L04 — Call-centre dispatch and escalation

**Prerequisites:** M12-L03

**Outcomes:** M12-L04-LO1: trace/model the mechanisms below in the worked scenario. M12-L04-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Source contract: operators first, then supervisors, then directors; directors handle any call, otherwise queue; no VIP priority and assumed-valid inputs; ranks, call states and dispatch eligibility.
2. Operator/supervisor/director escalation and queue ownership.
3. Completion, queued-call dispatch and invalid transition handling.

**Worked-example plan:** Trace a queued call escalated while a suitable employee becomes free.

**Trade-offs and when to use/avoid:** Model transitions and responsibilities explicitly; compare inheritance with rank-based policies.

**Quick-check focus:** Explain why completing an escalated call twice can free the wrong employee. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M12-L05 — Cards, decks and scoring

**Prerequisites:** M12-L04

**Outcomes:** M12-L05-LO1: trace/model the mechanisms below in the worked scenario. M12-L05-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Source contract: generic 52-card/four-suit deck extended to blackjack with assumed-valid inputs; suit/card abstraction and game-specific values.
2. Deck shuffle/deal/exhaustion and hand composition.
3. Blackjack aces, possible totals and best legal score.

**Worked-example plan:** Score a hand with two aces and a face card, then deal the final card.

**Trade-offs and when to use/avoid:** Keep deck mechanics separate from scoring policy; make randomness testable without promising statistical results.

**Quick-check focus:** Explain why assigning every ace a fixed value gives incorrect scores. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M12-L06 — Chat domain and relationship states

**Prerequisites:** M12-L05, M11-L02

**Outcomes:** M12-L06-LO1: trace/model the mechanisms below in the worked scenario. M12-L06-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Source contract: text-only, initially unscaled chat; user create/update/remove and friendship removal workflows, user-service ownership and private/group chat composition.
2. Message identity/history and membership changes.
3. Friend requests: pending/approved/rejected transitions, invitations and group membership authorisation.

**Worked-example plan:** Trace a rejected friend request followed by a group membership change.

**Trade-offs and when to use/avoid:** Keep local domain contracts separate from network delivery; avoid coupling user deletion to uncontrolled shared-state mutation.

**Quick-check focus:** Identify the permission check required before sending to a group. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M12 integrated package plan

**Integrated design exercise:** Extend the parking-lot model with a new fit/allocation rule and trace allocation, failed allocation and complete release.

**Reference solution and self-evaluation:** Reference package: class/responsibility diagram, contracts, representative operations and boundary cases; assess invariants and extension cost, not reproduction of source code.

**Synthesis outcome map:** M12-S1: extend the parking model with one fit/allocation rule and demonstrate preserved allocation/release invariants; other local models remain assessed in their companions. M12-EX1 measures this synthesis outcome using M12-L03-LO1 and M12-L03-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Choose composition, inheritance, indexes and state machines by responsibilities and change pressure. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## M13 — Architecture reading and synthesis

**Problem to solve:** Historical architecture diagrams invite copying decisions without their original constraints.

**Expected output:** Extract transferable decisions while identifying dated, missing and unsupported claims.

**Prerequisites:** M10–M12

### M13-L01 — Read architecture families critically

**Prerequisites:** M10-L08, M12-L06

**Outcomes:** M13-L01-LO1: trace/model the mechanisms below in the worked scenario. M13-L01-LO2: choose and defend an alternative using the stated decision and failure criteria.

**Teaching sequence:**
1. Compare processing, data-store, file-system and coordination architecture families.
2. Reconcile MapReduce/Spark/Storm, Bigtable/HBase/Cassandra, Dynamo/DynamoDB/MongoDB/Spanner, Redis/Memcached, GFS/HDFS, Chubby/ZooKeeper/Dapper/Kafka with their owning mechanism lessons.
3. Company architecture and engineering-blog catalogs are discovery resources; select and verify primary sources before claims.
4. Record source date, product/version, exact section, assumptions and limits; do not import third-party diagrams without rights checks.

**Worked-example plan:** Adapt one historical design to an original smaller workload and identify components that are unnecessary.

**Trade-offs and when to use/avoid:** Transfer a decision only when its constraint still applies; separate conceptual papers, historical systems and current products.

**Quick-check focus:** Explain why an old company-scale architecture is insufficient evidence for a present-day product guarantee. The separate companion measures LO1 with Q1–Q3 and LO2 with Q4–Q6 plus EX-1; it will include explanations and an outcome map.

### M13 integrated package plan

**Integrated design exercise:** Compare two historical architecture families with a new workload.

**Reference solution and self-evaluation:** Reference package: source/date/section ledger, constraint-to-component map, failure comparison and a proposed adaptation; assess evidence quality and transfer.

**Synthesis outcome map:** M13-S1: trace source assumptions to mechanisms and defend a constrained adaptation. M13-EX1 measures this synthesis outcome using M13-L01-LO1 and M13-L01-LO2. It does not claim all module lesson outcomes. Each lesson’s separate companion remains responsible for its complete LO1/LO2 assessment, and the course portfolio must reconcile all companions before course completion.

**Decision-summary table plan:** Select architecture evidence by problem similarity, date, authority and documented trade-offs. Each eventual row states trigger, option, mechanism, benefit, cost, failure signal, when to avoid, and the lesson reference.

## CP-01 — Cross-module final design

**Problem:** Design an original multi-region community marketplace with listings/media, buyer/seller messaging, activity feeds, keyword search, inventory reservation, weekly category rankings and account/usage reporting. Workload parameters will be provided as a coherent original dataset when the capstone is authored.

**Prerequisites:** M00–M13. **Expected output:** one design dossier that connects requirements, estimates, API/data contracts, synchronous/asynchronous flows, storage, cache, index and processing choices, geographic placement, security and operations.

**Planned stages:** baseline requirements and non-goals → workload/latency budgets → first viable design → core state transitions and interfaces → failure injection (duplicate event, stale cache, hot partition, regional partition and recovery) → revised design with two rejected alternatives → oral/written design defence.

**Reference-solution plan:** provide one justified baseline and at least two valid variants, including assumptions under which each is preferable. Keep inventory-reservation invariants distinct from eventually consistent feed/search/ranking views. Include calculations, request/event traces, repair paths and diagrams drawn originally for Academy.

**Self-evaluation rubric plan:** requirements/estimates 15%; mechanisms and end-to-end traces 25%; invariants and failure recovery 25%; alternatives/costs 15%; security/operations 10%; clarity and evidence 10%. A serious invariant violation cannot be hidden by a high aggregate score. Thresholds and task parameters need validation when authored.

**Capstone transfer outcomes and planned rubric map:** CP-LO1 frames a bounded workload and estimates a capacity/latency budget (requirements/estimates row; draws on M00–M01). CP-LO2 traces a public request and asynchronous update through interfaces, routing, storage, cache and index boundaries (mechanisms/traces row; M02–M08). CP-LO3 preserves reservation and authorisation invariants while repairing duplicate/stale/partitioned state (invariants/recovery row; M04–M09). CP-LO4 defends two alternatives by cost, failure behaviour and applicability (alternatives row; M10–M11). CP-LO5 supplies a diagnostic/recovery plan and explicit local interface contracts (security/operations and mechanisms rows; M09/M12). CP-LO6 distinguishes source evidence from assumptions in a clear design defence (clarity/evidence row; M13). These are transfer outcomes for this marketplace, not a promise to assess every lesson outcome; the complete lesson/module portfolio covers remaining domains and local models.

## Revision-1 scope and mapping audit

This candidate addresses first-review C1/C2/P1/P2: source-body attributions were rebuilt per actual file; matrix associations were reviewed by concept and instructional item; additional body leaves and OOD notebook constraints were made explicit; ID/rate-limit and GC/store lessons were split; module and capstone assessment claims now identify actual synthesis subsets. The original candidate and review remain unchanged. Counts include repeated source representations and headings, not unique concepts. Independent re-review must establish acceptance.

## Scope boundaries, overlap and outstanding assumptions

Search ownership: M08-L03 teaches tokenisation, indexes, shard fan-out and merge/rank mechanics; M10-L03 composes crawl/frontier/recrawl with that retrieval path; M10-L02 applies search to the feed domain without reteaching retrieval. M11-L03 adds recommendation and graph-query semantics. Cache ownership: M06 teaches policy/mechanisms; M10-L06 composes service-scale query caching; M12-L02 teaches local object contracts. Replication, sharding, SQL tuning and federation each have explicit mechanisms rather than being credited from a rationale.

Resource classification: translations duplicate inventoried English content; solution index summaries point to inventoried bodies; binary flashcards and visual source assets are study/rights resources; linked company architecture/blog catalogs are bounded discovery resources, not an obligation to crawl every external page. The real-world architecture table’s named mechanisms are nevertheless mapped to their owning lessons. Independent review must challenge missing leaves and any resource classification that hides knowledge.

Assumptions for human review: audience and English follow repository defaults; broad full-Primer coverage produces a substantial course with domain/OOD tracks; pacing and total hours remain undecided rather than invented. The current pinned revision is the agreed baseline; adopting a newer source requires a separate diff and coverage review. Older course artifacts are not used as approved teaching scope.

## Human confirmation gate

This draft must receive independent full-source coverage and plan-pedagogy review, then explicit user confirmation. Until that confirmation, do not author lessons/assessments, create an Epic/Story/Subtask delivery backlog, or resume historical content tasks. After confirmation, a separate course-delivery planning task may define stable course/module/lesson codes and Jira-style work packages, dependencies and acceptance criteria. Workflow-editing tasks remain separate.
