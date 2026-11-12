---
id: M02-decisions
status: draft
---

# Routing and delivery decisions

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A public service needs regional endpoint selection. | Use authoritative DNS steering. | Return eligible regional endpoints and account for cached records. | Can direct new resolutions across regions. | DNS query volume and uneven migration as caches expire. | New connections still reach a withdrawn address. | The decision must use per-request fields or change instantly. | [M02-L01](../lessons/M02-L01.md) |
| A browser fetches images over a lossy path. | Compare HTTP/2 and HTTP/3 with negotiated fallback. | Multiplex exchanges over TCP or over QUIC streams. | Can reduce cross-stream loss blocking with QUIC. | Client/network support and transport observability. | Connection failures or unexpectedly high fallback rates. | The edge or client cannot support the alternative reliably. | [M02-L02](../lessons/M02-L02.md) |
| Two backend pools share a public host. | Route at L7. | Terminate TLS at the routing boundary and select by HTTP path. | Keeps one client endpoint while separating backend work. | Parsing, certificates and proxy capacity. | Ingress CPU or queueing rises while backends are idle. | An equivalent pool needs only flow-based selection. | [M02-L03](../lessons/M02-L03.md) |
| Demand for public images varies by region. | Use pull caching with a protected origin. | Fetch misses, coalesce where supported and cap origin requests. | Limits repeated origin work after warmup. | Cold edges and extra capacity management. | Cold misses overload the origin. | The responses are private or the cold-start origin cost is unacceptable. | [M02-L04](../lessons/M02-L04.md) |
| Public image bytes change. | Publish a new versioned variant path. | Keep each version's bytes under its own cache identity and update references. | Allows long freshness for immutable variants. | Referring metadata needs its own lifecycle. | Clients keep reading old metadata or variant keys collide. | Revocation demands immediate withdrawal and the old URL remains publicly accessible. | [M02-L04](../lessons/M02-L04.md) |
