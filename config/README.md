# UMC Project Config

This directory is the single shared location for project-level configuration
used by both Codex and Claude workflows.

## Files

- `report_analysis_lag.json`
  - Shared configuration for the warning-only report-analysis sync gate.
  - Loaded by `.codex/hooks/report_analysis_lag_check.py`.
  - Referenced by Codex and Claude router files as the canonical settings path.

## Boundary

Do not store raw data, private platform text, post IDs, secrets, `.env` values,
or local machine settings in this directory.

## Shared Policy

Codex and Claude project routers must both use this directory as the shared
configuration source. Bounded parallel subagents are allowed only for
independent side checks inside an assigned worker boundary and must not receive
raw data, private platform text, post IDs, secrets, `.env` values, or local
settings.
