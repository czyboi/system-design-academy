# DB-01 Technical Review

**Task:** `SD-DB01-WORKFLOW-PILOT`  
**Artifact reviewed:** `author/draft.md`  
**Review scope:** Technical correctness, engine/version boundaries, example consistency, trade-offs, and failure modes. The SQL examples were not executed during this review.

## Findings

### T1 — Major: Label the exercise solution's engine at the code block

**Location:** `author/draft.md`, “Sample solution / Một lời giải mẫu,” SQL block (approximately lines 203–226). Exact example: `organizer_id BIGINT NOT NULL REFERENCES users(user_id)` and the two inline `REFERENCES` declarations in `meeting_participants`.

**Issue:** The main order DDL is explicitly scoped to PostgreSQL 18, and the lesson correctly explains that MySQL 8.4 parses and ignores column-level inline `REFERENCES`. The later exercise solution uses that same syntax without repeating an engine label at the block. If a learner copies that solution into MySQL 8.4, the organizer and participant foreign keys will not be created, so orphan references can be stored. The concluding source note says the DDL is PostgreSQL 18, but that scope is distant from this second code block.

**Evidence:** PostgreSQL 18 Constraints, §5.5.5, documents column-level `REFERENCES` syntax: https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-FK. MySQL 8.4 `CREATE TABLE`, §15.1.20, explicitly says it parses but ignores inline `REFERENCES` and accepts those clauses only in a separate `FOREIGN KEY` specification: https://dev.mysql.com/doc/refman/8.4/en/create-table.html. MySQL 8.4 Foreign Key Constraints, §15.1.20.5, describes the supported FK syntax and storage-engine conditions: https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html.

**Suggested correction:** Add a sentence immediately before the solution DDL saying it is an illustrative, unexecuted PostgreSQL 18 example and inherits the same engine scope as the order example. If the exercise is intended to be portable or copied into MySQL, show a separate MySQL 8.4 version using table-level `FOREIGN KEY` clauses and state the storage engine.

### T2 — Minor: Clarify that `UNIQUE` does not imply `NOT NULL`

**Location:** `author/draft.md`, “Keys và constraints: chọn theo invariant,” the bullet beginning “Unique constraint” (approximately line 154).

**Issue:** The definition correctly says that a unique constraint applies within a chosen scope, and the concrete payment key uses two `NOT NULL` columns. The general explanation could still leave learners with the impression that uniqueness alone makes a key value mandatory. PostgreSQL 18 permits multiple null-containing rows under a default unique constraint; null treatment also differs among implementations. The separate `NOT NULL` bullet helps, but explicitly connecting the two would prevent a common modeling error.

**Evidence:** PostgreSQL 18 Constraints, §5.5.3, explains that by default two null values are not considered equal for unique constraints and notes that null treatment is implementation-defined by the SQL standard: https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS.

**Suggested correction:** Add: “`UNIQUE` không tự buộc cột phải có giá trị; nếu thiếu giá trị không hợp lệ, thêm `NOT NULL`. Cách xử lý `NULL` trong unique constraint có thể khác theo DBMS.”

### T3 — Minor: Show the payment composite unique key in the ER diagram

**Location:** `author/draft.md`, Mermaid ERD in “Worked example: dữ liệu cho đơn hàng” (approximately lines 58–80), compared with the `payments_provider_reference_uq` constraint in the DDL (approximately lines 124–135).

**Issue:** The prose and DDL state that `(provider_code, provider_ref)` is unique, but the ERD lists both columns without indicating the composite unique constraint. This leaves the diagram less precise than the model it summarizes.

**Evidence:** The PostgreSQL 18 reference for unique constraints says a table-level unique constraint can cover a group of columns and enforces uniqueness of the combination: §5.5.3, https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS.

**Suggested correction:** Mark both attributes as a composite UK in the diagram (or add a short note that the ERD omits constraint detail and point to the DDL).

### T4 — Minor: Scope the MySQL automatic-index note to FK-capable storage engines

**Location:** `author/draft.md`, paragraph beginning “Không gọi ví dụ trên là SQL portable” (approximately line 148).

**Issue:** The statement that “MySQL may also create an index” is appropriately contrasted with PostgreSQL, but it is phrased broadly. MySQL 8.4 documents this behavior for foreign keys on engines that support them; the engine is part of the product behavior. `InnoDB` is the common case, while `NDB` has its own requirements.

**Evidence:** MySQL 8.4 Foreign Key Constraints, §15.1.20.5, says FK-capable engines require the index and the referencing index is created automatically if absent; the same section lists parent/child engine requirements: https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html.

**Suggested correction:** Say “For MySQL 8.4 InnoDB tables…” (or name the exact engine(s) supported by the lesson's scope), and avoid transferring this behavior to MySQL storage engines without FK support.

## Verified claims and review limits

- PostgreSQL 18's primary-key, foreign-key, unique, check, and not-null descriptions are correctly bounded to PostgreSQL in the lesson. The cited constraints page supports the statements that a PK is unique and non-null; FK checks non-null references; `CHECK` accepts true or null; and PostgreSQL `CHECK` constraints cannot guarantee cross-row/table invariants. See §§5.5.1–5.5.5: https://www.postgresql.org/docs/18/ddl-constraints.html.
- The statement that PostgreSQL does not automatically create an index on referencing FK columns is correct and properly workload-qualified. PostgreSQL says an index on the referencing columns is often useful but is not created automatically; same source, §5.5.5.
- The MySQL 8.4 inline-reference warning is correct. MySQL also creates a referencing index automatically when required for a supported FK and no suitable index exists; scope this to the relevant engine as in T4.
- The PostgreSQL numeric note is correctly cautious: PostgreSQL `numeric`/`decimal` are exact and recommended where exactness is required; floating-point types are inexact. The draft appropriately makes currency precision and rounding domain decisions rather than universal rules. PostgreSQL 18 Numeric Types, §§8.1.2–8.1.3: https://www.postgresql.org/docs/18/datatype-numeric.html.
- `TIMESTAMPTZ` is a valid PostgreSQL abbreviation for `timestamp with time zone`; PostgreSQL documents it as an extension. This is consistent with the draft's explicit PostgreSQL 18 scope. PostgreSQL 18 Date/Time Types, §8.5: https://www.postgresql.org/docs/18/datatype-datetime.html.
- The revised ERD now shows zero-or-many order items, matching the child-to-parent FK and the prose about un-enforced minimum child cardinality.
- The race explanation for check-then-insert is sound when the invariant is uniqueness and the final database constraint is actually installed; the application must handle the constraint violation, as the draft says.
- The MongoDB access-pattern reference is product-scoped in the lesson. MongoDB's manual states its model-specific principle in its Data Modeling page: https://www.mongodb.com/docs/manual/data-modeling/.
- The normalization discussion is framed as an introductory explanation and examples, rather than claiming that the cited Access documentation proves every anomaly taxonomy. Microsoft Learn, “Description of normalization”: https://learn.microsoft.com/en-us/previous-versions/troubleshoot/microsoft-365/microsoft-365-apps/access/database-normalization-description.
- The order-item price snapshot, natural/surrogate key discussion, and denormalized counter are presented conditionally as domain/workload design choices. The draft avoids claiming a guaranteed performance benefit.
- Both SQL blocks are explicitly unexecuted in the lesson's scope notes. Do not treat syntax or behavior as experimentally validated until the code is run in declared PostgreSQL 18 (and any optional MySQL 8.4) environments.

## Verdict

**revise** — fix T1 before learners are invited to copy the exercise solution; T2–T4 are small precision improvements. No blocker-level technical error was found in the main PostgreSQL 18 model after the authored corrections. This review does not approve publication.
