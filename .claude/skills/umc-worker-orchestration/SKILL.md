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

## Boundaries

- Do not delete or move existing user files without approval.
- Do not commit raw data, private platform text, `.env`, or local settings.
- Commit from the repository that owns the changed files.

