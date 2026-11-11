# Course delivery plan — SDA-v1

The approved SDA-v1 baseline defines the teaching scope and learner prerequisites. The backlog was created in [Issue 16](https://github.com/czyboi/system-design-academy/issues/16) and the delivery rules were revised in [Issue 17](https://github.com/czyboi/system-design-academy/issues/17). See the [baseline approval record](../curriculum/approved-baseline.json).

## Backlog contract

15 Epics, 73 Stories, 579 Subtasks. [backlog.json](backlog.json) records scope, source topic IDs, outputs, dependencies and acceptance criteria. These are local Jira-style IDs. Claim each Story through one Issue/spec/state/worklog and confirm exact input and output paths.

One Epic covers each module, with a final-course Epic for the capstone and audit. Historical backlog labels R/G/D/A/T/P/V/H mean research, course gate, teaching draft, companion assessment, technical/provenance review, teaching review, validation and human acceptance. New default execution is **research → author**, producing draft D/A together; T/P/V are optional user-triggered checks, not a mandatory automated continuation. H is a separate explicit human release decision.

## Delivery milestones

Each milestone groups existing Stories into one reviewable handoff. The backlog owns the Story membership. Select one, several or all nine milestones for a run. The [execution plan](EXECUTION_PLAN.md) describes readiness and handoff checks for the selected scope. See [Issue 18](https://github.com/czyboi/system-design-academy/issues/18).

| Milestone | Scope | Handoff result |
|---|---|---|
| SDA-MS01 Design method and foundations | M00–M01 (6 lessons) | A document-sharing design brief and an order-status service workload model comparing two failure policies. |
| SDA-MS02 Request paths and service boundaries | M02–M03 (7 lessons) | A global image catalogue request path and a justified service split with APIs and failure handling. |
| SDA-MS03 Data storage and scaling | M04–M05 (8 lessons) | An order database evolution under read growth, write growth and a hot tenant, plus storage choices for distinct access patterns. |
| SDA-MS04 Caching and asynchronous work | M06–M07 (6 lessons) | A query-result cache under a hot query and node loss, plus a media processing pipeline with status, retries and overload control. |
| SDA-MS05 Processing, retrieval and operations | M08–M09 (6 lessons) | A ranking and sharded search exercise with a slow shard, plus a security, correlated-failure and diagnostic review. |
| SDA-MS06 Complete system designs | M10 (8 lessons) | Eight worked designs and a comparison of two content-platform designs after a dominant constraint changes. |
| SDA-MS07 Specialised design domains | M11 (9 lessons) | Nine domain lessons and an exercise comparing unique-ID and distributed rate-limit invariants and failure policies. |
| SDA-MS08 Object design and architecture synthesis | M12–M13 (7 lessons) | An OOD portfolio with a parking allocation extension, plus a comparison of two historical architecture families for a new workload. |
| SDA-MS09 Capstone and whole-course audit | CP-01 and course audit | A multi-region marketplace capstone with a six-outcome rubric and a whole-course audit of all 473 topic mappings and learning outcomes. |

The lesson and module handoffs include the validated lesson and assessment drafts, integrated module packages, and current teaching and assessment evidence. The capstone and audit handoff includes the marketplace package and independent course audit. Record human approval separately.

## Draft readiness and dependency changes

The outline's learning prerequisites apply to learners. The backlog records production inputs separately. Independent parts of a package can proceed within the authorized scope. When a section consumes a specific example, diagram or assumption, integrate that section once the upstream draft is available. A module integration draft can be produced from available lesson drafts; checks/acceptance are tracked separately. A final course audit runs only when explicitly requested, against the existing module evidence and capstone draft.

Record concrete references at intake or when discovered: upstream Story, artifact path/section, and consuming downstream section or assessment. Git commits can be consulted for history without recording extra checksums. A `composition` input gates only the section using it. A `preview` or `reference` can be drafted from the outline and checked against the current target on explicit request.

When an upstream draft changes, inspect affected lessons, assessments and integrations only within authorized scope. Update the specific artifacts requested and manually set `review_status=needs_review` for substantive changes to previously reviewed content. Do **not** auto-invalidate tasks, rerun downstream work, refresh fingerprints or launch review/validation. Record unresolved impacts for the user's next decision. Keep content as draft until explicit human approval for merge/publication.

## Acceptance and carry-forward feedback

N1 from the accepted course review is recorded on M03-L02 and M06-L01. Their forward references are previews, and the detailed comparison can be assessed at integration. Each lesson companion assesses all its own outcomes. Module exercises assess the synthesis subsets in the outline.

When lesson teaching review is explicitly requested, capture each assigned topic ID, teaching path and explanatory heading without a file checksum. Record which teaching section and assessment items support each learning outcome. At module integration, consolidate this evidence in the module's `taught-coverage.csv` and `outcome-portfolio.json`, include its synthesis outcomes, and resolve gaps against the approved outline.

When requested, the final audit verifies all 473 approved source topic mappings against actual explanations, learner outcomes and assessment evidence, and checks cross-module consistency. It records findings without artifact hashes. Titles, citations and assessment items alone do not establish teaching coverage.

Capstone acceptance is based on its six transfer outcomes. Review the original marketplace workload, reference design, at least two justified variants, failure and recovery traces, and the rubric mapping to CP-LO1 through CP-LO6. Use the full portfolio for the course coverage decision.

## Epic and Story index

| Epic | Story | Package |
|---|---|---|
| SDA-M00 | SDA-M00-L01 | How to learn and check readiness |
| SDA-M00 | SDA-M00-L02 | From requirements to a defensible design |
| SDA-M00 | SDA-M00-INT | Integrated design, reference solution and decision summary |
| SDA-M01 | SDA-M01-L01 | Capacity and latency budgets |
| SDA-M01 | SDA-M01-L02 | Performance versus scalability |
| SDA-M01 | SDA-M01-L03 | Consistency and partition decisions |
| SDA-M01 | SDA-M01-L04 | Availability and failover budgets |
| SDA-M01 | SDA-M01-INT | Integrated design, reference solution and decision summary |
| SDA-M02 | SDA-M02-L01 | DNS and endpoint discovery |
| SDA-M02 | SDA-M02-L02 | TCP, UDP and HTTP |
| SDA-M02 | SDA-M02-L03 | Load balancing and reverse proxies |
| SDA-M02 | SDA-M02-L04 | CDN push, pull and cache control |
| SDA-M02 | SDA-M02-INT | Integrated design, reference solution and decision summary |
| SDA-M03 | SDA-M03-L01 | Application layers and microservices |
| SDA-M03 | SDA-M03-L02 | REST, RPC and interface contracts |
| SDA-M03 | SDA-M03-L03 | Service discovery and resilient calls |
| SDA-M03 | SDA-M03-INT | Integrated design, reference solution and decision summary |
| SDA-M04 | SDA-M04-L01 | Relational invariants and query-driven models |
| SDA-M04 | SDA-M04-L02 | Single-leader and multi-writer replication |
| SDA-M04 | SDA-M04-L03 | Federation, sharding and consistent hashing |
| SDA-M04 | SDA-M04-L04 | Denormalisation and derived views |
| SDA-M04 | SDA-M04-L05 | SQL tuning as an evidence loop |
| SDA-M04 | SDA-M04-INT | Integrated design, reference solution and decision summary |
| SDA-M05 | SDA-M05-L01 | Key-value and document stores |
| SDA-M05 | SDA-M05-L02 | Wide-column and graph stores |
| SDA-M05 | SDA-M05-L03 | SQL versus NoSQL and distributed-store guarantees |
| SDA-M05 | SDA-M05-INT | Integrated design, reference solution and decision summary |
| SDA-M06 | SDA-M06-L01 | Where and what to cache |
| SDA-M06 | SDA-M06-L02 | Cache update and coherence policies |
| SDA-M06 | SDA-M06-L03 | Bounded LRU and distributed query cache |
| SDA-M06 | SDA-M06-INT | Integrated design, reference solution and decision summary |
| SDA-M07 | SDA-M07-L01 | Message queues and task queues |
| SDA-M07 | SDA-M07-L02 | Back pressure, bounded work and retry control |
| SDA-M07 | SDA-M07-L03 | Event logs, ordering and replay |
| SDA-M07 | SDA-M07-INT | Integrated design, reference solution and decision summary |
| SDA-M08 | SDA-M08-L01 | MapReduce and distributed file storage |
| SDA-M08 | SDA-M08-L02 | Streaming aggregation, trends and top-k |
| SDA-M08 | SDA-M08-L03 | Indexes and scatter-gather search |
| SDA-M08 | SDA-M08-INT | Integrated design, reference solution and decision summary |
| SDA-M09 | SDA-M09-L01 | Security by trust boundary |
| SDA-M09 | SDA-M09-L02 | Measure, trace and recover |
| SDA-M09 | SDA-M09-L03 | Coordination and multi-data-centre control |
| SDA-M09 | SDA-M09-INT | Integrated design, reference solution and decision summary |
| SDA-M10 | SDA-M10-L01 | Paste storage, short links and expiry |
| SDA-M10 | SDA-M10-L02 | Social feed publication and timelines |
| SDA-M10 | SDA-M10-L03 | Crawler and web-search composition |
| SDA-M10 | SDA-M10-L04 | Financial aggregation and budgeting |
| SDA-M10 | SDA-M10-L05 | Distributed social-graph traversal |
| SDA-M10 | SDA-M10-L06 | Search query cache at service scale |
| SDA-M10 | SDA-M10-L07 | Category sales ranking |
| SDA-M10 | SDA-M10-L08 | Iteratively scaling a cloud application |
| SDA-M10 | SDA-M10-INT | Integrated design, reference solution and decision summary |
| SDA-M11 | SDA-M11-L01 | File synchronisation and collaborative documents |
| SDA-M11 | SDA-M11-L02 | Messaging and media sharing |
| SDA-M11 | SDA-M11-L03 | Recommendation and graph search |
| SDA-M11 | SDA-M11-L04 | CDN as a service and global data serving |
| SDA-M11 | SDA-M11-L05 | Unique-ID service |
| SDA-M11 | SDA-M11-L06 | Distributed API rate limiter |
| SDA-M11 | SDA-M11-L07 | Multiplayer card games and exchange order books |
| SDA-M11 | SDA-M11-L08 | Memory reclamation |
| SDA-M11 | SDA-M11-L09 | Key-value store and disposable cache composition |
| SDA-M11 | SDA-M11-INT | Integrated design, reference solution and decision summary |
| SDA-M12 | SDA-M12-L01 | Hash-table contracts and collisions |
| SDA-M12 | SDA-M12-L02 | LRU object collaboration |
| SDA-M12 | SDA-M12-L03 | Parking allocation and contiguous resources |
| SDA-M12 | SDA-M12-L04 | Call-centre dispatch and escalation |
| SDA-M12 | SDA-M12-L05 | Cards, decks and scoring |
| SDA-M12 | SDA-M12-L06 | Chat domain and relationship states |
| SDA-M12 | SDA-M12-INT | Integrated design, reference solution and decision summary |
| SDA-M13 | SDA-M13-L01 | Read architecture families critically |
| SDA-M13 | SDA-M13-INT | Integrated design, reference solution and decision summary |
| SDA-FINAL | SDA-CP-01 | Cross-module marketplace design capstone |
| SDA-FINAL | SDA-COURSE-AUDIT | Whole-course taught coverage and portfolio acceptance |
