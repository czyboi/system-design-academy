# M03 integration teaching and coverage recheck

## Reviewed scope

Rechecked the current English draft for middle and senior engineers. The brief, evidence, approved course outline, inventory and matrix have the same file hashes as in the first review. The revised solution and decision summary retain the brief's references to all three current M03 lessons. Checked those lesson references against the exact lesson bytes bound to their accepted teaching reviews.

## Findings and dispositions

| Finding | Disposition | Evidence in the current draft |
| --- | --- | --- |
| M03-INT-P1 | Resolved | **Discovery and failure trace** now distinguishes a stopped renderer that never accepted the call from a renderer that accepted work before its reply was lost. The alternate either creates the first acceptance or returns the existing acceptance for the same work ID. It preserves the common 300 ms budget, with 150 ms remaining at the latest start of the second attempt and 90 ms after its reply. |
| M03-INT-P2 | Resolved | **Self-evaluation**, Verification criterion, now calls for load and worker-loss tests that validate the maximum endpoint age and in-flight cap. The exercise remains open to values justified under the hypothetical workload and observed failure behavior. |
| M03-INT-TP1 | Teaching consequence addressed | **Ownership and deployment** shows a single guarded update on the row that holds version, approval and publication pointer. It follows both commit orders and clears the pointer atomically with a superseding edit or revocation. The decision summary carries the same rule. The rubric asks the learner to explain the serialization and test both orderings. |
| M03-INT-TP2 | Teaching consequence addressed | **Public and internal contracts** specifies an atomic durable acceptance by unique work ID across eligible endpoints, matching immutable inputs, and rejection of changed input. The decision summary retains the atomic acceptance requirement, and the trace explains repeat-safe output and completion if processing restarts. |

## Synthesis coverage and pedagogy

M03-EX1 still assesses M03-S1 with the three approved inputs. Task 1 measures M03-L01-LO2 by comparing deployment alternatives using the CPU and p99 constraints and protecting the version/approval invariant. Task 2 measures M03-L02-LO1 by tracing the editor resource interaction and renderer RPC, then reasoning about duplicate or delayed work. Task 3 measures M03-L03-LO2 by comparing caller-side and intermediary-side discovery with the same public and internal interfaces and defending a bounded retry policy. This is the deeper comparison deferred by N1. The remaining lesson outcomes stay in the separate companions.

The original workload, client versions and preview timing are intact. The revised rubric distinguishes good design reasoning, incomplete reasoning and contradiction, and permits alternative mechanisms that preserve the same invariant and bounds. The revised decision summary retains all eight required columns and its lesson links. No new material coverage, pedagogy or language finding.

Verdict **ready-for-human-review**.
