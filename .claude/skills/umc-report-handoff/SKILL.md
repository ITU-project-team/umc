---
name: umc-report-handoff
description: Move UMC Part 1, Part 2, or Part 3 analysis-worker evidence into report-safe DOCX comments, table notes, prose handoffs, or report-worker instructions without exposing raw data, private text, post IDs, or local raw paths.
allowed-tools: Read, Bash
---

# UMC Report Handoff

Use this skill when an analysis worker's findings need to become report-facing
guidance. The chain is analysis worker -> leader/orchestrator -> report DOCX
worker; analysis workers do not edit the DOCX directly unless ownership is
explicitly reassigned.

## Procedure

1. Inspect the live cmux layout and confirm the worker role.
2. Assign the analysis worker read-only evidence work inside its owning path:
   - Part 1: UMC index, Table 1 indicators, Section 3.1 figures/tables.
   - Part 2: HLM outputs, model checks, Section 3.2 association wording.
   - Part 3: platform text, Bayesian/inference workflow, Section 3.3 boundaries.
3. Require compact output: proposed comment or prose, checked non-raw files,
   no-go claims, and scope caveats.
4. Have the leader verify key facts directly before editing the report.
5. Convert the evidence into the right surface:
   - DOCX reviewer comment for editor-only guidance.
   - Compact table/figure/body note for reader-facing information.
   - Report-worker brief when prose should be drafted by `report-docx-manager`.
6. Validate the DOCX or affected rendered pages when visible layout changes.

## Boundaries

- Do not include raw survey rows, private platform text, post IDs, local raw-data
  paths, secrets, `.env`, or local settings in comments or handoffs.
- Keep Part 3 examples anonymized and category-level unless the report already
  contains a safe generalized case.
- State substantive interpretation first; use numbers only as support.
- Report residual dirty files and nested-repo warnings separately from the
  completed handoff.
