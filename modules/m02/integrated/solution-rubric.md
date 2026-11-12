---
id: M02-EX1-solution
status: draft
---

# Reference request path and rubric

## DNS, connections and routing

The browser asks its recursive resolver for the public hostname. On a miss, the resolver follows referrals and obtains the authoritative answer. In the DNS incident, R1's old answer expires at +90 s, so at +60 s it still supplies edge A. R2 queries and gets edge B. Existing connections, additional application caching, or a configured serve-stale fallback when refresh fails can produce a different observed migration timeline. Confirm which destination address new connections actually use. [RFC 1034 §5.3.3](https://datatracker.ietf.org/doc/html/rfc1034#section-5.3.3), [RFC 8767 §4](https://datatracker.ietf.org/doc/html/rfc8767#section-4)

The browser connects to the edge using HTTP/3 over QUIC when negotiated and reachable, or HTTP/2 over TLS and TCP for capable clients. The edge terminates browser TLS. It serves an eligible cached response on a hit. On a miss or for private traffic, the edge makes a separate encrypted connection to the origin ingress, for example pooled HTTP/2 when supported. The ingress terminates that TLS session and selects the media or saved-items pool by HTTP path. Backends and network trust boundaries have explicit encryption and authentication policies. The edge returns the response on the browser connection. [RFC 9113 §5](https://datatracker.ietf.org/doc/html/rfc9113#section-5), [RFC 9114 §2](https://datatracker.ietf.org/doc/html/rfc9114#section-2)

L4 balancing can distribute connections across equivalent ingress replicas without seeing HTTP. L7 selection needs the method, host or path after suitable HTTP/TLS processing. Use redundant ingress capacity and verify that removing one ingress still leaves enough capacity. Connection health alone cannot show that either application pool can handle requests.

## Cache behavior and origin capacity

Warm origin demand without coalescing is 10,000 × 0.02 = **200 fetches/s**. In the cold interval it is 8,000 × 0.02 + 2,000 = **2,160 fetches/s**. If all cold requests for each key share an in-flight fetch through one coalescing domain, and none initiates a second origin fetch within that interval, there are at most 80 cold fetches plus 160 warm misses, or **240 fetches/s** under that condition. Measure the actual origin request rate because independent edge shards and nonoverlapping misses can defeat that assumption. Put a bounded rate and concurrency limit ahead of the origin. Prefill only the most likely keys or ramp traffic when warming a new edge.

For public images, include the version and variant in the path so bytes for different sizes or formats have distinct keys. Store and serve with an explicit freshness policy. Publish a new path for replacement bytes, and give the referring catalogue metadata its own freshness and update policy. Invalidation can help when an old URL must stop being served at a controlled edge. Test how clients and intermediary caches behave when old links persist. [RFC 9111 §§4.1–4.2](https://datatracker.ietf.org/doc/html/rfc9111#section-4.1), [CloudFront, updating existing objects](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/UpdatingExistingObjects.html)

With an explicit and supported `stale-if-error` policy allowing 300 seconds beyond freshness expiry, a cached public variant 20 s past freshness at the start of the 90 s outage can remain eligible throughout, reaching 110 s past freshness. A miss has no saved response to serve. Use a bounded failure or an authorized alternative origin. The saved-items view sends `Cache-Control: private, no-store` and uses a route that bypasses shared storage and stale fallback. Configure that path and origin headers together and verify with two distinct user sessions. [RFC 5861 §4](https://datatracker.ietf.org/doc/html/rfc5861#section-4), [RFC 9111 §5.2.2](https://datatracker.ietf.org/doc/html/rfc9111#section-5.2.2)

In a failure drill, record the IP used by new connections, origin fetches per second and the version served. For a stale response, compare its reported `Age` with the applicable freshness lifetime and confirm the edge's stale-on-error indicator.

## Self-evaluation

Award 2 for complete reasoning, 1 for a correct but incomplete argument and 0 for a missing or contradictory argument.

| Criterion | Evidence for full credit |
| --- | --- |
| DNS trace | Correct R1/R2 outcomes and time math, with a concrete source of divergence from the DNS timeline. |
| Request path | Separates DNS, transport, TLS and HTTP. Traces hit/miss and private traffic and justifies the L4/L7 placement. |
| Capacity and freshness | Computes both origin rates and bounds overload. Explains variant keys, replacement and distinct policies for eligible stale, cold and private traffic. |
| Verification | Names destination, origin and freshness observations, tests a cold edge and an origin outage, and verifies private response isolation. |

Other protocols, routing and cache designs can earn full credit when their paths and assumptions meet the requirements. A design that exposes a private response through a shared cache fails the access requirement.
