# System Design Academy — Complete Curriculum Draft

**State:** planning candidate; not yet coverage-approved  
**Audience:** middle/senior software engineers who already build and operate backend services  
**Language:** English  
**Source boundary:** Donne Martin's System Design Primer at commit `ae9bbd7b02d90b9866215de185217d33f39ab733`; source inventory is `../research/source-inventory.md`.  
**Deliverable contract:** teaching lessons and their knowledge outlines only. This plan does not authorize lesson prose, quizzes, exercises, answer keys, or other learner-facing artifacts.

## Course intent and design rules

The course teaches engineers to connect workload and correctness needs to architecture choices, explain the mechanisms those choices rely on, and reason about their failure and operating costs. It assumes common programming, networking, SQL and backend-service experience. It does not teach introductory programming or SQL syntax.

The core sequence moves from design reasoning and quantitative constraints to request paths, data and cache mechanisms, asynchronous/distributed processing, security, and then applied system compositions. The final applied section uses the Primer's solution writeups and additional architecture prompts as teaching cases. An explicitly optional component-design appendix accounts for the Primer's adjacent OOD collection.

Every lesson below is a separately authorable unit. Its outline names concepts to explain in teaching order. Primer coverage is a topic map, not technical authority: later lesson research must verify claims against current primary sources. Historical figures, incomplete topics, and vendor examples are flagged for research rather than copied as facts.

## Core sequence

### Module 01 — Design reasoning and system constraints

**Purpose:** establish a concise, repeatable way to turn an open-ended system need into constraints and architecture decisions.

#### SD-01-01 — Frame a system design problem

- **Prerequisites:** experienced backend engineer.
- **Teaching outline:** define use cases and system boundaries; separate functional requirements from constraints and assumptions; translate requirements into measurable load, latency, durability, availability and consistency needs; sketch the high-level components and their connections; decompose one critical component and identify what to scale; use back-of-the-envelope estimates to test the design; show how to deepen or stop a design based on risk.
- **Source map:** `#study-guide`; `#how-to-approach-a-system-design-interview-question` and its Steps 1–4 and back-of-the-envelope section.

#### SD-01-02 — Performance, scalability, latency and throughput

- **Prerequisites:** SD-01-01.
- **Teaching outline:** distinguish response time from work completed per unit time; explain how queueing and resource saturation affect both; distinguish improving performance at a fixed workload from scaling as demand grows; compare vertical scale-up, horizontal scale-out and replication/cloning; connect bottlenecks to a next measurement or design change.
- **Source map:** `#performance-vs-scalability`; `#latency-vs-throughput`; `#system-design-topics-start-here`.

#### SD-01-03 — Estimate load, capacity and order of magnitude

- **Prerequisites:** SD-01-01, SD-01-02.
- **Teaching outline:** derive average and peak request rates from users and activity; estimate read/write mix, storage growth and network bandwidth; use powers of two and unit conversions without false precision; relate latency components to a request path; identify which assumptions dominate an estimate and how headroom changes capacity; treat published latency tables as historical comparisons that need current, workload-specific evidence.
- **Source map:** `#back-of-the-envelope-calculations`; `#powers-of-two-table`; `#latency-numbers-every-programmer-should-know`; `#latency-numbers-visualized`.

#### SD-01-04 — Availability, consistency and partition trade-offs

- **Prerequisites:** SD-01-01, SD-01-02.
- **Teaching outline:** distinguish whether a request receives a response from whether it observes the latest state; introduce partitions as a distributed-system failure condition; state the operational question behind CAP; reason through CP and AP behaviors during a partition using explicit operation semantics; surface the consequences for reads, writes and user-visible behavior.
- **Source map:** `#availability-vs-consistency`; `#cap-theorem`; `#cp---consistency-and-partition-tolerance`; `#ap---availability-and-partition-tolerance`.

#### SD-01-05 — Consistency models as application contracts

- **Prerequisites:** SD-01-04.
- **Teaching outline:** explain weak, eventual and strong consistency in terms of what a reader can observe after a write; distinguish convergence from a bounded freshness guarantee; connect read-your-writes and stale reads to product behavior; show what the chosen contract implies for replicas, caches and failover; flag that the Primer's labels require precise, current definitions during research.
- **Source map:** `#consistency-patterns`; `#weak-consistency`; `#eventual-consistency`; `#strong-consistency`.

#### SD-01-06 — Availability patterns and availability arithmetic

- **Prerequisites:** SD-01-04, SD-01-05.
- **Teaching outline:** compare failover with replication and clarify their different roles; explain active-passive and active-active behavior, health detection, promotion and split-brain/coordination risks; account for failover delay and lost in-flight or recently acknowledged work; calculate serial dependency availability versus parallel redundancy; interpret three and four nines over an explicit time period; identify when redundant components do not remove shared failure modes.
- **Source map:** `#availability-patterns` > Fail-over (Active-passive/Active-active subsections), Replication, Availability in numbers (99.9%/99.99% subsections), and Availability in parallel vs in sequence (In sequence/In parallel subsections). The inventory records the stable parent anchors and exact subsection titles.

### Module 02 — Network request paths and service topology

**Purpose:** teach how a request finds a service, moves through the network and application tiers, and is routed or accelerated.

#### SD-02-01 — DNS as naming, caching and traffic steering

- **Prerequisites:** SD-01-02.
- **Teaching outline:** trace name resolution through the DNS hierarchy; distinguish A, CNAME, MX and NS records; explain resolver and client caching through TTL; compare weighted, latency-based and geographic routing; reason about stale answers, propagation delay, health checks and DNS as a dependency or attack surface.
- **Source map:** `#domain-name-system`.

#### SD-02-02 — HTTP requests over TCP

- **Prerequisites:** SD-02-01.
- **Teaching outline:** trace an HTTP request/response and identify where method, status, cacheability and idempotence affect retries; explain TCP connection establishment, ordered delivery, acknowledgements, retransmission, flow control and congestion control; connect connection reuse/pooling to latency and resource limits; distinguish transport success from application-level success.
- **Source map:** `#hypertext-transfer-protocol-http`; `#transmission-control-protocol-tcp`.

#### SD-02-03 — UDP and application-managed delivery

- **Prerequisites:** SD-02-02.
- **Teaching outline:** contrast datagrams with TCP streams; reason about loss, duplication, ordering and connection state; explain why an application may choose UDP and which reliability, congestion or ordering behavior then belongs above transport; cover broadcast/multicast only where the deployment supports it; compare use cases and failure visibility.
- **Source map:** `#user-datagram-protocol-udp`.

#### SD-02-04 — RPC and REST service interfaces

- **Prerequisites:** SD-02-02.
- **Teaching outline:** explain RPC stubs, serialization/marshaling and request-response semantics; explain REST resources and representations using HTTP methods and status codes; compare coupling, discoverability, client generation, latency and failure/debugging behavior; connect retries, timeouts and idempotence to either interface style; distinguish design conventions from wire-protocol guarantees.
- **Source map:** `#remote-procedure-call-rpc`; `#representational-state-transfer-rest`; `#rpc-and-rest-calls-comparison`.

#### SD-02-05 — Content delivery networks

- **Prerequisites:** SD-02-01, SD-02-02.
- **Teaching outline:** place edge caches between clients and origin; compare push and pull population; reason about cache keys, TTL/purge, origin load, geographic latency and content freshness; account for invalidation, cache misses and cost; identify which content is safe to distribute and which must remain private or dynamic.
- **Source map:** `#content-delivery-network`; `#push-cdns`; `#pull-cdns`; additional prompt “Design a content delivery network like Cloudflare.”

#### SD-02-06 — Load balancing and horizontal scaling

- **Prerequisites:** SD-02-02, SD-02-05.
- **Teaching outline:** explain health checks and choosing an eligible backend; compare round-robin, random, least-loaded and session-aware routing; distinguish active-passive and active-active deployment; compare L4 and L7 routing decisions and their visibility; connect statelessness, sticky sessions and horizontal scale; identify balancer bottlenecks and shared failure domains.
- **Source map:** `#load-balancer`; `#active-passive`; `#active-active`; `#layer-4-load-balancing`; `#layer-7-load-balancing`; `#horizontal-scaling`.

#### SD-02-07 — Reverse proxies and web-server responsibilities

- **Prerequisites:** SD-02-06.
- **Teaching outline:** explain proxying requests to backend services; distinguish proxy functions such as TLS termination, routing, compression, caching and static-file delivery; compare the roles of a reverse proxy and a load balancer while showing where one component can perform both; account for proxy failure, configuration, and added latency.
- **Source map:** `#reverse-proxy-web-server`; `#load-balancer-vs-reverse-proxy`.

#### SD-02-08 — Application tiers, microservices and service discovery

- **Prerequisites:** SD-02-04, SD-02-06.
- **Teaching outline:** separate edge/web responsibilities from application logic; explain service boundaries as independent deployable responsibilities; compare a distributed service call with an in-process call; describe service registration and lookup; account for partial failure, versioning, operational overhead and why splitting a monolith does not by itself solve scaling.
- **Source map:** `#application-layer`; `#microservices`; `#service-discovery`.

### Module 03 — Database architecture and data placement

**Purpose:** connect data semantics and access patterns to relational/non-relational models and database scaling topologies.

#### SD-03-01 — Relational databases and ACID transactions

- **Prerequisites:** SD-01-05.
- **Teaching outline:** represent related records with tables, keys and constraints; explain atomicity, consistency, isolation and durability as correctness properties; show transaction boundaries around a multi-record business change; distinguish guarantees from performance/availability costs; identify why a database choice must follow access and correctness needs.
- **Source map:** `#relational-database-management-system-rdbms`; ACID concepts described within the `#database` section.

#### SD-03-02 — Primary/replica and multi-writer replication

- **Prerequisites:** SD-03-01, SD-01-05, SD-01-06.
- **Teaching outline:** explain primary/replica read/write roles, replication lag, promotion and read-after-write consequences; separately explain master-master/multi-writer routing, concurrent writes and conflict resolution; compare topology failure modes, write availability and operational complexity; cover lost acknowledged writes, replay pressure and split brain; map each topology to an explicit consistency contract.
- **Source map:** `#master-slave-replication`; `#master-master-replication`; `#replication`; `#availability-patterns`.

#### SD-03-03 — Federation by functional ownership

- **Prerequisites:** SD-03-01.
- **Teaching outline:** explain splitting data stores by domain/function; choose routing keys from ownership and query patterns; reason about cross-database joins, transactions and reporting; compare federation with horizontal sharding and replicas; identify migration, operational and coupling costs.
- **Source map:** `#federation`.

#### SD-03-04 — Sharding, partition keys and consistent hashing

- **Prerequisites:** SD-03-02, SD-03-03.
- **Teaching outline:** distinguish table partitioning within a database from distributing shards across database nodes; select a key from access patterns and write distribution; reason about hot keys, skew, fan-out queries and rebalancing; explain consistent hashing as a placement/remapping technique and where virtual nodes help; surface migration and cross-shard transaction costs.
- **Source map:** `#sharding`; `#sql-tuning` subsection “Partition tables”; the “Consistent hashing” list item under `#under-development`.

#### SD-03-05 — Denormalization and read models

- **Prerequisites:** SD-03-01.
- **Teaching outline:** explain why duplicate or precomputed data can shorten reads; compare normalized writes with denormalized read paths; cover materialized views and write amplification; reason about keeping copies synchronized, repair and stale reads; connect denormalization to query patterns rather than treating it as a universal speed-up.
- **Source map:** `#denormalization`.

#### SD-03-06 — SQL tuning as a workload loop

- **Prerequisites:** SD-03-01.
- **Teaching outline:** begin with workload and query measurements; tighten schema and data types; choose and validate indexes against reads, writes and storage; identify expensive joins and access paths; distinguish table partitioning from horizontal sharding; evaluate query/result caches and invalidation; iterate with profiling rather than adopting a one-rule tuning recipe.
- **Source map:** `#sql-tuning`; `#tighten-up-the-schema`; `#use-good-indices`; `#avoid-expensive-joins`; `#partition-tables`; `#tune-the-query-cache`.

#### SD-03-07 — NoSQL data models and their access patterns

- **Prerequisites:** SD-03-01, SD-03-04.
- **Teaching outline:** compare key-value lookup, document retrieval, wide-column access and graph traversal; show how each model represents relationships and query paths; relate partitioning and consistency behavior to the chosen model; explain BASE as a source term that requires careful current definitions; identify when model flexibility moves complexity into application code.
- **Source map:** `#nosql`; `#key-value-store`; `#document-store`; `#wide-column-store`; `#graph-database`; BASE terminology described within `#nosql`.

#### SD-03-08 — Choosing SQL or NoSQL from workload

- **Prerequisites:** SD-03-01 through SD-03-07.
- **Teaching outline:** compare transaction and relationship needs, query shape, schema change, throughput and scaling constraints; map read/write access patterns to model fit; include operational capability and migration cost; explain why “SQL versus NoSQL” is not a single universal ranking; connect the choice to consistency and partition strategy.
- **Source map:** `#sql-or-nosql`.

### Module 04 — Caching and derived data

**Purpose:** explain where cached data lives, how it is updated, and which freshness/failure costs it introduces.

#### SD-04-01 — Cache placement across the request path

- **Prerequisites:** SD-02-05, SD-03-01.
- **Teaching outline:** compare client, CDN, web-server, database and application caches; locate the cache relative to producer and consumer; estimate hit-rate benefit against extra network hops and invalidation complexity; identify privacy and tenant-isolation requirements; distinguish cache from durable source of truth.
- **Source map:** `#client-caching`; `#cdn-caching`; `#web-server-caching`; `#database-caching`; `#application-caching`.

#### SD-04-02 — Query caches, object caches and key design

- **Prerequisites:** SD-04-01.
- **Teaching outline:** compare caching query results with caching domain objects; choose key granularity from read patterns; account for parameters, tenant and version in keys; reason about invalidation scope and duplication; use a query-cache and distributed cache example without assuming product-specific behavior.
- **Source map:** `#caching-at-the-database-query-level`; `#caching-at-the-object-level`; `solutions/system_design/query_cache/README.md`; Memcached and Redis catalog entries.

#### SD-04-03 — Cache write and refresh strategies

- **Prerequisites:** SD-04-02, SD-03-02.
- **Teaching outline:** trace cache-aside on read and write; compare write-through, write-behind/write-back and refresh-ahead; reason about write ordering, failed updates, lost buffered writes and stale windows; choose a strategy from freshness, latency and durability needs; make fallback behavior explicit.
- **Source map:** `#when-to-update-the-cache`; `#cache-aside`; `#write-through`; `#write-behind-write-back`; `#refresh-ahead`.

#### SD-04-04 — Cache freshness, eviction and distributed failure

- **Prerequisites:** SD-04-03.
- **Teaching outline:** choose TTL and invalidation behavior; compare eviction policies including LRU; reason about stampede/miss pressure, stale reads, unavailable or empty replacement nodes; explain cache distribution and key remapping under membership changes; weigh hit ratio against memory and recovery cost.
- **Source map:** remaining trade-offs under `#cache`; disadvantages under the cache strategy subsections; `solutions/system_design/query_cache/README.md`; additional prompt “Design a cache system like Memcached.” Cache-stampede handling is an Academy addition requiring evidence.

### Module 05 — Asynchronous work and distributed data processing

**Purpose:** show how systems move work off request paths and process large or parallel workloads while managing delay and overload.

#### SD-05-01 — Message queues and task queues

- **Prerequisites:** SD-02-08.
- **Teaching outline:** contrast synchronous request work with queued work; trace producer, broker/queue, consumer and acknowledgement; distinguish event/message distribution from task/job assignment; explain retry and duplicate consequences as delivery behavior to verify with primary sources; account for queue delay, ordering, dead-letter/failure handling and backlogs.
- **Source map:** `#asynchronism`; `#message-queues`; `#task-queues`.

#### SD-05-02 — Backpressure, queue growth and Little's Law

- **Prerequisites:** SD-05-01, SD-01-03.
- **Teaching outline:** connect arrival rate, processing rate and queue depth; use Little's Law with its assumptions to relate in-flight work, throughput and time; identify overload before a queue grows without bound; compare admission control, load shedding, bounded queues and consumer scaling; trace how retries can amplify overload.
- **Source map:** `#back-pressure`; Little's Law further reading under `#asynchronism` (Academy addition to the direct topic tree).

#### SD-05-03 — MapReduce and batch dataflow

- **Prerequisites:** SD-05-01, SD-03-04.
- **Teaching outline:** partition input; map records into intermediate key/value groups; shuffle/group by key; reduce and materialize output; reason about parallelism, skew, retries and intermediate data; compare batch processing boundaries to request-path computation; verify MapReduce semantics from primary research before drafting.
- **Source map:** `#under-development` MapReduce; `#real-world-architectures` MapReduce; distributed processing category.

#### SD-05-04 — Stream processing and continuous aggregation

- **Prerequisites:** SD-05-01, SD-05-02.
- **Teaching outline:** compare continuous event processing with batch recomputation; explain windows, state and late/duplicate events at a conceptual level; reason about partitioning and aggregation; compare the patterns represented in the Primer's Spark and Storm architecture references only after checking their scope/date; map these mechanisms to trending-topic and top-k designs.
- **Source map:** Spark and Storm in `#real-world-architectures`; trending and top-k prompts in `#additional-system-design-interview-questions`. Academy addition requiring current research.

#### SD-05-05 — Scatter-gather and fan-out/fan-in

- **Prerequisites:** SD-02-08, SD-05-02.
- **Teaching outline:** split a request or data set across workers; collect partial results; account for stragglers, partial failures, timeout budgets and tail latency; compare parallel speed-up with coordination and fan-in cost; choose what result is acceptable when one branch fails; verify source topic via primary distributed-systems material.
- **Source map:** `#under-development` Scatter gather.

### Module 06 — Security and protective controls

**Purpose:** cover the security mechanisms explicitly listed in the source and one adjacent traffic-protection design prompt.

#### SD-06-01 — Security boundaries for system design

- **Prerequisites:** SD-02-02, SD-03-01.
- **Teaching outline:** identify data and trust boundaries; explain encryption in transit and at rest; validate and sanitize untrusted input at the correct boundary; trace XSS and SQL-injection risks; use parameterized queries; apply least privilege to services and data stores; separate general security principles from framework-specific mitigations and research current guidance.
- **Source map:** `#security` and its listed security concerns.

#### SD-06-02 — API rate limiting and overload protection

- **Prerequisites:** SD-01-03, SD-02-06, SD-05-02.
- **Teaching outline:** define the protected resource and identity key; compare fixed-window, sliding-window and token-bucket-style limits as candidate mechanisms to verify during research; distinguish client quota from system overload control; place enforcement at edge/service boundaries; explain distributed counters, burst behavior, fairness, false rejection and degraded-mode choices.
- **Source map:** additional prompt “Design an API rate limiter.” This is a planned Academy addition; the Primer lists a prompt, not a teaching explanation.

### Module 07 — System Design Primer solution cases

**Purpose:** teach how the preceding mechanisms combine in the eight in-repository system-design case studies. These are explanatory lessons, not interview drills or quizzes.

#### SD-07-01 — Pastebin and short-link architecture

- **Prerequisites:** SD-01-03, SD-02-04, SD-03-01, SD-04-01.
- **Teaching outline:** separate create, redirect/read, expiry and analytics paths; choose identifier generation and mapping storage; trace read-heavy traffic through cache/CDN and durable store; account for collisions, hot keys, abuse and expiration cleanup; distinguish synchronous response work from analytics processing.
- **Source map:** `solutions/system_design/pastebin/README.md`; Bitly/TinyURL prompts under `#additional-system-design-interview-questions`.

#### SD-07-02 — Timelines, feeds and search

- **Prerequisites:** SD-03-02, SD-03-05, SD-04-03, SD-05-01.
- **Teaching outline:** distinguish home feed from user timeline and keyword search; compare write fan-out with read-time assembly; explain celebrity/hot-key handling and denormalized feed materialization; connect notifications and search indexing to asynchronous updates; trace stale results and reconciliation; compare the same architecture questions across Twitter and Facebook feed/timeline prompts.
- **Source map:** `solutions/system_design/twitter/README.md`; Facebook feed and timeline prompts under `#additional-system-design-interview-questions`; `#denormalization`.

#### SD-07-03 — Web crawling and search indexing

- **Prerequisites:** SD-03-04, SD-05-01, SD-05-03.
- **Teaching outline:** maintain a frontier of URLs; fetch politely and concurrently; canonicalize and deduplicate URLs/content; schedule recrawls; handle failures and changing pages; turn crawled documents into searchable indexes and serve queries; distinguish crawler throughput from relevance/ranking scope.
- **Source map:** `solutions/system_design/web_crawler/README.md`; scalable web crawler and Google search prompts under `#additional-system-design-interview-questions`.

#### SD-07-04 — Mint-style financial aggregation

- **Prerequisites:** SD-03-01, SD-05-01, SD-06-01.
- **Teaching outline:** connect accounts and ingest transactions; normalize and categorize heterogeneous records; build budgets/aggregates from source events; preserve correctness and auditability through retries and corrections; isolate credentials and sensitive data; identify freshness, reconciliation and scaling boundaries.
- **Source map:** `solutions/system_design/mint/README.md`.

#### SD-07-05 — Social graph and graph search

- **Prerequisites:** SD-03-07, SD-03-08, SD-05-03.
- **Teaching outline:** model users and relationships as graph data; compare adjacency and index access patterns; explain shortest-path search and bounded traversal; distribute graph partitions and account for cross-partition hops; connect graph search to ranking and freshness; compare exact search with product-appropriate approximations only after research.
- **Source map:** `solutions/system_design/social_graph/README.md`; “Design the data structures for a social network” solution entry; Facebook graph-search prompt under `#additional-system-design-interview-questions`; `#graph-database`.

#### SD-07-06 — Query cache and key-value search store

- **Prerequisites:** SD-03-07, SD-04-02, SD-04-04.
- **Teaching outline:** distinguish caching a database result from a key-value data store; trace cache hits, misses, fills and invalidation; choose key shape and placement; shard cache/store nodes and account for remapping; reason about hot keys and stale results; explain how a search feature can use a key-value index without conflating it with a general search engine.
- **Source map:** `solutions/system_design/query_cache/README.md`; “Design a key-value store for a search engine” solution entry under `#system-design-interview-questions-with-solutions`; Redis prompt under `#additional-system-design-interview-questions`; `#key-value-store`.

#### SD-07-07 — Sales ranking by category

- **Prerequisites:** SD-03-06, SD-05-03, SD-05-04.
- **Teaching outline:** aggregate sales events into category scores; define ranking windows and tie behavior; compare batch recomputation and incremental updates; distribute sort/top-k work; serve cached rankings; handle late corrections and freshness requirements.
- **Source map:** `solutions/system_design/sales_rank/README.md`.

#### SD-07-08 — Scaling an application on AWS

- **Prerequisites:** SD-02-05 through SD-02-08, SD-03-02, SD-04-01.
- **Teaching outline:** follow incremental growth from a single host to separated web/application/data tiers; move static assets to object storage/CDN; add a load balancer and database read replicas; introduce monitoring and autoscaling; identify bottlenecks and operational risks at each growth step; label every AWS product behavior for version-specific research.
- **Source map:** `solutions/system_design/scaling_aws/README.md`; scaling start topic; CDN, load-balancing and replication topics.

### Module 08 — Additional architecture compositions

**Purpose:** account for the Primer's additional design prompts by teaching each distinct architecture pattern. Related prompts are deliberately grouped only where the outline covers each one.

#### SD-08-01 — File synchronization and cloud storage

- **Prerequisites:** SD-03-02, SD-04-01, SD-05-01.
- **Teaching outline:** separate metadata from file bytes; detect changed files and transfer deltas; coordinate clients, versions and conflicts; store and replicate blobs; design resumable transfer, deduplication and sync notifications; identify privacy and retention constraints.
- **Source map:** Dropbox file-sync prompt in `#additional-system-design-interview-questions`; real-world file-storage examples as supporting references.

#### SD-08-02 — Collaborative document editing

- **Prerequisites:** SD-01-05, SD-02-04, SD-05-01.
- **Teaching outline:** represent edits as operations/events; order concurrent changes; explain conflict resolution and convergence requirements; persist/replay document history; distribute presence and updates; compare latency, correctness and offline-edit behavior. OT/CRDT choices are Academy additions requiring primary-source research.
- **Source map:** Google Docs prompt in `#additional-system-design-interview-questions`.

#### SD-08-03 — Recommendation systems

- **Prerequisites:** SD-03-07, SD-05-03, SD-05-04.
- **Teaching outline:** separate candidate generation from ranking; distinguish offline model/data preparation from online serving; combine user/item features and interaction events; cache or precompute results; reason about freshness, cold start and feedback loops; identify the latency and quality trade-off.
- **Source map:** Amazon recommendation prompt in `#additional-system-design-interview-questions`.

#### SD-08-04 — Realtime messaging systems

- **Prerequisites:** SD-02-03, SD-03-02, SD-04-01, SD-05-01.
- **Teaching outline:** manage connection/session state; route messages to online recipients and persist history for offline users; define delivery, ordering and retry behavior; fan out group messages; scale presence and reconnect; compare direct chat and group chat failure modes.
- **Source map:** WhatsApp and Facebook chat prompts in `#additional-system-design-interview-questions`; OOD online-chat example in the optional component-design module.

#### SD-08-05 — Photo-sharing and media delivery

- **Prerequisites:** SD-02-05, SD-03-02, SD-04-01, SD-07-02.
- **Teaching outline:** upload and validate media; store metadata separately from large objects; create asynchronous transformations/thumbnails; distribute media through a CDN; assemble profile and home feeds; manage privacy, deletion, and cache invalidation.
- **Source map:** Instagram photo-sharing prompt; related Twitter/Facebook feed prompts; CDN topic.

#### SD-08-06 — Trending topics and streaming top-k

- **Prerequisites:** SD-05-02, SD-05-04, SD-07-07.
- **Teaching outline:** define a trend window and event semantics; partition and aggregate high-volume events; maintain approximate or exact top-k candidates; handle skew, late events and changing windows; serve results with a stated freshness target; research algorithm and product guarantees before drafting.
- **Source map:** Twitter trending-topic and top-k-within-an-interval prompts; Storm in `#real-world-architectures`.

#### SD-08-07 — Distributed identifier generation

- **Prerequisites:** SD-01-03, SD-03-02, SD-03-04.
- **Teaching outline:** define uniqueness, ordering and opacity needs; compare centralized allocation, random identifiers and time/node-based schemes; reason about clock and node identity assumptions; quantify collision or coordination costs; connect identifier properties to index locality and privacy.
- **Source map:** random ID generation prompt in `#additional-system-design-interview-questions`; Pastebin/Bitly case.

#### SD-08-08 — Multi-data-center serving

- **Prerequisites:** SD-01-04 through SD-01-06, SD-03-02.
- **Teaching outline:** choose read/write locality and data ownership; compare synchronous and asynchronous replication; reason about regional failover, conflict and recovery; distinguish availability from consistency promises during inter-region partitions; account for latency, failback and operational blast radius.
- **Source map:** multiple-data-center serving prompt; `#availability-patterns`; replication topics.

#### SD-08-09 — Multiplayer game state

- **Prerequisites:** SD-02-03, SD-05-01, SD-05-05.
- **Teaching outline:** represent a game session and authoritative state; route players to a session; order actions and reject invalid transitions; handle latency, disconnect/reconnect and timeout; choose which state to persist or replay; distinguish turn-based from real-time synchronization.
- **Source map:** online multiplayer card-game prompt in `#additional-system-design-interview-questions`; scatter-gather only where independently useful.

#### SD-08-10 — Stock exchange architecture

- **Prerequisites:** SD-01-02, SD-03-01, SD-05-01.
- **Teaching outline:** separate order admission, validation, matching and market-data publication; explain ordering and deterministic state transitions; preserve an auditable event history; isolate high-throughput reads from matching writes; reason about backpressure, recovery and correctness before latency optimization.
- **Source map:** Stock Exchange prompt in `#additional-system-design-interview-questions`. The README supplies references, not verified matching-engine claims.

#### SD-08-11 — Garbage-collection system design (optional adjacent topic)

- **Prerequisites:** experience with managed runtimes; SD-01-02.
- **Teaching outline:** define managed heap and liveness at a conceptual level; compare tracing and reference-counting families; explain pause-time versus throughput goals; distinguish local runtime collection from distributed data cleanup; make clear which mechanisms are in scope and which require runtime-specific research.
- **Source map:** garbage-collection prompt in `#additional-system-design-interview-questions`. Optional because it is adjacent to, rather than a core distributed-system design topic; details require primary-source evidence.

### Module 09 — Architecture patterns from real systems

**Purpose:** turn the Primer's architecture catalog into teachable patterns while treating product names and old writeups as research leads.

#### SD-09-01 — Distributed file-system architecture

- **Prerequisites:** SD-03-02, SD-03-04, SD-05-03.
- **Teaching outline:** separate file namespace/metadata from block or chunk storage; distribute large files across storage nodes; reason about replication, chunk placement and failure recovery; compare batch-oriented file access with low-latency object access; use GFS/HDFS as historical architecture references whose actual guarantees and versions must be checked.
- **Source map:** GFS and HDFS in `#real-world-architectures`.

#### SD-09-02 — Coordination, tracing and messaging infrastructure

- **Prerequisites:** SD-01-06, SD-02-08, SD-05-01.
- **Teaching outline:** explain why distributed services need coordination/leases or configuration; distinguish coordination from data storage; trace a request across service boundaries and explain distributed tracing context; compare an event log/broker with task delivery; map Chubby, ZooKeeper, Dapper and Kafka to these patterns without implying current product equivalence.
- **Source map:** Chubby, Dapper, Kafka and ZooKeeper in `#real-world-architectures`; Kafka also maps to `#message-queues`.

### Module 10 — Optional object design foundations

**Purpose:** account for the Primer's adjacent OOD examples as an optional component-design track; this is not a prerequisite for the core distributed-systems sequence.

#### SD-10-01 — Hash tables and LRU cache components

- **Prerequisites:** experienced programmer.
- **Teaching outline:** map key equality and hashing to lookup; compare collision strategies and load-factor trade-offs; explain the hash-map plus linked-list structure for LRU order; connect eviction to the system-level cache policy in SD-04-04; mark notebook gaps instead of treating pseudocode as production behavior.
- **Source map:** `solutions/object_oriented_design/hash_table/hash_map.ipynb`; `solutions/object_oriented_design/lru_cache/lru_cache.ipynb`; eviction by LRU in the cache topic and SD-04-04.

#### SD-10-02 — Modeling workflow and physical-resource domains

- **Prerequisites:** experienced programmer.
- **Teaching outline:** identify entities, responsibilities, state and transitions; model escalation/routing in a call center; represent cards/decks/hands and specialization; allocate vehicles to differently sized parking spaces; compare the invariants and extension points each example makes explicit.
- **Source map:** OOD `call_center`, `deck_of_cards` and `parking_lot` notebooks.

#### SD-10-03 — Object model for an online chat service

- **Prerequisites:** SD-10-02.
- **Teaching outline:** model users, friend requests, private/group chats and messages; distinguish entity relationships from transport/session concerns; make membership and message-history invariants explicit; connect the object model to the separately taught distributed messaging architecture in SD-08-04.
- **Source map:** `solutions/object_oriented_design/online_chat/online_chat.ipynb`.

### Module 11 — Reading real-world architecture writeups

#### SD-11-01 — Extracting patterns from architecture reports

- **Prerequisites:** SD-01-01 through SD-09-02.
- **Teaching outline:** extract problem, workload, constraints, components and failure assumptions from an architecture report; classify each component by responsibility; compare recurring patterns and the limits of their use; separate measured evidence from author opinion and historical context; decide what claim needs a current primary source before carrying it into a lesson.
- **Source map:** `#study-guide`; `#real-world-architectures`; `#company-architectures`; `#company-engineering-blogs`.

## Coverage decisions to verify during independent review

1. Every leaf in `research/source-inventory.md` must map to an exact lesson and outline item in the final matrix. The Database regression topics federation, master-master replication, and the full SQL-tuning subtopics have explicit lesson outlines above.
2. The eight in-repository system-design solutions are all separate teaching cases in Module 07. Additional design prompts are mapped to Modules 02–10, including the distinct Google Docs, recommendation, chat, media, trend/top-k, identifier, multi-data-center, game, rate-limiter, stock-exchange and optional garbage-collection topics.
3. Primer architecture examples are examples, not a guarantee that the linked historical product details remain current. MapReduce, consistent hashing and scatter-gather have explicit teaching outlines but require primary-source research before authoring.
4. The source catalog of company architectures and engineering blogs is taught as a method of extracting and validating patterns, not as a promise to write one lesson per company or to reproduce external articles.
5. The OOD appendix is explicitly optional and adjacent. The circular-array entry has no in-repository teaching material and must receive an explicit final matrix disposition.

## Explicitly outside this plan's teaching-content scope

No assessment, quiz, exercise, answer explanation, lesson prose, diagram, copied image, or vendor-specific instruction is drafted here. The Primer's flashcard decks, translations, contribution guidance, project metadata, license, credits, source link catalogs and images remain resources or attribution inputs; they are not teaching lessons. Their specific dispositions are in `research/source-inventory.md` and must remain visible in the final source matrix where applicable.
