---
id: M06-EX1-solution
status: draft
---

# Reference design and rubric

## Size and route the query cache

Use a shared application cache of complete ordered pages. A key includes canonical query, locale, filters, page, authorized audience, catalogue generation and ranking version. Hash the full key for routing and compare full keys on lookup. Keep the rights check authoritative. An object cache would reuse listing cards across queries but would still need a membership and ranking computation.

The primary working set is 30,720 × 4 KiB = 120 MiB. Each node has 76.8 MiB usable. Steady memory is at most 40 + 8 = 48 MiB per node. After loss, an upper bound under the stated remap is 40 + 8 + 20 = 68 MiB per survivor, even counting retained replica entries separately. Cap by bytes and evict from the least recently used end if recency predicts reuse. Use expiry independently and consider excluding measured one-off scans from admission.

Route base traffic by sharded ownership and keep a copy of the hot result on each of the three nodes so two copies can survive any single-node loss. With the hot key alone on one survivor, ordinary traffic of 160 lookups/s can bring that node to 300 + 160 = 460 lookups/s. Split the hot key 150/s to each eligible copy. The envelope becomes 310 lookups/s per survivor. If one hot copy is unavailable, use paced rerouting and shed when needed. Coalescing the expensive fill still leaves cache lookups to handle. Re-route other keys under the new membership, and monitor routing skew while old membership views drain.

## Trace coherence and recovery

Start with a lightweight authoritative check for access and catalogue generation and an explicit expected ranking version. A hit under the complete tuple is eligible only if its source deadline still holds. At a miss, one shared fill leader for the exact key uses a fresh primary snapshot, obtains the data and its generation together and computes with the requested rank version. Reserve time for returning to waiting callers, who each validate their requested tuple and the source observation deadline. If the fill observes a new generation, discard the result for the old group and retry under the newly resolved complete key. That may change shard and coalescer identity. Charge the retry to the same budgets. [PostgreSQL 18, Read Committed](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED).

For the write, commit the record and generation together. A check started after the commit selects the new key, including records newly eligible for a page. Old in-flight results cannot populate that key. Old entries may remain in memory until expiry or eviction. At rank rollout, bind the payload to the ranking code version and change that key field. An old replica is ineligible for the new tuple. Never extend a deadline because an old fill was retried or moved. If the current generation or a fresh result cannot be confirmed within the budget, return unavailable.

After loss, the cold non-hot demand without protection is 40 + 110 = 150 starts/s against 120. Even with perfect no-retry saturation, 30/s cannot start in that envelope. With 45 eligible selective-copy hits from that set, demand falls to 105 starts/s, leaving 15/s for further work under the stated inputs. If the hot key changes, the one new shared fill uses that allowance, as do retries and any warm-up. A fleet-wide admission control enforces 120 starts per rolling second. Cap in-flight origin work separately and wait only within each request deadline. The baseline 600 lightweight checks/s leaves 200 reads/s under the stated single-check combined read for rights and generation. Coordinate retries under that second limit. If the authority cannot answer, do not treat the replica as proof of eligibility. [Scaling Memcache at Facebook, §3.2.1](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf#page=4).

## Score the drill

The observed success rate is 5,770 / 6,000 ≈ 96.17%. The target needs 5,880 successes, so the candidate is 110 short. All late, unavailable or ineligible responses remain in the original cohort. Inspect per-shard lookup and eviction counts, unique fills and duplicate coalescer work, dependency admission and timeouts, result age and old-generation responses. Compare the returned page's actual source revision and ranking version against the fixture for that request's check. Test loss just before a generation change, missing replicas, and late fill replies. Capacity arithmetic alone cannot certify the measured result.

| Criterion | Points | Full credit |
| --- | ---: | --- |
| Unit, key and memory | 3 | Computes both memory states, accounts for the eviction and reuse decision, and protects the audience and key variants. |
| Coherence and recovery | 3 | Traces the read/write race, rank or generation mismatch, age limit, rerouting and eligible replicas. |
| Dependency budgets | 2 | Sizes the hot lookup split and origin demand, limits all starts and checks, and states failure behavior. |
| Client outcome | 2 | Scores the complete cohort and names tests or signals tied to eligible results and capacity. |

Accept designs that meet the same input, age, authority and capacity assumptions with justified different layouts.
