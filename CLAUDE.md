# UMC Claude Project Router

Use this file as the root Claude router for `/Users/ujunbin/project/umc`.

## Project Topic

An Integrated Methodology for Measuring Universal and Meaningful Connectivity (UMC) in a Hyper-Connected City

Report target: full report; the current draft is incomplete.

## Local Agents

- `report-docx-manager`: report DOCX structure, section edits, figure/table placement, and layout risk.
- `report-figure-generator`: report figure generation/repair, source-data checks, academic styling, and DOCX layout verification.
- `part1-analysis-manager`: Part 1 UMC index construction, district scores, report-ready figures/tables, and Section 3.1 handoff.
- `part2-analysis-manager`: Part 2 HLM/multilevel analysis, model outputs, validity checks, and Section 3.2 handoff.
- `part3-analysis-manager`: consolidated Part 3 text/Bayesian/inference workflow and data-boundary review.
- `project-verifier`: read-only verification of claims, paths, Git state, and protected-artifact boundaries.

Bounded parallel subagents are allowed for independent side checks inside each
worker's assigned boundary. Worker prompts must keep ownership explicit and
must not expose raw data, private platform text, post IDs, secrets, `.env`, or
local settings to subagents.

## Project Rules

- Keep UMC-specific Claude skills and agents in this project root.
- Nested analysis repos may keep their own `.claude` skills and agents for narrow execution details.
- Keep shared project settings in `config/`; Codex and Claude routers should point to the same config paths.
- Do not move or delete raw data, existing DOCX/PDF files, or local settings without explicit approval.
- Use role-based worker labels and compact worker briefs.
- Keep generated check/render files in `tmp/` unless a durable output path is specified.

## Report Front Matter and Result Framing

- Front matter page 2 should present the user-authored Problem Statement; page 3 should present the Key Results Summary. Keep both pages independent from chapter numbering.
- Write front-matter pages in English unless the user explicitly requests another language.
- Result summaries must prioritize substantive interpretation over numeric dashboarding. Do not lead with multipliers, ICC values, p-values, row counts, or other isolated numbers.
- State what the evidence shows: district differences are dimension-specific; the HLM results do not support a statistically meaningful general relationship between district-level conditions and individual digital use; individual vulnerability explains more of the digital-use divide; platform text and Bayesian updating are exploratory evidence-integration signals, not prevalence estimates or causal proof.
- Use numbers only as secondary support after the finding has been stated in words.

## Active Paths

- Active draft: `docs/ITU UMC Data Hackathon 2026.docx`
- Literature folder: `paper/`
- Part 1~3 repo: `analysis/part 1~3`
- Report evidence-framing term dictionary: `docs/style/umc_report_evidence_terms.json`
- PPT-first source-evidence component: `docs/components/umc_ppt_source_evidence_20260528.json`
- Shared report-analysis sync config: `config/report_analysis_lag.json`
