# System Design Academy — Complete Curriculum Draft

**State:** planning candidate; not yet coverage-approved  
**Audience:** middle/senior software engineers who already build and operate backend services  
**Language:** English  
**Source boundary:** Donne Martin's System Design Primer at commit `ae9bbd7b02d90b9866215de185217d33f39ab733`; final reconciled inventory is `source-inventory.md`, and pinned solution/OOD body observations are in `../research/pinned-example-evidence-2026-11-10.md`.  
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
- **Teaching outline:** trace an HTTP request/response and identify where method, status, cacheability and idempotence affect retries; explain TCP connection establishment, ordered delivery, checksums, acknowledgements, retransmission, flow control and congestion control; connect connection reuse/pooling to latency and resource limits; distinguish transport success from application-level success.
- **Source map:** `#hypertext-transfer-protocol-http`; `#transmission-control-protocol-tcp`.

#### SD-02-03 — UDP and application-managed delivery

- **Prerequisites:** SD-02-02.
- **Teaching outline:** contrast datagrams with TCP streams; reason about loss, duplication, ordering and connection state; explain why an application may choose UDP and which reliability, congestion or ordering behavior then belongs above transport; cover broadcast/multicast use cases where the deployment supports them; compare use cases and failure visibility.
- **Source map:** `#user-datagram-protocol-udp`.

#### SD-02-04 — RPC and REST service interfaces

- **Prerequisites:** SD-02-02.
- **Teaching outline:** explain RPC stubs, serialization/marshaling and request-response semantics; explain REST resources and representations using HTTP methods and status codes; cover stateless interaction and its effect on client/server state; cover hypermedia as a REST constraint and how clients discover related actions; compare coupling, discoverability, client generation, latency and failure/debugging behavior; connect retries, timeouts and idempotence to either interface style; distinguish design conventions from wire-protocol guarantees.
- **Source map:** `#remote-procedure-call-rpc`; `#representational-state-transfer-rest`; `#rpc-and-rest-calls-comparison`.

#### SD-02-05 — Content delivery networks

- **Prerequisites:** SD-02-01, SD-02-02.
- **Teaching outline:** place edge caches between clients and origin; compare push and pull population; reason about cache keys, TTL/purge, origin load, geographic latency and content freshness; account for invalidation, cache misses and cost; identify which content is safe to distribute and which must remain private or dynamic.
- **Source map:** `#content-delivery-network`; `#push-cdns`; `#pull-cdns`; additional prompt “Design a content delivery network like Cloudflare.”

#### SD-02-06 — Load balancing and horizontal scaling

- **Prerequisites:** SD-02-02, SD-02-05.
- **Teaching outline:** explain health checks and choosing an eligible backend; compare round-robin, random, least-loaded and session-aware routing; distinguish active-passive and active-active deployment; compare L4 and L7 routing decisions and their visibility; connect statelessness, sticky sessions and horizontal scale; identify balancer bottlenecks and shared failure domains.
- **Source map:** `#load-balancer` discussion of multiple balancers in active-passive or active-active mode (the inline links point to `#active-passive`/`#active-active` under Availability patterns); `#layer-4-load-balancing`; `#layer-7-load-balancing`; `#horizontal-scaling`.

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

#### SD-04-02 — Cache granularity, keys and local file-cache limits

- **Prerequisites:** SD-04-01.
- **Teaching outline:** distinguish row-level, query-result, fully formed serializable-object and fully rendered-HTML cache values; choose granularity and keys from read patterns, parameters, tenant and version; compare invalidation scope, duplication and stale-copy risk at each level; explain why a local file cache can make instance cloning and autoscaling harder; use query-cache and distributed-cache examples without assuming product-specific behavior.
- **Source map:** `#caching-at-the-database-query-level`; `#caching-at-the-object-level`; the four cache levels and file-cache caveat in `#cache`; `solutions/system_design/query_cache/README.md`; Memcached and Redis catalog entries.

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

### Module 07 — Case studies and search systems

**Purpose:** teach how preceding mechanisms combine in the eight in-repository system-design case studies, then separate crawler ingestion from the search-index and query-serving subsystems described by the Primer. These are explanatory lessons, not interview drills or quizzes.

#### SD-07-01 — Pastebin and short-link architecture

- **Prerequisites:** SD-01-03, SD-02-04, SD-03-01, SD-04-01.
- **Teaching outline:** separate paste-text upload/storage/retrieval from short-URL mapping and redirect; check short-code uniqueness before accepting a generated code; trace the example's hash of IP plus timestamp or random input followed by Base 62 encoding; choose identifier and mapping storage; trace read-heavy traffic through cache/CDN and durable store; account for collisions, hot keys, abuse and expiry cleanup; distinguish synchronous response work from monthly hit-count analytics aggregated from Web Server logs with MapReduce, cross-referenced to SD-05-03.
- **Source map:** `solutions/system_design/pastebin/README.md`; Bitly/TinyURL prompts under `#additional-system-design-interview-questions`.

#### SD-07-02 — Timelines, feeds and notifications

- **Prerequisites:** SD-03-02, SD-03-05, SD-04-03, SD-05-01.
- **Teaching outline:** distinguish home feed from user timeline; compare write fan-out with read-time assembly; explain celebrity/hot-key handling and denormalized feed materialization; trace notification generation and timeline freshness; identify Twitter keyword search as a separate index/query-serving subsystem taught in SD-07-09 and SD-07-10; compare the same feed architecture questions across Twitter and Facebook prompts.
- **Source map:** `solutions/system_design/twitter/README.md` for posting, fan-out, timelines and notifications; Facebook feed and timeline prompts under `#additional-system-design-interview-questions`; `#denormalization`. Twitter keyword search is mapped to SD-07-09 and SD-07-10.

#### SD-07-03 — Web crawling and document acquisition

- **Prerequisites:** SD-03-04, SD-05-01.
- **Teaching outline:** maintain and prioritize a URL frontier; fetch within politeness and concurrency limits; canonicalize URLs and deduplicate URLs/content; schedule recrawls from freshness and change signals; handle failures, robots rules and changing pages; publish acquired documents to downstream processing without teaching index construction, query retrieval or ranking in this lesson.
- **Source map:** crawl-ingestion sections of `solutions/system_design/web_crawler/README.md`; scalable web crawler and Google web crawler prompts under `#additional-system-design-interview-questions`. Search-index and serving sections from the same README are mapped to SD-07-09 and SD-07-10.

#### SD-07-04 — Mint-style financial aggregation

- **Prerequisites:** SD-03-01, SD-05-01, SD-06-01.
- **Teaching outline:** connect financial accounts and ingest transactions; normalize and categorize heterogeneous records; use categorized history to recommend a budget; schedule refresh and budget updates according to freshness needs; design high availability and recovery while preserving correctness and auditability through retries/corrections; isolate credentials and sensitive data.
- **Source map:** `solutions/system_design/mint/README.md`.

#### SD-07-05 — Social graph and graph search

- **Prerequisites:** SD-03-07, SD-03-08, SD-05-03.
- **Teaching outline:** model users and relationships as graph data; state the source example's unweighted-edge assumption; compare adjacency and index access patterns; explain shortest-path search and bounded traversal; distribute graph partitions and account for cross-partition hops; connect graph search to ranking and freshness; compare exact search with product-appropriate approximations only after research.
- **Source map:** `solutions/system_design/social_graph/README.md`; “Design the data structures for a social network” solution entry; Facebook graph-search prompt under `#additional-system-design-interview-questions`; `#graph-database`.

#### SD-07-06 — Query cache and key-value search store

- **Prerequisites:** SD-03-07, SD-04-02, SD-04-04.
- **Teaching outline:** distinguish caching a database result from a key-value data store; trace cache hits, misses, fills and invalidation; choose key shape and placement; shard cache/store nodes and account for remapping; reason about hot keys and stale results; explain how a search feature can use a key-value index without conflating it with a general search engine.
- **Source map:** `solutions/system_design/query_cache/README.md`; “Design a key-value store for a search engine” solution entry under `#system-design-interview-questions-with-solutions`; Redis prompt under `#additional-system-design-interview-questions`; `#key-value-store`.

#### SD-07-07 — Sales ranking by category

- **Prerequisites:** SD-03-06, SD-05-03, SD-05-04.
- **Teaching outline:** aggregate sales events into category scores for the past week, allowing a product in multiple categories; publish refreshed results hourly; compare batch recomputation and incremental updates; distribute sorting/top-k work; serve read-heavy ranking requests; handle late corrections, availability and freshness requirements.
- **Source map:** `solutions/system_design/sales_rank/README.md`.

#### SD-07-08 — Scaling an application on AWS

- **Prerequisites:** SD-02-05 through SD-02-08, SD-03-02, SD-04-01.
- **Teaching outline:** follow incremental growth from a single host to separated web/application/data tiers; move static assets to object storage/CDN; add a load balancer and database read replicas; introduce monitoring and autoscaling; identify bottlenecks and operational risks at each growth step; label every AWS product behavior for version-specific research.
- **Source map:** `solutions/system_design/scaling_aws/README.md`; scaling start topic; CDN, load-balancing and replication topics.

#### SD-07-09 — Search index construction

- **Prerequisites:** SD-07-03, SD-03-04, SD-05-01, SD-05-03.
- **Teaching outline:** accept crawled or posted documents; parse and normalize content; deduplicate document versions; build an inverted term-to-document index; choose batch and incremental update boundaries; partition index data and publish completed segments; reason about update lag, storage growth, skew and consistency between source documents and index versions.
- **Source map:** reverse-index/document-processing sections of `solutions/system_design/web_crawler/README.md`; indexing path in `solutions/system_design/twitter/README.md`; Google search prompt under `#additional-system-design-interview-questions`.

#### SD-07-10 — Search query retrieval and ranking

- **Prerequisites:** SD-07-09, SD-04-02, SD-02-08.
- **Teaching outline:** parse a query; retrieve candidate documents from index shards; combine term matches; apply a bounded ranking stage; paginate and return results within a latency budget; use caching where keys and freshness permit; trace stale indexes, unavailable shards and partial-result choices; keep web-scale relevance models and personalization outside scope until separately evidenced.
- **Source map:** query, ranking and result-serving sections of `solutions/system_design/web_crawler/README.md`; keyword-search path in `solutions/system_design/twitter/README.md`; Google search prompt under `#additional-system-design-interview-questions`.

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

#### SD-09-01 — Distributed data-store architecture families

- **Prerequisites:** SD-03-02, SD-03-04, SD-03-07, SD-03-08.
- **Teaching outline:** map Bigtable, HBase and Cassandra to partitioned wide-column storage patterns; compare document-oriented modeling represented by MongoDB and DynamoDB; explain how a globally distributed relational store such as Spanner raises questions of replication, transaction consistency and regional placement; compare those store patterns with the key-value/cache roles of Memcached and Redis; separate the architecture pattern from any product-version claim and verify each system's semantics using primary research.
- **Source map:** Bigtable, HBase, Cassandra, DynamoDB, MongoDB, Spanner, Memcached and Redis in `#real-world-architectures`; NoSQL model and cache sections.

#### SD-09-02 — Distributed file-system architecture

- **Prerequisites:** SD-03-02, SD-03-04, SD-05-03.
- **Teaching outline:** separate file namespace/metadata from block or chunk storage; distribute large files across storage nodes; reason about replication, chunk placement and failure recovery; compare batch-oriented file access with low-latency object access; use GFS/HDFS as historical architecture references whose actual guarantees and versions must be checked.
- **Source map:** GFS and HDFS in `#real-world-architectures`.

#### SD-09-03 — Coordination, tracing and messaging infrastructure

- **Prerequisites:** SD-01-06, SD-02-08, SD-05-01.
- **Teaching outline:** explain why distributed services need coordination/leases or configuration; distinguish coordination from data storage; trace a request across service boundaries and explain distributed tracing context; compare an event log/broker with task delivery; map Chubby, ZooKeeper, Dapper and Kafka to these patterns without implying current product equivalence.
- **Source map:** Chubby, Dapper, Kafka and ZooKeeper in `#real-world-architectures`; Kafka also maps to `#message-queues`.

#### SD-09-04 — Key-value store design

- **Prerequisites:** SD-03-07, SD-03-08, SD-04-04.
- **Teaching outline:** define a key/value API and consistency/durability contract; choose value representation and memory/durable storage boundary; partition and route keys while accounting for skew and hot keys; compare replication, failure recovery, eviction and persistence choices; distinguish a general key-value store design from a cache and from any Redis-specific guarantee.
- **Source map:** `README.md#additional-system-design-interview-questions` prompt “Design a key-value store like Redis”; `README.md#real-world-architectures` Redis entry; `README.md#nosql` key-value model.

### Module 10 — Optional object design foundations

**Purpose:** account for the Primer's adjacent OOD examples as an optional component-design track; this is not a prerequisite for the core distributed-systems sequence.

#### SD-10-01 — Hash tables and LRU cache components

- **Prerequisites:** experienced programmer.
- **Teaching outline:** map key equality and hashing to lookup; explain the notebook's integer-key simplification, chaining and set/get/remove operations; state that its fixed-size table leaves load-factor handling/resizing outside the example; teach rehashing only as an Academy extension; explain the hash-map plus linked-list structure for LRU order and connect eviction to SD-04-04.
- **Source map:** `solutions/object_oriented_design/hash_table/hash_map.ipynb`; `solutions/object_oriented_design/lru_cache/lru_cache.ipynb`; eviction by LRU in the cache topic and SD-04-04.

#### SD-10-02 — Modeling workflow and physical-resource domains

- **Prerequisites:** experienced programmer.
- **Teaching outline:** identify entities, responsibilities, state and transitions; model call routing, rank escalation, queues and unhandled calls; state that the notebook excludes VIP priority from its scenario/implementation; discuss VIP priority only as a clearly labeled Academy extension; represent cards/decks/hands and specialization; allocate vehicle types to differently sized parking spaces and levels.
- **Source map:** OOD `call_center`, `deck_of_cards` and `parking_lot` notebooks.

#### SD-10-03 — Object model for an online chat service

- **Prerequisites:** SD-10-02.
- **Teaching outline:** model users, friend requests, private/group chats and messages; distinguish entity relationships from transport/session concerns; make membership and message-history invariants explicit; connect the object model to the separately taught distributed messaging architecture in SD-08-04.
- **Source map:** `solutions/object_oriented_design/online_chat/online_chat.ipynb`.

### Module 11 — Reading real-world architecture writeups

#### SD-11-01 — Extracting patterns from architecture reports

- **Prerequisites:** SD-01-01 through SD-09-04.
- **Teaching outline:** extract problem, workload, constraints, components and failure assumptions from an architecture report; classify each component by responsibility; compare recurring patterns and the limits of their use; separate measured evidence from author opinion and historical context; decide what claim needs a current primary source before carrying it into a lesson.
- **Source map:** `#study-guide`; `#real-world-architectures`; `#company-architectures`; `#company-engineering-blogs`.

## Coverage decisions to verify during independent review

1. Every leaf in `research/source-inventory.md` must map to an exact lesson and outline item in the final matrix. The Database regression topics federation, master-master replication, and the full SQL-tuning subtopics have explicit lesson outlines above.
2. The eight in-repository system-design solutions are all separate teaching cases in Module 07. Additional design prompts are mapped to Modules 02–10, including the distinct Google Docs, recommendation, chat, media, trend/top-k, identifier, multi-data-center, game, rate-limiter, stock-exchange and optional garbage-collection topics.
3. Primer architecture examples are examples, not a guarantee that the linked historical product details remain current. MapReduce, consistent hashing and scatter-gather have explicit teaching outlines but require primary-source research before authoring.
4. The source catalog of company architectures and engineering blogs is taught as a method of extracting and validating patterns, not as a promise to write one lesson per company or to reproduce external articles.
5. The OOD appendix is explicitly optional and adjacent. Circular array is explicitly excluded from the lesson plan because the pinned index contains only a contribution placeholder and no implementation or teaching material; the matrix records that disposition and rationale.

## Explicitly outside this plan's teaching-content scope

No assessment, quiz, exercise, answer explanation, lesson prose, diagram, copied image, or vendor-specific instruction is drafted here. The Primer's flashcard decks, translations, contribution guidance, project metadata, license, credits, source link catalogs and images remain resources or attribution inputs; they are not teaching lessons. Their specific dispositions are in `research/source-inventory.md` and must remain visible in the final source matrix where applicable.

## Round 1 finding dispositions

| Finding | Disposition in this candidate |
|---|---|
| A complete source-to-lesson matrix was missing at the review gate. | Added the row-level matrix below. It maps each meaningful source topic/prompt/example to a lesson and a specific outline concept, or records an explicit resource/exclusion disposition. |
| Real-world data-store examples did not have explicit mapping. | Added SD-09-01 with separate wide-column, key-value/document, globally distributed relational, and cache architecture pattern outlines. Matrix rows name every store in the catalog. |
| Load-balancer active/passive source locators were incorrect. | Removed nonexistent duplicate-heading anchors. SD-02-06 now cites the `#load-balancer` passage, which links to the active/passive and active/active patterns under Availability. |
| REST hypermedia was absent. | Added client discovery of related actions through hypermedia to SD-02-04. |
| Pastebin did not distinguish stored paste content from short URL mapping. | Added separate upload/storage/retrieval and URL-map/redirect paths to SD-07-01. |
| Google search scope was conflated with crawling. | The original revision-2 boundary is superseded by the round-3 disposition below: SD-07-03 covers crawler ingestion; SD-07-09 and SD-07-10 separately cover index construction and query retrieval/ranking. |
| Circular-array disposition was unresolved. | Explicitly excluded as a separate lesson because the pinned OOD index has only a contribution placeholder and no solution or teaching material. |
| Five solution bodies and six OOD notebook bodies were unavailable to the reviewer. | The parent fetched the five pinned solution READMEs and all six pinned `.ipynb` files through the GitHub repository-file API on 2026-11-10. The evidence summary follows the matrix. |

## Round 2 finding dispositions

| Finding | Disposition in this candidate |
|---|---|
| Load-balancer links were assigned nonexistent duplicate-heading anchors. | Replaced them with the exact `#load-balancer` passage and its inline links to `#active-passive` and `#active-active` under Availability patterns; the matrix explains that distinction. |
| Call-center VIP priority and hash-map load-factor handling were incorrectly attributed to the notebooks. | SD-10-02 and its evidence row state that VIP priority is excluded by the source and any treatment is an Academy extension. SD-10-01 and its evidence row preserve the fixed-size hash-map assumption and label rehashing as an Academy extension. |
| REST statelessness, Mint budget recommendations/high availability, and the sales-rank time window/update cadence were missing or too broad. | Added each to its lesson outline and to a specific matrix row; the source-body verification table confirms the Mint and sales-rank evidence. |
| Redis prompt mapping did not teach a key-value store design. | Added SD-09-04 with an API/contract, storage boundary, partition/routing/skew, replication, recovery, eviction and persistence outline, distinct from cache-only behavior. |
| Additional prompts, architecture catalog items and the hash-map example lacked precise source locators. | Prompt rows now include the pinned README section plus the named prompt; architecture rows include the section plus each category/item; OOD mappings cite exact notebook paths. |

## Round 3 finding dispositions

| Finding | Disposition in this candidate |
|---|---|
| Cache granularity omitted row-level and fully formed/rendered values; file-cache scaling caveat absent. | SD-04-02 now outlines row-level, query-result, serializable-object and rendered-HTML caching plus the file-cache cloning/autoscaling cost. The matrix maps all four source cache levels, the distinct object-cache subsection and the file-cache caveat. |
| Pastebin short-code uniqueness, hash/Base62 flow and monthly analytics were too vague. | SD-07-01 names the uniqueness check, source-proposed hash inputs, Base 62 encoding and monthly Web Server log aggregation through MapReduce; the lesson cross-references SD-05-03. |
| Coding-resource catalog was absent from candidate matrix. | Added an exact-anchor resource row with an explicit outside-teaching-scope disposition. |
| Crawler ingestion and search index/query-serving were combined. | SD-07-03 is limited to crawl acquisition; SD-07-09 teaches index construction; SD-07-10 teaches query retrieval and ranking. Google crawler, Google search, Twitter keyword search and the distinct crawler README sections map to their bounded outlines. |
| Pinned solution/OOD body evidence was not independently available in round 3. | Parent retrieved all 14 bodies at the pinned SHA and recorded the evidence in `../research/pinned-example-evidence-2026-11-10.md`; coverage recheck is asked to compare the revised mappings against that pack and source locators. |

## Source-to-lesson coverage matrix — revision 3

Statuses mean **planned teaching** unless marked `resource` or `excluded`. They do not mean a lesson exists or that technical claims have been verified. The Primer's additional design questions are prompts with external references, not source-authored explanations; their mapping means the Academy proposes an original case lesson and must research it independently. Real-world architecture entries are historical research leads. Repeated references map to the outline that teaches the distinct mechanism; they are not counted as extra coverage.

| Source locator/item | Disposition | Lesson | Exact outline evidence |
|---|---|---|---|
| `README.md#study-guide` | adapted | SD-01-01 | Course sequence starts broad, then deepens mechanisms and applied cases for experienced engineers. |
| `README.md#how-to-approach-a-system-design-interview-question` — Step 1: use cases, constraints, assumptions | mapped | SD-01-01 | Set system boundary, requirements, measurable constraints and assumptions. |
| README.md#how-to-approach-a-system-design-interview-question — Step 2: high-level design | mapped | SD-01-01 | Sketch components, responsibilities and connections. |
| README.md#how-to-approach-a-system-design-interview-question — Step 3: core components | mapped | SD-01-01, SD-02-04, SD-02-08 | Decompose a critical component; explain APIs and service boundaries. |
| README.md#how-to-approach-a-system-design-interview-question — Step 4: scale the design | mapped | SD-01-01, SD-01-02, SD-02-06 | Identify the bottleneck, choose a scaling action and account for its costs. |
| README.md#how-to-approach-a-system-design-interview-question — back-of-the-envelope calculations | mapped | SD-01-03 | Estimate request rate, storage, bandwidth and peak/headroom from explicit assumptions. |
| `README.md#system-design-topics-start-here` — vertical/horizontal scaling, clones, cache, load balancing, replication/partitioning, async | merged | SD-01-02, SD-02-06, SD-03-02, SD-03-04, SD-04-01, SD-05-01 | Foundations distinguish scale-up/out; later lessons teach the corresponding mechanisms and trade-offs. |
| `README.md#system-design-topics-start-here` — Scalability video/article and `#next-steps` external links | resource | SD-11-01 | Teach how to evaluate linked explanations; links are not copied or treated as Primer-authored instruction. |
| `README.md#under-development` — distributed computing with MapReduce | mapped; primary research required | SD-05-03 | Teach the explicit map, shuffle/group and reduce stages while treating the incomplete Primer entry as a topic lead. |
| `README.md#under-development` — consistent hashing | mapped; primary research required | SD-03-04 | Teach placement/remapping mechanics and assumptions; distinguish this Academy outline from the source's incomplete topic stub. |
| `README.md#under-development` — scatter-gather | mapped; primary research required | SD-05-05 | Teach fan-out/fan-in, stragglers, partial failure and tail-latency trade-offs; the source entry is explicitly incomplete. |
| `README.md#performance-vs-scalability` | mapped | SD-01-02 | Distinguish fixed-workload performance from growth under increasing workload/resources. |
| `README.md#latency-vs-throughput` | mapped | SD-01-02 | Distinguish time per request from completed work per unit time and locate saturation. |
| `README.md#availability-vs-consistency` and `#cap-theorem` | mapped | SD-01-04 | Partition behavior and the application-visible choice between returning a response and current state. |
| `#cp---consistency-and-partition-tolerance` | mapped | SD-01-04 | Explain which operations may reject/delay during partition to preserve the chosen consistency contract. |
| `#ap---availability-and-partition-tolerance` | mapped | SD-01-04 | Explain which operations may return stale/conflicting state to remain responsive during partition. |
| `README.md#consistency-patterns` — weak consistency | mapped | SD-01-05 | Define observable write visibility and stale-read behavior. |
| README.md#consistency-patterns — eventual consistency | mapped | SD-01-05 | Explain convergence and its limits for application freshness guarantees. |
| README.md#consistency-patterns — strong consistency | mapped | SD-01-05 | Explain current-state reads and consequences for replicas, latency and availability. |
| `README.md#availability-patterns` — failover, Active-passive/Active-active | mapped | SD-01-06 | Compare detection, promotion, split-brain risk, delay and loss of in-flight/recently acknowledged work. |
| README.md#availability-patterns — failover disadvantages | mapped | SD-01-06 | Identify shared failures, recovery time and coordination costs that a standby does not remove. |
| README.md#availability-patterns — replication | mapped | SD-01-06, SD-03-02 | Explain replication's role in redundancy and data placement; database topologies are taught in SD-03-02. |
| README.md#availability-patterns — availability in numbers (99.9%, 99.99%) | mapped | SD-01-06 | Convert a stated availability target to downtime over an explicit interval. |
| README.md#availability-patterns — parallel versus sequential availability | mapped | SD-01-06 | Calculate serial dependency availability and parallel redundancy while exposing shared dependencies. |
| `README.md#domain-name-system` | mapped | SD-02-01 | Trace hierarchy, resolution, caches/TTL, common record types, steering and stale-answer/failure risks. |
| `README.md#content-delivery-network` | mapped | SD-02-05 | Place edge delivery relative to origin; explain origin offload, cost and freshness. |
| README.md#content-delivery-network — Push CDNs | mapped | SD-02-05 | Explain pre-positioning content and its update/capacity trade-offs. |
| README.md#content-delivery-network — Pull CDNs | mapped | SD-02-05 | Explain fill-on-demand and origin-miss behavior. |
| `README.md#load-balancer` — routing/health; passage says multiple load balancers may use active-passive or active-active mode and links to `#active-passive`/`#active-active` under Availability patterns | mapped | SD-02-06 | Route only to eligible backends; compare deployment and routing modes using the Availability-pattern discussion, while preserving the load-balancer section as the source of the scaling example. |
| README.md#load-balancer — Layer 4 | mapped | SD-02-06 | Explain routing using transport-level connection information. |
| README.md#load-balancer — Layer 7 | mapped | SD-02-06 | Explain application-aware routing and its added visibility/cost. |
| README.md#load-balancer — horizontal scaling and disadvantages | mapped | SD-02-06 | Relate statelessness, sticky sessions, balancer bottlenecks and shared failures. |
| `README.md#reverse-proxy-web-server`; load balancer versus reverse proxy | mapped | SD-02-07 | Explain proxy routing/TLS/compression/cache/static serving and distinguish proxy responsibility from backend selection. |
| `README.md#application-layer` | mapped | SD-02-08 | Separate web and application responsibilities. |
| README.md#application-layer — microservices | mapped | SD-02-08 | Explain independent service boundaries and distributed-call costs. |
| README.md#application-layer — service discovery | mapped | SD-02-08 | Explain registration and lookup with failure/versioning implications. |
| `README.md#database` — RDBMS and ACID | mapped | SD-03-01 | Explain relational constraints and transaction properties as correctness contracts. |
| `README.md#master-slave-replication` | mapped | SD-03-02 | Primary/replica read/write routing, lag, promotion and read-after-write behavior. |
| `README.md#master-master-replication` | mapped | SD-03-02 | Multi-writer routing, concurrent updates, conflict handling and operational trade-offs. |
| `README.md#federation` | mapped | SD-03-03 | Functional ownership split, routing, cross-database joins and migration/operations costs. |
| `README.md#sharding` | mapped | SD-03-04 | Shard-key choice, skew/hotspots, cross-shard queries and rebalancing. |
| `README.md#denormalization` | mapped | SD-03-05 | Read/write trade-off, materialized views, duplicated data and repair/freshness. |
| `README.md#sql-tuning` — profile/benchmark | mapped | SD-03-06 | Start from observed workload and query measurements. |
| README.md#sql-tuning — tighten schema | mapped | SD-03-06 | Choose schema/data types for the measured access pattern. |
| README.md#sql-tuning — use indexes | mapped | SD-03-06 | Evaluate read benefit against write/storage cost. |
| README.md#sql-tuning — avoid expensive joins | mapped | SD-03-06 | Identify join/access-path costs and query shape. |
| README.md#sql-tuning — partition tables | mapped | SD-03-06 | Explain table partitioning separately from sharding. |
| README.md#sql-tuning — tune query cache | mapped | SD-03-06 | Evaluate result caching, invalidation and measurement. |
| `README.md#nosql` — BASE terminology | mapped with research flag | SD-03-07 | Compare semantics only after primary-source verification; BASE is not treated as a universal guarantee. |
| README.md#nosql — key-value store | mapped | SD-03-07 | Explain direct key lookup and its access-pattern limits. |
| README.md#nosql — document store | mapped | SD-03-07 | Explain aggregate/document retrieval and relationship/query trade-offs. |
| README.md#nosql — wide-column store | mapped | SD-03-07 | Explain partitioned row/column-family access and workload fit. |
| README.md#nosql — graph database | mapped | SD-03-07 | Explain relationship traversal and graph query patterns. |
| `README.md#sql-or-nosql` | mapped | SD-03-08 | Compare transaction/relationship needs, query shape, throughput, schema and operating costs. |
| `README.md#cache` — client caching | mapped | SD-04-01 | Explain client-side placement and its ownership/privacy implications. |
| README.md#cache — CDN caching | mapped | SD-04-01 | Explain edge placement and freshness. |
| README.md#cache — web-server caching | mapped | SD-04-01 | Explain web-tier placement relative to origin. |
| README.md#cache — database caching | mapped | SD-04-01 | Explain database cache placement and source-of-truth boundary. |
| README.md#cache — application caching | mapped | SD-04-01 | Explain application cache placement and added invalidation responsibility. |
| README.md#cache — query-level caching | mapped | SD-04-02 | Explain query-result keys and invalidation scope. |
| README.md#cache — object-level caching | mapped | SD-04-02 | Explain object granularity and duplicate/stale copies. |
| README.md#cache — row-level caching | mapped | SD-04-02 | Distinguish fine-grained row values from query and object cache values; state invalidation scope. |
| README.md#cache — fully formed serializable objects | mapped | SD-04-02 | Explain caching an assembled/serialized object and its duplicate/stale-copy cost. |
| README.md#cache — fully rendered HTML | mapped | SD-04-02 | Explain caching a rendered response and its freshness/personalization boundary. |
| README.md#cache — file-based caching caveat | mapped | SD-04-02 | Explain how node-local files complicate cloning and autoscaling. |
| README.md#cache — cache-aside | mapped | SD-04-03 | Trace miss-fill and read/write behavior. |
| README.md#cache — write-through | mapped | SD-04-03 | Trace coordinated cache/source writes and failure ordering. |
| README.md#cache — write-behind/write-back | mapped | SD-04-03 | Trace buffered writes, durability risk and replay. |
| README.md#cache — refresh-ahead | mapped | SD-04-03 | Explain proactive refresh and unnecessary work/staleness limits. |
| README.md#cache — TTL, invalidation, LRU, stale data, failure/empty node | mapped | SD-04-04 | Choose freshness/eviction policy and explain miss pressure/recovery. |
| `README.md#asynchronism` — message queues | mapped | SD-05-01 | Trace producer, queue, consumer, acknowledgement and failure handling. |
| README.md#asynchronism — task queues | mapped | SD-05-01 | Distinguish job assignment from event/message distribution. |
| README.md#asynchronism — back pressure | mapped | SD-05-02 | Bound admission/queues, shed or defer work, and avoid retry-amplified overload. |
| README.md#asynchronism — disadvantages of asynchronism | mapped | SD-05-01 | Explain delayed completion, queue/consumer operations and the extra failure/retry paths created by decoupling. |
| `README.md#asynchronism` — further-reading reference: Little's Law in further reading | supplemental | SD-05-02 | Add a researched queueing relationship and state assumptions; marked Academy addition. |
| `README.md#communication` — HTTP | mapped | SD-02-02 | Explain request/response, methods, safety/idempotence and cacheability. |
| README.md#communication — TCP | mapped | SD-02-02 | Explain setup, ordered delivery, checksums, acknowledgement/retransmission, flow/congestion control and pooling. |
| README.md#communication — UDP | mapped | SD-02-03 | Explain datagrams, loss/order, broadcast/multicast context, connection state and application-managed behavior. |
| README.md#communication — RPC | mapped | SD-02-04 | Explain stubs, marshaling, calls, coupling and debugging. |
| README.md#communication — REST resources, representation and methods | mapped | SD-02-04 | Explain resource interface and HTTP method/status semantics. |
| `README.md#representational-state-transfer-rest` — stateless interaction | mapped | SD-02-04 | Explain that each request carries the context needed for the server to process it and discuss the resulting client/server state boundary. |
| README.md#communication — REST hypermedia and RPC/REST comparison | mapped | SD-02-04 | Explain action discovery through hypermedia and compare interface/interaction trade-offs. |
| `README.md#security` — encryption in transit/at rest | mapped | SD-06-01 | Place protection at network and storage boundaries. |
| README.md#security — validate/sanitize; XSS; SQL injection; parameterized queries; least privilege | mapped | SD-06-01 | Trace input threats to validation/query mechanisms and service/data permissions. |
| `README.md#powers-of-two-table` | mapped | SD-01-03 | Use binary magnitude and unit conversion for storage/capacity estimates. |
| `README.md#latency-numbers-every-programmer-should-know` and `#latency-numbers-visualized` | mapped/resource | SD-01-03 | Teach request-path latency decomposition; treat visual/table values as historical references requiring current evidence. |
| `solutions/system_design/pastebin/README.md` | mapped | SD-07-01 | Separate paste storage/retrieval from short-code mapping/redirect; check uniqueness, hash input and Base 62 flow; cross-reference monthly log-to-MapReduce hit counts with SD-05-03. |
| `solutions/system_design/twitter/README.md` | mapped | SD-07-02, SD-07-09, SD-07-10 | Map posting, timeline fanout and notifications to SD-07-02; map keyword search's index and query paths to SD-07-09 and SD-07-10. |
| `solutions/system_design/web_crawler/README.md` — crawl acquisition sections | mapped | SD-07-03 | Explain prioritized frontier, polite/concurrent fetch, canonicalization/deduplication, recrawl and failure handling. |
| `solutions/system_design/web_crawler/README.md` — reverse index/document processing | mapped | SD-07-09 | Explain parsing, inverted-index construction, partitioned index data and update lag. |
| `solutions/system_design/web_crawler/README.md` — user query, ranking and results | mapped | SD-07-10 | Explain candidate retrieval, bounded ranking, serving latency and partial failure choices. |
| `solutions/system_design/mint/README.md` | mapped | SD-07-04 | Explain account connection, transaction extraction/categorization, budget recommendations, scheduled freshness and high-availability/recovery design. |
| `solutions/system_design/social_graph/README.md` | mapped | SD-07-05 | Explain an unweighted shortest-path query over a graph too large for one machine. |
| `solutions/system_design/query_cache/README.md` | mapped | SD-07-06 | Explain query cache hit/miss, limited-memory placement, key/value choice and distribution. |
| `solutions/system_design/sales_rank/README.md` | mapped | SD-07-07 | Explain the past-week category ranking, hourly publication updates, multi-category products, distributed sort/top results and read-heavy serving. |
| `solutions/system_design/scaling_aws/README.md` | mapped | SD-07-08 | Explain incremental growth from a single host through static-asset separation, read replicas, monitoring and autoscaling; research AWS versions separately. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Dropbox/file sync | mapped | SD-08-01 | Separate metadata/blob, deltas, versions, conflicts, resumable transfer and notifications. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Google search engine | mapped | SD-07-09, SD-07-10 | Teach document indexing in SD-07-09 and query retrieval/ranking/serving in SD-07-10; web-scale relevance and personalization remain out of scope pending evidence. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Google web crawler | mapped | SD-07-03 | Explain crawl frontier, politeness/concurrency, canonicalization, dedupe, recrawl and failure handling. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Google Docs | mapped | SD-08-02 | Explain operations, concurrent edits, ordering/convergence, history and offline behavior; OT/CRDT require research. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Redis key-value store | mapped | SD-09-04 | Define key/value operations, storage/durability contract, partitioning, replication, recovery and cache-versus-store distinction. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Memcached cache | mapped | SD-04-04, SD-09-01 | Explain cache-specific placement/eviction/failure and the architecture catalog distinction. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — recommendation system | mapped | SD-08-03 | Explain candidate generation, online ranking, features, caching, cold start and feedback. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Bitly/TinyURL | mapped | SD-07-01 | Explain identifier allocation, short-code mapping, redirect and expiry. |
| `README.md#additional-system-design-interview-questions` — Additional prompts — WhatsApp chat and Facebook chat | merged | SD-08-04 | Explain connections/presence, delivery/order/retry, group fanout and offline history. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Instagram/photo sharing | mapped | SD-08-05 | Explain upload, metadata/blob split, async transforms, CDN and privacy-aware feed delivery. |
| `README.md#additional-system-design-interview-questions` — Additional prompts — Facebook news feed and timeline | merged | SD-07-02 | Explain feed fanout/materialization, read-time assembly and timeline freshness. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Facebook graph search | mapped | SD-07-05 | Explain graph traversal, partition hops and bounded/approximate result choice. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — Cloudflare-like CDN | mapped | SD-02-05 | Explain edge cache placement, push/pull, invalidation and origin behavior. |
| `README.md#additional-system-design-interview-questions` — Additional prompts — Twitter trending and top-k per interval | merged | SD-08-06 | Explain windows, partitioned aggregation, skew, late events and top-k freshness. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — random identifier generation | mapped | SD-08-07 | Compare uniqueness/order/opacity needs, allocation coordination and collision/clock assumptions. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — multiple data centers | mapped | SD-08-08 | Explain regional read/write placement, replication, partition behavior, failover and recovery. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — multiplayer card game | mapped | SD-08-09 | Explain authoritative session state, action ordering, reconnect and persistence. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — garbage-collection system | mapped optional | SD-08-11 | Teach a limited systems-adjacent conceptual scope; optionality is explicit and primary-source research required. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — API rate limiter | mapped Academy addition | SD-06-02 | Explain identity keys, limit mechanism, distributed counters, burst/fairness and overload behavior. |
| `README.md#additional-system-design-interview-questions` — Additional prompt — stock exchange | mapped Academy addition | SD-08-10 | Explain order admission/matching, deterministic state, audit log, backpressure and recovery. |
| `README.md#real-world-architectures` — Real-world data processing — MapReduce | mapped | SD-05-03 | Explain map, shuffle/group, reduce, skew and retry/recovery. |
| `README.md#real-world-architectures` — Real-world architecture category — data processing | adapted | SD-05-03, SD-05-04 | Explain batch and continuous processing patterns represented by the catalog. |
| `README.md#real-world-architectures` — Real-world data processing — Spark | mapped as architecture example | SD-05-04 | Compare its documented processing boundary only after verifying the historical reference with primary sources. |
| `README.md#real-world-architectures` — Real-world data processing — Storm | mapped as architecture example | SD-05-04 | Compare its documented continuous processing boundary only after verifying the historical reference with primary sources. |
| `README.md#real-world-architectures` — Real-world architecture category — data stores and caches | adapted | SD-09-01 | Teach recurring architecture families represented by the catalog rather than every external product implementation. |
| `README.md#real-world-architectures` — Real-world store — Bigtable | mapped as architecture example | SD-09-01 | Teach partitioned wide-column storage patterns; verify product semantics in current primary sources. |
| `README.md#real-world-architectures` — Real-world store — HBase | mapped as architecture example | SD-09-01 | Teach the wide-column implementation relationship identified by the source; verify product/version semantics. |
| `README.md#real-world-architectures` — Real-world store — Cassandra | mapped as architecture example | SD-09-01 | Teach partitioned wide-column architecture questions; verify product/version semantics. |
| `README.md#real-world-architectures` — Real-world store — DynamoDB | mapped as architecture example | SD-09-01 | Teach the source-listed document-oriented pattern; verify current product semantics instead of inferring guarantees from the Primer label. |
| `README.md#real-world-architectures` — Real-world store — MongoDB | mapped as architecture example | SD-09-01 | Teach document-oriented access-pattern fit; verify current guarantees separately. |
| `README.md#real-world-architectures` — Real-world store — Spanner | mapped as architecture example | SD-09-01 | Explain global relational placement, transaction/replication questions and regional trade-offs; verify current product semantics. |
| `README.md#real-world-architectures` — Real-world cache — Memcached | mapped | SD-04-02, SD-04-04, SD-09-01 | Teach cache role, memory/eviction, invalidation and distributed placement where supported by current evidence. |
| `README.md#real-world-architectures` — Real-world cache — Redis | mapped | SD-04-02, SD-04-04, SD-09-01 | Teach cache/data-structure role, persistence distinction where evidenced, eviction, invalidation and distribution. |
| `README.md#real-world-architectures` — Real-world architecture category — file systems | adapted | SD-09-02 | Explain distributed file-system patterns represented by the catalog. |
| `README.md#real-world-architectures` — Real-world file system — GFS | mapped | SD-09-02 | Explain metadata/data blocks, chunk placement, replication and recovery as architecture patterns. |
| `README.md#real-world-architectures` — Real-world file system — HDFS | mapped | SD-09-02 | Explain metadata/data blocks, chunk placement, replication and recovery as architecture patterns. |
| `README.md#real-world-architectures` — Real-world architecture category — other infrastructure | adapted | SD-09-03 | Explain coordination, tracing and messaging roles represented by the catalog. |
| `README.md#real-world-architectures` — Real-world infrastructure — Chubby, ZooKeeper | mapped as pattern examples | SD-09-03 | Explain coordination/configuration and the assumptions/cost of a shared coordination service. |
| `README.md#real-world-architectures` — Real-world infrastructure — Dapper | mapped as pattern example | SD-09-03 | Explain request tracing across service boundaries and context propagation. |
| `README.md#real-world-architectures` — Real-world infrastructure — Kafka | mapped as pattern example | SD-05-01, SD-09-03 | Explain broker/log role and distinguish event streaming from task assignment after verifying semantics. |
| `README.md#object-oriented-design-interview-questions-with-solutions` (under development) | adapted optional | SD-10-01–03 | Teach the six linked component examples in an explicitly optional track; preserve notebook assumptions and incompleteness. |
| `README.md#company-architectures` external catalog | resource | SD-11-01 | Teach extracting constraints, responsibilities, evidence and historical context; do not create one lesson per linked company article. |
| `README.md#company-engineering-blogs` external catalog | resource | SD-11-01 | Teach how to assess a primary company writeup and its date/claim provenance. |
| `solutions/object_oriented_design/hash_table/hash_map.ipynb` | mapped optional | SD-10-01 | Teach the notebook's integer-key simplification, chaining and set/get/remove; state that load-factor handling/resizing is outside its fixed-size example; rehashing is an Academy extension. |
| `solutions/object_oriented_design/lru_cache/lru_cache.ipynb` | mapped optional | SD-10-01 | Teach hash lookup plus linked-list recency/eviction; relate to SD-04-04. |
| `solutions/object_oriented_design/call_center/call_center.ipynb` | mapped optional | SD-10-02 | Teach call routing, rank escalation, queues and unhandled calls; preserve the notebook's exclusion of VIP priority, which is only an Academy extension. |
| `solutions/object_oriented_design/deck_of_cards/deck_of_cards.ipynb` | mapped optional | SD-10-02 | Teach card/deck/hand responsibilities and blackjack specialization assumptions. |
| `solutions/object_oriented_design/parking_lot/parking_lot.ipynb` | mapped optional | SD-10-02 | Teach vehicle types, spot sizes, levels and allocation rules. |
| `solutions/object_oriented_design/online_chat/online_chat.ipynb` | mapped optional | SD-10-03 | Teach users, friend requests, private/group chats and messages; distinguish object model from SD-08-04 distribution. |
| `README.md#object-oriented-design-interview-questions-with-solutions` — circular array contribution placeholder | excluded with rationale | — | The pinned index links to contribution guidance and has no implementation or teaching material; no separate lesson is justified. Revisit only if the pinned source adds content or the Academy changes scope. |
| `README.md#motivation`, `README.md#contributing`, `README.md#credits`, `README.md#contact-info`, `README.md#license`, `CONTRIBUTING.md` | resource | — | Project context, attribution, licensing and contributor process; not teaching material. |
| `README.md#anki-flashcards`, `resources/flash_cards/` decks | resource | — | Assessment/review assets; no deck content is copied into lessons or this plan. |
| `README.md` translation links; `README-ja.md`, `README-zh-Hans.md`, `README-zh-TW.md` and other listed language variants | resource | — | Alternate-language resources, not additional English topic trees. |
| `README.md#coding-resource-interactive-coding-challenges` | resource / outside teaching scope | — | The linked interactive-coding repository and coding deck are resource references, not System Design teaching topics. |
| `images/` and embedded external diagrams | resource | — | Asset rights must be checked separately; images do not establish instructional coverage. |
| README “Source(s) and further reading” sections and linked external articles | resource | SD-11-01 | References inform later claim research; a citation or linked product name is not teaching evidence. |
| Repository software tools and notebook code | resource | — | Inventory only; tools are not course lessons. |

## Pinned example-body verification performed during revision

GitHub repository-file API reads at the pinned commit on 2026-11-10 verified the following body details beyond the README titles:

| Pinned file(s) | Observed source material | Plan check |
|---|---|---|
| `solutions/system_design/mint/README.md` | Connect a financial account; extract transactions; recommend a budget; high availability; scheduled refresh assumptions; large account/transaction volume and a read/write ratio. | SD-07-04 explicitly includes account connection, ingestion/categorization, budget recommendation, refresh freshness, high availability/recovery, correctness and privacy. |
| `solutions/system_design/social_graph/README.md` | Search for a person and show the shortest path; unweighted graph; data does not fit one machine; high availability. | SD-07-05 includes graph representation, shortest-path query and partitioned traversal. |
| `solutions/system_design/query_cache/README.md` | Query cache hit and miss; ordered query-to-results values; limited memory, low-latency placement and nonuniform traffic. | SD-07-06 covers hit/miss/fill, key/value choice, limited memory and distribution. |
| `solutions/system_design/sales_rank/README.md` | Past week's popular products by category; hourly result updates; items may be in multiple categories; read-heavy serving. | SD-07-07 explicitly covers this window/update cadence, multi-category products, distributed sort/top-k and read-heavy serving. |
| `solutions/system_design/scaling_aws/README.md` | Evolve from a basic single-host setup to millions of users; relational data; separate static assets; add read replicas, monitoring and autoscaling over steps. | SD-07-08 describes this progression and marks AWS behavior for version-specific research. |
| `solutions/system_design/pastebin/README.md` | Creation verifies code uniqueness; proposed code uses hash(IP + timestamp) or random input then Base 62 encoding; monthly Web Server logs feed MapReduce hit-count aggregation. | SD-07-01 names all three mechanisms and points to SD-05-03 for MapReduce. |
| `solutions/system_design/twitter/README.md` | Posting, fan-out, notifications, timelines and a distinct keyword-search path. | SD-07-02 is limited to social delivery/timelines; SD-07-09 and SD-07-10 own index and query-serving content. |
| `solutions/system_design/web_crawler/README.md` | Crawl acquisition and recrawl; a downstream reverse-index/document-processing path; a separate user query/ranking/results path. | SD-07-03, SD-07-09 and SD-07-10 each own one named subsystem and its matrix rows. |
| `solutions/object_oriented_design/hash_table/hash_map.ipynb`; `solutions/object_oriented_design/lru_cache/lru_cache.ipynb` | Hash-map integer-key simplification, chaining and operations; load-factor handling is outside the fixed-size example; LRU cache's hash lookup and recency structure. | SD-10-01 preserves those assumptions; any resizing/rehashing treatment is marked an Academy extension. |
| `solutions/object_oriented_design/call_center/call_center.ipynb` | Employee rank/escalation, queueing and what happens when nobody can answer; VIP priority is excluded by the source scenario/implementation. | SD-10-02 covers routing/escalation/unhandled calls and explicitly does not credit VIP behavior as source content. |
| `solutions/object_oriented_design/deck_of_cards/deck_of_cards.ipynb`; `parking_lot/parking_lot.ipynb` | Deck/card/suit/blackjack assumptions; vehicle types, different spot sizes and multiple levels. | SD-10-02 outlines both domain models and allocation/specialization decisions. |
| `solutions/object_oriented_design/online_chat/online_chat.ipynb` | User/friend-request/chat/message entities; notebook says not to address scaling initially. | SD-10-03 teaches object boundaries only; distributed behavior is separately taught in SD-08-04. |

The exact quantitative assumptions and historical system/product behavior in these examples are not copied as current facts. Their future authors must use approved primary sources and preserve the distinction between the example scenario and current engineering guarantees.

The remaining three in-repository system-design solution bodies were also checked in the independent review: Pastebin's body/content versus short-code/redirect flows, Twitter's post/feed/search flows, and crawler frontier/fetch/deduplication/recrawl/search indexing. The matrix above maps those distinct mechanisms to their corresponding lessons.
