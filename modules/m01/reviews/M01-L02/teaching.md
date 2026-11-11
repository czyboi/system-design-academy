# M01-L02 actual coverage and pedagogy review

## Scope and sources

Lesson mode for middle/senior engineers. Reviewed the approved SDA-v1 outline, lesson, companion and evidence. The source map is Donne Martin's The System Design Primer, revision ae9bbd7b02d90b9866215de185217d33f39ab733. The listed locators were inspected in the pinned source. The course review's N1 concerns M03-L02 and M06-L01 and does not affect this lesson.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H032 | Core concepts and mechanisms | taught | README.md#L412. States comparison axis, common load mix and success targets, then explains vertical and horizontal changes. |
| PR-H034 | Core concepts and mechanisms | taught | README.md#L426. Defines per-operation latency and useful completions per unit time, including sampling and errors. |

All assigned topics have explanatory lesson evidence.

## Pedagogy and assessment

The problem leads through metrics, state placement, queueing, a model and measurement criteria. The applied assessment needs changed inputs.

The companion has six explained checks and a rubric, with both outcomes mapped. The exercise and Q2–Q3 duplicate the worked numeric example, so LO1 transfer cannot be established by those calculations.

## Findings

**P01 — major.** Assessment EX-1 repeats the Worked example's exact arrival rates, 10-second burst, 100/65-server capacities and 90/s backend cap. Q2 and Q3 repeat the same queue growth and drain calculations. A learner can reproduce the central model from the teaching example rather than demonstrate the stated modeling outcome on a new workload. Change the exercise inputs and recalculate the answer key, keeping the same assumptions, failure comparison and rubric.

**P02 — minor.** LO2 maps to Trade-offs and failure modes, while Q4's queueing mechanism and Q5's state-placement mechanism are taught under Queueing and saturation and Core concepts and mechanisms. Add explicit references to those sections in the map's chosen teaching section or the companion.

Verdict: **revise**.
