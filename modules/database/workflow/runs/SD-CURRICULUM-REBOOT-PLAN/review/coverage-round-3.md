# Coverage review — round 3

**Verdict:** `revise`  
**Artifact:** revision-2 curriculum candidate  
**Reviewer:** independent `curriculum-coverage-reviewer`  
**Source:** [System Design Primer README at pinned commit `ae9bbd7b02d90b9866215de185217d33f39ab733`](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md)  
**Scope:** independent README topic-tree, prompt, architecture-catalog and under-development enumeration; compare source coverage with the candidate outlines/matrix; inspect pinned solution/OOD bodies where accessible. No lesson or assessment was reviewed.

## Material findings

| Severity | Source and candidate location | Finding | Required change |
|---|---|---|---|
| Medium | [`README.md#cache`](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#cache); SD-04-02 and matrix rows 521–522 | The pinned cache section enumerates row-level, query-level, serialized-object and rendered-HTML caching, and warns that file caching complicates cloning/autoscaling. The source inventory omits these details; SD-04-02 and the matrix cover query/object levels only. | Add the omitted cache levels and scaling caveat to the lesson outline and matrix, or record an explicit scope disposition for each. |
| Medium | [`solutions/system_design/pastebin/README.md`](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/pastebin/README.md); SD-07-01 and matrix row 544 | The source describes a short-code uniqueness check and hash/Base62 path, plus monthly hit-count analytics aggregated from web-server logs with MapReduce. The outline only says identifier generation and analytics paths, which is too broad to evidence these source mechanisms. | Make the short-code uniqueness/hash/Base62 flow explicit; name the monthly log aggregation and cross-reference SD-05-03 for MapReduce if that mechanism is taught there. |
| Low | [`README.md#coding-resource-interactive-coding-challenges`](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#coding-resource-interactive-coding-challenges); candidate resource rows 602–607 | The README links an interactive-coding repository and coding deck. The source inventory has an out-of-scope disposition, but the candidate matrix omits this resource. | Add a matrix row that identifies the resource and states that it is outside the System Design teaching scope. |

## Coverage summary

- **README topic tree:** The major topic families are mapped. The omitted cache levels and cache scaling caveat are the material under-enumeration found.
- **Eight solution writeups:** All eight map to SD-07-01 through SD-07-08. The Pastebin body was checked and has the mechanism gaps above. Twitter and crawler bodies were also fetched and their main flows are represented.
- **Additional prompts:** All 23 are mapped. Related chat, feed/timeline and trending/top-k prompts are grouped in outlines that name their relevant mechanisms.
- **Real-world architecture catalog:** All listed items map to the proposed pattern lessons: MapReduce/Spark/Storm; Bigtable/HBase/Cassandra/DynamoDB/MongoDB/Spanner/Memcached/Redis; GFS/HDFS; and Chubby/Dapper/Kafka/ZooKeeper.
- **OOD examples:** The six notebook paths map to optional lessons; the circular-array contribution placeholder is excluded. Notebook-body mappings could not be independently confirmed in this round.
- **Under-development topics:** MapReduce, consistent hashing and scatter-gather each have an outline and primary-research flag.
- **Resources:** Company catalogs, translations, flashcards, images, further reading and tools have dispositions. The coding-resource link is missing from the candidate matrix.

## Source-access limitation

The reviewer inspected the pinned README and independently fetched the pinned Pastebin, Twitter and crawler bodies. Exact-SHA raw/blob requests returned cache-miss and the Contents API was inaccessible for the remaining five solution bodies—Mint, social graph, query cache, sales rank and AWS scaling—and all six OOD notebooks—hash map, LRU cache, call center, deck of cards, parking lot and online chat. Search results for current `master` were excluded because they do not establish content at the pinned commit. The candidate's source-body verification table was not treated as independent confirmation. This limits independent verification of those eleven bodies.

## Gate result

The candidate is not coverage-approved. This is the third coverage review, and the task specification permits no more than two automated revision cycles. The findings therefore require human judgment before finalization. The report does not establish technical correctness, rights clearance, authored lesson coverage, human approval or publication readiness.
