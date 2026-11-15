---
id: M00-decisions
status: draft
---

# Design and study decisions

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
|---|---|---|---|---|---|---|---|
| A failure trace breaks at a transaction boundary. | Targeted prerequisite repair. | Replay two cases with the failure on opposite sides of commit, then explain each from memory. | Makes the gap and improvement observable. | Takes time away from broader practice. | The learner predicts the same durable state for both traces. | The learner can already trace the boundary and explain what survives retry. | [M00-L01](../lessons/M00-L01.md) |
| The service brief has unresolved priorities. | Rank must-have use cases and verify constraints first. | Turn the top user risk into an observable acceptance check and trace the corresponding request. | Identifies the design decision that needs the most detail. | Requires a stakeholder answer or a documented assumption. | Alternatives satisfy different unstated definitions of success. | The decision is already bounded by verified requirements. Use the same checks to compare candidates. | [M00-L02](../lessons/M00-L02.md) |
| Forecast growth threatens one resource. | Change the measured bottleneck. | Reproduce the limit, profile the path, change one variable and repeat the test. | Connects the design change to a measurable effect. | Requires representative test traffic and instrumentation. | The bottleneck moves or errors rise without useful throughput improving. | A hard failure requirement already rules out the topology. Address that requirement first. | [M00-L02](../lessons/M00-L02.md) |
