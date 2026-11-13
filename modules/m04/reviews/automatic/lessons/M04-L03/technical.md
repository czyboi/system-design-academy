# M04-L03 technical and provenance review

Round 0 reviewed the lesson, companion and evidence at draft commit `ac46917` on 2026-11-13.

## Technical findings

| ID | Severity | Status | Location | Finding and correction | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M04-L03-T1 | major | open | Lesson line 37, Move data with one writable owner. Companion lines 20, 58 and 64–70, EX-1 and Safe migration. | The cutover describes fencing and a new epoch, but leaves the failure boundary at “before the switch” undefined. If the directory update commits and its reply is lost, treating the timeout as a pre-switch failure and reopening the source can conflict with a destination that already opened. State which durable compare-and-set makes the new epoch authoritative, require each shard to enforce its writable epoch at write admission with the drain covering already admitted work, and keep the source fenced while the publication result is unknown. Show a stale request being rejected, then refreshed at the router. A proven pre-publication abort may restore the source only after excluding delayed target activation. After publication, re-establish source ownership only through a newer fenced transition that preserves target writes. Carry the same failure rule into the companion solution and rubric. | [Vitess 24 Reshard, SwitchTraffic and ReverseTraffic](https://vitess.io/docs/24.0/reference/vreplication/reshard/#switchtraffic), [write cutover timeout and catch-up](https://vitess.io/docs/24.0/reference/vreplication/reshard/#--timeout), [VReplication overview, cutover journaling and routing](https://vitess.io/docs/24.0/reference/vreplication/vreplication/) |
| M04-L03-T2 | minor | open | Lesson lines 31–33 and evidence Ring row. | The lesson uses a clear inclusive token boundary and the example is arithmetically correct. The cited Dynamo partitioning prose describes moving to a larger token, while its replication section writes right-inclusive ranges. Label equality handling as this teaching ring's explicit convention, and cite the paper for successor routing and virtual nodes rather than suggesting the paper defines the exercise's tie behavior. | [Dynamo §§4.2–4.3 and Figure 2](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf#page=5) |

The lesson distinguishes dividing by ownership from dividing a logical dataset by rows. The dashboard's independent reads and the tenant list's fan-out follow from those choices. Hashing only the tenant ID cannot distribute one hot tenant across owners. Bucketed ticket keys can distribute independent writes when the buckets are placed across owners, with no promise of even request rates. The lesson's ring moves only `(20, 35]` from B to D under its stated convention. The exercise correctly moves key 12 from B to D, leaves 28 at B and wraps 90 to A. [Azure Architecture Center data ownership](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/data-considerations), [sharding strategies](https://learn.microsoft.com/en-us/azure/architecture/patterns/sharding#sharding-strategies), [Dynamo §4.2](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf#page=5).

## Provenance

Azure Architecture Center guidance supports the architecture distinctions. Vitess 24 documents a concrete copy, verification, catch-up and traffic-switch workflow. The epoch protocol is an original teaching design. The Dynamo paper supports the ring and virtual-node mechanisms, and the examples use independently chosen coordinates and workloads. The package imports no code, figures or other third-party assets.

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the lesson, companion and evidence at draft commit `21b3905` on 2026-11-13.

| ID | Status | Verification and next action | Primary evidence |
| --- | --- | --- | --- |
| M04-L03-T1 | open | The revision resolves the original timeout and abort race. Activation and abort compete on one pending plan, and a lost reply leaves the source fenced. A delayed local open after a directory read still needs a write-side guard. An activation handler can read proof for destination epoch 2, pause, and attempt to open epoch 2 after rollback has fenced it and reopened the source at epoch 3. Persist a monotonic closed-through epoch at each shard, serialize open against that guard and reject any delayed activation at or below the local closed epoch. Show the delayed command losing even when it previously obtained valid proof. Apply that guard to the companion's expected rollback. | [etcd v3.6 transactions](https://etcd.io/docs/v3.6/learning/api/#transaction), [etcd v3.6 strict serializability and uncertain operations](https://etcd.io/docs/v3.6/learning/api_guarantees/), [Burrows, Chubby §2.4, stale requests and recipient-side sequencer checks](https://www.usenix.org/legacy/events/osdi06/tech/full_papers/burrows/burrows.pdf#page=5) |
| M04-L03-T2 | resolved | The lesson labels the inclusive tie rule as a teaching-example convention and the companion uses that convention explicitly. Ownership and movement calculations still agree. | [Dynamo §§4.2–4.3](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf#page=5) |

The etcd sources support the conditional directory transaction and a linearizable read of its result. Shard-level admission fencing belongs to the application. Vitess documents a related source write stop and catch-up for its own traffic switch.

### Verdict

`revise`

## Round 2 targeted re-review

Reviewed the lesson, companion and evidence at draft commit `ec068f6` on 2026-11-13.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M04-L03-T1 | resolved | The lesson's migration section and the companion now serialize local open, close and write admission through a single gate. If destination epoch 2 opens before the fence, closing through epoch 2 stops admissions and all earlier writes drain and copy before source epoch 3 opens. If epoch 2 pauses before the fence, the durable floor blocks its later open even if it already read valid directory proof. The close applies even to an assigned epoch that never opened. The directory's activation and abort remain mutually exclusive, and a lost reply keeps the source fenced until the plan is resolved. The solution and rubric cover both the stale local command and the preservation of destination writes. | [Burrows, Chubby §2.4, recipient-side sequencer checks](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows.pdf#page=5), [etcd v3.6 conditional transactions](https://etcd.io/docs/v3.6/learning/api/#transaction), [etcd v3.6 uncertain operations](https://etcd.io/docs/v3.6/learning/api_guarantees/), [Vitess 24 write cutover](https://vitess.io/docs/24.0/reference/vreplication/reshard/#switchtraffic) |
| M04-L03-T2 | resolved | The earlier correction to the inclusive-token convention remains in place in the lesson and companion. | [Dynamo §§4.2–4.3](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf#page=5) |

The Chubby source supports rejecting stale authority at the protected resource. The lesson and evidence scope the durable closed-through epoch to the illustrative migration design. The revision preserves the hot-tenant and ring traces and imports no third-party assets.

### Verdict

`ready-for-human-review`
