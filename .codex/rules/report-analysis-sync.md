# UMC Report-Analysis Sync Gate

This project-local gate warns when report-relevant analysis work may not have
been handed off to the root report artifacts yet. It is warning-only by default:
it never blocks Codex or Claude Stop hooks, and it must not inspect raw data,
private platform text, post IDs, secrets, `.env` files, local settings, existing
PDFs, or existing DOCX contents.

## Manual Check

Run from `/Users/ujunbin/project/umc`:

```bash
python3 .codex/hooks/report_analysis_lag_check.py
```

For machine-readable output:

```bash
python3 .codex/hooks/report_analysis_lag_check.py --json
```

For manual CI-style checks where warnings should fail the command:

```bash
python3 .codex/hooks/report_analysis_lag_check.py --strict
```

## Stop Hook Behavior

Controller-level hook registration is handled outside this project. When the
checker is called as:

```bash
python3 .codex/hooks/report_analysis_lag_check.py --hook stop
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

Path patterns and privacy exclusions live in
`.codex/config/report_analysis_lag.json`.

## When A Warning Fires

1. Inspect the named repo counts and timestamps in the manual or JSON report.
2. Verify whether the changed analysis outputs, scripts, or report-facing tables
   require a DOCX, figure, table, prose, or component update in the root repo.
3. Update root report-facing artifacts only when needed. Do not touch raw data,
   private text, post IDs, `.env`, existing PDFs/DOCX contents, or local
   settings unless the user explicitly asks.
4. Commit nested analysis repos separately from root report changes.
5. Re-run the checker and the task-specific analysis/report verification.
