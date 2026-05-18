# UMC Claude Project Router

Use this file as the root Claude router for `/Users/ujunbin/project/umc`.

## Local Skills

- `umc-worker-orchestration`: worker assignment, cmux context, result review, and artifact hygiene.
- `umc-analysis-workflow`: Part 1, Part 2, Part 3, text preprocessing, Bayesian aggregation, inference, and report handoff.
- `umc-report-theory`: Chapter 2 theory/background writing using `paper/` and the active DOCX.
- `umc-academic-table-formatting`: academic DOCX table creation/review, compact row rules, captions, appendix prompt/keyword tables, and PDF layout checks.

## Local Agents

- `report-docx-manager`: report DOCX structure, section edits, figure/table placement, and layout risk.
- `report-figure-generator`: report figure generation/repair, source-data checks, academic styling, and DOCX layout verification.
- `part3-analysis-manager`: consolidated Part 3 text/Bayesian/inference workflow and data-boundary review.
- `project-verifier`: read-only verification of claims, paths, Git state, and protected-artifact boundaries.

## Project Rules

- Keep UMC-specific Claude skills and agents in this project root.
- Nested analysis repos may keep their own `.claude` skills and agents for narrow execution details.
- Do not move or delete raw data, existing DOCX/PDF files, or local settings without explicit approval.
- Use role-based worker labels and compact worker briefs.
- Keep generated check/render files in `tmp/` unless a durable output path is specified.

## Active Paths

- Active draft: `docs/draft_20260518.docx`
- Literature folder: `paper/`
- Part 3 repo: `analysis/part 3`
