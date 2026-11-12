# M01-L03 technical and provenance review

## Findings

No actionable technical or provenance findings in the metadata changes.

## Scope and checks

Targeted Stage A review of [PR #55 comment 2](https://github.com/czyboi/system-design-academy/pull/55#issuecomment-6820605428) on 2026-11-12. Compared `e2158e2..434dc63` for the lesson, evidence and assessment. The diff updates two `taught_in` strings and explains their order in the assessment body. The [earlier module review](../../technical.md) records the prior verdict for the unchanged teaching and evidence.

| Outcome | Assessment location | Teaching sections and technical fit |
| --- | --- | --- |
| M01-L03-LO1 | `M01-L03.md:7`, Q1–Q3 | “Read and write histories” explains stale reads and ordering of overlapping operations for Q1–Q2. “Preserve a session and reconcile edits” explains how a successful session read reflects the caller's acknowledged write for Q3. [Herlihy and Wing, §2.2](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf#page=6) · [Terry et al., Session Guarantees, §3.1](https://pages.cs.wisc.edu/~remzi/Classes/739/Papers/bayou-sessions94.pdf#page=3) |
| M01-L03-LO2 | `M01-L03.md:10`, Q4–Q6 and EX-1 | “Choose operations during a partition” explains an unavailable current-value read for Q4 and EX-1. “Preserve a session and reconcile edits” gives the snapshot-inclusion rule for Q5 and EX-1 and the deterministic conflict policy for Q6 and EX-1. The exercise retains the common ordered-prefix assumption for the scalar token and evaluates the multi-writer conflict separately. [Gilbert and Lynch, §§2.2–3.1](https://www.comp.nus.edu.sg/~gilbert/pubs/BrewersConjecture-SigAct.pdf#page=3) · [Terry et al., Session Guarantees, §5](https://pages.cs.wisc.edu/~remzi/Classes/739/Papers/bayou-sessions94.pdf#page=6) · [Terry et al., Managing Update Conflicts, §5](https://www.scs.stanford.edu/nyu/01fa/sched/bayou.pdf#page=5) |

Both strings use the lesson's exact headings in the same order as the assessment table and [module outcome portfolio](../../../../integrated/outcome-portfolio.json). The item IDs agree across the assessment front matter and the portfolio. Questions, answers, vendor/version scope and citations are unchanged. The diff adds no external assets or adaptations. The CMU and MIT PDF hosts timed out during this check. The report links to the same primary papers on the authors' Columbia and NUS publication sites.

**Verdict: ready-for-human-review.**

## Round 1 targeted re-review

Compared `434dc63..68d36a4` for L03-P1. Q6 is now listed under LO1 in the assessment front matter, the narrative outcome map and the module portfolio. It also remains under LO2 in all three places. The existing Q6 asks learners to choose a deterministic rule for concurrent edits, specify delivery and identify a cost. Its answer follows both replicas from receipt of the same edits to selection of the same winner. That reasoning supports LO1's reconciliation outcome, and the rule choice and its trade-off support LO2. The lesson teaches both in “Preserve a session and reconcile edits.” The correction changes only mappings and introduces no technical or provenance regression. [Terry et al., Managing Update Conflicts, §5](https://www.scs.stanford.edu/nyu/01fa/sched/bayou.pdf#page=5)

**Current verdict: ready-for-human-review.**
