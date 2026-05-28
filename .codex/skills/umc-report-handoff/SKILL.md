---
name: umc-report-handoff
description: Use in `/Users/ujunbin/project/umc` when Part 1, Part 2, or Part 3 analysis-worker evidence must be converted into report-safe DOCX comments, table notes, prose handoffs, or report-worker instructions without exposing raw data, private text, post IDs, or local raw paths.
---

# UMC Report Handoff

## Overview

Use this skill to move analysis evidence into the report through a controlled
worker chain: analysis worker -> leader/orchestrator -> report DOCX worker.
It is for handoff, verification, and safe wording; it is not a license for
analysis workers to edit the report directly.

## Trigger

Use this skill for tasks such as:

- Table 1 indicator/source notes from Part 1 into DOCX comments or table notes.
- Section 3.1/3.2/3.3 evidence checks that need report-safe prose.
- HLM or Part 3 interpretation updates where analysis claims must be bounded.
- Passing reviewer feedback from analysis owners to `report-docx-manager`.

Also use `$umc-cmux-worker-supervision` for pane routing, `$umc-report-commenting`
for DOCX comments, `$umc-report-evidence-framing` for interpretation wording,
and `$doc` when editing or validating the DOCX.

## Workflow

1. Re-check the live workspace:

```bash
cmux tree --workspace workspace:1
git status --short --branch
```

2. Assign the analysis worker read-only evidence work.
   - Part 1 owns UMC index construction, Table 1 indicators, Section 3.1
     figures/tables, and source notes.
   - Part 2 owns HLM/multilevel outputs, model validity, and Section 3.2
     association wording.
   - Part 3 owns platform text, Bayesian/inference workflow, and Section 3.3
     exploratory evidence boundaries.
   - Allow bounded parallel subagents only for independent read-only checks
     inside that worker's owning path.

3. Require a compact worker return:
   - finding or proposed comment text;
   - exact non-raw files or outputs checked;
   - claims that must not be made;
   - privacy or scope caveats.

4. The leader verifies the key facts directly before touching the report.
   Check at least the relevant codebook/output/script lines, rendered page,
   or document anchor when feasible. Do not delegate final judgment.

5. Convert evidence into report-safe form.
   - For editor-only guidance, add Word comments with `$umc-report-commenting`.
   - For reader-facing information, add compact table/figure/body notes.
   - For interpretive text, state the substantive finding first and numbers
     second; avoid causal, prevalence, or representativeness overclaims.

6. Brief `보고서 DOCX 담당 · report-docx-manager`.
   Include the active DOCX path, comment anchors or section anchors, the
   intended reader-facing output, and the no-go claims. Analysis workers should
   not edit the DOCX unless the leader explicitly reassigns ownership.

7. Validate and report.
   Reopen the DOCX or render when visible layout changed, run project link
   checks after capability edits, and report residual dirty files or nested-repo
   warnings separately from the completed handoff.

## Output Contract

A finished handoff should say:

- which worker was used and whether it stayed read-only;
- what was added to the DOCX or passed to the report worker;
- which files or outputs the leader checked directly;
- what remains dirty, blocked, or awaiting later report writing.

## Boundaries

- Never put raw survey rows, private platform text, post IDs, local raw-data
  paths, secrets, `.env` values, or local settings into comments or handoffs.
- Keep UMC-only skills and agents project-local under `.codex/` and `.claude/`
  unless the user explicitly asks for a global reusable capability.
- Commit root and nested analysis repos separately when publication is requested.
