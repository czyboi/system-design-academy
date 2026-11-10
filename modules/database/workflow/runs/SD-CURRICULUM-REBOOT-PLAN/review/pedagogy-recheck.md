# Pedagogical recheck — revision 3

**Verdict:** `revise`  
**Artifact:** revision-3 curriculum candidate  
**Reviewer:** independent `pedagogy_reviewer`  
**Scope:** middle/senior audience fit, prerequisite and topic sequence, lesson-sized boundaries, and the teaching-only constraint. This plan-stage review does not establish technical correctness or lesson quality.

## Material finding

| Severity | Candidate location | Finding and learner/author impact | Recommended change |
|---|---|---|---|
| Medium | SD-07-06; SD-07-09; SD-07-10 | SD-07-06 still mentions explaining how a search feature can use a key-value index. SD-07-09 owns index construction, while SD-07-10 owns query retrieval and ranking. The overlap blurs whether SD-07-06 teaches key-value storage mechanics or search-index design, making lesson ownership harder to author and review independently. | Bound SD-07-06 to generic key-value store and cache mechanics, with the search-store prompt serving only as a context/example. Keep index construction and query-serving mechanisms in SD-07-09 and SD-07-10, with an explicit handoff. |

## Findings that pass

- SD-07-03 is bounded to crawler acquisition, frontier/fetch behavior, deduplication, recrawl and failures; it explicitly excludes indexing and query serving.
- SD-07-09 followed by SD-07-10 gives a clear progression from index construction/publication to query retrieval, ranking and serving.
- Twitter keyword search is routed to SD-07-09/10; its mention in SD-07-02 functions as a handoff.
- The sequence and prerequisites fit middle/senior backend engineers. The plan remains teaching-only and contains no quiz, exercise, assessment, answer or rubric content.

## Gate result

The pedagogy gate remains open because the SD-07-06/09 boundary needs clarification. Under the task specification, do not finalize the curriculum until the required independent rechecks have no material blockers. Any additional revision requires user authorization.
