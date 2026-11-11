# Independent technical and provenance review — M02-L01

Reviewed 2026-11-11.

## Technical findings

- **M02-L01-TP1 · Minor · Open.** Lesson, **Resolution and record roles**, address-record paragraph. The plural “IPv4 addresses” attached to “An A record” leaves record versus record-set cardinality unclear. State that each A or AAAA resource record contains one address, and a name can have several records of a given type. Link the IPv4 record definition directly as well as the name-record definitions. [RFC 1035 §3.4.1](https://datatracker.ietf.org/doc/html/rfc1035#section-3.4.1) [RFC 3596 §2](https://datatracker.ietf.org/doc/html/rfc3596#section-2)

The resolver and authority roles, alias resolution, caching and optional serve-stale behavior are consistent with the standards. The worked expiry calculations are −240 + 300 = 60 seconds and −30 + 300 = 270 seconds. The companion's expiry is −40 + 120 = 80 seconds, and age at the queried instant is 90 seconds. Its 2:1 selection weighting does not promise a request split because the two resolvers represent unequal cohorts. The vendor routing example leaves health and fallback behavior conditional, which matters because Route 53 may answer from records considered unhealthy when none are healthy. [RFC 1034 §5.3.3](https://datatracker.ietf.org/doc/html/rfc1034#section-5.3.3) [RFC 8767 §4](https://datatracker.ietf.org/doc/html/rfc8767#section-4) [Route 53 weighted routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-weighted.html) [Route 53 health and fallback](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-how-route-53-chooses-records.html)

## Provenance findings

No material provenance finding. The evidence identifies the specific M01-L04 concept and source revision, and the DNS timeline and cohort exercise are independent examples. The lesson cites standards for DNS mechanics and AWS for product policy behavior. No third-party diagram, code, or other asset is reproduced. Attribution identifies Donne Martin, the pinned revision, and CC BY 4.0. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

## Verdict

`ready-for-human-review`
