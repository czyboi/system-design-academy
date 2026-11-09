---
id: DB-07
title: Database Availability, Backup and Recovery
status: draft
level: intermediate
estimated_time: 90 minutes
prerequisites: [DB-04]
source_review_date: 2026-11-09
reviewer: pending
---

# DB-07 — Database Availability, Backup and Recovery

## Learning outcomes

- Distinguish high availability (HA), backup and disaster recovery (DR).
- Define recovery point objective (RPO) and recovery time objective (RTO).
- Explain why backup success is not proven until restore is tested.
- Design a recovery approach that covers accidental deletion, corruption and regional failure.

## 1. Three different protections

- **Replication:** keeps another node relatively current and may support failover/read scaling.
- **Backup:** provides a recoverable copy from an earlier point in time.
- **Disaster recovery:** the people, systems, procedures and resources needed to restore service after a major incident.

A replicated deletion can propagate to replicas. A corrupted write can replicate. Therefore, replicas do not replace backups.

## 2. RPO and RTO

- **RPO:** maximum acceptable data loss measured in time (how far back recovery may need to go).
- **RTO:** target time to restore service after disruption.

Example: RPO 5 minutes means recovery should lose no more than roughly five minutes of committed business data under the defined scenario. RTO 60 minutes means the service target is to resume within an hour. These are business requirements, not settings that a database automatically guarantees.

## 3. Backup strategies

Common components include full/base backups, incremental backups, transaction-log/WAL/binlog archiving, snapshots, retention policies and offsite/isolated copies. Exact mechanics vary by database and managed service. Point-in-time recovery requires a valid base backup plus an unbroken required log sequence and correct restore procedure.

## 4. Restore testing

A credible backup program regularly tests:
- restore into an isolated environment;
- data integrity and application-level invariants;
- measured time to restore;
- ability to recover to a requested point in time;
- access to credentials, encryption keys and network configuration;
- runbook clarity and owner availability.

A successful backup job is only one input. A successful restore test is stronger evidence.

## 5. HA and DR design

Define failure scenarios separately: process crash, VM/host loss, AZ/zone loss, region loss, operator error, logical corruption, credential compromise. The recovery plan should specify detection, promotion/restore authority, fencing, endpoint changes, data-loss expectations, communication and reconciliation.

## Exercise

A commerce database has target RPO 5 minutes and RTO 45 minutes. Propose a high-level design with primary/standby, backups and log archiving. Explain which failure scenarios are covered and which need a separate regional DR design. Include one restore drill and its success criteria.

## Knowledge check

1. Why does replication not protect against accidental deletion?
2. What is the difference between RPO and RTO?
3. Why is a backup that has never been restored weak evidence?
4. Which additional secrets/configuration may be needed in a restore?
5. Does a standby replica guarantee a zero-data-loss failover? Explain.

## Answer guide

1. The delete can be faithfully copied to the standby/replica; replicas generally mirror current state rather than preserve a historical clean copy.
2. RPO expresses acceptable data-loss window; RTO expresses target time to restore service.
3. The backup may be incomplete, corrupted, inaccessible, missing required logs/keys, or too slow to restore within the target.
4. Encryption keys, credentials, network/DNS configuration, certificates, schema/migration artifacts, application config and operational runbooks.
5. No. Asynchronous replication can lag; synchronous guarantees depend on exact configuration, failure model and what acknowledgment means. Even synchronous designs need documented failover constraints.


## References

- PostgreSQL 18 — pg_basebackup: https://www.postgresql.org/docs/current/app-pgbasebackup.html
- PostgreSQL 18 — High Availability: https://www.postgresql.org/docs/current/high-availability.html
- PostgreSQL 18 — Continuous Archiving and Point-in-Time Recovery: https://www.postgresql.org/docs/current/continuous-archiving.html
- MySQL 8.4 — Replication: https://dev.mysql.com/doc/refman/8.4/en/replication.html
- Amazon DynamoDB — PITR best practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
