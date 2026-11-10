# Course delivery plan — SDA-v1

Official outline: [approved baseline](../curriculum/approved-baseline.json). Planning task: SD-COURSE-DELIVERY-PLAN ([Issue 16](https://github.com/czyboi/system-design-academy/issues/16)).

## Backlog contract

15 Epics, 73 Stories, 579 Subtasks. Full scope, source topic IDs, outputs, dependencies and acceptance criteria are in [backlog.json](backlog.json). Codes are local Jira-style IDs; no Jira project or external tickets have been created for the planned packages.

One Epic per module plus a final-course Epic. One independently authorable Story per lesson; one per module integration package; separate capstone and final audit stories. R/G/D/A/T/P/V/H suffixes mean research, approved gate, teaching draft, companion assessment, technical/provenance review, teaching review, validation, human acceptance. D and A execute within the single author step of the six-step lesson pipeline. The two reviews can run in parallel and must be independent. Revisions are conditional, up to two cycles.

## Delivery order and readiness

1. W0: official baseline recorded; confirm intake prerequisites and output ownership before claiming a story.
2. W1: M00–M03 foundations.
3. W2: M04–M06 storage and caching.
4. W3: M07–M09 asynchronous systems, processing and operations.
5. W4: M10 system compositions.
6. W5: M11 domain applications and M12 local object design.
7. W6: M13 synthesis, then CP-01 and whole-course audit.

These are dependency waves, not dated sprints or duration estimates. Exact story dependencies in JSON govern scheduling; a wave is a navigation aid, not an extra completion gate. Estimate after the first accepted package provides evidence. Assign an owner only when work is claimed. M00-L01 is the initial eligible lesson story.

At intake create/reuse one Issue/spec/state/worklog per bounded Story; do not create Issues for internal subtasks. Use course/lesson templates where applicable, and an explicitly scoped package graph for integration/capstone. All future content stays draft until independently reviewed and accepted by a human. Workflow edits belong to separate SD-WORKFLOW tasks and are not part of this backlog.

## Acceptance and carry-forward feedback

N1 from the accepted course review is recorded on M03-L02 and M06-L01: later lesson references are previews/deferred comparisons. Each lesson companion assesses all its own outcomes; module exercises and capstone assess only their declared synthesis/transfer subsets. Whole-course acceptance needs the complete teaching and assessment portfolio, not capstone success alone.

## Epic and Story index

| Epic | Story | Package | Depends on |
|---|---|---|---|
| SDA-M00 | SDA-M00-L01 | How to learn and check readiness | Entry knowledge |
| SDA-M00 | SDA-M00-L02 | From requirements to a defensible design | SDA-M00-L01 |
| SDA-M00 | SDA-M00-INT | Integrated design, reference solution and decision summary | SDA-M00-L01, SDA-M00-L02 |
| SDA-M01 | SDA-M01-L01 | Capacity and latency budgets | SDA-M00-L02 |
| SDA-M01 | SDA-M01-L02 | Performance versus scalability | SDA-M01-L01 |
| SDA-M01 | SDA-M01-L03 | Consistency and partition decisions | SDA-M01-L02 |
| SDA-M01 | SDA-M01-L04 | Availability and failover budgets | SDA-M01-L03 |
| SDA-M01 | SDA-M01-INT | Integrated design, reference solution and decision summary | SDA-M01-L01, SDA-M01-L02, SDA-M01-L03, SDA-M01-L04 |
| SDA-M02 | SDA-M02-L01 | DNS and endpoint discovery | SDA-M01-L04 |
| SDA-M02 | SDA-M02-L02 | TCP, UDP and HTTP | SDA-M02-L01 |
| SDA-M02 | SDA-M02-L03 | Load balancing and reverse proxies | SDA-M02-L02 |
| SDA-M02 | SDA-M02-L04 | CDN push, pull and cache control | SDA-M02-L03 |
| SDA-M02 | SDA-M02-INT | Integrated design, reference solution and decision summary | SDA-M02-L01, SDA-M02-L02, SDA-M02-L03, SDA-M02-L04 |
| SDA-M03 | SDA-M03-L01 | Application layers and microservices | SDA-M02-L03 |
| SDA-M03 | SDA-M03-L02 | REST, RPC and interface contracts | SDA-M02-L02, SDA-M03-L01 |
| SDA-M03 | SDA-M03-L03 | Service discovery and resilient calls | SDA-M03-L02, SDA-M02-L01 |
| SDA-M03 | SDA-M03-INT | Integrated design, reference solution and decision summary | SDA-M03-L01, SDA-M03-L02, SDA-M03-L03 |
| SDA-M04 | SDA-M04-L01 | Relational invariants and query-driven models | SDA-M03-L02 |
| SDA-M04 | SDA-M04-L02 | Single-leader and multi-writer replication | SDA-M04-L01, SDA-M01-L04 |
| SDA-M04 | SDA-M04-L03 | Federation, sharding and consistent hashing | SDA-M04-L02 |
| SDA-M04 | SDA-M04-L04 | Denormalisation and derived views | SDA-M04-L03 |
| SDA-M04 | SDA-M04-L05 | SQL tuning as an evidence loop | SDA-M04-L04 |
| SDA-M04 | SDA-M04-INT | Integrated design, reference solution and decision summary | SDA-M04-L01, SDA-M04-L02, SDA-M04-L03, SDA-M04-L04, SDA-M04-L05 |
| SDA-M05 | SDA-M05-L01 | Key-value and document stores | SDA-M04-L03 |
| SDA-M05 | SDA-M05-L02 | Wide-column and graph stores | SDA-M05-L01 |
| SDA-M05 | SDA-M05-L03 | SQL versus NoSQL and distributed-store guarantees | SDA-M05-L02, SDA-M01-L03 |
| SDA-M05 | SDA-M05-INT | Integrated design, reference solution and decision summary | SDA-M05-L01, SDA-M05-L02, SDA-M05-L03 |
| SDA-M06 | SDA-M06-L01 | Where and what to cache | SDA-M05-L01, SDA-M02-L04 |
| SDA-M06 | SDA-M06-L02 | Cache update and coherence policies | SDA-M06-L01 |
| SDA-M06 | SDA-M06-L03 | Bounded LRU and distributed query cache | SDA-M06-L02, SDA-M04-L03 |
| SDA-M06 | SDA-M06-INT | Integrated design, reference solution and decision summary | SDA-M06-L01, SDA-M06-L02, SDA-M06-L03 |
| SDA-M07 | SDA-M07-L01 | Message queues and task queues | SDA-M03-L03 |
| SDA-M07 | SDA-M07-L02 | Back pressure, bounded work and retry control | SDA-M07-L01, SDA-M01-L02 |
| SDA-M07 | SDA-M07-L03 | Event logs, ordering and replay | SDA-M07-L02 |
| SDA-M07 | SDA-M07-INT | Integrated design, reference solution and decision summary | SDA-M07-L01, SDA-M07-L02, SDA-M07-L03 |
| SDA-M08 | SDA-M08-L01 | MapReduce and distributed file storage | SDA-M07-L03 |
| SDA-M08 | SDA-M08-L02 | Streaming aggregation, trends and top-k | SDA-M08-L01 |
| SDA-M08 | SDA-M08-L03 | Indexes and scatter-gather search | SDA-M05-L02, SDA-M07-L03 |
| SDA-M08 | SDA-M08-INT | Integrated design, reference solution and decision summary | SDA-M08-L01, SDA-M08-L02, SDA-M08-L03 |
| SDA-M09 | SDA-M09-L01 | Security by trust boundary | SDA-M03-L02, SDA-M02-L03 |
| SDA-M09 | SDA-M09-L02 | Measure, trace and recover | SDA-M09-L01, SDA-M01-L04 |
| SDA-M09 | SDA-M09-L03 | Coordination and multi-data-centre control | SDA-M09-L02, SDA-M05-L03 |
| SDA-M09 | SDA-M09-INT | Integrated design, reference solution and decision summary | SDA-M09-L01, SDA-M09-L02, SDA-M09-L03 |
| SDA-M10 | SDA-M10-L01 | Paste storage, short links and expiry | SDA-M06-L03, SDA-M09-L01 |
| SDA-M10 | SDA-M10-L02 | Social feed publication and timelines | SDA-M10-L01, SDA-M07-L03 |
| SDA-M10 | SDA-M10-L03 | Crawler and web-search composition | SDA-M08-L03, SDA-M10-L02 |
| SDA-M10 | SDA-M10-L04 | Financial aggregation and budgeting | SDA-M08-L01, SDA-M09-L01 |
| SDA-M10 | SDA-M10-L05 | Distributed social-graph traversal | SDA-M05-L02, SDA-M09-L03 |
| SDA-M10 | SDA-M10-L06 | Search query cache at service scale | SDA-M06-L03, SDA-M08-L03 |
| SDA-M10 | SDA-M10-L07 | Category sales ranking | SDA-M08-L02, SDA-M10-L04 |
| SDA-M10 | SDA-M10-L08 | Iteratively scaling a cloud application | SDA-M09-L02, SDA-M10-L07 |
| SDA-M10 | SDA-M10-INT | Integrated design, reference solution and decision summary | SDA-M10-L01, SDA-M10-L02, SDA-M10-L03, SDA-M10-L04, SDA-M10-L05, SDA-M10-L06, SDA-M10-L07, SDA-M10-L08 |
| SDA-M11 | SDA-M11-L01 | File synchronisation and collaborative documents | SDA-M10-L03 |
| SDA-M11 | SDA-M11-L02 | Messaging and media sharing | SDA-M10-L02 |
| SDA-M11 | SDA-M11-L03 | Recommendation and graph search | SDA-M10-L05, SDA-M08-L03 |
| SDA-M11 | SDA-M11-L04 | CDN as a service and global data serving | SDA-M10-L08, SDA-M09-L03 |
| SDA-M11 | SDA-M11-L05 | Unique-ID service | SDA-M10-L01, SDA-M09-L03 |
| SDA-M11 | SDA-M11-L06 | Distributed API rate limiter | SDA-M07-L02, SDA-M11-L05 |
| SDA-M11 | SDA-M11-L07 | Multiplayer card games and exchange order books | SDA-M11-L06, SDA-M09-L03 |
| SDA-M11 | SDA-M11-L08 | Memory reclamation | SDA-M00-L01, SDA-M11-L07 |
| SDA-M11 | SDA-M11-L09 | Key-value store and disposable cache composition | SDA-M10-L06, SDA-M11-L08 |
| SDA-M11 | SDA-M11-INT | Integrated design, reference solution and decision summary | SDA-M11-L01, SDA-M11-L02, SDA-M11-L03, SDA-M11-L04, SDA-M11-L05, SDA-M11-L06, SDA-M11-L07, SDA-M11-L08, SDA-M11-L09 |
| SDA-M12 | SDA-M12-L01 | Hash-table contracts and collisions | SDA-M00-L01 |
| SDA-M12 | SDA-M12-L02 | LRU object collaboration | SDA-M12-L01, SDA-M06-L03 |
| SDA-M12 | SDA-M12-L03 | Parking allocation and contiguous resources | SDA-M12-L01 |
| SDA-M12 | SDA-M12-L04 | Call-centre dispatch and escalation | SDA-M12-L03 |
| SDA-M12 | SDA-M12-L05 | Cards, decks and scoring | SDA-M12-L04 |
| SDA-M12 | SDA-M12-L06 | Chat domain and relationship states | SDA-M12-L05, SDA-M11-L02 |
| SDA-M12 | SDA-M12-INT | Integrated design, reference solution and decision summary | SDA-M12-L01, SDA-M12-L02, SDA-M12-L03, SDA-M12-L04, SDA-M12-L05, SDA-M12-L06 |
| SDA-M13 | SDA-M13-L01 | Read architecture families critically | SDA-M10-L08, SDA-M12-L06 |
| SDA-M13 | SDA-M13-INT | Integrated design, reference solution and decision summary | SDA-M13-L01 |
| SDA-FINAL | SDA-CP-01 | Cross-module marketplace design capstone | SDA-M00-INT, SDA-M01-INT, SDA-M02-INT, SDA-M03-INT, SDA-M04-INT, SDA-M05-INT, SDA-M06-INT, SDA-M07-INT, SDA-M08-INT, SDA-M09-INT, SDA-M10-INT, SDA-M11-INT, SDA-M12-INT, SDA-M13-INT |
| SDA-FINAL | SDA-COURSE-AUDIT | Whole-course taught coverage and portfolio acceptance | SDA-CP-01 |
