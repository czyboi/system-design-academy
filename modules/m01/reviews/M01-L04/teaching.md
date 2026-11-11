# M01-L04 actual coverage and pedagogy review

## Scope and sources

Lesson mode for middle/senior engineers. Reviewed the approved SDA-v1 outline, lesson, companion and evidence. The source map is Donne Martin's The System Design Primer, revision ae9bbd7b02d90b9866215de185217d33f39ab733. The listed locators were inspected in the pinned source. The course review's N1 concerns M03-L02 and M06-L01 and does not affect this lesson.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H046 | Core concepts and mechanisms | taught | README.md#L499. Names traffic roles and replication as complementary availability mechanisms. |
| PR-H047 | Core concepts and mechanisms | taught | README.md#L503. Explains failure detection, fencing, promotion, routing and readiness. |
| PR-H048 | Core concepts and mechanisms | taught | README.md#L505. Contrasts serving and standby capacity with hot/warm/cold readiness. |
| PR-H049 | Core concepts and mechanisms | taught | README.md#L513. Explains serving from both sites and surviving capacity/freshness. |
| PR-H050 | Trade-offs and failure modes | taught | README.md#L521. Discusses resource, startup, stale-data and multi-writer costs. |
| PR-H051 | Core concepts and mechanisms | taught | README.md#L526. Explains replicated copies, possible asynchronous loss and backup recovery. |
| PR-H052 | Core concepts and mechanisms | taught | README.md#L528. Contrasts single write authority with multi-writer conflict requirements. |
| PR-H053 | Core concepts and mechanisms | taught | README.md#L535. Derives downtime from a stated time window. |
| PR-H054 | Core concepts and mechanisms | taught | README.md#L539. Calculates three-nines downtime for exactly 30 days. |
| PR-H055 | Core concepts and mechanisms | taught | README.md#L548. Calculates four-nines downtime for exactly 30 days and distinguishes request measures. |
| PR-H056 | Core concepts and mechanisms | taught | README.md#L557. Defines serial and either-suffices path events and assumptions. |
| PR-H057 | Core concepts and mechanisms | taught | README.md#L561. Derives a two-component serial example. |
| PR-H058 | Core concepts and mechanisms | taught | README.md#L571. Derives two-path redundancy and models a shared dependency. |

All assigned topics have explanatory lesson evidence.

## Pedagogy and assessment

Traffic and data roles precede failover and arithmetic, followed by a worked timeline and decision criteria. Each simplification states assumptions that can be challenged.

The distinct exercise changes timeline, RTO and RPO inputs. Six checks with explanations cover time and dependency arithmetic, liveness, standby limits and recovery. Both outcomes map to exercise or checks and the rubric gives alternative valid changes.

## Findings

**P01 — minor.** LO1 maps to Worked example, which teaches failover and time-budget arithmetic. The independent serial and parallel dependency calculation assessed by Q2 is taught in Core concepts and mechanisms. Link that section from the mapped location or include it in a fuller human-readable outcome map.

Verdict: **ready-for-human-review**.
