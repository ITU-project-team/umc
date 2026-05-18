---
name: umc-worker-orchestration
description: Coordinate UMC cmux workers, including role labels, compact briefs, context resets, result review, artifact hygiene, and Git repository boundaries.
allowed-tools: Read, Bash
---

# UMC Worker Orchestration

Use for UMC work split across visible worker panels.

## Procedure

1. Inspect the current cmux layout before naming or assigning workers.
2. Use functional labels such as `보고서 DOCX 담당`, `Part 1 분석 총괄`, `Part 2 분석 총괄`, `Part 3 분석 총괄`, and `검증 담당`.
3. Send compact briefs with:
   - exact file or repo path;
   - target section, table, figure, script, or output;
   - scope boundary: read-only, edit allowed, or report-only;
   - evidence source;
   - expected return format.
4. Read the worker result, judge sufficiency, verify important claims directly when feasible, and send the next bounded instruction.
5. Keep temporary renders, checks, and backups under `tmp/`.

For report/DOCX work, treat the lead session as the orchestrator and verifier:

- Ask the relevant analysis worker to verify source files, result claims, prompt locations, and pipeline stages.
- Ask `보고서 DOCX 담당` or `검증 담당` to check rendered pages, figure placement, captions, appendix tables, and pagination.
- Do not treat a worker answer as completion until the important file paths or rendered pages have been checked directly.
- If the user asks for a prompt to be inserted "as-is" or "verbatim", preserve the exact source prompt text in the appendix instead of replacing it with a summary table.
- Do not add sentence-style explanatory footers inside report figures or as one-line notes directly below figures.

## Boundaries

- Do not delete or move existing user files without approval.
- Do not commit raw data, private platform text, `.env`, or local settings.
- Commit from the repository that owns the changed files.
