# M01-L03 technical and provenance review

Checked 2026-11-11. Reviewed the teaching draft, companion, evidence, and pinned curriculum inputs recorded in the verdict.

## Technical findings

- **L03-T1 · minor · Worked example, minimum-version token.** The version-7 token is sufficient for the two-version trace. Name the invariant if readers generalize it: an eligible replica applies a complete prefix of the same ordered history, so satisfying the threshold proves that the session's write was applied. Independent replica counters do not provide that evidence. [Terry et al., §3.1 and §5](https://pages.cs.wisc.edu/~remzi/Classes/739/Papers/bayou-sessions94.pdf).

The weak, eventual and linearizable contracts match the scoped histories. The overlapping read answer preserves real-time precedence and admits only an otherwise legal ordering. The asynchronous CAP model and the distinction between completing an operation successfully and returning an unavailability response are consistent with the original read/write object theorem. The partition policies are stated by operation and the text separates CAP from the operational success percentage and application invariants. The profile recovery conditions include communication and conflict resolution. The balance example scopes its guarantee to the read. A payment implementation would need to preserve its balance invariant across authorization and any debit. [Gilbert and Lynch, §§2.1–2.3 and §3.1](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer6.pdf) · [Brewer, Why “2 of 3” Is Misleading and Partition Mode](https://sq4007-2025.github.io/website/pdfs/Brewer%20-%202012%20-%20CAP%20twelve%20years%20later%20How%20the%20rules%20have%20changed.pdf) · [Vogels, Client-side Consistency](https://www.allthingsdistributed.com/2008/12/eventually_consistent.html).

BASE is presented as an approach, with separate contracts for freshness, conflicts and transactions. AWS explicitly scopes the last-writer rule and potentially stale local strongly consistent read to multi-Region eventual consistency mode in global tables version 2019.11.21. The mode is identified in both the lesson and Q6. The text makes no universal claim about cross-Region latency. [Pritchett, An Acid Alternative and Consistency Patterns](https://web.stanford.edu/class/cs245/spr2019/readings/base.pdf) · [AWS, Versions and Multi-Region eventual consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/V2globaltables_HowItWorks.html).

## Provenance findings

- **L03-P1 · minor · CAP and session-guarantee citations in lesson and evidence.** The Princeton PDF returned 403 and the UChicago PDF returned 502 during this check. The original papers were accessible through Nancy Lynch's MIT publication list and the University of Wisconsin course copy. Prefer those locations. The Terry paper's guarantee is §3.1 and its version-vector implementation is §5. [Gilbert and Lynch original paper](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer6.pdf) · [Terry et al. original paper](https://pages.cs.wisc.edu/~remzi/Classes/739/Papers/bayou-sessions94.pdf).

The scenarios, histories, conflicts and assessment use original examples. Academic and AWS references support facts and are linked as sources. No third-party figures, code, or other assets were reproduced. The Primer attribution supplies Donne Martin, pinned revision, CC BY 4.0 and a change statement. No implied endorsement was found. [Primer license at pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt).

Verdict: **ready-for-human-review**.
