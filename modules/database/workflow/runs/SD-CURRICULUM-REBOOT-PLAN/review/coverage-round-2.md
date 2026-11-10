# Coverage review — round 2

**Verdict:** `revise`  
**Mode:** plan gate; middle/senior backend engineers; English; no lessons or assessments reviewed.  
**Source:** Donne Martin/System Design Primer, commit `ae9bbd7b02d90b9866215de185217d33f39ab733`, inspected 2026-11-10. The reviewer independently re-enumerated the README hierarchy and fetched all eight system-design solution bodies and six OOD notebooks through the GitHub repository-file API. Statuses below mean planned teaching evidence, not completed instruction.

## Findings requiring changes

| Severity | Source and candidate evidence | Finding | Required change |
|---|---|---|---|
| High | `README.md#load-balancer`; SD-02-06 source map/matrix | The source has no load-balancer headings for active/passive or active/active. Its inline links point to the earlier availability-pattern headings `#active-passive` and `#active-active`. Candidate anchors `#active-passive-1` and `#active-active-1` do not exist. | Use `#load-balancer` with the exact passage/subsection wording and distinguish it from the linked availability discussion. Keep the mode comparison. |
| High | `solutions/object_oriented_design/call_center/call_center.ipynb`; SD-10-02 and verification row | Notebook explicitly answers **no** to VIP priority. Candidate incorrectly represents VIP handling as a source assumption and behavior. | Correct the source disposition. If VIP is retained, label it an Academy extension/open design choice, not source behavior. |
| Medium | `README.md#representational-state-transfer-rest`; SD-02-04 | REST stateless interaction is missing from the outline though hypermedia is now present. | Add statelessness explicitly. |
| Medium | `solutions/system_design/mint/README.md`; SD-07-04 and matrix | Source use cases include budget recommendations and high availability; the outline mentions aggregation and scaling boundaries only. | Add recommendation behavior and availability design, or narrow matrix claims. |
| Medium | `solutions/system_design/sales_rank/README.md`; SD-07-07 and matrix | Source specifies a past-week window with hourly updates; outline only says ranking windows. | Teach that window/update example explicitly or correct the mapping. |
| Medium | `README.md#additional-system-design-interview-questions`; Redis prompt to SD-03-07/SD-09-01 | Generic key-value model/family comparison does not establish a key-value store design. | Outline store operations, placement/storage, and failure choices, or justify a narrowed disposition. |
| Medium | Candidate matrix additional-prompt/catalog rows | Many rows omit exact README anchors; shorthand `Same` is ambiguous. The hash-map row cites the OOD index rather than the notebook path. | Give each prompt/catalog row its exact pinned section locator and item; use the exact notebook path. |
| Low | `solutions/object_oriented_design/hash_table/hash_map.ipynb`; SD-10-01 | Notebook explicitly sets load-factor handling outside its simplified assumptions; candidate credits load-factor trade-offs as notebook content. | Preserve that simplification and label any added load-factor instruction as an Academy extension. |

## Independent coverage summary

| Source area | Candidate evidence | Status |
|---|---|---|
| `#study-guide`; `#how-to-approach-a-system-design-interview-question`; `#system-design-topics-start-here`; performance/scalability; latency/throughput | SD-01-01–03, request/data/async mechanisms; external scalability links as resources | Planned/adapted; appropriate for audience. |
| Availability/consistency, CAP/CP/AP, weak/eventual/strong consistency, failover/replication/nines/serial and parallel availability | SD-01-04–06, SD-03-02 | Planned with semantics research flagged. |
| DNS, CDN push/pull, load balancing modes/L4/L7/horizontal scaling, reverse proxy, application layer/microservices/discovery | SD-02-01–08 | Planned; correct the load-balancer locator. |
| RDBMS/ACID, primary/replica and multi-writer replication, federation, sharding, denormalization, every SQL-tuning leaf, NoSQL models/BASE and SQL-vs-NoSQL | SD-03-01–08 | Planned; explicit federation, master-master and broad SQL tuning are present. |
| Cache locations, query/object levels, cache-aside/write-through/write-behind/refresh-ahead, TTL/LRU/invalidation/failure | SD-04-01–04 | Planned. |
| Message/task queues, back pressure, Little's Law addition, MapReduce, Spark/Storm, scatter-gather | SD-05-01–05 | Planned; primary-source research flagged for incomplete topics and additions. |
| HTTP/TCP/UDP/RPC/REST, security | SD-02-02–04, SD-06-01 | REST statelessness is the remaining topic omission; security topics are planned. |
| Powers of two and historical latency figures | SD-01-03 | Planned as estimation/reference with figures flagged for fresh evidence. |
| Eight system-design solution bodies: Pastebin, Twitter, crawler, Mint, social graph, query cache, sales rank, AWS scaling | SD-07-01–08 | All have distinct outlines. Mint and sales-rank outline/matrix alignment needs correction. |
| All 23 prompts in `README.md#additional-system-design-interview-questions` | Dropbox SD-08-01; search/crawler SD-07-03; Docs SD-08-02; Redis SD-03-07/SD-09-01; Memcached SD-04-04/SD-09-01; recommendation SD-08-03; Bitly SD-07-01; WhatsApp/Facebook chat SD-08-04; Instagram SD-08-05; feed/timeline SD-07-02; graph search SD-07-05; CDN SD-02-05; trend/top-k SD-08-06; IDs SD-08-07; multi-DC SD-08-08; game SD-08-09; GC SD-08-11; rate limiter SD-06-02; stock exchange SD-08-10 | All prompts are mapped; Redis needs more explicit store-design instruction. Prompt/reference is not source-authored teaching. |
| `#real-world-architectures`: MapReduce/Spark/Storm; Bigtable/HBase/Cassandra/DynamoDB/MongoDB/Spanner/Memcached/Redis; GFS/HDFS; Chubby/Dapper/Kafka/ZooKeeper | SD-05-03/04, SD-09-01/02/03, cache lessons | Named systems map to patterns and require current product research. |
| Company architecture/blog catalogs | SD-11-01, pattern extraction and source evaluation | Appropriate catalog/resource disposition; no one-lesson-per-company requirement. |
| Six OOD notebooks and circular-array contribution placeholder | SD-10-01–03 optional; circular array excluded because no implementation/teaching material exists | Planned; correct the VIP and load-factor source claims. |
| Motivation, translations, flashcards, contribution/license/credits/contact, images, further reading, tooling | Resource/exclusion rows | Appropriate for this teaching-only plan; rights and source checks remain separate. |

The matrix is materially more auditable after revision 1, but exact locators and outline-evidence alignment need another pass. No source-body access limits remain in this round.

## Required changes before the next coverage gate

1. Correct the load-balancer locator; correct call-center VIP and hash-map load-factor provenance.
2. Add REST statelessness, Mint budget-recommendation/availability teaching, and the sales-rank past-week/hourly-update scenario to the outlines and align matrix evidence.
3. Strengthen Redis from model comparison to a scoped key-value store design lesson or give a justified disposition.
4. Replace ambiguous source shorthand with exact pinned README anchors/items for every additional prompt and architecture catalog row; cite the exact hash-map notebook path.
5. Recheck every modified mapping, all 23 prompts, every named architecture example, and all solution/OOD bodies independently in round 3.

The plan's foundation-to-composition order and middle/senior audience fit are coherent. Optional OOD is correctly separated. This coverage verdict does not establish technical correctness, pedagogy, rights, lesson completion, human approval, or publication readiness.
