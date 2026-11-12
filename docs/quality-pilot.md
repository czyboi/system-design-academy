# Content-quality pilot (independent lesson review)

**Status: cases selected; M01-L02 has a first draft on a separate branch but is not yet independently reviewed.** This document is a lightweight experiment plan, **not** a new task type, workflow stage, adapter, content schema or quality verdict.

## Representative cases from approved SDA-v1

| Story | What to test | Evidence of genuine understanding |
| --- | --- | --- |
| `SDA-M01-L02` — Performance versus scalability | Foundations: latency/throughput, saturation, vertical vs horizontal scale | Explain why two slower servers can increase capacity without reducing single-request service time; calculate steady-state Little's Law with assumptions; reason about p99 near saturation |
| `SDA-M04-L03` — Federation, sharding and consistent hashing | Mechanism: ownership, ring membership, vnodes and hot tenants | Trace a key before/after a node join; discuss exactly which ranges move; compare bounded movement with load balance and cross-shard trade-offs |
| `SDA-M10-L02` — Social feed publication and timelines | End-to-end design: fan-out, durable post, read hydration and retries | Trace ordinary/celebrity authors to two readers, show write-amplification estimate and delayed/reordered delivery; keep search internals delegated to M08-L03 |

Each pilot must use its existing backlog Story, approved outline and canonical `modules/mXX/evidence/`, `lessons/` and `assessments/` paths via the **existing** `research → author` task template. Follow normal task intake/state/handoff; do not create substitute examples or mark a task complete merely because this plan exists. Run the three cases individually to avoid hiding quality failures with batch averages.

## Source starting points (not a completed research pack)

- M01-L02: [Dean & Barroso, *The Tail at Scale*](https://research.google/pubs/the-tail-at-scale/) — tail-latency mechanisms; [IBM, WebSphere Performance Cookbook](https://publib.boulder.ibm.com/httpserv/cookbook/WAS_Performance_Cookbook.pdf) — Little's Law/queue measurements. Verify applicability and the model's assumptions before quoting.
- M04-L03: [Karger et al., consistent hashing](https://people.csail.mit.edu/karger/Papers/web.pdf); [Apache Cassandra, token ring and vnodes](https://cassandra.apache.org/doc/stable/cassandra/architecture/dynamo); [AWS DynamoDB partition-key guidance](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html). Keep theoretical properties and vendor-specific behavior separate.
- M10-L02: [Redis Retwis timeline example](https://redis.io/docs/latest/develop/use/patterns/twitter-clone/) — example write fan-out, not proof of current Twitter internals; [X Engineering, home timeline prediction pipeline (2020)](https://blog.x.com/en/engineering/streaming-logging-pipeline-of-home-timeline-prediction-system) — ranking pipeline context, not proof of a fan-out algorithm. Treat architecture choices as original design proposals, not claims of how X currently operates.

Research Agent must open primary sections, collect claim-level support, mark uncertainty and identify product/version boundaries **before** Author drafts. This reference list is only a starting point.

## Quality assessment — automatic for each lesson

For each draft, inspect actual paragraphs, diagrams, numbers and exercises against these five questions. Record specific examples/evidence and actionable defects, not a made-up numeric score:

1. **Technical truth:** Does every important mechanism and formula hold under stated assumptions? Are vendor claims scoped and supported?
2. **Curriculum coverage:** Does the lesson really teach each numbered outline item and outcome (not merely list it)? Are lesson boundaries respected?
3. **Pedagogy:** Can a middle/senior engineer follow the causal steps, trace the example and explain why alternatives fail?
4. **Practical decisions:** Are realistic workload numbers, diagram flows, bottlenecks, skew, failure cases and trade-offs worked through?
5. **Assessment alignment:** Do EX-1 and 5–8 substantive knowledge checks have defensible answers, explanations and rubric, and test material actually taught?

Record **ready for human evaluation / revise / blocked** with citations to lesson sections and source evidence. AI self-checks are part of authorship; **two independent reviewer agents run immediately after each lesson's draft handoff**, then targeted corrections/re-review if needed (up to two rounds per lesson). At module close, a separate synthesis review checks only integration and cross-lesson coherence. No reviewer can publish the draft.

## Format and rendering are different

`python scripts/validate_content.py --scope lesson --lesson PATH --assessment PATH` runs during normal scoped draft handoff to check metadata, paths, safe Markdown and local assets; repository-wide validation remains on demand. A data PASS does not evaluate the five quality questions. There is currently **no actual website renderer**: Mermaid, mathematical notation, layout, solution visibility and browser security cannot be declared rendered successfully until the website exists. When a renderer is built, test these three lessons with the actual rendering library instead of recreating a second Markdown parser.

Only scale authoring after reviewing the pilot results. If a real content problem appears, update Research/Author instructions first; fix data checking only for an actual data or security defect.
