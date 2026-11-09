# Content Guidelines

## Audience and teaching stance

- Audience: backend engineers who know basic SQL and application development but are learning system design.
- Language: English-only learner-facing prose, diagrams, exercises, quizzes, rubrics, and answer explanations. Keep source titles and quotations in their original language; do not use bilingual headings.
- Start from a concrete engineering problem, then introduce the concept.
- Explain mechanisms, constraints and trade-offs; avoid lists of definitions without causal explanation.
- Distinguish general database principles from PostgreSQL, MySQL, MongoDB or DynamoDB-specific behavior.
- State assumptions and workload shape whenever making a recommendation.

## Required lesson structure

1. Title, status, level, prerequisites, estimated learner time.
2. Learning outcomes (observable, assessable verbs).
3. Problem and motivating scenario.
4. Core concepts and mechanism.
5. Architecture/data-flow diagram when it materially helps.
6. Worked example with explicit assumptions.
7. Trade-offs and failure modes.
8. Practical decision framework.
9. Knowledge check (5–8 questions; varied difficulty).
10. Hands-on exercise with acceptance criteria.
11. Worked solution or rubric.
12. References: source, section, version/date checked, claim supported.
13. Attribution and change notes if adapting CC-licensed expression.

## Technical accuracy rules

- Never generalize vendor-specific behavior as universal SQL/NoSQL behavior.
- Prefer primary sources: official documentation, standards, original papers. Engineering blogs may add implementation context but should not be the only support for a critical claim.
- For any version-sensitive statement, specify product and major version (e.g. PostgreSQL 18, MySQL 8.4).
- Avoid absolute wording such as “always”, “never”, “guarantees” unless the source explicitly supports it and the scope is clear.
- Separate logical concepts from physical implementation details.
- A replica is not a backup. Replication does not by itself protect against accidental deletion, corruption or malicious changes.
- Partitioning inside one database instance is not the same as sharding across independently managed nodes.
- Indexes can accelerate reads but add storage and write/maintenance cost; do not recommend “index every queried column”.
- An index does not guarantee the optimizer will use it.
- ACID, isolation levels and consistency guarantees must be described precisely and, where needed, per engine.
- Avoid claiming that choosing NoSQL automatically makes a system scalable or that SQL cannot scale.

## Attribution rules

- Record each source and license in the source registry.
- CC BY 4.0 material may be copied, adapted and used commercially subject to attribution, license link, change notice and no implied endorsement.
- Do not assume images, diagrams, notebooks, flashcards or linked third-party resources inherit the repository's CC BY license.
- Prefer creating original diagrams, code and examples.
- Keep the original source URL and commit/hash for adapted content.

## Editorial quality

- Use one primary concept per section.
- Define acronyms at first occurrence.
- Give examples with small, understandable data sets before introducing scale.
- Explain why an option is chosen and what is sacrificed.
- Ensure each learning outcome is tested by at least one question or exercise.
- Keep questions answerable from the taught material; do not test trivia.
