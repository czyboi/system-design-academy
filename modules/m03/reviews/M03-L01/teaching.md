# M03-L01 actual coverage and pedagogy review

## Scope and sources

Reviewed the draft lesson, companion and evidence for middle and senior engineers against the approved SDA-v1 M03-L01 outline and its three assigned inventory rows. Inspected the application-layer and microservices sections and their trade-offs in [The System Design Primer at the pinned revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L773-L798).

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator, explanation and assessment |
| --- | --- | --- | --- |
| PR-H078 | Logical layers and deployment tiers | taught | README.md#L773. The web layer receives and translates, the application layer applies the business rule, and the data layer persists state. The catalogue trace separates CPU-intensive asynchronous work from the interactive path and gives it a distinct capacity allocation. LO1 Q1–Q3 and EX-1 trace these responsibilities. |
| PR-H079 | Logical layers and deployment tiers | taught | README.md#L785. The lesson compares explicit modules in one deployable application with a remote capability that owns an interface and its data. The worked example compares an independently scalable media capability with entity-level services and explains why autonomy depends on release, contract and data coupling. LO2 Q4–Q5 and EX-1 apply the comparison. |
| PR-H081 | Costs of a remote boundary | taught | README.md#L795. Required remote fan-out increases failure exposure, and independent deployables require compatible contracts, operational ownership and coordination of local transactions. The saga discussion makes compensations and failed compensation explicit. LO2 Q4, Q6 and EX-1 exercise these costs. |

The boundary with discovery and interface design stays clear. This lesson names a failure contract and leaves its protocol and discovery mechanics to M03-L02 and M03-L03.

## Pedagogy and language

An image-conversion contention problem motivates the separation of responsibilities and the service decision. The trace follows the ownership check through persistence, remote conversion and result validation. The comparison keeps the publication invariant with the catalogue owner, so learners can reason about why a remote cut has a different cost depending on what it crosses.

The English companion has six explained checks and an explicit map for both outcomes. EX-1 applies both to a reservation invariant and a PDF workload with a one-minute delay allowance. The learner must choose an ownership boundary, compare synchronous fan-out, and explain a remote failure and what to measure. The answer recognizes both a separate processor and a modular monolith with isolated worker capacity. The rubric awards points for the invariant, costs and verification, in addition to the proposed split.

## Findings

- **M03-L01-P1 (minor).** The map points LO2 to **Decision framework**, which summarizes the criteria, while Q6's compensation behavior is taught in **Costs of a remote boundary**. LO1's mapped worked example demonstrates the combined trace, while Q2's deployment distinction is introduced in **Logical layers and deployment tiers**. Add those exact subsection pointers in the companion to speed item-level audit.
- **M03-L01-P2 (note).** The EX-1 answer accepts a modular monolith with separately allocated worker capacity. An explicit example of isolating receipt workers from reservation CPU within that option would make the alternate design easier to score under the contention constraint.

Verdict **ready-for-human-review**.
