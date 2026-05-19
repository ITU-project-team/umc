# UMC Claude Project Router

Use this file as the root Claude router for `/Users/ujunbin/project/umc`.

## Local Skills

- `umc-worker-orchestration`: worker assignment, cmux context, result review, and artifact hygiene.
- `umc-analysis-workflow`: Part 1, Part 2, Part 3, text preprocessing, Bayesian aggregation, inference, and report handoff.
- `umc-report-evidence-framing`: cautious HLM/LLM/Bayesian wording, exploratory-evidence limits, policy-framing alignment, and term dictionary use.
- `umc-report-theory`: Chapter 2 theory/background writing using `paper/` and the active DOCX.
- `umc-academic-table-formatting`: academic DOCX table creation/review, compact row rules, captions, appendix prompt/keyword tables, and PDF layout checks.

## Local Agents

- `report-docx-manager`: report DOCX structure, section edits, figure/table placement, and layout risk.
- `report-figure-generator`: report figure generation/repair, source-data checks, academic styling, and DOCX layout verification.
- `part1-analysis-manager`: Part 1 UMC index construction, district scores, report-ready figures/tables, and Section 3.1 handoff.
- `part2-analysis-manager`: Part 2 HLM/multilevel analysis, model outputs, validity checks, and Section 3.2 handoff.
- `part3-analysis-manager`: consolidated Part 3 text/Bayesian/inference workflow and data-boundary review.
- `project-verifier`: read-only verification of claims, paths, Git state, and protected-artifact boundaries.

Default worker mapping:

- `보고서 DOCX 담당 · report-docx-manager` -> `report-docx-manager`
- `Part 1 분석 총괄 · part1-analysis-manager` -> `part1-analysis-manager`
- `Part 2 분석 총괄 · part2-analysis-manager` -> `part2-analysis-manager`
- `Part 3 분석 총괄 · part3-analysis-manager` -> `part3-analysis-manager`
- `검증 담당 · project-verifier` -> `project-verifier`

Bounded parallel subagents are allowed for independent side checks inside each
worker's assigned boundary. Worker prompts must keep ownership explicit and
must not expose raw data, private platform text, post IDs, secrets, `.env`, or
local settings to subagents.

## Project Rules

- Keep UMC-specific Claude skills and agents in this project root.
- Nested analysis repos may keep their own `.claude` skills and agents for narrow execution details.
- Do not move or delete raw data, existing DOCX/PDF files, or local settings without explicit approval.
- Use role-based worker labels and compact worker briefs.
- Keep generated check/render files in `tmp/` unless a durable output path is specified.

## Active Paths

- Active draft: `docs/ITU UMC Data Hackathon 2026.docx`
- Literature folder: `paper/`
- Part 3 repo: `analysis/part 3`
- Report evidence-framing term dictionary: `docs/style/umc_report_evidence_terms.json`
