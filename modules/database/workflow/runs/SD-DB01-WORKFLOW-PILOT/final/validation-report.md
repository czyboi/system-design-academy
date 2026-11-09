# DB-01 Workflow Pilot — Validation Report

**Task:** `SD-DB01-WORKFLOW-PILOT`  
**Date:** 2026-11-09  
**Final lesson:** `modules/database/lessons/DB-01-data-modeling.md`  
**Status:** Draft; automation validation only

## Commands and results

| Command | Result | What it establishes |
|---|---|---|
| `python scripts/validate_content.py` | **Passed.** 7 lesson files found, 20 source-registry rows, 10 shared skills, 6 custom agents. It reported 0 internal Markdown links checked. | Required front matter/sections, source registry shape, manifest, skills/agents config, and structural safeguards. It does not test external URL reachability, technical truth, legal rights, or pedagogy. The separate DB-08 case study is not counted among the 7 lesson files. |
| `python -m unittest discover -s tests -v` | **OK:** 12 tests ran, 1 skipped. | Task-state and repository integration behaviors covered by the current tests. `test_path_validation_rejects_absolute_and_symlink_inputs` skipped because this Windows process lacks symlink privilege (`WinError 1314`). |
| `python scripts/taskctl.py validate` | **Passed.** | Task specs/state schema and task graph validation. |

The first test attempt used a temporary directory under the lesson run folder and hit a Windows cleanup-handle error. The suite was rerun from a separate writable scratch directory; the result above is that successful rerun.

## Review findings applied

The three independent reports reviewed the author draft and returned `revise`. The task parent applied the findings to the final lesson:

| Review | Applied change |
|---|---|
| Technical | Scoped both SQL blocks to illustrative, unexecuted PostgreSQL 18 syntax; clarified MySQL 8.4/InnoDB boundaries; explained `UNIQUE` versus `NOT NULL`; documented the payment composite key. |
| Pedagogical | Corrected outcome-to-assessment mapping; added a sample ERD; clarified organizer requirements; defined key terms in Vietnamese. The 90-minute estimate remains provisional. |
| Provenance | Added the direct CC BY 4.0 link, an explicit change notice, a no-endorsement statement, and a pinned Primer commit reference. |

No independent reviewer pass was run against the post-revision artifact. The human reviewer should inspect the final lesson and review reports before approval.

## Remaining human actions

- Confirm that learners can access the Microsoft Learn normalization page or replace it with an accessible source. The provenance reviewer saw an access-required banner.
- Decide whether to run the illustrative PostgreSQL 18 DDL in a declared environment before treating it as executable instructional code. No SQL was run in this pilot.
- Pilot the lesson with learners to validate the provisional 90-minute estimate and question clarity.
- Update the shared source registry's Primer snapshot from moving `master` to the pinned commit in a separately scoped task; this pilot pins the lesson reference but does not edit the shared registry.
- Complete human technical, pedagogical, and provenance review before any approval or publication.

## Interpretation

Structural validation and the repository unit tests passed with the documented symlink-test skip. These results do not establish factual correctness, source reachability, legal clearance, or learner effectiveness. The canonical lesson remains `status: draft`; this report does not approve or publish it.
