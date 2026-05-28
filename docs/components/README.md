# UMC External Components

This directory stores reusable project components outside the report body.
Use these files as the managed source for presentation, report, and verifier
workflows that need the project pipeline or data-source inventory.

## Components

- `umc_data_sources_20260521.json`
  - Data-source registry.
  - Source authority: `ppt/High-Five_20260507.pptx`, especially slides 2-5.
  - Keep this file aligned with the PPT when source coverage, links, or access
    routes change.

- `umc_ppt_source_evidence_20260528.json`
  - PPT-first source-evidence component for report revisions.
  - Source authority: `ppt/High-Five_20260507.pptx`; use existing components
    as secondary references only.
  - Covers source notes for SKT, affordability, 5G base-station mapping, and
    Danggeun data-scope wording raised in mentor feedback.

- `umc_analysis_pipeline_20260521.json`
  - Analysis pipeline registry for Sections 3.1, 3.2, and 3.3.
  - Covers scripts, inputs, outputs, validation checks, report artifacts, and
    the Section 3.3 agent pipeline.

- `report_analysis_sync_gate_20260521.json`
  - Project-local warning gate metadata for analysis-to-report handoff checks.
  - Covers the checker, configuration, sync rule, monitored repo boundaries, and
    privacy-safe output policy.
  - Its shared configuration lives in `config/report_analysis_lag.json`, not in
    separate Codex-only or Claude-only config copies.

## Boundary

These components must not contain raw post text, post IDs, user identifiers,
local credentials, or private data values. They can reference local paths and
aggregate outputs.

## Update Rule

When a source file, script, prompt, output table, or report figure changes, add
a new dated component file or update the current dated component if the change
is part of the same revision cycle. Preserve the PPT and repository paths used
as evidence.
