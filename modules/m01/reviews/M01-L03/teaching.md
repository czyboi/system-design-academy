# M01-L03 actual coverage and pedagogy review

## Scope and sources

Lesson mode for middle/senior engineers. Reviewed the approved SDA-v1 outline, lesson, companion and evidence. The source map is Donne Martin's The System Design Primer, revision ae9bbd7b02d90b9866215de185217d33f39ab733. The listed locators were inspected in the pinned source. The course review's N1 concerns M03-L02 and M06-L01 and does not affect this lesson.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H036 | Partition choices and CAP | taught | README.md#L438. Contrasts consistency and modeled request availability under message loss. |
| PR-H037 | Partition choices and CAP | taught | README.md#L440. Explains model assumptions and indistinguishable completed-write histories. |
| PR-H038 | Partition choices and CAP | taught | README.md#L456. Shows waiting or declining where a safe result cannot be established. |
| PR-H039 | Partition choices and CAP | taught | README.md#L460. Explains response through a split and staleness or resolution contract. |
| PR-H041 | Core concepts and mechanisms | taught | README.md#L473. Compares observable object histories across three contracts. |
| PR-H042 | Core concepts and mechanisms | taught | README.md#L477. Explains a permitted stale post-write read with no convergence promise. |
| PR-H043 | Core concepts and mechanisms | taught | README.md#L483. States update quiescence, propagation and reconciliation conditions for convergence. |
| PR-H044 | Core concepts and mechanisms | taught | README.md#L489. Defines linearizable object history and distinguishes overlapping operations. |

All assigned topics have explanatory lesson evidence.

## Pedagogy and assessment

A concrete stale history introduces the model before operation-specific partition choices and recovery. The intended middle/senior audience and English language fit the plan.

Six explained questions and the practical exercise cover stale and overlapping histories, CAP behavior, read-your-writes, convergence and a scoped vendor example. The separate answer key gives a defensible policy and rubric.

## Findings

**P01 — minor.** The LO2 map points to Decision framework, while the version-token mechanism and convergence/conflict conditions are explained in Worked example and Trade-offs and failure modes. Cross-reference those sections from the mapped location to make the full outcome trace explicit.

Verdict: **ready-for-human-review**.
