# UMC Codex Components

This folder is the project-local Codex component layer for UMC.

## Skills

- `skills/umc-cmux-worker-supervision/SKILL.md`: cmux worker ownership, worker briefs, context hygiene, artifact placement, and repository boundaries.
- `skills/umc-analysis-workflow/SKILL.md`: Part 1, Part 2, Part 3, text preprocessing, inference, report handoff, and verification workflow.
- `skills/umc-report-evidence-framing/SKILL.md`: cautious HLM/LLM/Bayesian wording, exploratory-evidence limits, policy-framing alignment, and term dictionary use.
- `skills/umc-academic-table-formatting/SKILL.md`: academic DOCX table creation/review, compact row rules, captions, appendix prompt/keyword tables, and PDF layout checks.

## Agents

- `agents/report-docx-manager.toml`: report DOCX editing, section structure, figures, academic tables, captions, and layout-risk verification.
- `agents/report-figure-generator.toml`: report figure generation and repair, source-data checks, consistent academic styling, and DOCX figure layout verification.

Default worker mapping:

- `보고서 DOCX 담당 · report-docx-manager` -> `agents/report-docx-manager.toml`
- `Part 1 분석 총괄 · part1-analysis-manager` -> cmux role prompt plus `skills/umc-analysis-workflow/SKILL.md`, owning path `analysis/part 1`
- `Part 2 분석 총괄 · part2-analysis-manager` -> cmux role prompt plus `skills/umc-analysis-workflow/SKILL.md`, owning path `analysis/part 2`
- `Part 3 분석 총괄 · part3-analysis-manager` -> Claude agent `.claude/agents/part3-analysis-manager.md` plus `skills/umc-analysis-workflow/SKILL.md`, owning path `analysis/part 3`
- `검증 담당 · project-verifier` -> Claude agent `.claude/agents/project-verifier.md`, read-only verification across touched paths

Bounded parallel subagents are allowed for independent side checks inside each
worker's assigned boundary. Worker prompts must keep ownership explicit and
must not expose raw data, private platform text, post IDs, secrets, `.env`, or
local settings to subagents.

## Scope Rule

Keep UMC-specific Codex components here. Do not place UMC-only skills or agents in `/Users/ujunbin/.codex` unless the user explicitly asks for a global capability.

## Maintenance

After changing skills or agents:

```bash
python3 /Users/ujunbin/.codex/scripts/check-agent-skill-links.sh --json
```

For substantial local component changes, write provenance under `.codex/logs/`.
