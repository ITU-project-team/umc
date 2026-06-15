# UMC Report-Analysis Sync Gate

This project-local gate warns when report-relevant analysis work may not have
been handed off to the root report artifacts yet. It is warning-only by default:
it never blocks Codex or Claude Stop hooks, and it must not inspect raw data,
private platform text, post IDs, secrets, `.env` files, local settings, existing
PDFs, or existing DOCX contents.

## Manual Check

Run from `/Users/ujunbin/project/umc`:

```bash
python3 scripts/hooks/report_analysis_lag_check.py
```

For machine-readable output:

```bash
python3 scripts/hooks/report_analysis_lag_check.py --json
```

For manual CI-style checks where warnings should fail the command:

```bash
python3 scripts/hooks/report_analysis_lag_check.py --strict
```

## Hook Activation Policy

Only this lag check is wired as an automatic hook; every other project rule
(tmp-path discipline, no unauthorized raw-data deletion, evidence-level framing,
privacy boundaries) stays prose-enforced and is confirmed after the fact by
`project-verifier` and its split verification roles. The hook is warning-only and
fails open, so a missing script or config never blocks a worker.

Both controllers register the same project-local checker and nothing more:

- Codex: global registration in `/Users/ujunbin/.codex/hooks.json`.
- Claude: project-scoped `SubagentStop` hook in `.claude/settings.local.json`,
  matching `report-docx-manager`, `report-prose-writer`, `report-method-explainer`,
  `report-evidence-boundary-editor`, `report-appendix-curator`, `report-figure-generator`,
  `reader-comprehension-verifier`, and the `part1`/`part2`/`part3` analysis managers. Claude `Stop` hooks ignore
  `matcher`, so `SubagentStop` is used to fire only when a report or analysis
  worker finishes — not on every main-loop turn.

The canonical checker path is `paths.hooks.report_analysis_lag_check`
(`scripts/hooks/report_analysis_lag_check.py`), shared by both controllers.

## Stop Hook Behavior

When the checker is called as:

```bash
python3 scripts/hooks/report_analysis_lag_check.py --hook stop
```

it emits `{"continue": true}` when no warnings exist. If warnings exist, it
emits Stop-hook JSON with `continue` set to `true` and `systemMessage` set to a
concise report-analysis lag warning. The process still exits `0`.

If the hook is invoked while the current working directory is outside the UMC
project root, it returns `0` with no output.

If hook input is missing, malformed, or missing an absolute `cwd`, the checker
fails open by emitting `{"continue": true}` and exiting `0`.

## What The Gate Checks

- Report-relevant dirty changes in nested analysis repositories:
  `analysis/part 1`, `analysis/part 2`, and `analysis/part 3`.
- Report-facing dirty changes in the root repo: the active report DOCX path,
  `docs/components`, `docs/reviews`, `docs/figures`, `writing`, and the local
  report-analysis sync hook/config/rule/skill files.
- Latest relevant analysis commit timestamp versus the latest root
  report-facing commit timestamp, so a clean analysis worktree can still warn if
  analysis was committed after the last report-facing root update.

Path patterns and privacy exclusions live in the shared project config:
`config/report_analysis_lag.json`.

## When A Warning Fires

1. Inspect the named repo counts and timestamps in the manual or JSON report.
2. Verify whether the changed analysis outputs, scripts, or report-facing tables
   require a DOCX, figure, table, prose, or component update in the root repo.
3. Update root report-facing artifacts only when needed. Do not touch raw data,
   private text, post IDs, `.env`, existing PDFs/DOCX contents, or local
   settings unless the user explicitly asks.
4. Commit nested analysis repos separately from root report changes.
5. Re-run the checker and the task-specific analysis/report verification.
