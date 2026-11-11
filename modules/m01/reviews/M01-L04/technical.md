# M01-L04 technical and provenance review

Checked 2026-11-11. Reviewed the teaching draft, companion, evidence, and pinned curriculum inputs recorded in the verdict.

## Technical findings

- **L04-T1 · minor · Traffic roles and readiness.** A hot or warm standby is described as having “current state.” A ready standby can still lag, as the replication section and six-second recovery point illustrate. Specify a replicated state that is ready to use subject to freshness and lag checks. Distinguish the prepared capacity of AWS hot standby from its reduced-capacity warm standby when using that vendor's terminology. [AWS, Warm standby and Multi-site active/active](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html) · [PostgreSQL 18, §26.2.5 and §26.2.8](https://www.postgresql.org/docs/18/warm-standby.html).
- **L04-T2 · minor · Worked example, 30-second fencing event.** The timeline assumes the controller can verify fencing after losing reachability to the old writer. State the assumed control, such as an independent path that can verify shutdown. Without a verified exclusion mechanism, the sequence must keep write authority disabled on the standby. The text already separates heartbeat detection from fencing. [PostgreSQL 18, §26.3](https://www.postgresql.org/docs/18/warm-standby-failover.html).

The 30-day time budgets are 2,592 s at 99.9% and 259.2 s at 99.99%. The lesson's 65 s interruption leaves 194.2 s. Its RTO and RPO comparisons miss by 5 s and 1 s respectively. The assessment yields 70 s of interruption, 10 s inside the RTO, 2 s beyond the RPO, and 189.2 s of time budget left. The serial 98.01%, parallel 99.99% and shared-dependency 98.9901% examples use correct same-window and independence assumptions. Readiness, enough surviving capacity, routing and correlated failures receive separate treatment. Replication and backups have distinct recovery roles. [AWS, REL13-BP01](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/rel_planning_for_recovery_objective_defined_recovery.html) · [Google SRE, Appendix A](https://sre.google/sre-book/availability-table/) · [AWS, Availability with dependencies](https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/availability-with-dependencies.html) · [AWS, Availability with redundancy](https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/availability-with-redundancy.html).

## Provenance findings

- **L04-P1 · minor · Replication and recovery, PostgreSQL link.** The label cites §26.1 and §26.2, but the linked page only opens §26.1. The evidence includes both destinations. Link directly to §26.2.8 for the synchronous replication discussion. [PostgreSQL 18, §26.2](https://www.postgresql.org/docs/18/warm-standby.html).

The timeline and arithmetic are original. The window is explicitly defined and the figures are derived, with the cited availability table used for the method and comparison. The text does not reproduce vendor diagrams, tables or executable commands. The Primer credit includes author, pinned revision, CC BY 4.0 and a change statement. No other assets or implied endorsement were found. [Primer license at pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt).

Verdict: **ready-for-human-review**.
