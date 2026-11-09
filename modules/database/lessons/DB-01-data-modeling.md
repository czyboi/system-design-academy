---
id: DB-01
title: Data Modeling and Relational Foundations
status: draft
level: intermediate
estimated_time: 90 minutes (provisional; not yet tested with learners)
prerequisites: [basic SQL, familiarity with tables, primary keys, and foreign keys]
source_review_date: 2026-11-09
reviewer: pending
---

# DB-01 — Data Modeling and Relational Foundations

## Learning outcomes

By the end of this lesson, you should be able to:

1. Turn business requirements and read/write patterns into entities, relationships, and constraints.
2. Choose primary, foreign, and unique keys to express stated business rules.
3. Explain an update anomaly and how normalization reduces duplicated facts and inconsistent updates.
4. Decide when a derived read model may be useful and explain its synchronization cost.
5. Distinguish rules a database constraint can enforce from rules that belong to an application workflow.

## The problem: one business fact, many copies

Imagine an order service that must answer four questions:

- Which customer placed an order?
- Which products and quantities did the order contain?
- What price did the customer agree to at checkout?
- Which payment provider issued a given payment reference?

A first attempt might put customer, order, and product details in one wide table. That feels simple because one query can return a lot of information. But a customer with three order lines may appear in three rows. If the customer's email changes and only two rows are updated, the database now contains two competing answers to the question “What is this customer's email?”

The design problem is therefore not “Which columns should go in the first table?” Start with three questions instead:

1. What facts must the system remember?
2. Which rules must remain true as data changes?
3. How does the application read and write those facts?

This lesson follows one order example from those questions to a relational schema. Read the walkthrough first; the meeting-scheduling exercise at the end asks you to transfer the same reasoning to a new domain.

## Step 1: write down requirements and access patterns

A requirement describes what the system must do. An access pattern describes a common way it needs to read or change data. Both help shape a model, but neither proves that a particular schema or index will be fast.

| Question | Example requirement |
|---|---|
| What facts are we storing? | Customer, product, order, order item, and payment |
| What relationships exist? | A customer places many orders; each order has zero or more items |
| What must remain true? | Every order belongs to a customer; quantity is positive; each item refers to an existing product |
| How will the application read data? | Get an order by ID; list a customer's orders by time; get all items for one order |
| Which facts can change later? | A product's display name and list price may change after purchase |
| Which historical facts must remain fixed? | The agreed price for a confirmed order item |

A rule that must remain true is often called an invariant. For example, “quantity is greater than zero” is an invariant. An access pattern is an input to the decision, not evidence that an index will help; index selection and query plans belong to DB-02.

**Pause and predict:** If a product's list price changes tomorrow, should yesterday's order total change too? The answer depends on the business rule. If an order must preserve the agreed price, the model needs to preserve that historical fact.

## Step 2: identify entities and relationships

An entity is a kind of thing the system needs to remember independently, such as a customer or product. A relationship connects entities. A relational model represents these facts with tables and references.

The order requirements lead to five entities:

- **Customer** stores facts about a buyer.
- **Product** stores the current catalog identity and list price.
- **Order** records that a customer placed an order.
- **OrderItem** connects an order to a product and stores the purchased quantity and agreed price.
- **Payment** records payment attempts or references associated with an order.

Order and product have a many-to-many relationship: an order may contain multiple products, and a product may appear in many orders. The OrderItem entity represents that relationship and gives each line a place for its own facts, such as quantity and price at purchase.

~~~mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : referenced_by
    ORDERS ||--o{ PAYMENTS : has

    CUSTOMERS {
      bigint customer_id PK
      text email UK
    }
    ORDERS {
      bigint order_id PK
      bigint customer_id FK
      text status
    }
    ORDER_ITEMS {
      bigint order_id PK,FK
      integer line_no PK
      bigint product_id FK
      numeric unit_price_at_purchase
    }
    PRODUCTS {
      bigint product_id PK
      text sku UK
      numeric list_price
    }
    PAYMENTS {
      bigint payment_id PK
      bigint order_id FK
      text provider_code
      text provider_ref
    }
~~~

The crow's-foot symbol says an order may have zero or many order items while it is being created. A foreign key from OrderItem to Order proves that each item points to an existing order. It does **not** prove the reverse rule “every order has at least one item.” If the business requires an order to contain an item before confirmation, that rule needs enforcement in the confirmation workflow or another deliberately designed mechanism. The diagram should show what the model actually guarantees.

The payment reference is assumed to be unique only within one provider. That means the candidate key is the pair (provider_code, provider_ref), not two separate unique values.

## Step 3: choose keys and constraints from the rules

A key gives a row an identity or expresses uniqueness. A constraint makes a rule explicit where data is stored.

- A **primary key** identifies each row. The OrderItem key is (order_id, line_no): line number 1 can appear in many orders, but only once inside a particular order.
- A **foreign key** requires a reference to match a row in another table. It protects the child-to-parent direction; it does not require every parent to have a child.
- A **unique constraint** expresses uniqueness within a chosen scope. Payment references are unique within a provider, so use a composite unique constraint on (provider_code, provider_ref). A unique constraint alone does not require a value; PostgreSQL 18 allows multiple NULL values by default, so keep NOT NULL when the provider identity is required. [PostgreSQL 18 — Constraints, §5.5.3](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS)
- A **not-null constraint** says a value must be present. A foreign key alone allows a missing value unless the column is also NOT NULL.
- A **check constraint** is useful for a condition on the same row, such as quantity greater than zero or an end time after a start time.

A natural key, such as an email address or provider reference, comes from business data. A surrogate key, such as customer_id, is assigned for database identity. Choose based on stability and uniqueness scope: can the value change, can two tenants or providers use the same value, and how many references would need updating if it changed? Neither key style is best for every domain.

The database is also the final guard for uniqueness when multiple writers can act at once. “Check whether the row exists, then insert” can race: two writers may both observe no row before either inserts. A unique constraint makes one write fail instead of storing a duplicate. The application must handle that conflict; the constraint does not replace user-friendly validation.

## Step 4: translate the model into tables

The DDL below is an illustrative example for **PostgreSQL 18**. It has not been executed in a declared environment, so treat it as teaching code rather than tested deployment SQL.

~~~sql
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    email       TEXT NOT NULL UNIQUE,
    full_name   TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL
);

CREATE TABLE products (
    product_id  BIGINT PRIMARY KEY,
    sku         TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    list_price  NUMERIC(14, 2) NOT NULL CHECK (list_price >= 0)
);

CREATE TABLE orders (
    order_id    BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    status      TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL,
    CONSTRAINT orders_customer_fk
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id              BIGINT NOT NULL,
    line_no               INTEGER NOT NULL,
    product_id            BIGINT NOT NULL,
    quantity              INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_at_purchase NUMERIC(14, 2) NOT NULL CHECK (unit_price_at_purchase >= 0),
    PRIMARY KEY (order_id, line_no),
    CONSTRAINT order_items_order_fk
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT order_items_product_fk
        FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id    BIGINT PRIMARY KEY,
    order_id      BIGINT NOT NULL,
    provider_code TEXT NOT NULL,
    provider_ref  TEXT NOT NULL,
    amount        NUMERIC(14, 2) NOT NULL CHECK (amount >= 0),
    status        TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL,
    CONSTRAINT payments_order_fk
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT payments_provider_reference_uq
        UNIQUE (provider_code, provider_ref)
);
~~~

Now connect the business rules to the DDL:

- **PRIMARY KEY** prevents two rows from sharing the chosen identity.
- **FOREIGN KEY** on orders.customer_id prevents an order from naming a customer row that does not exist.
- **CHECK (quantity > 0)** rejects a row with zero or negative quantity.
- **NOT NULL** makes required values explicit; it is separate from referential integrity.
- **UNIQUE (provider_code, provider_ref)** protects the provider-scoped payment reference.

PostgreSQL 18 defines primary keys as unique and not null. Foreign keys protect references, and CHECK constraints test expressions on the row being inserted or updated. CHECK is not a substitute for NOT NULL: a null result is not the same as false. A row-level CHECK is also not a general way to enforce rules across other rows or tables. [PostgreSQL 18 — Constraints, §§5.5.1–5.5.5](https://www.postgresql.org/docs/18/ddl-constraints.html)

The numeric example assumes one currency with two decimal places and an appropriate range. A real domain must define supported currencies, precision, and rounding explicitly; do not copy NUMERIC(14, 2) blindly for every monetary value. [PostgreSQL 18 — Numeric Types, §§8.1.2–8.1.3](https://www.postgresql.org/docs/18/datatype-numeric.html)

The example uses table-level foreign-key declarations. Do not describe it as portable SQL: MySQL 8.4 parses and ignores column-level inline REFERENCES declarations, so foreign keys must be written in the supported table-level form. For InnoDB tables in MySQL 8.4, the engine can create a supporting index on the referencing columns when one is needed and absent. Those are product and engine-specific details, not universal relational-database rules. [MySQL 8.4 — CREATE TABLE, §15.1.20](https://dev.mysql.com/doc/refman/8.4/en/create-table.html), [MySQL 8.4 — Foreign Key Constraints, §15.1.20.5](https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html)

PostgreSQL creates indexes for primary-key and unique constraints, but it does not automatically create an index on the referencing side of a foreign key. Whether to add one depends on the application's queries and on operations that need to find child rows, such as deleting or updating a parent. Use workload and query-plan evidence; DB-02 covers that decision. [PostgreSQL 18 — Constraints, §5.5.5](https://www.postgresql.org/docs/18/ddl-constraints.html)

## Step 5: decide which facts to normalize

Normalization is a way to organize facts so that each fact has a clear home and changes do not require updating many accidental copies. It helps reduce redundancy and inconsistent dependencies; the example below illustrates an update anomaly rather than attempting to define every normal form. [Microsoft Learn — Database normalization basics, “Description of normalization” and “Second normal form”](https://learn.microsoft.com/en-us/previous-versions/troubleshoot/microsoft-365/microsoft-365-apps/access/database-normalization-description)

Suppose customer email and product name are copied into every order-item row:

~~~text
order_id | customer_email   | product_sku | product_name | quantity
O-17     | sam@example.com  | MUG-1       | Blue mug     | 2
O-17     | sam@example.com  | NOTE-2      | Notebook     | 1
O-23     | sam@example.com  | MUG-1       | Blue mug     | 1
~~~

If Sam changes email, every matching row must be found and updated. Missing one row creates two answers for the same fact. Separating Customer and Product from OrderItem gives the current email and product name a single home; foreign keys connect each order line back to those entities.

Historical facts are different from current facts. The product's current list price may change, but the agreed transaction price should remain attached to the order item when that is the business rule. Storing unit_price_at_purchase is not accidental duplication if it records a distinct historical fact. If an immutable catalog version already preserves the exact price, the order could reference that version instead. State the domain rule before choosing.

## Step 6: denormalize only for a measured read need

Normalization is a useful starting point, not a goal to maximize regardless of workload. A derived read model stores or computes a representation for a particular read pattern from the system's underlying facts. A dashboard might repeatedly need the number of items on each order. The system could store an item_count on Order to make that read simpler, but now every insert or delete of an order item must keep the count correct.

That extra copy creates synchronization work. A retry, a duplicate event, or a partial failure can make the stored count drift from the actual rows. If a specific read path is frequent and measurement shows a real need, a derived read model may be reasonable. Plan how updates, retries, backfills, and reconciliation will repair it. Denormalization does not guarantee faster performance.

## Step 7: place each rule where it can be enforced

A row-level rule such as quantity > 0 can be expressed with a CHECK. A rule such as “every confirmed order has at least one item” spans the order and its child rows. A CHECK on a single order row cannot count the related items. The confirmation workflow must enforce the transition with a suitable transaction or another mechanism designed for that invariant.

This separation does not mean that the application should validate everything. The application can give a useful error before saving; the database constraint protects stored data across concurrent writers and every write path. For rules that depend on several rows or an external service, define the responsible transaction or workflow explicitly. [PostgreSQL 18 — Constraints, §5.5.1](https://www.postgresql.org/docs/18/ddl-constraints.html)

## A decision checklist for this design

Before calling the schema ready, ask:

1. Does every requirement map to a stored fact, a relationship, or an explicit workflow rule?
2. Is each key unique in the domain scope that actually matters?
3. Which values are current facts, and which must preserve history?
4. Which constraints can be checked on one row, and which require several rows or an application transition?
5. What read and write patterns will the design support?
6. If data is duplicated for reads, how will retries, backfills, and repair keep it consistent?

| Modeling choice | When it helps | Cost or failure mode |
|---|---|---|
| Separate entities connected by keys | A fact is shared and should have one current home | Reads may need joins; migrations and constraint rollout need care |
| Composite key for a locally scoped row | A line number is only meaningful within one order | References must carry all columns of the key |
| Snapshot a transaction fact | The value must remain as agreed at transaction time | Define exactly what is frozen and how corrections or refunds work |
| Store a derived read value | A measured read path justifies simpler retrieval | Adds synchronization, retry, backfill, reconciliation, and partial-failure work |
| Enforce an invariant in the database | Multiple writers must obey the same rule | Writers must handle constraint violations; rollout may need a migration plan |

Common mistakes include using a mutable display name or email as a permanent identifier without checking the domain; using check-then-insert instead of a unique constraint for uniqueness; assuming a foreign key creates every useful index; and choosing a monetary type without defining currency and rounding.

## Practical exercise: model a meeting scheduler

Design a relational model for a meeting-scheduling service.

Requirements:

- A user can organize many meetings; every meeting has exactly one organizer.
- A meeting may have many participants; a user can appear at most once in the same meeting.
- Each participant response is accepted, declined, or tentative.
- The meeting end time must be later than its start time.
- The application must list upcoming meetings for a user and list participants for one meeting.
- A draft meeting may have no participants. This exercise does not require a minimum participant count. As a hypothetical future rule, explain where the system should enforce a requirement of at least two participants before confirmation.

Submit an ERD, DDL for at least three tables, the primary/foreign/unique/check constraints, and two read patterns that identify which data each operation needs. Do not select or justify indexes; index mechanics are taught in DB-02.

A good design must prevent duplicate participants with a key or unique constraint, represent the time rule, and explain one database-enforceable invariant and one workflow-level rule.

Expected relationships: one user can organize many meetings; every meeting has one organizer; one meeting can have zero or many participants; one user can participate in many meetings. The pair (meeting_id, user_id) identifies a participant row within a meeting.

### Sample solution

One reasonable design uses users, meetings, and meeting_participants. IDs are supplied by the application in this example.

The following is illustrative PostgreSQL 18 syntax and has **not been executed**. If adapting it to MySQL 8.4, declare foreign keys in the supported table-level form and state the storage-engine assumptions.

~~~mermaid
erDiagram
    USERS ||--o{ MEETINGS : organizes
    MEETINGS ||--o{ MEETING_PARTICIPANTS : has
    USERS ||--o{ MEETING_PARTICIPANTS : joins
~~~

~~~sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    email   TEXT NOT NULL UNIQUE
);

CREATE TABLE meetings (
    meeting_id   BIGINT PRIMARY KEY,
    organizer_id BIGINT NOT NULL REFERENCES users(user_id),
    starts_at    TIMESTAMPTZ NOT NULL,
    ends_at      TIMESTAMPTZ NOT NULL,
    status       TEXT NOT NULL,
    CHECK (ends_at > starts_at)
);

CREATE TABLE meeting_participants (
    meeting_id BIGINT NOT NULL REFERENCES meetings(meeting_id),
    user_id    BIGINT NOT NULL REFERENCES users(user_id),
    response   TEXT NOT NULL CHECK (response IN ('accepted', 'declined', 'tentative')),
    PRIMARY KEY (meeting_id, user_id)
);
~~~

The composite primary key prevents the same user from being added twice to one meeting. The foreign keys require the organizer and participants to refer to existing users and meetings. The CHECK validates start and end times from the same meeting row. If a future requirement says that a meeting needs at least two participants before confirmation, that condition counts rows in another table and belongs in the confirmation transaction or another explicitly designed workflow.

| Rubric criterion | Points |
|---|---:|
| Entities and organizer/participant relationships are represented correctly | 20 |
| Primary/foreign keys protect identity and participant uniqueness | 25 |
| Time and response constraints are stated or enforced | 20 |
| Two read patterns map to the required data and relationships | 15 |
| One database invariant and one application-workflow rule are distinguished; one assumption or trade-off is explained | 20 |

The minimum-participant rule is hypothetical, not part of the current requirements; a strong answer explains that it counts rows across tables and should be checked in the confirmation workflow. Alternative schemas can earn full credit when they satisfy the stated requirements, make assumptions explicit, and explain their trade-offs. Index selection is not graded because it is covered in DB-02.

## Knowledge check

Answer these after the walkthrough and exercise. Each explanation below connects the answer to a design rule from the lesson.

1. The catalog price changes after an order is confirmed. What fact should the order item preserve, and what domain model could make a direct price snapshot unnecessary?
2. What does a foreign key from meeting_participants.user_id to users.user_id guarantee? Does it require every user to attend a meeting?
3. If customer email is copied to every order row, describe an update anomaly and how a separate Customer entity helps.
4. Why can “look for a participant, then insert if missing” still create duplicates with concurrent writers? What database rule closes that race?
5. When might you store a derived item count on an order? Name two synchronization or repair responsibilities that come with it.
6. In PostgreSQL 18, does declaring a foreign key automatically create an index on the referencing columns? When might that index be useful?
7. Which rule fits a row-level CHECK: end time later than start time, or at least two participants before confirmation? Explain the scope difference.
8. If two payment providers may issue the same provider_ref, what uniqueness rule matches that assumption?

### Answer key and explanations

1. Preserve unit_price_at_purchase when the business rule says the agreed transaction price must not change with the catalog. An immutable catalog-price version that the order references could preserve the same history without copying the price directly.
2. The foreign key requires the participant's user_id, when present, to reference an existing user. It does not require every user to participate in at least one meeting; that would be a different rule in the opposite direction.
3. If only some copied rows are updated, one customer has conflicting email values. A separate Customer entity gives the current email one home. If the system needs a historical shipping address, that is a separate historical fact and needs its own model.
4. Two writers can both observe that no row exists before either insert completes. A primary-key or unique constraint rejects one duplicate write; the application should handle that conflict.
5. Consider it when a specific read path is frequent and measurement justifies keeping the derived value. Keep updates consistent with item changes, make retries safe, and provide backfill or reconciliation to repair drift.
6. No. PostgreSQL 18 does not automatically index the referencing columns. Such an index may help queries that find child rows or parent deletes/updates that must locate them; decide from workload and query-plan evidence. Do not generalize this behavior to every DBMS.
7. End time later than start time uses two values from the same meeting row and fits a CHECK. “At least two participants” counts rows in another table and must be enforced by the confirmation workflow or another mechanism designed for multirow state.
8. Use UNIQUE (provider_code, provider_ref) when a reference is unique only within its provider. If the provider guarantees global uniqueness, a different key may fit; record that assumption explicitly.

## Outcome-to-assessment mapping

| Learning outcome | Assessment |
|---|---|
| 1. Turn requirements and access patterns into entities, relationships, and constraints | Worked order model; meeting exercise ERD and read patterns; questions 1 and 2 |
| 2. Choose primary, foreign, and unique keys for business rules | Worked DDL; exercise rubric criteria 1–2; questions 2, 4, and 8 |
| 3. Explain how normalization reduces an update anomaly | Normalization walkthrough; question 3 |
| 4. Decide when a derived read model may help and state its cost | Denormalization walkthrough; question 5 |
| 5. Distinguish database constraints from workflow rules | Rule-placement walkthrough; exercise rubric criterion 5; question 7 |

## References

- PostgreSQL Global Development Group, [PostgreSQL 18 — Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html), §§5.5.1–5.5.5: CHECK, NOT NULL, UNIQUE, primary-key, foreign-key, and referencing-side index behavior.
- PostgreSQL Global Development Group, [PostgreSQL 18 — Numeric Types](https://www.postgresql.org/docs/18/datatype-numeric.html), §§8.1.2–8.1.3: exact numeric/decimal and floating-point types; currency precision and rounding depend on the domain.
- Oracle, [MySQL 8.4 — CREATE TABLE](https://dev.mysql.com/doc/refman/8.4/en/create-table.html), §15.1.20; [Foreign Key Constraints](https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html), §15.1.20.5: product-specific syntax and foreign-key semantics.
- Microsoft Learn, [Database normalization basics](https://learn.microsoft.com/en-us/previous-versions/troubleshoot/microsoft-365/microsoft-365-apps/access/database-normalization-description), “Description of normalization” and “Second normal form”: introductory context for redundancy and dependencies; not evidence for a performance claim.
- MongoDB, [Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/), “Model Data for Access Patterns”: product-specific reference from the current manual, not a universal rule for relational schemas.
- Donne Martin, [System Design Primer — Database topic area at the reviewed commit](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#database): used as a topic map, not as the sole technical authority. The repository's [LICENSE.txt at the reviewed commit](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt) states CC BY 4.0 for author-provided material; [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) requires attribution and a change notice. Third-party assets remain subject to separate rights checks.

## Scope and source notes

PostgreSQL and MySQL references were checked on 2026-11-09; claims are limited to the product versions named. The MongoDB reference is the current manual and is not pinned to a server version. The SQL examples are illustrative PostgreSQL 18 and **have not been executed**. The Microsoft Learn normalization page showed an access-required banner during provenance review; confirm learner access or replace it before release. No learner timing study or legal review has been completed.

The topic scope and sequence were independently reorganized and supplemented using the Database topic area of Donne Martin's The System Design Primer at commit ae9bbd7b02d90b9866215de185217d33f39ab733, licensed CC BY 4.0 for author-provided material. Changes include original lesson flow, explanations, example, diagrams, exercise, questions, and answers. No Primer paragraphs, figures, code, or flashcards were copied. Nothing here implies endorsement. Third-party material in the Primer repository is not assumed to be covered by its license.
