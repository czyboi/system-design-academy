# Pinned System Design Primer Source Inventory

**Purpose:** establish the auditable topic boundary for the new Academy curriculum. This inventory describes what is present in the source; it does not certify technical claims in the Primer.

**Source:** [System Design Primer README at commit `ae9bbd7b02d90b9866215de185217d33f39ab733`](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md)  
**Repository:** `donnemartin/system-design-primer`  
**Inspected:** 2026-11-10  
**Method:** README hierarchy and named in-repository solution collections inspected at the pinned revision. The eight system-design solution READMEs and six linked OOD notebooks were opened. External linked articles and every binary asset were not individually audited.

README anchors below are relative to the pinned README URL. A source mention or resource link does not by itself count as planned teaching coverage.

## Topic hierarchy

| Source anchor | Meaningful topics and leaves |
|---|---|
| `#study-guide` | Learning timelines; breadth versus depth; suggested reading and case-study progression. Treat as guidance for sequencing, not a separate technical lesson. |
| `#how-to-approach-a-system-design-interview-question` | `#step-1-outline-use-cases-constraints-and-assumptions`; `#step-2-create-a-high-level-design`; `#step-3-design-core-components`; `#step-4-scale-the-design`; `#back-of-the-envelope-calculations`. The external video/article under the topic-start section are references. |
| `#system-design-topics-start-here` | Vertical and horizontal scaling, clones, caches, load balancing, database replication and partitioning, asynchronous processing; links to the scalability video and article. |
| `#performance-vs-scalability` | Performance versus scalability as workload and resources grow. |
| `#latency-vs-throughput` | Latency and throughput as distinct performance measures. |
| `#availability-vs-consistency` | `#cap-theorem`; `#cp---consistency-and-partition-tolerance`; `#ap---availability-and-partition-tolerance`; behavior during network partition. |
| `#consistency-patterns` | `#weak-consistency`, `#eventual-consistency`, `#strong-consistency`; visibility of writes and replicated data. |
| `#availability-patterns` | `#fail-over`; `#active-passive`; `#active-active`; failover drawbacks; `#replication`; `#master-slave-and-master-master`; `#availability-in-numbers`; three nines and four nines; `#availability-in-parallel-vs-in-sequence`; serial and parallel availability calculations. |
| `#domain-name-system` | Name-resolution hierarchy and caches; TTL; NS, MX, A and CNAME records; weighted, latency-based and geolocation routing; delay, stale answers and DNS attacks. |
| `#content-delivery-network` | Edge delivery and origin offload; `#push-cdns`; `#pull-cdns`; cost and stale content. |
| `#load-balancer` | Health and failure handling; capacity; TLS termination and session persistence; random, least-loaded, session-based and round-robin routing; active-passive and active-active; `#layer-4-load-balancing`; `#layer-7-load-balancing`; `#horizontal-scaling`; vertical scaling; scaling and load-balancer drawbacks. |
| `#reverse-proxy-web-server` | Backend protection, routing, TLS termination, compression, caching and static content; `#load-balancer-vs-reverse-proxy`; proxy failure and operational complexity. |
| `#application-layer` | Separate web and application tiers; `#microservices`; `#service-discovery`; deployment and operational complexity. |
| `#database` | RDBMS, transactions and ACID; replication, federation, sharding, denormalization, SQL tuning, NoSQL models and SQL-versus-NoSQL choices (full leaves below). |
| `#cache` | Cache placement and granularity, update strategies, invalidation, eviction, stale data and failure behavior (full leaves below). |
| `#asynchronism` | `#message-queues`; producer/worker job lifecycle; `#task-queues`; `#back-pressure`; delay and operational trade-offs. Little's Law appears in further reading. |
| `#communication` | `#hypertext-transfer-protocol-http`; `#transmission-control-protocol-tcp`; `#user-datagram-protocol-udp`; `#remote-procedure-call-rpc`; `#representational-state-transfer-rest`; `#rpc-and-rest-calls-comparison` (full subtopics below). |
| `#security` | Encryption in transit and at rest; input validation/sanitization; XSS; SQL injection; parameterized queries; least privilege. The section notes that it may need updating. |
| `#appendix` | `#powers-of-two-table`; `#latency-numbers-every-programmer-should-know`; `#latency-numbers-visualized`; `#additional-system-design-interview-questions`; `#real-world-architectures`; `#company-architectures`; `#company-engineering-blogs`. |
| `#under-development` | Distributed computing with MapReduce; consistent hashing; scatter-gather. These are listed as in-progress topics, not complete README lessons. |

### Database topic leaves

| Source anchor | Meaningful topics and leaves |
|---|---|
| `#relational-database-management-system-rdbms` | Relational tables and transactions; ACID properties. |
| `#master-slave-replication` | Primary/replica roles, read/write routing, promotion and failover. |
| `#master-master-replication` | Multi-writer reads/writes, write routing, synchronization and conflict handling; shared replication issues include lag, lost recent writes, replay load and operational cost. |
| `#federation` | Functional partitioning, routing, cross-database joins and operational cost. |
| `#sharding` | Partitioning data across databases; shard key; skew; rebalancing; cross-shard joins; consistent-hashing reference. |
| `#denormalization` | Read/write trade-offs, duplicated data, materialized views and keeping copies synchronized. |
| `#sql-tuning` | Benchmarking/profiling; `#tighten-up-the-schema`; `#use-good-indices`; `#avoid-expensive-joins`; `#partition-tables`; `#tune-the-query-cache`. |
| `#nosql` | BASE terminology and non-relational models; `#key-value-store`; `#document-store`; `#wide-column-store`; `#graph-database`. |
| `#sql-or-nosql` | Schema and relationship needs, joins, transaction needs, workload, throughput and example access patterns. |

### Cache topic leaves

| Source anchor | Meaningful topics and leaves |
|---|---|
| `#client-caching` | Client-side cache placement and consequences. |
| `#cdn-caching` | Edge caching and content delivery. |
| `#web-server-caching` | Web-tier caching. |
| `#database-caching` | Database cache placement. |
| `#application-caching` | Application-level caching. |
| `#caching-at-the-database-query-level` | Query-result cache keys and invalidation scope. |
| `#caching-at-the-object-level` | Object cache granularity and invalidation implications. |
| `#when-to-update-the-cache` | `#cache-aside`; `#write-through`; `#write-behind-write-back`; `#refresh-ahead`; each strategy's staleness, failure and cost considerations. |
| `#cache` | TTL, eviction (including LRU), invalidation, stale data, cache failures and empty replacement nodes. |

### Communication topic leaves

| Source anchor | Meaningful topics and leaves |
|---|---|
| `#hypertext-transfer-protocol-http` | Request/response; GET, POST, PUT, PATCH and DELETE; method safety, idempotence and cacheability. |
| `#transmission-control-protocol-tcp` | Connection setup; ordering; checksums; acknowledgements and retransmission; flow and congestion control; connection pooling. |
| `#user-datagram-protocol-udp` | Connectionless datagrams; loss and ordering; broadcast and application use cases. |
| `#remote-procedure-call-rpc` | Client/server stubs; marshaling; calls and responses; coupling and debugging drawbacks. |
| `#representational-state-transfer-rest` | Resources and representations; HTTP methods and status responses; hypermedia; REST drawbacks. |
| `#rpc-and-rest-calls-comparison` | RPC and REST interface/interaction trade-offs. |

## In-repository system-design solutions

Index anchor: `#system-design-interview-questions-with-solutions`.

| Pinned repository path | Specific material to account for in the curriculum |
|---|---|
| `solutions/system_design/pastebin/README.md` | Paste/short-link creation and reads; analytics; expiry; encoding/hash choices and scaling. |
| `solutions/system_design/twitter/README.md` | Posting; home and user timelines; fanout; notifications; keyword search and scaling. |
| `solutions/system_design/web_crawler/README.md` | Crawl workflow; URL/content deduplication; recrawl scheduling; search-result serving. |
| `solutions/system_design/mint/README.md` | Financial-account connection; transaction extraction/categorization; budgeting; security and scaling. |
| `solutions/system_design/social_graph/README.md` | Social graph representation; shortest-path search and distribution. |
| `solutions/system_design/query_cache/README.md` | Cache hits/misses; cache implementation and update; distribution and consistent-hashing reference. |
| `solutions/system_design/sales_rank/README.md` | Weekly sales aggregation by category; distributed sort; serving ranked results. |
| `solutions/system_design/scaling_aws/README.md` | Incremental architecture growth; static assets; database separation/read replicas; monitoring and autoscaling. Product behavior requires version-specific research when taught. |

These solution writeups repeat some README topics. Repeated mentions should cross-reference the main topic row, not inflate the source count.

## Object-oriented design collection

Index anchor: `#object-oriented-design-interview-questions-with-solutions`. The README labels this collection as under development.

| Pinned repository path | Example |
|---|---|
| `solutions/object_oriented_design/hash_table/hash_map.ipynb` | Hash map; hash function; collision chaining; set/get/remove; load-factor assumptions. |
| `solutions/object_oriented_design/lru_cache/lru_cache.ipynb` | LRU cache; hash lookup; linked-list recency and eviction. |
| `solutions/object_oriented_design/call_center/call_center.ipynb` | Call routing; employee ranks; escalation and queue handling. |
| `solutions/object_oriented_design/deck_of_cards/deck_of_cards.ipynb` | Cards, suits, deck, hands and blackjack specialization. |
| `solutions/object_oriented_design/parking_lot/parking_lot.ipynb` | Vehicles, levels, spot sizes and parking allocation. |
| `solutions/object_oriented_design/online_chat/online_chat.ipynb` | Users, friend requests, private/group chats and messages. |

The seventh README idea, circular array, links to contribution instructions rather than an implementation. Some notebooks contain incomplete methods; none should be represented as production-ready implementations.

## Appendix and reference collections

### Additional design prompts

Anchor: `#additional-system-design-interview-questions`. The README lists 23 prompts; they are links to external materials rather than completed lessons:

1. File synchronization service (Dropbox).
2. Search engine (Google).
3. Scalable web crawler (Google).
4. Collaborative document editor (Google Docs).
5. Key-value store (Redis).
6. Cache system (Memcached).
7. Recommendation system (Amazon).
8. Short URL service (Bitly).
9. Chat application (WhatsApp).
10. Photo-sharing system (Instagram).
11. News feed (Facebook).
12. Timeline (Facebook).
13. Chat (Facebook).
14. Social graph search (Facebook).
15. Content delivery network (Cloudflare).
16. Trending topics (Twitter).
17. Random ID generation.
18. Top-k requests within a time interval.
19. Serving data from multiple data centers.
20. Online multiplayer card game.
21. Garbage collection system.
22. API rate limiter.
23. Stock exchange (NASDAQ/Binance examples).

Each item must later be explicitly mapped to a teaching lesson/outline or have a justified scope disposition. A prompt title alone is not evidence that the design is taught.

### Real-world architecture catalog

Anchor: `#real-world-architectures`. The README advises readers to identify shared principles, component purpose, limits and lessons learned rather than memorize low-level details. Its categories and listed systems are:

- **Data processing:** MapReduce, Spark, Storm.
- **Data stores and caches:** Bigtable, HBase, Cassandra, DynamoDB, MongoDB, Spanner, Memcached, Redis.
- **File systems:** Google File System (GFS), Hadoop Distributed File System (HDFS).
- **Other infrastructure:** Chubby, Dapper, Kafka, ZooKeeper.

### Company architecture and engineering-blog catalogs

- `#company-architectures` is an external case-study catalog for Amazon, Cinchcast, DataSift, Dropbox, ESPN, Google, Instagram, Justin.tv, Facebook, Flickr, Mailbox, Netflix, Pinterest, Playfish, PlentyOfFish, Salesforce, Stack Overflow, TripAdvisor, Tumblr, Twitter, Uber, WhatsApp and YouTube.
- `#company-engineering-blogs` is a separate catalog of company engineering blogs (including Airbnb, Atlassian, AWS, Bitly, Box, Cloudera, Dropbox, Quora, eBay, Evernote, Etsy, Facebook, Flickr, Foursquare, GitHub, Google, Groupon, Heroku, HubSpot, High Scalability, Instagram, Intel, Jane Street, LinkedIn, Microsoft, Netflix, PayPal, Pinterest, Reddit, Salesforce, Slack, Spotify, Stripe, Twilio, Twitter, Uber, Yahoo, Yelp and Zynga).

The links are discovery resources. Their linked articles were not individually audited and must not be represented as claims authored by the Primer.

### Quantitative references

- `#powers-of-two-table`: binary magnitudes and storage estimates.
- `#latency-numbers-every-programmer-should-know`: relative latency examples and unit conversions; `#latency-numbers-visualized` links an image.

These figures are historical reference material. Any figures reused in future teaching require current evidence and clear units/context.

## Resource and non-topic dispositions

| Source area | Inventory disposition |
|---|---|
| `#motivation`, `#contributing`, `#credits`, `#contact-info`, `#license`, `CONTRIBUTING.md` | Project context, contribution process and attribution; not System Design teaching topics. |
| `#anki-flashcards`, `resources/flash_cards/` | Three flashcard decks (System Design, System Design Exercises, OO Design). Review/assessment resources, not source lesson prose; do not copy the decks. |
| `#coding-resource-interactive-coding-challenges` | Link to a separate repository and coding-interview deck; outside this System Design teaching inventory. |
| README translations and translation requests | Alternate-language copies/resources, not additional English topic trees. |
| `images/`, embedded images and third-party diagrams | Visual assets; separate rights review required before reuse. They do not establish topic coverage. |
| “Source(s) and further reading” links | Reference catalogs. Do not treat a linked citation or product name as teaching evidence. |
| Repository software, notebooks and contribution tooling | Source artifacts and examples; inventory only where listed above. Tools are not course lessons. |

## Limitations and research flags

- The inventory covers the pinned English README topic tree and named in-repository system-design/OOD solutions. It does not recursively inventory every unrelated repository file, every asset, or every linked external article.
- The README's shorthand on CAP, ACID/isolation, NoSQL guarantees, TCP behavior, SQL tuning and cache strategies is a topic map, not current technical authority. Future lesson research must verify claim-level semantics using current primary sources.
- Security is explicitly flagged by the source as potentially needing updates. Historical latency figures, linked architectures and product descriptions also require verification before use.
- MapReduce, consistent hashing and scatter-gather are under development in the source; their proposed teaching outlines require evidence from primary technical sources before authoring.
- Coverage reviewers must independently compare the pinned repository and each matrix mapping before the plan can claim complete source coverage.
