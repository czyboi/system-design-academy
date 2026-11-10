# Project Specification — System Design Academy

**Status:** Draft 0.1  
**Owner:** Project owner  
**Primary language:** Vietnamese, retaining standard English technical terminology  
**Initial audience:** Backend engineers with programming and basic database experience  
**Initial content source:** System Design Primer plus official documentation, standards, papers, and engineering case studies

## 1. Product goal

Create a structured learning experience that teaches learners to reason about system design decisions, not merely memorize interview answers. The curriculum should connect requirements, workload characteristics, architecture choices, failure modes, operational consequences, and trade-offs.

## 2. Initial scope

The first release targets a foundation-to-intermediate System Design track. Planned areas:

1. System design fundamentals and requirements.
2. Capacity estimation and workload modeling.
3. Networking and edge infrastructure.
4. Application architecture and service communication.
5. Database architecture and data modeling.
6. Caching.
7. Asynchronous processing and messaging.
8. Distributed systems and consistency.
9. Reliability, security, observability, and operations.
10. End-to-end system design case studies.

The Database module is the first pilot and is stored in `modules/database/`.

## 3. Learning design principles

- Start from a concrete engineering problem, then introduce concepts needed to solve it.
- Explain when a technique is useful and when it is harmful or unnecessary.
- Make assumptions explicit: scale, read/write pattern, latency, durability, consistency, cost, and operational constraints.
- Separate conceptual explanations from vendor-specific implementation details.
- Use original examples, datasets, diagrams, and exercises wherever possible.
- Every lesson must have measurable learning outcomes and assessments mapped to those outcomes.
- Include worked solutions and explain alternative valid designs.

## 4. Standard lesson contract

Each lesson should contain:

1. Metadata: ID, title, status, level, prerequisites, estimated learner time, last verified date.
2. Learning objectives.
3. Motivating problem and context.
4. Core concepts and mechanism.
5. Architecture/sequence/data diagram when helpful.
6. Worked example.
7. Trade-offs, failure modes, and operational concerns.
8. Knowledge check (normally 5–8 questions) with answer explanations.
9. Hands-on or design exercise with solution/rubric.
10. References mapped to important claims.
11. Adaptation and attribution notes where applicable.

## 5. AI workflow responsibilities

- **Orchestrator:** Reads task state, chooses the next bounded unit, enforces retry and publication rules.
- **Researcher:** Retrieves exact sources and records provenance; flags conflicts and missing evidence.
- **Author:** Produces original educational exposition using approved source material and the lesson contract.
- **Diagram/Assessment generator:** Creates editable diagrams, exercises, quizzes, solutions, and rubrics.
- **Technical reviewer:** Audits technical claims independently against primary sources.
- **Pedagogical reviewer:** Checks clarity, sequencing, prerequisites, and assessment alignment.
- **License reviewer:** Checks reuse rights for adapted text and each third-party asset.
- **Human approver:** Makes final approval and publication decisions.

These roles can be separate AI runs using the same model; they must have separate prompts, evidence, and acceptance criteria. AI self-review is not equivalent to independent expert review.

## 6. Content state machine

`PENDING -> RESEARCHING -> DRAFTING -> TECHNICAL_QA -> PEDAGOGICAL_QA -> LICENSE_QA -> READY_FOR_HUMAN_REVIEW -> APPROVED -> PUBLISHED`

Any failed gate returns the lesson to `REVISION_REQUIRED`. After two unsuccessful automated revision cycles, stop and request human judgment. `APPROVED` and `PUBLISHED` require an explicit human action.

## 7. Definition of done for a lesson

A lesson is ready for human review only when:

- All required sections exist.
- All learning objectives are assessed.
- Important/version-sensitive claims have direct, working references.
- Vendor-specific claims identify the product and version/scope.
- No unsupported claims, fabricated measurements, or invented links remain.
- Diagrams are editable and explained.
- Quiz answers and exercise rubrics are present.
- Technical, pedagogical, and license QA reports are attached.
- The lesson remains marked `draft` or `ready-for-human-review`.

## 8. Out of scope for the pilot

- Learner-facing LMS, accounts, payments, and analytics.
- Video production.
- Unattended autonomous publication.
- Automatic legal conclusions.
- Claims of certification, accreditation, or endorsement by source authors.

## 9. Success criteria

The pilot succeeds when the Database module can be generated and reviewed using a repeatable, auditable workflow; sources and licenses are traceable; lessons pass a consistent QA checklist; and generation does not require manually writing every lesson.
