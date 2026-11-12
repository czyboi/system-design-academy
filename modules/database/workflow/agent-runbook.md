# Database workflow — use shared Academy rules

This older module-specific runbook is superseded by the repository's [module-pipeline skill](../../../.agents/skills/module-pipeline/SKILL.md) and [workflow contract](../../../docs/workflow-contract.md). Do not use the former fingerprint/review-automated process.

New lesson work has only **research → author**. Use the exact canonical lesson, assessment and evidence paths in `delivery/backlog.json`. Keep task state explicit, preserve quality standards in `GOVERNANCE.md`, and request independent review/content validation only when needed. Cross-environment handoff uses committed/pushed Git artifacts and `taskctl handoff`.
