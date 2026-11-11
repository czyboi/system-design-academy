# Technical and provenance review for M03-L03

Reviewed 2026-11-11 by the orchestrator, independently of the lesson author and teaching reviewer.

## Technical findings

- D03-T1, minor. The worked example says to query operation status before repeating a timed-out write. A status result must positively establish whether the original operation took effect or whether the service permits safe reissue. A stale absence by itself cannot rule out a committed charge. The lesson and assessment already require an explicit durable deduplication or status contract, so this is a precision point. [AWS Builders' Library, retries and side effects](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- The 300 ms example leaves 240 ms at the second attempt and 180 ms at response. The separate exercise's 3 × 2 upstream cap follows from the stated total-attempt counts. The lesson separates failure observation, registry update, consumer refresh, and local attempt policy.
- Consul's registration endpoint accepts service and health data. The health query's passing filter is explicit. etcd expiry deletes leased keys and ZooKeeper ephemeral nodes follow session lifetime. SRV provides target, port, priority and weight, and the lesson qualifies client support. [Consul registration](https://developer.hashicorp.com/consul/api-docs/agent/service#register-service), [Consul health](https://developer.hashicorp.com/consul/api-docs/health#list-nodes-for-service), [etcd 3.6 lease API](https://etcd.io/docs/v3.6/learning/api/#lease-api), [ZooKeeper 3.9.4 ephemeral nodes](https://zookeeper.apache.org/doc/r3.9.4/zookeeperProgrammers.html#Ephemeral+Nodes), [RFC 2782](https://datatracker.ietf.org/doc/html/rfc2782)

## Provenance and rights findings

The evidence distinguishes product documentation from illustrative mechanisms and settings. The two scenarios and their inputs are original. Primer attribution includes author, repository, pinned revision, license, and change statement. The pair redistributes no third-party assets.

## Verdict

ready-for-human-review.
