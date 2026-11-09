# DB-01 Provenance and Asset Review

**Task:** `SD-DB01-WORKFLOW-PILOT`  
**Artifact reviewed:** `author/draft.md`  
**Review date:** 2026-11-09  
**Verdict:** `revise` before human review; this is not legal approval.

## Asset and source ledger

| Source or asset | Creator / publisher | Use in the lesson | Rights / scope recorded | Review result |
|---|---|---|---|---|
| *The System Design Primer* — Database topic area | Donne Martin | Topic coverage and high-level organization only, as described by the lesson | The Primer repository's `LICENSE.txt` states CC BY 4.0. The repository also warns that embedded or linked third-party works must be checked separately. | No matching Primer paragraphs, figures, flashcards, notebooks, or code were identified in this draft. The lesson states that its prose, order-management example, Mermaid diagram, exercise, questions, and answers are original. Because it also says topic organization was informed by the Primer, clarify the adaptation boundary and complete the attribution block described below. |
| PostgreSQL 18 documentation | PostgreSQL Global Development Group | Direct references for constraint, numeric, foreign-key and index semantics | The lesson links to exact PostgreSQL 18 documentation sections and limits product claims to PostgreSQL 18. It does not reproduce documentation passages. | Traceability is good at the claim level in the draft. SQL is explicitly described as illustrative and unexecuted. |
| MySQL 8.4 Reference Manual | Oracle | Direct citations for the inline `REFERENCES` portability caveat and foreign-key semantics | Product version and sections are identified; pages are linked rather than copied. | Scope is explicit. No MySQL code or screenshots are redistributed. |
| Database normalization basics | Microsoft Learn; page applies to Access 2021/2019/2016/2013 | Supports a limited introductory statement about redundancy and maintenance problems | The draft identifies the exact article sections and limits it to introductory normalization context. | No passage appears copied. The page showed an access-required banner during this review even though article text was visible; check reader reachability before release or replace it with a reliably accessible source. |
| Data Modeling in MongoDB | MongoDB | Supports a clearly product-scoped example of MongoDB's access-pattern recommendation | The lesson names the “Model Data for Access Patterns” section and labels the manual current rather than claiming a fixed server version. | Appropriate as a MongoDB-specific reference; it is explicitly not generalized as a universal relational rule. |
| SQL examples, Mermaid ERD, exercise schema, rubric, questions and answer explanations | System Design Academy draft authorship | Original teaching materials | No third-party asset or code source is identified for these items. | They appear newly authored in the reviewed draft. No external image, diagram, notebook, flashcard, or other embedded asset was found. |

## Findings

### [Major] Complete the Primer attribution or state the boundary more precisely

**Location:** `author/draft.md`, “References” and “Scope and source notes.”

The draft names Donne Martin and the Primer, links the Database section, reports CC BY 4.0, and says there is no endorsement. It does not link the CC BY 4.0 license text or state a concise change notice. The lesson also says that its topic scope and organization were informed by the Primer, while asserting that its own prose, examples and diagram are new. The current note therefore leaves unclear whether only general topic ideas were used or whether the Primer's topic selection/arrangement was adapted.

**Recommended fix:** add the direct license link `https://creativecommons.org/licenses/by/4.0/` and a short notice that this lesson independently reorganizes and supplements the Database topic area, with original explanations, examples, diagrams, exercises and assessments. Keep the no-endorsement statement. If no protectable expression or arrangement was adapted, say so clearly instead of implying a broader adaptation. The Primer's own `LICENSE.txt` is the relevant source for its stated CC BY 4.0 terms; the license should not be assumed to cover third-party assets linked or embedded in that repository.

### [Minor] Pin the Primer snapshot used for topic organization

**Location:** `author/draft.md`, Primer reference; `modules/database/sources/source-registry.csv`, `SRC-001` and `SRC-002`.

The lesson links to the moving `master` branch, and the source registry records “Repository master snapshot” plus a checked date but no commit hash. Since this source is used for topic coverage/organization rather than a stable technical claim, this is not a technical-citation defect; it does make the exact attributed snapshot hard to reproduce.

**Recommended fix:** record the Primer commit SHA or another immutable snapshot URL in the source registry/run evidence and retain the checked date. Keep the human-readable section link in the lesson if useful.

## Review scope and limits

- The linked sources were opened on 2026-11-09. This review checked attribution and source-use framing, not the technical truth of every cited claim; that belongs to the separate technical review.
- The review found no verbatim passage, third-party visual asset, copied code, or implied endorsement in the reviewed draft. This is an inspection finding, not a legal conclusion.
- Direct links to official product documentation are used for factual support. Linking alone does not grant permission to redistribute copied text or assets; none were identified here.
- Before commercial publication, the project's policy calls for qualified legal review of actual course assets, attribution placement, terms of sale, and third-party materials.

## Verdict

`revise` — add the license URL and clarify the Primer adaptation/change notice, and make the source snapshot reproducible. No asset issue currently warrants blocking the draft from continued editorial revision. This report does not grant legal approval.
