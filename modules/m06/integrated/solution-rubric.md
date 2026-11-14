---
id: M06-EX1-solution
status: draft
---

# Reference design and rubric

## Size and route the query cache

Use a shared application cache of complete ordered pages. A key includes canonical query, locale, filters, page, authorized audience, affected dependency-domain generation and ranking version. Hash the full key for routing and compare full keys on lookup. Keep the rights check authoritative. An object cache would reuse listing cards across queries but would still need a membership and ranking computation.

The primary working set is 30,720 × 4 KiB = 120 MiB. Each node has 76.8 MiB usable. Steady memory is at most 40 + 8 = 48 MiB per node. After loss, an upper bound under the stated remap is 40 + 8 + 20 = 68 MiB per survivor, even counting retained replica entries separately. Cap by bytes and evict from the least recently used end if recency predicts reuse. Use expiry independently and consider excluding measured one-off scans from admission.

Route base traffic by sharded ownership and keep a copy of the hot result on each of the three nodes so two copies can survive any single-node loss. With the hot key alone on one survivor, ordinary traffic of 160 lookups/s can bring that node to 300 + 160 = 460 lookups/s. Split the hot key 150/s to each eligible copy. The envelope becomes 310 lookups/s per survivor. The balanced 310 includes one lookup per original, leaving only 40 lookup attempts/s per node for probes or retries. If only one copy is eligible, its 350/s ceiling less 160 ordinary lookups leaves at most 190 hot lookups/s; pace at that rate and return unavailable for excess or expired requests, rather than overloading it. Count every alternate probe and retry against the destination node limit. Coalescing the expensive fill still leaves cache lookups to handle. Re-route other keys under the new membership, and monitor routing skew while old membership views drain.

## Trace coherence and recovery

Start with a lightweight authoritative check for access and catalogue generation and an explicit expected ranking version. A hit under the complete tuple is eligible only if its source deadline still holds. At a miss, one shared fill leader for the exact key uses a fresh primary snapshot, obtains the data and its generation together and computes with the requested rank version. Reserve time for returning to waiting callers, who each validate their requested tuple and the source observation deadline. If the fill observes a new generation or the worker cannot execute the requested ranking version, discard the mismatched attempt, select a supported rank and fresh authoritative generation, and retry under the newly resolved complete key. That may change shard and coalescer identity. Charge the retry to the same budgets. [PostgreSQL 18, Read Committed](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED).

For the write, commit the record and the generation of its complete affected dependency domain together, including every query and page whose membership or order could change. A check started after the commit selects the new key, including records newly eligible for a page. Old in-flight results cannot populate that key. Old entries may remain in memory until expiry or eviction. At rank rollout, bind the payload to the ranking code version and change that key field. An old replica is ineligible for the new tuple. Never extend a deadline because an old fill was retried or moved. If the current generation or a fresh result cannot be confirmed within the budget, return unavailable.

After loss, unprotected non-hot demand is 40 + 110 = 150 expensive starts/s against 120; at least 30/s cannot start in that envelope. The 45/s candidates belong to unaffected domains. If all are actually eligible throughout a measured interval, they reduce demand to 105/s and leave 15/s of conditional headroom. Their two-second observation deadlines still apply: copying or moving an entry cannot renew its age. Count every refresh, rewarm, retry and new hot fill in the same rolling 120/s budget; without their schedule, 105/s is a warm best case, not a sustained capacity proof.

After the edit both old hot copies are ineligible for the new tuple. Admit one fleet-wide coalesced primary fill for the new generation and rank. Publish that same eligible result to both survivors with its original source-observation deadline; each waiter checks its own final tuple, authorization and deadline. While neither copy is ready, wait only within the original 200 ms or return unavailable. When one is ready, pace hot lookups within its remaining 190/s and shed excess; split 150/s each only after both are eligible. Refresh or refill before expiry under the same origin ceiling; if a fresh eligible copy cannot be supplied, shed instead of extending the old deadline. Rank-worker mismatches discard and re-route/re-coalesce using a supported rank within the same original deadline and budgets.

A fleet-wide admission control enforces 120 expensive starts per rolling second, with a separate in-flight cap. The baseline 600 combined rights and generation checks/s leaves 200 reads/s under the 800/s lightweight limit; retries consume that limit and all per-node lookup allowances too. If either authority check cannot complete within budget, return unavailable. [Scaling Memcache at Facebook, §3.2.1](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf#page=4).

## Score the drill

The observed success rate is 5,770 / 6,000 ≈ 96.17%. The target needs 5,880 successes, so the candidate is 110 short. All late, unavailable or ineligible responses remain in the original cohort. Inspect per-shard lookup and eviction counts, unique fills and duplicate coalescer work, dependency admission and timeouts, result age and old-generation responses. Compare actual ordered IDs and relevant content with the independent fixture for the final successful attempt's authoritative check and required rank; verify source observation time from trace evidence. Test a first check at the old generation followed by a retry at the new generation: the new page must match its fixture within the original ID's first-arrival deadline. Also test rank-worker mismatch, one or no usable replica, bounded probes and late fill replies. Capacity arithmetic alone cannot certify the measured result.

| Criterion | Points | Full credit |
| --- | ---: | --- |
| Unit, key and memory | 3 | Computes both memory states, accounts for the eviction and reuse decision, and protects the audience and key variants. |
| Coherence and recovery | 3 | Traces the complete affected domain, read/write race, rank or generation mismatch, source-age limit, rerouting and eligible replicas. |
| Dependency budgets | 2 | Sizes both- and one-copy hot paths and conditional origin demand; counts probes, refresh, rewarm and retries within all rolling limits and sheds excess. |
| Client outcome | 2 | Scores the complete cohort; compares actual ordered content with the final-check fixture and verifies observation age and unchanged original deadline, including the old-to-new retry trace. |

Accept designs that meet the same input, age, authority and capacity assumptions with justified different layouts.
