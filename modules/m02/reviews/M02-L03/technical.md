# Independent technical and provenance review — M02-L03

Reviewed 2026-11-11.

## Technical findings

- **M02-L03-TP1 · Minor · Open.** Lesson, **Worked example**, step 3, and companion **Answer key / rubric**. The checkout branch calls for application-defined idempotency but leaves the actor that retries implicit. In an ingress lesson this can suggest that a generic proxy can infer the contract. Specify that the proxy does not automatically replay a request whose semantics are non-idempotent or unknown. The application-aware caller can retry an operation known to be idempotent under the documented contract, reusing its operation identity within the deadline. RFC 9110 §9.2.2 distinguishes the obligations of clients and proxies. [HTTP Semantics, idempotent methods](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.2)

The read retry is conditional on response progress, budget and selection of a healthy alternate, and preserves the user's session only when its shared dependency is reachable. The NGINX example supports the response-progress constraint. The L4 and L7 roles, affinity and health-check limitations, ingress redundancy and transfer exercise are technically consistent. The connection-budget calculations check out at 12 × 20 = 240, 6 × 30 = 180, 200 − 35 = 165, and 6 × 27 = 162. [NGINX proxy retry controls](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_next_upstream) [NGINX stream proxy](https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html) [RFC 3022 §2.2](https://www.rfc-editor.org/rfc/rfc3022.html#section-2.2) [ALB sticky sessions](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html#sticky-sessions)

## Provenance findings

- **M02-L03-PP1 · Note · Open.** Lesson, **Routing and backend selection**, algorithm paragraph. The NGINX load-balancing overview supports round robin, least connections and weighting. Add the upstream module's direct `random` section when citing the full list. [NGINX upstream module, random](https://nginx.org/en/docs/http/ngx_http_upstream_module.html#random)

The cited NGINX modules and ALB documentation describe product examples, with no cross-product defaults asserted. The illustrative scenarios, rubrics and capacity inputs are original. No third-party diagrams, code or other assets are reproduced. The attribution identifies Donne Martin and CC BY 4.0. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

## Verdict

`ready-for-human-review`
