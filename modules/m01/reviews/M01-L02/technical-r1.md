# M01-L02 revision 1 technical and provenance recheck

Checked 2026-11-11. Reviewed the revised teaching and assessment drafts, unchanged evidence and pinned curriculum inputs bound to the verdict.

## Technical findings

- **L02-T1 · resolved · Worked example and companion EX-1.** Both scenarios now specify dispatch into the backend and sufficient in-flight capacity while prior requests wait. The lesson's 120 offered operations/s at a 90/s backend produces 300 queued operations over 10 s. The companion's distinct 150/s versus 110/s over 12 s yields 480 operations. Both explain that a lower-capacity front end can queue some offered work upstream. [Google SRE, Queue Management](https://sre.google/sre-book/addressing-cascading-failures/#queue-management) · [Microsoft Azure Architecture Center, Application design considerations](https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling#application-design-considerations).
- **L02-T2 · resolved · Core concepts and mechanisms.** The revised p99 statement gives the empirical threshold interpretation and names the successful-request population and observation window. Timeout, rejection and error counts remain separate. [Google SRE, The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals).

Recomputed the revised assessment. Its 150/s burst against 120/s accumulates 360 in 12 s and drains in 12 s at a net 30/s. Each balanced worker receives 75/s against 80/s capacity. Losing one worker leaves 80/s against 90/s normal demand. Q2 and Q3 correctly model a 120-request backlog and 6 s of drain time. The exercise accepts decisions based on stated assumptions and asks for measurements rather than treating these modeled figures as observations. No material technical finding remains.

## Provenance findings

The new arithmetic and scenarios use original model inputs. The underlying source scopes and attribution are intact. The work cites the primary practice guidance and essay for its design reasoning and preserves credit for the Primer topic map, pinned revision and license. No third-party assets are included. [Vogels, A Word on Scalability](https://www.allthingsdistributed.com/2006/03/a_word_on_scalability.html) · [Primer license at pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt).

Verdict: **ready-for-human-review**.
