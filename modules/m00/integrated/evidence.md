# Evidence for M00 integrated design

Initial sources checked 2026-11-11. Sources and claims for the 2026-11-15 restoration were checked against the current M00-L02 evidence. The document-sharing service, workload figures and verification targets are hypothetical exercise inputs.

| Claim ID | Claim | Publisher, version and section | Scope and confidence |
|---|---|---|---|
| M00-I1 | Start with a feasible baseline, state resource assumptions, and reconsider the design when workload or failure changes its feasibility. | Google, *The Site Reliability Workbook* (2018), Chapter 12, [Design Process and Initial Requirements](https://sre.google/workbook/non-abstract-design/#design-process). | Verified as a design method illustrated by Google. The exercise's review format and numeric inputs are Academy choices. |
| M00-I2 | Derive measurable success and latency indicators from the user's critical activities, using a specified population and observation point. | Google, *The Site Reliability Workbook* (2018), Chapter 2, [What to Measure and A Worked Example](https://sre.google/workbook/implementing-slos/#what-to-measure-using-slis). | Verified. The exercise asks for candidate indicators and measurement plans. Production feasibility requires data. |
| M00-I3 | A later authorization check on the same grant observes a completed revoke under the stated linearizable contract. An HTTP response with `no-store` is not stored by compliant caches. | Herlihy and Wing (1990), [§2.2](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf#page=7). IETF, RFC 9111 (2022), [§5.2.2.5](https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2.2.5). | Abstract order and HTTP directive only. Verify the chosen grant store and actual client path. |
| M00-I4 | A request may have taken effect when its response is lost. | IETF, RFC 9110 (2022), [§9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2). | Terminal publication and reference checks are safeguards in the proposed design. The RFC does not specify object cleanup. |

The approved SDA-v1 M00 integrated outline scopes the synthesis to M00-S1 and M00-EX1. The separate companion assessments measure readiness and the individual lesson outcomes. External sources are cited for facts and methods. All exercise text and examples are original.
