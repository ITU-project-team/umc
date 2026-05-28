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

## Default Worker Assignments

Re-check `cmux tree --workspace workspace:1` before assigning work. Surface IDs
can drift; the worker label and agent name are authoritative.

Observed `workspace:1` assignment as of 2026-05-28. Verify live state before
using any surface ID; the worker label and agent name are authoritative.

| Visible worker label | Current surface | Assigned agent | Owning path | Primary skills/rules |
| --- | --- | --- | --- | --- |
| `검증 담당 · project-verifier` | `surface:1` | `project-verifier` | touched root or nested repo paths | read-only verification; findings first |
| `보고서 DOCX 담당 · report-docx-manager` | `surface:2` | `report-docx-manager` | `docs/ITU UMC Data Hackathon 2026.docx` | `umc-report-evidence-framing`, `umc-academic-table-formatting`, `umc-report-handoff` |
| `Part 3 분석 총괄 · part3-analysis-manager` | `surface:3` | `part3-analysis-manager` | `analysis/part 3` | `umc-analysis-workflow`, `umc-report-evidence-framing`; no raw/private text or post IDs |
| `Part 1 분석 총괄 · part1-analysis-manager` | `surface:4` | `part1-analysis-manager` | `analysis/part 1` | `umc-analysis-workflow`, `umc-report-handoff`; protect raw data |
| `Part 2 분석 총괄 · part2-analysis-manager` | `surface:6` | `part2-analysis-manager` | `analysis/part 2` | `umc-analysis-workflow`, `umc-report-evidence-framing`, `umc-report-handoff`; HLM as association analysis |

Begin worker briefs with:

```text
[역할 지정] 이 패널의 담당 agent는 `<agent-name>`입니다.
```

## Parallel Subagents

Bounded parallel subagents are allowed by default for independent side checks
inside the worker's assigned path and scope, unless the leader says otherwise.

- The worker owns integration and final judgment.
- Split only disjoint files, sections, scripts, outputs, or read-only evidence targets.
- Do not pass raw data, private platform text, post IDs, secrets, `.env`, or local settings to subagents.
- Keep verification subagents read-only and require findings-first output with exact files or commands checked.
- For write subtasks, state the owned file path or module and forbid reverting other workers' edits.
- Report what each subagent checked or changed before returning to the leader.

For report/DOCX work, treat the lead session as the orchestrator and verifier:

- Ask the relevant analysis worker to verify source files, result claims, prompt locations, and pipeline stages.
- Use `umc-report-handoff` when analysis-worker evidence must become DOCX comments, table notes, prose instructions, or report-worker briefs.
- Ask `보고서 DOCX 담당` or `검증 담당` to check rendered pages, figure placement, captions, appendix tables, and pagination.
- Do not treat a worker answer as completion until the important file paths or rendered pages have been checked directly.
- If the user asks for a prompt to be inserted "as-is" or "verbatim", preserve the exact source prompt text in the appendix instead of replacing it with a summary table.
- Do not add sentence-style explanatory footers inside report figures or as one-line notes directly below figures.

## Boundaries

- Do not delete or move existing user files without approval.
- Do not commit raw data, private platform text, `.env`, or local settings.
- Commit from the repository that owns the changed files.
