---
id: M03-decisions
status: draft
---

# Service boundary and interface decisions

## Connect the boundary, contract and failure policy

Start with the work that needs separate capacity and the state that must still change atomically. In the catalogue example, CPU-heavy conversion can finish asynchronously. The transactional catalogue still owns the state that allows an item to become public. Moving those state changes behind separate services would add coordination to the publication decision. [M03-L01 worked example](../lessons/M03-L01.md#worked-example)

The boundary creates two contracts. An editor can follow a resource link to inspect progress, while the dispatcher invokes a focused operation. Atomically save the scoped key, immutable inputs, stable work ID and pending dispatch before sending; retries and restart reuse that identity. A durable acceptance record resolves a lost reply, and a stored result reference permits completion replay or lookup. Unresolved acceptance at expiry needs reconciliation under the same identity. [M03-L02 worked example](../lessons/M03-L02.md#worked-example)

Choose who selects endpoints based on the caller population and the cost of a shared intermediary. A cached endpoint can fail after its last healthy observation. Charge the elapsed wait and backoff to one deadline, select another eligible endpoint if time remains, and use an attempt cap and a bound on concurrent work to contain amplification. If the cached view expires during a discovery outage, defer work or fail according to the operation's deadline. [M03-L03 ownership and failure controls](../lessons/M03-L03.md#ownership-and-failure-controls) · [M03-L03 worked trace](../lessons/M03-L03.md#worked-example-stale-endpoint-and-deadline-failure-trace)

## Decision table

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| One atomic rule spans several state changes. | Keep a transactional owner. | Publish only when rendered, current and approved versions match on the authoritative row. Clear approval and pointer in the same update as an edit or revocation. | Localizes the invariant and its recovery. | Shared deployment may couple release and capacity. | An attempted split needs synchronous coordination for every write. | A capability has independent scale and can expose an acceptable cross-boundary contract. | [M03-L01](../lessons/M03-L01.md) |
| Preview CPU crowds out metadata requests. | Deploy rendering separately. | Pass immutable inputs across a versioned contract and record results asynchronously. | Capacity can follow the distinct workload. | Requires durable progress and operations for another service. | Preview lag grows even as metadata p99 recovers. | Local resource isolation meets all four targets with lower operating cost. | [M03-L01](../lessons/M03-L01.md) |
| Clients release on different schedules and poll job state. | Expose a resource interface over HTTP. | Preserve status semantics and links; add fields only for tolerant clients, or opt strict clients into a new representation. Test old clients with new responses and new clients with old responses. | Gives diverse clients a way to track work. | Representation and compatibility commitments. | A new release breaks older clients' interpretation of job state. | A focused internal operation already fits the controlled client ecosystem. | [M03-L02](../lessons/M03-L02.md) |
| Internal callers need a typed rendering operation. | Use a schema-defined RPC. | Generated stubs encode an operation and stable work ID. The renderer accepts each ID with an atomic create-if-absent. | Makes the contract explicit for supported callers. | Schema evolution, SDK distribution and observability work. | A dropped reply creates another logical job. | Clients cannot use the schema/tooling or the requirement is chiefly resource navigation. | [M03-L02](../lessons/M03-L02.md) |
| Endpoint lists change during deployments. | Cache discovery and assign one retry owner. | Refresh eligibility outside the call path. Use cached endpoints only within the maximum list age. The retry owner may try a distinct eligible endpoint within the remaining deadline and attempt cap. | Tolerates some transient failures while limiting work. | Cache staleness and retry budget management. | Connection failures grow after endpoint removal or attempts multiply. | Stop using the cached list after its maximum age. Suppress retries when the operation lacks a safe retry contract or spare capacity is exhausted. | [M03-L03](../lessons/M03-L03.md) |
