# MS01–MS02 content format audit — Step 1

> Snapshot-only audit for Issue #39. **No canonical content, reviewer verdict, task workflow, or public website code is modified by this step.**

## Source snapshots and selection

| Milestone | Branch | Audited commit | Modules | Lesson IDs |
| --- | --- | --- | --- | --- |
| MS01 | `codex/SDA-MS01` | `e823c8d72e59f1691ce7bfc65f37c209066eca99` | `m00`, `m01` | 6 |
| MS02 | `codex/SDA-MS02` | `ec753d7bcfd69ad68e5fff260aeb088059e42540` | `m02`, `m03` | 7 |

Both milestone branches are separate from `main` as observed in this audit. The course outline is SDA-v1; the 13 lessons are *draft and review-ready*, not publicly approved.

Selection is based on the `modules/mXX/integrated/outcome-portfolio.json` teaching paths, **not** on newest filename or directory order:

| ID | Selected teaching path | Matching assessment path | Why |
| --- | --- | --- | --- |
| `M01-L02` | `modules/m01/lessons/revision-1/M01-L02.md` | `modules/m01/assessments/revision-1/M01-L02.md` | Referenced by M01 outcome portfolio and revision-bound review |
| `M02-L02` | `modules/m02/lessons/revision-1/M02-L02.md` | `modules/m02/assessments/revision-1/M02-L02.md` | Referenced by M02 outcome portfolio and revision-bound review |

Other lesson IDs use their normal `modules/mXX/lessons/MXX-LYY.md` path. Historical base versions of those two revised lessons were inspected but excluded from the 13 selected-lesson aggregate counts.

## Observed format inventory

| Observation | Result on 13 selected lessons | Implication |
| --- | --- | --- |
| `.md` with YAML front matter | 13/13 | Existing structure is usable without migrations |
| Front matter fields | All include `id`, `title`, `status`, `level`, `prerequisites`, `outcomes`, `assessment`, `source_review_date`, `reviewer` | Preserve; do not add required fields to reviewed source |
| Draft status | 13/13 `draft` | Review-ready is not publication approval |
| Distinct assessment file | 13/13 | Preserve separation and visibility policy |
| Outcome IDs in lesson front matter | 13/13; two explicit outcome IDs each | Keep stable IDs and outcome mapping |
| GFM-style pipe tables | 7/13 | Table renderer is a practical v1 requirement |
| Fenced code blocks | 1/13 (`text`, M01-L01) | `text` must be supported; do not require a programming language |
| Mermaid fences | 0/13 | Cannot claim diagram rendering is already exercised |
| Markdown image syntax | 0/13 | Asset support needs future fixtures |
| Raw HTML tags | 0/13 observed | Define safe handling for future content |
| LaTeX math delimiters | 0/13 observed | Renderer capability remains unproven |
| Markdown reference links | Present throughout | Preserve links and validate local assets |

All 13 companion assessments have six `Q`-numbered knowledge checks and outcome mappings. Crucially, answer markup varies: some have `Answer:` and `Explanation:`, while others use `**Answer:**` and `**Explanation:**` (e.g., `modules/m02/assessments/M02-L01.md`). A string matcher requiring only unformatted `Answer:` is not a safe extraction contract.

Heading text also varies. Example: M00-L01 uses `## Worked example and historical architecture`; other lessons use `## Worked example`. Many lessons add their own named sections. Website rendering must not hardcode a section splitter that assumes identical headings.

Four module integrated packages (`m00`–`m03`) have distinct `brief.md`, `solution-rubric.md`, `decision-summary*.md`, and `outcome-portfolio.json` patterns. They are not lesson-shaped documents. The revised integrated files and reports also refer to selected revision paths.

## Gaps / risks for the website

1. **Revision ambiguity:** one ID can point to original and reviewed revision. Resolve through an explicit, hash-verified selection contract; failing closed is safer than guessing.
2. **Representation vs quality:** existing structural validators and reviewers verify different dimensions. A parser passing does not establish visual fidelity or technical accuracy.
3. **Assessment variants:** a later interactive quiz extractor must support both emphasized and plain answer labels. Parsing Markdown with naive regex risks silent loss.
4. **Unsupported rich content:** no current Mermaid, image, HTML, or math samples demonstrate web render compatibility. Prepare fixtures and renderer tests before committing to support.
5. **Incomplete publication model:** existing artifacts are drafts; there is no website-specific approved-content manifest on the inspected branches.
6. **Metadata semantics:** `prerequisites` includes entry-knowledge text in M00-L01 and lesson IDs elsewhere; a frontend must not assume all prerequisites are navigable lessons.
7. **Branch integration:** two milestone outputs remain on separate branches. Do not copy their content or merge branches as a side effect of the format-contract step.

## Explicitly NOT concluded by this audit

- No browser rendering was executed, and no claim is made that all Markdown renders identically in every parser.
- No production website, parser, security sanitizer, content manifest, or publication gate was created.
- No new authoring validator has run against these branches. Existing milestone review reports are provenance and QA evidence, not a live re-run of those tests.
- The absence of diagrams is an observation, **not** a verdict that all 13 lessons need diagrams; decide that through pedagogical review, not format enforcement.

## Follow-on milestones (separate scoped changes)

1. Approve or revise [the candidate format contract](authoring-format-contract-v1.md) without touching previously reviewed lesson bytes.
2. Implement parser-backed format validation and regression fixtures; preserve historical variants and add negative cases.
3. Add a thin loader and explicit revision/hash selection; no LLM in build path.
4. Add per-artifact human approval and fail-closed publication control.
5. Integrate the website and run real rendering/visual QA.
