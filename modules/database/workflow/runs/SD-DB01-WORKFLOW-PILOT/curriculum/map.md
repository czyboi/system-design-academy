# DB-01 Curriculum Map

**Task:** SD-DB01-WORKFLOW-PILOT  
**Status:** Curriculum mapping proposal; not a technical verification  
**Unit:** DB-01 — Data Modeling and Relational Foundations

## Scope and non-goals

DB-01 should teach learners to translate a small application problem into a relational model that represents its entities, relationships, business invariants, and read/write patterns. It should establish why keys and constraints belong in the model, and introduce normalization and deliberate denormalization as choices with costs.

Keep these topics at an introductory decision level in DB-01:

- Requirements, access patterns, entities, relationships, keys, and constraints.
- Normalization and the consistency obligations introduced by denormalization.
- A small worked model and a practical schema-design exercise.

Defer index selection and query-plan interpretation to DB-02; transaction isolation, MVCC and locking to DB-03; replication and read consistency to DB-04; partitioning and sharding to DB-05; and comparison of relational and non-relational models to DB-06. DB-01 can foreshadow those topics, but should link forward instead of teaching their mechanisms. Detailed vendor administration, exhaustive SQL syntax, ORM use, warehousing, and production-scale benchmarking remain outside this unit.

## Target learner and prerequisites

**Target:** backend engineers learning system design who can read and write basic SQL and understand application data requirements.

**Entry knowledge assumed:** tables and rows; basic `SELECT`, `INSERT`, and `CREATE TABLE`; familiarity with primary and foreign keys. The current lesson lists basic SQL and primary/foreign keys as prerequisites. Since keys are also lesson outcomes, treat prior key knowledge as familiarity with the terms and purpose; the lesson should teach how to choose and apply them.

Requirements, access patterns, and invariants should be introduced in the lesson's motivating scenario rather than assumed as prior system-design knowledge. A short glossary or recap can support learners who have not recently used relational databases.

## Sequence, dependencies, and effort

Within the proposed 10-module course, Databases is Module 05, following Fundamentals, Capacity Estimation, Networking & Edge, and Application Architecture. The master map does not define lesson-level prerequisites across those modules. DB-01 does not require a specific earlier module if it briefly introduces workload/access-pattern thinking in context.

Within the Database module, DB-01 is the foundation for DB-02 and DB-03. The proposed dependency graph is:

```text
DB-01 ──┬──> DB-02 ──┐
        ├──> DB-03 ──> DB-04 ──┬──> DB-05 ──> DB-06
        │                     └──> DB-07
        └──────────────────────────┐
                                   └──> DB-08 (integrates DB-01–DB-07)
```

DB-05 also depends on DB-02; DB-06 also depends on DB-01; DB-08 integrates all preceding lessons. This matches the current module sequence and assessment plan.

| Unit | Placement | Prerequisites | Provisional effort | Assessment |
|---|---|---|---:|---|
| DB-01 | First lesson in Database module; foundational for DB-02 and DB-03 | Basic SQL; familiarity with PK/FK | 90 minutes | Model a meeting-booking domain with entities, keys, constraints, and two indexes justified by access patterns |

The 90-minute estimate is provisional. It includes the reading and current exercise but has not been validated with learners. The module estimate of 12–16 hours is also provisional.

## Learning outcome to assessment map

The lesson currently states five outcomes. Its six knowledge-check questions and meeting-booking exercise provide an initial assessment set.

| Outcome | Existing assessment evidence | Alignment | Recommended clarification |
|---|---|---|---|
| 1. Turn use cases and access patterns into entities, relationships, and constraints. | Exercise: produce an ER model and DDL for the meeting-booking domain; acceptance criteria require all relationships and invalid time ranges to be represented. | Direct | Ask learners to list the target reads/writes before drawing the model, so the exercise measures the full translation process. |
| 2. Choose primary keys and foreign keys that preserve important invariants. | Exercise requires relationships and a uniqueness constraint for meeting participants; Q2 asks which invariant a foreign key protects; Q6 asks when a composite primary key is appropriate. | Direct, with room to improve | Require learners to identify the candidate key and foreign key for each relationship in their submitted model. |
| 3. Explain why normalization reduces certain update anomalies. | Q4 asks for an update anomaly caused by duplicated customer data. The worked order example distinguishes current product price from historical purchase price. | Partial | Ask learners to explain the anomaly prevented by separating one repeated fact into its own relation, not only name an example. |
| 4. Decide when denormalization is a deliberate performance/read-model trade-off. | Q5 asks what responsibility follows from denormalizing a value. The lesson discusses trade-offs, but the exercise does not require a normalization/denormalization decision. | Gap | Add a short workload scenario and ask whether to keep the normalized model or add a derived read representation; require learners to state the consistency cost. |
| 5. Identify what the database should enforce versus what belongs in application logic. | Q3 tests why an application-side duplicate check is unsafe under concurrent writers; the exercise requires a database constraint preventing duplicate participants. | Partial | Add a second case that distinguishes a row-level invariant suitable for a database constraint from user-facing validation or a rule spanning an external service. Keep the expected reasoning within taught material. |

The exercise acceptance criteria already assess relationships, uniqueness, time-range validity, and two access patterns. The content guidelines also call for a worked solution or rubric; the current exercise has acceptance criteria but no worked solution or scoring rubric. Add one so learners can compare their design and reviewers can assess it consistently.

## Gaps and overlaps

### Gaps to address in DB-01

- Make the assessment alignment explicit in the lesson plan and ensure each outcome is measured by a question or exercise criterion.
- Add an exercise prompt that directly measures the denormalization decision, not only its synchronization cost.
- Add an exercise solution or rubric.
- Keep prerequisite language precise: learners need basic familiarity with keys, while DB-01 teaches their design use.

### Cross-lesson overlap to manage

- DB-01 uses access patterns to motivate a model; DB-02 uses them to choose indexes. DB-01 should name candidate access paths and hand index mechanics to DB-02.
- The DB-01 exercise currently asks learners to justify two indexes before DB-02 teaches index selection and query plans. Either make this a light preview with index mechanics deferred, or move index justification to DB-02; otherwise the current sequence creates a hidden prerequisite.
- DB-01 mentions concurrent writers to motivate database-enforced uniqueness; DB-03 owns transaction isolation, locking, and concurrency mechanisms. DB-01 should not imply that a uniqueness constraint teaches all concurrency control.
- DB-01 introduces denormalization; DB-06 revisits workload-oriented storage models. Keep DB-01 focused on relational modeling and refer broader SQL/NoSQL decisions to DB-06.
- DB-08 reuses the data model and constraints. It should assess transfer to the order-management design rather than repeat DB-01's explanation.

## Assumptions and unresolved curriculum decisions

- Learners have basic application-development experience and know enough SQL to read the lesson's DDL and query examples.
- The course is taught in Vietnamese, retaining standard English technical vocabulary.
- The Database module remains a system-design decision course, not an administration course.
- The 90-minute estimate and question difficulty are hypotheses until a small learner pilot provides timing and comprehension data.
- This map makes no technical-source verification claim. Product-specific behavior belongs in the separate evidence report and should identify product/version scope.
- If the course's overall target later includes learners without relational-database familiarity, add a prerequisite primer or revise DB-01's scope and effort before generating the full module.
