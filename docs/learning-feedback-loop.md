# Learning feedback loop — verified, compact, and reviewable

AI agents do not retrain themselves or automatically improve shared skills. The Academy reuses **repository-tracked, independently re-reviewed corrections** as small task-specific guidance without expanding the task graph.

## Before writing or reviewing

The parent derives relevant lower-case hyphenated topic tags from the assigned approved Story, outcomes and primary-source topics. For each agent, run:

```bash
python scripts/learning_memory.py suggest --tags cap-theorem,consistency --role lesson_author --limit 3
python scripts/learning_memory.py suggest --tags cap-theorem,consistency --role technical_reviewer --limit 3
python scripts/learning_memory.py suggest --tags system-design,pedagogy --role pedagogy_reviewer --limit 3
```

Only pass matched reminders, never the entire knowledge file. Zero matches is valid. These are prompts to check prior failure modes, **not technical authority, replacements for task specs, or permission to pad a lesson**. Current primary sources and the canonical task spec take precedence.

## After module QA and targeted correction

Only when `scripts/review_cycle.py status mXX` is `ready`, at least one corrective revision occurred, both reviewers completed independent re-review, and the final applicable report identifies the original finding as `resolved` with an exact supporting source, extract a genuinely reusable prevention rule:

```bash
python scripts/learning_memory.py record \
  --module m00 --review-role technical --finding-id T-1 \
  --key distinguish-consistency-contracts \
  --tags consistency,distributed-systems \
  --problem "Conflating distinct meanings of consistency in design decisions" \
  --prevention "Separate each consistency contract with an operation-level example" \
  --evidence "https://example.org/primary-source-section" \
  --applies-to lesson_author,technical_reviewer
```

The evidence URL above is illustrative, **not** a source endorsement. Use the real primary document or approved curriculum path which appears exactly in the final resolved review report.

The recorder rejects unfinished/blocked/revision-0 cycles, missing/resolution-less finding IDs, unsupported/unmentioned evidence, unsafe paths, conflicting rules for an existing key and duplicate occurrence IDs. Its checks are *provenance gates*, not automated factual verification; the independent reviewer and parent must inspect whether evidence truly supports the corrected claim. Skip incidental one-off wording edits and unresolved reviewer opinions.

The file `.academy/knowledge/lessons-learned.json` is versioned with the module review reports, task memory and cycle state by `draft_handoff.py --review-report`. It keeps only a short problem, short prevention guidance, tags, agent roles and cited occurrences. No new research agent, similarity service, embeddings database or model fine-tuning is needed.

## Promote repeated problems to Skill improvements

```bash
python scripts/learning_memory.py promotions
```

Only an **identical stable key verified in at least two distinct modules** qualifies. The parent inspects whether the proposed rule is broadly valid, source-supported, not already in the relevant Skill, and not contradictory. If safe and meaningful, it may create a **separate pull request** with a minimal proposed Skill change, links to the evidence and a clear reason. The user reviews and merges that PR explicitly. Do not silently change Skills, agent models or permissions; do not repeatedly open the same proposal. If evidence conflicts, record the conflict and ask for review instead.

A finding can recur despite these precautions: topic-tag retrieval may miss it, source versions may differ, or a reviewer can be wrong. The loop helps reduce repeat errors, but does not guarantee quality or substitute for human publication approval.
