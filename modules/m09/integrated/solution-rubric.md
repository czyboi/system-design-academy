---
id: M09-EX1-solution
status: draft
---

# M09 integrated reference solution and self-evaluation rubric

## Trace the exposed data boundary

```text
Browser --HTTPS, verified proxy--> Reverse proxy
  --authenticated encrypted hop, validated delegated token--> Statement API
Statement API --TLS, verified DB server, limited API principal---------> SQL database
Statement API --authenticated producer, protected enqueue-------------> Durable job queue
Durable job queue --authenticated consumer, protected delivery--------> Report worker
Report worker --TLS, verified DB server, separate limited principal---> SQL database
Report worker --TLS, verified store; scoped worker write------------> Result store
Statement API --TLS, verified store; scoped API read----------------> Result store
Statement API --fresh requester/tenant/action authorization-----------> Browser (via proxy)
Statement API --coordinator lease/epoch--> Storage gateway --fenced write--> Projection
```

The proxy strips untrusted identity headers, authenticates its forwarding workload and forwards the user-delegated token over an authenticated channel. The API validates signature, issuer, audience, expiry and configured permissions; only then can it derive Bo's issuer-scoped subject. A valid `statements:read` claim is insufficient for statement `s-9`: Bo's trusted tenant membership is C, the row is D, so the API denies without leaking record content. If membership cannot be established, do not fall back to a cached “allow all” or to the database's broad service privileges. Bind statement ID and tenant C into a tenant-constrained parameterized query, or enforce the equivalent predicate in a trusted database policy; the API still needs an object authorization decision. The API verifies the database endpoint, negotiates the required encrypted transport and authenticates using its own restricted principal; if required verification fails, it issues no query. [M09-L01](../lessons/M09-L01.md).

For the **asynchronous path**, the API first verifies the delegated user's permission to request a tenant-C report; the broad `statements:read` scope alone does not grant another tenant's records. Only its authenticated producer principal can enqueue a job. It derives the trusted tenant from policy, not an arbitrary request field, and persists a schema-validated, integrity-protected envelope `{job_id, issuer_scoped_subject_ref, tenant_id=C, action=generate_report, bounded_selection}`; the queue carries neither the raw bearer token nor statement contents. Broker access controls allow only the producer to enqueue and the intended worker principal to consume over authenticated, encrypted channels. On consumption, reject forged/altered, expired or malformed jobs; re-resolve the requester and current tenant/action/record permissions **at execution** and fail closed on a missing or failed membership lookup. If a membership is revoked during queue wait, the worker must not reuse the enqueue authorization as permanent authority. Read with a tenant- and selection-constrained predicate (or an equivalent trusted row-level policy); verify actual record ownership rather than trusting the tenant label in the job. Recheck the retrieving caller's present authorization before releasing the result, even if the job ID is known. [M09-L01](../lessons/M09-L01.md).

The worker opens its **own TLS connection** with verification of the intended database server, authenticating with a **worker-specific, minimally privileged DB account** restricted to its report read paths; it does not inherit the API's credential or use a cross-tenant administrator identity. Failure of TLS identity, authorization or the DB policy check stops the job and yields a non-disclosing failure. For both the worker-to-result-store and API-to-result-store connections, require TLS and verify the intended result-store service identity before transferring report data. Authenticate the worker and API with separate workload principals: authorize the worker only to write the intended tenant/job result and the API only to read the intended tenant/job result. If transport setup, peer verification, workload authentication or the relevant permission check fails, stop without transferring the result. These workload permissions do not replace the fresh end-user authorization at release. Keep JWTs, sensitive report rows and credentials out of job payloads, error messages and logs. Worker and API workload identities are separate from Bo's delegated user identity. These are application-level enforcement choices, supported by [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request) and [OWASP Database Security](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html#implementing-transport-layer-protection), and [OWASP TLS guidance](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-tls-for-all-pages) and [correct domain names](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-correct-domain-names); these are not guarantees provided by a queue.

A notes mutation authenticated by cookies needs a server-validated anti-CSRF mechanism appropriate to the session, input validation to business bounds, and *output-context encoding* when rendering user-supplied notes. Parameter binding prevents SQL syntax injection, not XSS or missing authorization. Encryption at rest does not replace per-record access checks, and a TLS connection terminating at the proxy does not encrypt the next hop unless explicitly configured.

## Diagnose without hiding failed originals

Sum **exclusive** intervals only: 40 + 50 + 760 + 50 + 80 + 160 + 40 + 20 = **1,200 ms**. The API's inclusive span is a parent and is not another interval. Queue wait of 760 ms is the largest observed component. A worker-capacity hypothesis would predict increasing oldest-job age, busy workers and reduced wait after a controlled serialization/worker-capacity intervention at the same offered traffic and request mix. It can be disproved if queue age does not respond or if increased worker concurrency only saturates the database. A downstream-database hypothesis would predict rising DB service/wait and network-call durations, more query execution or lock waits and correlated queue growth; it weakens if DB evidence remains at baseline and worker CPU profiles explain most queue delay. Use service metrics over the cohort, not one sampled trace, to distinguish. [M09-L02](../lessons/M09-L02.md).

For the five-minute first-ingress cohort, only **930/1,000 = 93%** of original valid requests reach client-validated receipt within two seconds of first ingress; the **99% target fails**. Excluding 20 rejected, 20 timed-out, 10 failed or 20 late requests makes a misleading success-biased statistic. The numerator is reconciled to first-ingress and validated-client-receipt IDs. Success-only p95 is diagnostic, not the original-operation availability SLI. A missing client receipt is not proven success from an edge send event.

## Fence the protected resource, not just the lease

W1 may hold a local “leader” flag after its coordinator lease expires. W2 acquires epoch 42 from B+C, then **must durably install fence 42 at the projection gateway**. Only after confirmation can it write. The gateway serializes the fence with all tenant mutations and rejects W1's later epoch-41 command. If the fence response is unknown, W2 stops and reconciles/retries installation idempotently; leadership is not proof of an installed storage barrier. An old epoch-41 command that arrives before fence 42 installs is a stated residual risk of this model, so the guarantee is scoped to no old writes *after installation* and no overlap with W2. Idempotency and version preconditions are still needed against duplicate epoch-42 updates. [M09-L03](../lessons/M09-L03.md).

A alone lacks two votes; the B+C majority may progress subject to protocol and available storage. If gateway or coordinator majority is unavailable, prefer an explicit failure/retry policy over an uncoordinated second writer. Losing a common identity provider or shared network could disable both regions even with three separate machines. A surviving quorum does not prove the reporting database is readable, that a backup restores to the RPO target, or that a browser receives correct output.

## Test an assertion that could be false

Run a controlled mixed workload in a safe environment while instrumenting original request IDs, client validated receipts, queue oldest age, worker profiles, database waits, fence epochs, stale-write rejects and recovery markers. Pause W1 across expiry, admit W2 only after stored fence 42 is acknowledged, and inject W1's late command: verify no stale mutation committed in the storage audit trail. Inject a dropped fence acknowledgment: W2 must not write before reconciliation. Partition A from B+C; observe minority rejection and majority behavior. Then remove a shared dependency, restore a database backup in an isolated environment and verify recoverable data point, usable read/write service and measured restoration time from declared incident boundaries. Measure the original report cohort through its original deadlines during these drills; do not discard rejected/late requests. [M09-L02](../lessons/M09-L02.md), [M09-L03](../lessons/M09-L03.md).

## Self-evaluation rubric (12 points)

| Criterion | Points | Evidence for full credit |
| --- | ---: | --- |
| Authorization and encrypted boundaries | 3 | Protected synchronous and queue/worker/DB hops; TLS and intended result-store peer verification on both worker and API connections, with distinct authenticated principals scoped to the intended tenant/job write or read and no transfer on failed checks; fresh end-user authorization at release; object/tenant checks at enqueue and execution, tamper-resistant job envelope, fail-closed lookup/revocation, safe logs/results, tenant-denied record and bounded notes defenses |
| Diagnostic reconstruction | 3 | Correct 1,200 ms exclusive total, 760 ms queue interval and two falsifiable hypotheses; five-minute original-valid first-ingress cohort through client-validated receipt within two seconds, with late, rejected, timed-out and failed originals retained; 930/1,000 = 93% misses the 99% target; distinguish admitted-success latency from the original-operation SLI |
| Coordination invariant | 3 | Quorum placement, confirmed durable fence before W2, stale W1 rejection, unacknowledged-fence stop and pre-install caveat |
| Correlated risk and recovery evidence | 3 | At least two shared dependencies, backup versus election distinction and an executable-in-principle drill with outcome evidence |

Equivalent architectures may receive full credit if they defend the same record/operation boundaries and demonstrate the invariant. Do not award coordination correctness points merely for “use ZooKeeper” or SLO points for an admitted-only percentile.

## Synthesis outcome mapping

**M09-S1:** justify security controls, identify diagnostic evidence and defend coordination under a stale owner. The integrated **M09-EX1** draws on **M09-L01-LO2** (control choice), **M09-L02-LO1** (trace/model) and **M09-L03-LO2** (coordination choices). This exercise does **not** replace the three separate lesson companions that evaluate all six LO1/LO2 outcomes.
