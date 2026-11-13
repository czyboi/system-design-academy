# M05-L01 pedagogy and curriculum coverage review

Reviewed the canonical lesson, companion assessment and evidence at draft handoff `f99e5b9` for middle and senior engineers. The scope is the [approved M05-L01 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-l01), assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the pinned Primer [key-value and document sections](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1003-L1037) and [MongoDB architecture entry](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1705), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Finding

| ID | Severity | Status | Location and learner impact | Suggested correction |
| --- | --- | --- | --- | --- |
| M05-L01-P1 | major | open | [Lesson, Compare concrete product contracts](../../../../lessons/M05-L01.md#compare-concrete-product-contracts) teaches how a cache miss or failure is handled, but gives no trace of an old **positive** cache entry after a confirmed revocation. [Q4 and EX-1](../../../../assessments/M05-L01.md#practical-exercise) require the learner to prevent that stale positive from authorizing a request and grade authority failure. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-l01) requires decisions based on access paths and failure criteria. | Teach a concrete validation and revocation timeline showing how each post-confirmation request consults an authority with the required read semantics or uses an equivalent coordinated mechanism. Include the stale hit, unavailable authority and fail-closed result. Keep the exercise answer and rubric aligned with the chosen contract. |

## Coverage

| Topic | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H108, key-value stores | taught with P1 gap in applied failure trace | **Start with the access path** traces token-derived keyed lookup and category-plus-sort-key range access. **Compare concrete product contracts** describes Redis and Memcached access. Q1–Q2 and EX-1 apply access paths. |
| PR-H110, document stores | taught | **Trace an indexed product document** models a bounded aggregate, an indexed query and price update. It also explains compatible indexed fields during schema evolution. Q2–Q3, Q5 and EX-1 apply those ideas. |
| PR-ARCH-MONGODB, MongoDB architecture mechanism | taught | **Trace an indexed product document** and **Compare concrete product contracts** discuss the document unit, indexing and single-document atomic update. EX-1 applies a product aggregate and explicitly asks for product-specific verification. |

## Pedagogy and assessment

The lesson connects exact token keys and attribute-based product browsing to different access paths, then traces a product moving across a price threshold and a mixed-schema rollout. The DynamoDB, Redis, Memcached and MongoDB cases identify distinct operations and scope rather than inferring one guarantee from a category name. The separate companion has six explained checks and a practical exercise with a point-bearing rubric. LO1 maps to Q1–Q3 and EX-1, and LO2 maps to Q4–Q6 and EX-1. The stale-positive authorization trace in M05-L01-P1 is necessary to make the LO2 assessment fully reproducible from the lesson.

**Verdict: revise.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the changed lesson and companion at `f69ce20`. **Compare concrete product contracts** now traces a stale positive after a confirmed revocation, an authoritative same-region strongly consistent read, and denial when the authority cannot answer. It also specifies the permitted outcome of a validation that overlaps revocation and identifies the stronger protected-action ordering as a separate requirement. Q4, EX-1, the sample solution and rubric use the same timing contract. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-l01) requires the learner to select an access path with its failure criteria.

| Finding | Status | Evidence |
| --- | --- | --- |
| M05-L01-P1 | resolved | [Lesson, Compare concrete product contracts](../../../../lessons/M05-L01.md#compare-concrete-product-contracts) and [assessment, Practical exercise and sample solution](../../../../assessments/M05-L01.md#practical-exercise). |

**Trace an indexed product document** now explains why the top-level field remains authoritative while old writers exist, followed by compatible dual writes, backfill, verification and reader migration. Q3 and the exercise solution and rubric assess that sequence. The DynamoDB listing includes active status in its routing design. Both outcomes and the assigned topic dispositions remain supported by the revised teaching and assessment.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.
