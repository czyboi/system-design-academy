---
id: M00-EX1
status: draft
outcomes: [M00-S1]
---

# Design brief for sharing inspection documents

A maintenance team wants to distribute signed inspection PDFs to named employees. A publisher uploads a PDF and grants or revokes access. A reader opens the link while signed in. A new authorization check that starts after the service confirms a revocation must deny the former reader. A reader who already downloaded a copy may retain it.

The team expects 12 publishers, 200 readers, peak downloads of 50 per minute, and PDFs up to 2 MiB. This release serves one office and excludes public sharing and collaborative editing. The team can support one small deployment and accepts an interruption during host replacement. Ask what would change if serving through one host failure became a requirement.

## M00-EX1

Write a one-page brief for a design review. Prioritize the use cases, state two measurable constraints or targets, and mark requirements, assumptions and unknowns. Show the publish, download and revoke paths at component and interface level. Examine the authorization check closely enough to explain what happens on a request after revocation.

Compare two designs against the same constraints. Choose an initial design and name one workload or failure observation that would change the choice. Describe how you would get that evidence.

## M00-S1

Frame the design and defend its scope with requirements, alternatives and evidence. This exercise draws on both outcomes in [From requirements to a defensible design](../lessons/M00-L02.md).
