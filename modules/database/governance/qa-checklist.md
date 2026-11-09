# Lesson QA Checklist

Use this as a gate. A lesson cannot be marked `approved` if any critical item fails.

## A. Source and traceability

- [ ] Every material technical claim has a nearby reference or an explicit statement that it is a reasoned design recommendation.
- [ ] The cited source actually supports the claim; title/snippet alone is not enough.
- [ ] Vendor/version scope is stated where behavior differs by product or version.
- [ ] Source URL, section, access/check date and version are recorded.
- [ ] Any adapted Primer expression/asset has attribution and change notice.
- [ ] External images, diagrams, code and linked resources have separate license checks.

## B. Technical correctness

- [ ] Terminology is precise; no conflation of partitioning and sharding.
- [ ] No false guarantees or unsupported absolute claims.
- [ ] Assumptions and workload are explicit.
- [ ] Trade-offs include at least one downside/cost for each recommended design.
- [ ] Failure modes and recovery behavior are covered where relevant.
- [ ] Examples/SQL are syntactically plausible for the stated engine/version.
- [ ] Any query plan or performance claim avoids extrapolating toy data to production.

## C. Pedagogy

- [ ] Learning outcomes use observable verbs.
- [ ] A concrete problem motivates the topic.
- [ ] Concepts progress from simple to complex.
- [ ] At least one worked example is included.
- [ ] Each outcome is assessed by a question or exercise.
- [ ] Answer key explains reasoning, not just the correct option.
- [ ] A learner can distinguish general principle from vendor-specific detail.

## D. Editorial and publishing

- [ ] No copied long passages without permission/attribution.
- [ ] Diagram is readable and consistent with the explanation.
- [ ] Terms and abbreviations are consistent.
- [ ] Broken links are checked.
- [ ] Front matter status is correct (`draft`, `review`, `approved`, `published`).
- [ ] Human reviewer and review date are recorded before publication.

## Severity

- **Critical:** materially wrong behavior, fabricated source, unlicensed asset, unsafe migration/recovery advice. Must block publication.
- **Major:** missing trade-off, misleading simplification, unsupported core claim, broken practical exercise. Must fix before approval.
- **Minor:** wording, formatting, nonessential link or clarity issue. May be tracked for later.
