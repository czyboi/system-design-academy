---
id: M01-decisions
status: draft
---

# Workload and failure decisions

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
|---|---|---|---|---|---|---|---|
| A daily total hides rush-hour load. | Estimate a peak range. | Convert by time window, split the request mix and test under a representative burst. | Makes required throughput and bandwidth explicit. | Requires traffic and payload data. | Peak latency misses the target while daily capacity looks sufficient. | For a known burst schedule, model the measured arrival trace directly. | [M01-L01](../lessons/M01-L01.md) |
| Frontends saturate at 120 reads/s. | Add ready app capacity. | Spread work across workers and provision a survivor to handle 150 reads/s. | Can relieve app queueing and sustain load after zone loss. | Extra compute and a need for balanced routing. | Store wait time rises while workers remain idle. | Shared storage or auth limits useful throughput. | [M01-L02](../lessons/revision-1/M01-L02.md) |
| Customers can use a briefly older status during a split. | Allow a bounded local display. | Check lag conservatively, label the result and cut off fallback on expiry. | Preserves some customer reads. | Added projection operations and a degraded experience. | Lag becomes unknown or exceeds 60 s. | Refund authorization and other operations that require current authority. | [M01-L03](../lessons/M01-L03.md) |
| One serving zone must be expendable. | Keep a ready, sized alternate path. | Route eligible traffic to the surviving zone and verify capacity and state. | Removes startup from the recovery path. | Spare capacity and recurring failure drills. | Both paths fail through shared auth or the survivor saturates. | A slower restore already meets the interruption and data-loss objectives. | [M01-L04](../lessons/M01-L04.md) |
