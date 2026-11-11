# Independent technical and provenance review — M02 synthesis

Reviewed 2026-11-11.

## Technical findings

- **M02-INT-TP1 · Note · Open.** Reference solution, **Cache behavior and origin capacity**, saved-items paragraph. The end-to-end shared-storage bypass and two-user isolation check are sound. The example could name its origin policy explicitly, such as `Cache-Control: private, no-store` for this sensitive response, alongside the cache-bypass configuration. The header communicates intent and the edge settings enforce the route's shared-storage policy. [RFC 9111 §§5.2.2.5 and 5.2.2.7](https://datatracker.ietf.org/doc/html/rfc9111#section-5.2.2) [CloudFront minimum TTL caveat](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache-key-understand-cache-policy.html)

The authoritative change and R1's cached record have distinct lifetimes. R1 expires at −30 + 120 = +90 s and supplies A at +60 s; uncached R2 obtains B. The solution conditions serving expired DNS data on failed refresh and keeps the DNS lookup, browser connection, edge and encrypted origin connection separate. The L4 stage can select equivalent ingress instances by flow, while the path-specific choice needs HTTP visibility. HTTP/3 uses QUIC with TCP-based HTTP fallback when QUIC connectivity fails. [RFC 1034 §5.3.3](https://datatracker.ietf.org/doc/html/rfc1034#section-5.3.3) [RFC 8767 §§4–5](https://datatracker.ietf.org/doc/html/rfc8767#section-4) [RFC 9113 §3.2](https://datatracker.ietf.org/doc/html/rfc9113#section-3.2) [RFC 9114 §3.1](https://datatracker.ietf.org/doc/html/rfc9114#section-3.1)

Warm origin demand is 10,000 × 0.02 = 200 fetches/s. The specified cold interval yields 8,000 × 0.02 + 2,000 = 2,160 fetches/s, above capacity of 1,000. The conditional collapsed total of 80 + 160 = 240 fetches/s is valid if each cold key initiates at most one fetch and the 160 warm misses are the other work. The text calls out the coalescing domain and concurrent arrival assumptions, then caps actual rate and concurrency. The eligible stale public variant reaches 20 + 90 = 110 s past freshness, inside the 300 s tolerance. A cold miss has no stale candidate and the private route bypasses stale fallback. [RFC 9111 §§4–4.2](https://datatracker.ietf.org/doc/html/rfc9111#section-4) [RFC 5861 §4](https://datatracker.ietf.org/doc/html/rfc5861#section-4)

## Provenance findings

No material provenance finding. The brief labels the traffic, cache and failure inputs as scenario assumptions. The solution uses IETF specifications for protocol behavior and official CloudFront documentation for a versioned-URL example. The evidence ledger scopes provider behavior. The synthesis reproduces no third-party code, diagrams, benchmarks or other assets.

## Verdict

`ready-for-human-review`
