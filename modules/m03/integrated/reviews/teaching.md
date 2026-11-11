# M03 integration teaching and coverage review

## Scope and sources

Reviewed the English draft exercise, reference solution, decision summary and evidence for middle and senior engineers. Compared them with the approved SDA-v1 M03 integrated package plan, the canonical SD-M03-INTEGRATION specification and the three current M03 lessons. The pinned [System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733) topic assignments are reconciled at lesson level. This review evaluates the synthesis subset and its connections to that teaching. The module validation step consolidates the exact lesson topic and outcome records.

## Synthesis coverage

| Approved synthesis input | Exercise evidence | Reference and rubric evidence |
| --- | --- | --- |
| M03-L01-LO2, defend a deployment boundary | M03-EX1 task 1 compares isolated capacity in a modular application, a separate renderer and an entity split under a measured p99 and CPU constraint. It asks learners to protect the current-version publication rule. | **Ownership and deployment** gives a distinct renderer option and a viable in-process capacity option, identifies one transactional owner and calls for latency, CPU and lag observations. **Self-evaluation** scores the alternatives and invariant. |
| M03-L02-LO1, trace the resource and remote operation paths | M03-EX1 task 2 requires editor create/status contracts, the internal rendering operation and a request/reply trace that survives ambiguous outcomes and older mobile versions. | **Public and internal contracts** shows acceptance versus completion, the stub path in both directions, authorization, durable duplicate identity and a private status representation. **Self-evaluation** grades the interface trace and its behavior. |
| M03-L03-LO2, defend discovery and retry ownership | M03-EX1 task 3 compares caller-side and intermediary-side selection after the lesson sequence. It asks learners to bound wait and concurrent work across a stale endpoint and a lost reply. | **Discovery and failure trace** states both ownership choices and trade-offs, separates endpoint and retry owners, and traces at most two attempts. The worst jitter produces 150 ms remaining at retry start and 90 ms after the successful response. **Self-evaluation** grades the failure policy and its verification. |

M03-EX1 measures the declared M03-S1 with exactly those three source outcomes. The brief and decision table reference the current lesson paths. The decision table has trigger, option, mechanism, benefit, cost, failure signal, when to avoid and lesson columns with different workload and failure criteria. The N1 comparison occurs in this integration. Learners compose a public resource interface, an internal operation and two discovery ownership options, then trace how that choice affects attempts under a shared budget.

## Pedagogy and language

The exercise revisits the media-isolation context from M03-L01 with a distinct preview-version invariant, measurable workload, two mobile client versions and concrete timeout inputs. A learner must combine lessons, explain a failure and justify the split, with space for alternate designs. The solution explains why a late version cannot advance the public pointer and why reusing a durable work ID matters after an unanswered RPC. The separate rubric rewards a choice supported by measurements and conditions as well as the trace. English is clear and appropriate to the audience.

## Findings

- **M03-INT-P1 (minor).** M03-EX1 task 3 names both a stopped renderer and a lost reply after acceptance. The reference trace models the common observable timeout and describes the same-ID retry if the first attempt accepted work. An explicit sentence for the stopped-before-acceptance branch and its first successful acceptance would make the two cases easier to score.
- **M03-INT-P2 (note).** The solution calls for an in-flight dispatch bound and maximum cached membership age. The brief provides no measured limits for these, so a choice calibrated by load and rollout tests is appropriate. Explicitly naming such a calibration criterion in the rubric would help assess alternate valid values.

Verdict **ready-for-human-review**.
