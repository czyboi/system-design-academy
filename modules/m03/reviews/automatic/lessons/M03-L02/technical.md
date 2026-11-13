# M03-L02 technical and provenance review

Reviewed 2026-11-12 against draft handoff `7459b0a`. Scope covers the teaching lesson, companion assessment, and claim matrix for SDA-M03-L02.

## Technical findings

| ID | Severity | Status | Location | Evidence and suggested correction |
| --- | --- | --- | --- | --- |
| API-T1 | minor | open | `modules/m03/lessons/M03-L02.md:39,43`, `modules/m03/evidence/M03-L02.md:19` | The server page-size limit bounds items per response. A byte bound also depends on item sizes and representation overhead. Specify the item bound and keep the cursor as the continuation position. The companion already says pagination *can* limit payload size. [Google API Improvement Proposal 158, Guidance](https://google.aip.dev/158#guidance) |
| API-T2 | minor | open | `modules/m03/lessons/M03-L02.md:45`, Compatibility and safe retries | The phrase “scoped to an authenticated caller and payload” could imply that a changed payload creates a different deduplication key. Use authenticated caller and key to look up the operation, then compare the recorded payload to reject mismatches. The export example at line 49 and EX-1 answer already describe the intended behavior. [Amazon Builders’ Library, Same client request ID, different intent](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/#Same_client_request_ID,_different_intent) |

The REST section at lesson lines 25–31 distinguishes server resource state from conversational client context and covers all four uniform interface constraints, layered visibility, cacheability, and optional code on demand. Lines 33–39 describe the outbound and return paths with the remote failure boundary intact. RFC 5531 §4 supports the illustrative model for ONC RPC version 2. The gRPC method shapes are scoped to the gRPC docs, and proto3 wire evolution at line 43 is scoped to the binary format and distinguished from application compatibility. Q2 and Q4 follow the same distinctions. [Fielding, Chapter 5, §§5.1–5.2](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) · [RFC 5531, §4](https://datatracker.ietf.org/doc/html/rfc5531#section-4) · [gRPC Core concepts, Service definition and RPC life cycle](https://grpc.io/docs/what-is-grpc/core-concepts/) · [Proto3 guide, Updating a message type](https://protobuf.dev/programming-guides/proto3/#updating)

Lesson lines 45 and 49–53 and assessment lines 57–63 and 75–79 separate the caller's timeout from the actual outcome. The exercise makes the inventory owner guard the reservation effect atomically with the stable operation ID. The API and inventory keep the identity or tombstone after cached response expiry, and the at-most-once property is explicitly conditioned on retained identities. The example's `202 Accepted` with a status link is consistent with acceptance for processing and allows the client to observe progress. [RFC 9110, §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) · [RFC 9110, §15.3.3](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3) · [Amazon Builders’ Library, Reducing client complexity and Late arriving requests](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) · [gRPC Deadlines](https://grpc.io/docs/guides/deadlines/)

The N1 preview at lesson line 53 and Q3 at assessment lines 43–47 agree with the archived source trace. The failed attempt consumes 40 ms and backoff consumes 20 ms, leaving 240 ms of the initial 300 ms for attempt two. B replies at 120 ms on the original timeline. A create on the same discovery path still requires an unknown-outcome policy. The evidence records the planned update to the canonical trace after M03-L03 review. [Archived M03-L03 worked example](https://github.com/czyboi/system-design-academy/blob/ec753d7bcfd69ad68e5fff260aeb088059e42540/modules/m03/lessons/M03-L03.md#worked-example-stale-endpoint-and-deadline-failure-trace)

## Provenance and rights

The claim matrix gives source and version scope for the cited dissertation, standards, and living vendor documents. The export and reservation examples, interface sketches, and questions are original Academy scenarios. The discovery example is credited to the archived Academy lesson. The lesson credits Donne Martin, the pinned Primer revision, and CC BY 4.0 for topic selection. The reviewed artifacts contain no third-party figures, code, or scenario assets. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt) · [Archived Academy evidence](https://github.com/czyboi/system-design-academy/blob/ec753d7bcfd69ad68e5fff260aeb088059e42540/modules/m03/evidence/M03-L02.md)

## Verdict

`ready-for-human-review`. No blocker or major findings. The two minor findings are wording clarifications.

## Human-feedback technical re-review, 2026-11-13

Reviewed `e805261..fdbe268` for M03-L02 in response to [issue #64](https://github.com/czyboi/system-design-academy/issues/64#issuecomment-6841513179). Scope covers the changed teaching, companion and canonical evidence.

| ID | Severity | Status | Location | Finding and correction | Evidence |
| --- | --- | --- | --- | --- | --- |
| MS02-H-T-API-1 | major | open | `modules/m03/assessments/M03-L02.md:75–77` | The sample says to look up and persist the association without establishing a unique atomic claim before dispatch. Two API instances can observe an absent caller/key pair and independently call inventory with different reservation IDs. Persist one caller/key, input and pending reservation ID atomically before dispatch, and resume pending dispatch using that ID after a restart. Keep inventory's atomic identity/effect update. | [AWS Builders' Library, reducing client complexity](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) |

Caller plus key is the lookup identity and the stored payload is the equivalence check. The teaching paragraph already describes atomic recording of the key and created operation. A 50-item page can contain 5,000 KB of item bodies at the assumed maximum, before envelope overhead. Separate byte limits and an application-level compatibility check make the constraints explicit. [AWS Builders' Library, changed intent](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/#same_client_request_id_different_intent) · [Protocol Buffers, updating a message type](https://protobuf.dev/programming-guides/proto3/#updating)

The exercise and model are original illustrative material. No third-party asset was added. The prior attribution remains in the lesson.

**Human-feedback re-review verdict: `revise`.**

## Human-feedback correction re-review, 2026-11-13

Reviewed `fdbe268..31b2eb0` for the finding below and adjacent regressions.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| MS02-H-T-API-1 | resolved | `modules/m03/assessments/M03-L02.md:75–79` creates one unique caller/key claim and pending reservation ID before dispatch. Concurrent callers use the same durable record, mismatched input is rejected, and a restarted API resumes with the persisted ID. Inventory records that ID atomically with its effect. The answer also retains an identity or tombstone beyond the response cache and preserves the distinction between items and bytes. | [AWS Builders' Library, reducing client complexity and changed intent](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) |

**Correction re-review verdict: `ready-for-human-review`.**
