# DB-01 Language and Teaching Audit

**Task:** SD-DB01-ENGLISH-TEACHING-REVISION  
**Date:** 2026-11-09  
**Scope:** Current learner-facing Database module material and the DB-01 teaching revision

## Language audit

The project specification, Database README, and content guidelines previously designated Vietnamese as the primary course language. DB-01 therefore followed the written policy: its body, metadata, and headings were Vietnamese or bilingual.

The active learner-facing files DB-02 through DB-07, the DB-08 case study, the assessment blueprint, and the master Database curriculum are already in English. This task leaves those files unchanged. DB-01 was the only non-English active lesson found in the Database pilot.

Historical workflow snapshots, reviews, task notes, and reports may preserve the language used when that task ran. They are internal process records rather than learner-facing lessons and were not translated.

## Teaching audit

The prior DB-01 draft did contain teaching: it explained data modeling, keys and constraints, normalization, denormalization, and rule placement, and included a worked order schema. It also had an exercise, sample answer, and eight knowledge checks. So the impression that DB-01 had no teaching was understandable, but not literally correct.

The issue was presentation. The explanations were compressed into short reference-style sections, the worked schema arrived before learners had been walked through each design decision, and the module-level quiz, curriculum, and QA artifacts can look like tests because they are planning or assessment documents rather than lessons.

The revised lesson now teaches one design in sequence:

1. Start with an order-service problem and identify facts, rules, and access patterns.
2. Derive entities and relationships, then read the ERD cardinalities.
3. Choose keys and constraints from those business rules.
4. Map the model to PostgreSQL 18 example DDL and explain what each constraint does.
5. Use duplicated customer facts to explain an update anomaly and normalization.
6. Discuss when a derived read model may be justified and the work needed to keep it correct.
7. Separate row-level database rules from workflow rules before the transfer exercise and knowledge check.

The walkthrough precedes the formal assessment. The lesson remains a draft; the 90-minute estimate remains provisional, the example SQL is unexecuted, and a new independent reviewer pass and learner pilot have not been run.

## Where to read

- **The lesson:** modules/database/lessons/DB-01-data-modeling.md
- **Module sequence and outcomes:** modules/database/curriculum/database-module.md
- **Quiz plan:** modules/database/assessments/database-quiz.md
- **First-pass quality review:** modules/database/qa/database-pilot-review.md

The curriculum, quiz plan, and QA report support the lesson workflow; they are not substitutes for the lesson itself.
