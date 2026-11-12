---
id: M02-EX1
status: draft
outcomes: [M02-S1]
---

# A global image catalogue request path

The catalogue serves public, versioned image variants and a private saved-items view on the same public host. Requests arrive from several regions. Most browsers support HTTP/2 and some support HTTP/3. The origin routes media and saved-items requests to separate pools. Design for two independent incidents: withdrawal of a public edge endpoint and temporary failure of the media origin.

| Input | Planning assumption |
| --- | --- |
| DNS change | At time zero, authoritative answers change from edge A to edge B. Resolver R1 cached the old answer with a 120 s TTL at time −30 s. Resolver R2 has no cached answer. Assume both can reach authoritative DNS and clients make fresh connection attempts using their resolver's current answer. |
| Peak media traffic | 10,000 requests/s. At warm edges the hit rate is 98%. A cold edge receives 2,000 of these requests per second, all misses before coalescing during the first modeled second. The warm edges still hit 98%. |
| Media origin capacity | 1,000 fetches/s. In the cold interval, there are 80 distinct cold keys, and the path can coalesce concurrent requests for the same key. Each uncoalesced edge miss reaches the origin directly. Assume no intermediate cache hits, extra retries or other origin traffic. |
| Origin failure | An eligible public variant is 20 s past freshness when a 90 s origin outage starts. The catalogue tolerates up to 300 s past freshness for that variant. Some variants are absent from caches. |
| Access | The saved-items view contains user-specific data. The service must protect it from shared cache reuse. |

## M02-EX1

1. Trace DNS to the edge, edge hit and edge miss, and response to the browser. Predict the endpoint for R1 and R2 at time +60 s and say which assumption could change the result.
2. Choose the browser and origin protocols and identify TLS boundaries. Explain where L4 balancing suffices and why the component routing media and saved-items by HTTP path needs L7 visibility.
3. Compare warm and cold media origin load. Propose a way to stay within capacity and state the conditions it relies on. Specify media and private cache policies, replacement, and behavior for stale and absent objects during the origin outage.
4. Identify an observable signal for DNS convergence, overload and freshness. Explain how you would verify the behavior under failure.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M02-S1

Trace DNS-to-origin delivery and justify proxy and CDN choices. Apply [DNS selection](../lessons/M02-L01.md), [protocol behavior](../lessons/M02-L02.md), [L4 and L7 routing](../lessons/M02-L03.md) and [CDN cache controls](../lessons/M02-L04.md).
