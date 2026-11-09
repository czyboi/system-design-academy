# DB-01 Pedagogical Review

**Task:** `SD-DB01-WORKFLOW-PILOT`  
**Artifact reviewed:** `author/draft.md`  
**Review date:** 2026-11-09  
**Reviewer:** Independent pedagogy reviewer; report recorded by the task parent from the reviewer’s returned findings because the reviewer session could not write files.  
**Verdict:** `revise`

## Summary

The lesson has a clear learner path: problem → modeling method → worked order example → constraints and trade-offs → practice. The eight questions include explanations, and the exercise accepts alternative schemas that satisfy the requirements. This is a solid draft for review, with several alignment and clarity fixes recommended.

## Findings

### [Minor] The outcome-to-assessment table overstates what the exercise rubric measures

**Location:** `author/draft.md`, “Outcome-to-assessment mapping,” lines 268–272.

Outcomes 3 and 4 are mapped to rubric criterion 5, but that criterion scores application-versus-database invariants and a general trade-off; it does not explicitly score normalization or a denormalization decision. Outcome 5 is mapped to criterion 3, which scores time and response constraints, not where an invariant belongs. Questions 3, 5, and 7 do assess those outcomes, so the lesson has coverage; the crosswalk should name those direct checks and remove unsupported rubric references, or add matching rubric criteria.

**Recommended change:** Make each row cite the question(s) that directly assess it. If the rubric is meant to assess an outcome, add a rubric dimension that explicitly scores that outcome.

### [Minor] The exercise asks for an ERD but the sample solution gives only DDL and prose

**Location:** `author/draft.md`, practical exercise and sample solution, lines 186–228.

Learners submit an ERD, but the sample solution does not show one. The DDL and explanation help, yet learners cannot compare their relationship/cardinality diagram directly.

**Recommended change:** Add a small sample ERD or list expected entities and cardinalities explicitly.

### [Minor] The organizer requirement is redundant and could confuse the meeting state model

**Location:** `author/draft.md`, practical exercise and sample solution, lines 190, 195, 213, and 228.

The exercise says each meeting has exactly one organizer, then separately says a meeting cannot become `confirmed` without one. The sample solution uses `organizer_id NOT NULL` for every state.

**Recommended change:** Clarify whether draft meetings can exist without an organizer. If they cannot, remove the separate confirmation requirement. If they can, make the schema and transition rule reflect that lifecycle.

### [Minor] Define key terms when they first appear

**Location:** `author/draft.md`, learning outcomes and later explanatory sections, lines 18–22, 168, and 181.

“Invariant” and “read model” appear in the outcomes before explanation; “backfill,” “reconciliation,” and “partial failure” appear later without concise definitions.

**Recommended change:** Keep the English terms but add short Vietnamese explanations where each first matters.

### [Note] Validate the 90-minute estimate with learners

**Location:** `author/draft.md`, front matter, line 6.

The lesson includes two DDL examples, eight knowledge checks with explanations, and a schema-design exercise. The estimate is correctly labeled provisional.

**Recommended change:** Measure completion time during the learner pilot before fixing the estimate.

## Review scope

This review assessed learner flow, sequencing, outcome coverage, assessment clarity, and workload. It did not assess technical correctness or source/legal validity; those are covered by separate reports.

## Verdict

`revise` — address the outcome-to-assessment crosswalk, add a comparable ERD/sample cardinalities, clarify organizer lifecycle assumptions, and define jargon at first use. No issue found here requires a human decision before editorial revision.
