# M09-L01 technical and provenance review

Round 0 reviewed the lesson, companion assessment and evidence at draft commit `e6775ee` on 2026-11-15.

## Technical findings

| ID | Severity | Status | Location | Finding and suggested fix | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M09-L01-T1 | major | open | `modules/m09/lessons/M09-L01.md:21,26,34,59`, worked request and threat table. `modules/m09/assessments/M09-L01.md:62–69`, EX-1 solution and rubric. | The trace identifies three network boundaries. The concrete recommendation covers “both hops,” which leaves the API-to-database boundary without an explicit encrypted channel and verified server identity, although it carries query parameters, credentials or results. Extend the worked read and threat table to cover that third link. Name TLS with verification of the intended database endpoint, the reporting service’s separately scoped database principal, and failure of connection setup when required transport or peer verification fails. Apply the same contract to the EX-1 sample, grading and evidence; keep vendor configuration outside this generic case. | [OWASP Database Security, Implementing Transport Layer Protection and Configuring Secure Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html#implementing-transport-layer-protection), [NIST SP 800-207 §2.1 tenet 2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf#page=15) |
| M09-L01-T2 | minor | open | `modules/m09/lessons/M09-L01.md:23–25`, identity trace. `modules/m09/assessments/M09-L01.md:34,62`, Q2 and EX-1. | The proxy forwards identity assertions and the API validates a JWT, but the example leaves the source of Ada’s canonical user identity implicit when both are present. State which credential establishes the user and why. In the JWT path, use the validated, issuer-scoped user subject from the configured user-delegated access-token profile for policy checks; treat proxy authentication as workload identity. In Q2’s header-authenticated variant, specify the proxy derives the assertion from its own verified caller authentication and delivers it across a trusted channel. If the lesson elects to name RFC 9068 specifically, include its access-token type check and keep scope as an application permission requirement. | [IETF RFC 9700 §4.13, TLS-terminating reverse proxies](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.13), [IETF RFC 9068 §2.2 and §4, subject and validation](https://www.rfc-editor.org/rfc/rfc9068.html#section-4), [IETF RFC 8725 §3.12, mutually exclusive JWT validation](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.12) |

For the stated membership assumptions, binding tenant A with `r-42` or tenant C with `s-9` excludes the other tenant's record, and an unavailable policy service yields denial. The lesson and exercise consistently omit an immediate-revocation timing promise. The bound SQL separates values from query syntax and is labelled conceptual. The browser example distinguishes HTML text encoding, authorization and a server-validated synchronizer token for a cookie-authenticated mutation. The backup example correctly depends on separate key access. [OWASP per-request authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request), [SQL parameter binding](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html#defense-option-1-prepared-statements-with-parameterized-queries), [XSS output encoding](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#output-encoding), [CSRF synchronizer token pattern](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#synchronizer-token-pattern), [Cryptographic Storage key separation](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#separation-of-keys-and-data).

## Provenance

| Material | Role and use |
| --- | --- |
| Donne Martin, System Design Primer at `ae9bbd7` | Topic map for security, encryption, injection, XSS and least privilege. The narrative, recorded identifiers and assessment use original examples and prose. [Pinned topic map](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| IETF RFCs, NIST SP 800-207 and OWASP Cheat Sheet Series | Factual references for protocol requirements and security guidance. The draft makes no product-specific configuration claim or financial-compliance claim. The identifiers, roles and sample query are original scenario material. [RFC 8446 §1](https://www.rfc-editor.org/rfc/rfc8446.html#section-1), [RFC 9700 §2.3](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3), [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final), [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) |
| Illustrations, code and data | Original conceptual SQL and synthetic identifiers. The review inspected the SQL as an illustrative parameterized statement. The package imports no external code, visuals, financial data or substantial passages. |

The reverse-proxy and database transport evidence requested in T1 and the token-profile source requested in T2 delimit factual applicability. No third-party asset or adaptation rights issue was identified.

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the corrected lesson, companion and evidence at draft commit `dce189b` on 2026-11-15.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M09-L01-T1 | resolved | The worked read and decision table now protect all three network hops. The API requires TLS, verifies the intended database server and logs in as a distinct restricted database principal. Failed protection or verification ends setup before issuing the query. EX-1 asks for these conditions, shows the failure behavior and requires it for full credit. Evidence C6 scopes these requirements to generic SQL database guidance and the scenario contract. Locations are lesson lines 26, 34 and 61, assessment lines 20, 62 and 69, and evidence line 12. | [OWASP Database Security, Implementing Transport Layer Protection](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html#implementing-transport-layer-protection), [NIST SP 800-207 §2.1 tenet 2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf#page=15) |
| M09-L01-T2 | resolved | The API derives the user from the validated issuer-scoped subject under the assumed user-delegated JWT profile. The protected internal hop authenticates the proxy workload. The separately stated Q2 variant requires the proxy to strip supplied identity headers, verify caller authentication, derive its user assertion and send it through an authenticated channel. The API retains object authorization in both scenarios. EX-1 and its rubric distinguish the two identities. Evidence C7 identifies RFC 9068 as a source for the user-delegated subject pattern and scopes the teaching example to its assumed profile. Locations are lesson lines 21–25 and 36, assessment lines 18–20, 32–34, 62 and 68, and evidence line 13. | [IETF RFC 9068 §2.2, access-token subject](https://www.rfc-editor.org/rfc/rfc9068.html#section-2.2), [IETF RFC 7519 §4.1.2, subject scope](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.2), [IETF RFC 9700 §4.13, protected proxy assertions](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.13) |

The revised trace still denies Ada and Bo access to the other tenant's record and stops if membership cannot be established. The transport change preserves separation of database authentication, statement parameter binding and record authorization. The scoped changes preserve backup, browser and secret-handling coverage and introduce no third-party assets.

### Verdict

`ready-for-human-review`
