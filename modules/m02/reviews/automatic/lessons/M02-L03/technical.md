# M02-L03 technical and provenance review

Reviewed 2026-11-12 at draft handoff `2171a9d`. Scope covers the canonical load balancing and reverse proxies lesson, assessment and evidence pack.

## Findings

| ID | Severity | Status | Location | Evidence and suggested change |
| --- | --- | --- | --- | --- |
| M02-L03-T1 | note | optional | `modules/m02/lessons/M02-L03.md:31`, weighted selection | The capacity example is sound. For precision, say that configured weights assign larger shares, with capacity as one input to choosing weights. The algorithm does not need to discover backend capacity. [NGINX upstream server weights](https://nginx.org/en/docs/http/ngx_http_upstream_module.html#server) |

## Technical checks

- The lesson separates address and port translation from connection proxying. An HTTP path is application-layer information. When the HTTP message is encrypted, the routing component needs access to its decrypted form. The lesson and Q4 distinguish the ingress termination and backend trust boundaries. [RFC 3022 §2.2](https://www.rfc-editor.org/rfc/rfc3022.html#section-2.2) · [NGINX stream proxy](https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html) · [ALB path conditions](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/rule-condition-types.html#path-conditions)
- The selection policies distinguish configured weights and randomness from connection count as a load signal. Health eligibility can lag or miss failures. Cookie affinity influences routing and does not reconstruct a lost local session, as Q2 tests. The shared store and redundant ingress scenarios state the remaining reachability and common dependencies. [NGINX upstream methods](https://nginx.org/en/docs/http/ngx_http_upstream_module.html#random) · [ALB duration-based stickiness](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html#duration-based-stickiness)
- The proxy responsibilities accurately describe work transferred to ingress. Buffering, caching and compression carry resource or freshness costs. The forwarded-address guidance and Q6 correctly require a trusted boundary and account for shared source IPs. The modeled pool arithmetic yields `12 × 20 = 240` in the lesson and `6 × 30 = 180` against a 165-connection web budget in EX-1. Capping each of the six pools at 27 yields 162 and leaves three unused. [NGINX proxy buffering](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffering) · [NGINX gzip](https://nginx.org/en/docs/http/ngx_http_gzip_module.html) · [NGINX connection limits](https://nginx.org/en/docs/http/ngx_http_limit_conn_module.html) · [RFC 7239 §8.1](https://www.rfc-editor.org/rfc/rfc7239.html#section-8.1)
- The worked read retry uses an eligible alternate and a bounded deadline before a partial response is sent. The write trace leaves commit unknown after a timeout. The ingress avoids automatic non-idempotent replay. The application-aware caller reuses the operation ID and input only when its deduplication contract and time budget cover the retry. Q1, Q3 and the EX-1 sample answer follow those boundaries. [NGINX upstream retry behavior](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_next_upstream) · [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

## Provenance and assets

The evidence pack distinguishes general protocol behavior from NGINX and ALB capabilities. Academy scenarios and arithmetic are illustrative. The attribution credits Donne Martin and identifies the pinned Primer revision for topic selection. The canonical draft identifies its archived Academy predecessor and links the earlier evidence matrix. The lesson and assessment contain no reproduced third-party diagrams, code or other assets. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

**Verdict: ready-for-human-review.** The reviewed package has no open technical or provenance finding requiring a correction round.

## Human-feedback technical re-review, 2026-11-13

Reviewed `e805261..fdbe268` for M02-L03 in response to [issue #64](https://github.com/czyboi/system-design-academy/issues/64#issuecomment-6841513179). Scope covers the changed teaching, companion and canonical evidence.

No open technical or provenance findings in the changed scope.

`modules/m02/assessments/M02-L03.md:74–78` accounts for 165 connections after the reserve, 14 overlapping pools, and 154 connections under the 11-per-instance proposal. The 11 headroom assumes the two failed pools already obey the smaller limit. The answer distinguishes path selection at the TLS termination boundary, local session loss, and an ambiguous purchase result. Same-ID replay depends on the durable contract and remaining deadline. [NGINX HTTP proxy, proxy_pass](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass) · [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

The exercise and model are original illustrative material. No third-party asset was added. The prior attribution remains in the lesson.

**Human-feedback re-review verdict: `ready-for-human-review`.**
