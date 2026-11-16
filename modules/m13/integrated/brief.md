---
id: M13-EX1
status: draft
outcomes: [M13-S1]
---

# Transfer a historical dataflow design under changed constraints

A team managing a small regional analytics service must generate a correct daily reconciliation report. A colleague proposes cloning a historical MapReduce cluster plus the Google File System because those papers describe large resilient workloads; another proposes a Spark-style lineage engine on existing object storage. The user requires **one immutable correct report per data revision before 06:00**. There is no real-time dashboard requirement. The decision is not “which famous architecture is better”: it is **which historical assumptions hold, which component proves the new invariant, and what can be removed**.

M13-S1 uses the mechanisms in M13-L01-LO1/LO2. It does **not** claim the course's other lesson outcomes are integrated or QA passed.

## Synthetic workload and evidence constraints

| Variable | Declared envelope |
| --- | --- |
| Source | 20 GiB immutable versioned object-storage input per day, 200 deterministic aggregate tasks |
| Product deadline | Final verified report readable by 06:00 each day, 60-minute available compute window |
| Current team | One region, 3 engineers; existing object storage, relational DB and scheduled worker service |
| Original-operation identity | `(report_date, dataset_version)`, stable across retries, once published output version |
| Failure drill | Worker dies after writing 60% of an attempt output; controller receives an ambiguous commit response |
| Metrics | Thirty scheduled original report runs; 27 correct before deadline, 2 late, 1 invalid |
| Evidence | Primary research source with author, publication year and exact relevant section; old company blog is discovery-only |
| Rights | Link historical diagrams, do not copy them without review/permission |

## M13-EX1

1. Compare **historical Google MapReduce (2004) + GFS (2003)** with a **Spark RDD-style lineage family (2012) over contemporary object storage**. For each, record paper, date, specific mechanism, failure assumptions and where the target workload differs. No claim about current managed offerings is admissible without a product/version primary source.
2. Draw an adapted architecture for the smallest feasible workload. Mark input snapshot, deterministic partition computation, stable run identity, intermediate output, completeness check and guarded final publication. Justify which historical components disappear, which remain as patterns and which must be measured before changing.
3. In a crash-after-partial-output trace, distinguish a successful worker-attempt callback from an externally readable report. Show retry, deduplication, immutable attempt namespace and manifest/final status selection under lost response.
4. Estimate the required average processing envelope: 20 GiB in 60 minutes, **ignoring compute overhead** as a theoretical lower bound. Do not invent a benchmark. Explain whether 200 tasks imply 200 simultaneous workers (they do not) and what measured bottleneck would justify distributed shuffle, Spark lineage or a streaming engine.
5. Score the observed 30-run cohort and specify at least six experiments that would disprove the minimal design. Write a rights-safe source and current-version verification plan.

[Reference design and scoring](solution-rubric.md) · [Decision summary](decision-summary.md)

## Authority and feedback boundary

This exercise compares source assumptions and a constrained adaptation. The included date/paper ledger is not a review of current product SLAs and does not override independent technical/provenance or pedagogy QA.
