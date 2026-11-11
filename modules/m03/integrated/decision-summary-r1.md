---
id: M03-decisions
status: draft
---

# Service boundary and interface decisions

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| One atomic rule spans several state changes. | Keep a transactional owner. | Guard the pointer update on the authoritative version and approval row. Invalidate the pointer in the same update as an edit or revocation. | Localizes the invariant and its recovery. | Shared deployment may couple release and capacity. | An attempted split needs synchronous coordination for every write. | A capability has independent scale and can expose an acceptable cross-boundary contract. | [M03-L01](../lessons/M03-L01.md) |
| Preview CPU crowds out metadata requests. | Deploy rendering separately. | Pass immutable inputs across a versioned contract and record results asynchronously. | Capacity can follow the distinct workload. | Requires durable progress and operations for another service. | Preview lag grows even as metadata p99 recovers. | Local resource isolation meets both targets with lower operating cost. | [M03-L01](../lessons/M03-L01.md) |
| Clients release on different schedules and poll job state. | Expose a resource interface over HTTP. | Use stable identities, status links, optional fields and an explicit duplicate contract. | Gives diverse clients a way to track work. | Representation and compatibility commitments. | A new release breaks older clients' interpretation of job state. | A focused internal operation already fits the controlled client ecosystem. | [M03-L02](../lessons/M03-L02.md) |
| Internal callers need a typed rendering operation. | Use a schema-defined RPC. | Generated stubs encode an operation and stable work ID. The renderer accepts each ID with an atomic create-if-absent. | Makes the contract explicit for supported callers. | Schema evolution, SDK distribution and observability work. | A dropped reply creates another logical job. | Clients cannot use the schema/tooling or the requirement is chiefly resource navigation. | [M03-L02](../lessons/M03-L02.md) |
| Endpoint lists change during deployments. | Cache discovery and assign one retry owner. | Refresh eligibility outside the call path and retry a distinct eligible endpoint within the remaining deadline. | Tolerates some transient failures while limiting work. | Cache staleness and retry budget management. | Connection failures grow after endpoint removal or attempts multiply. | Ambiguous operations lack a suitable retry contract or spare capacity is exhausted. | [M03-L03](../lessons/M03-L03.md) |
