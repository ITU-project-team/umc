# UMC Codex Components

This folder is the project-local Codex component layer for UMC.

## Skills

- `skills/umc-cmux-worker-supervision/SKILL.md`: cmux worker ownership, worker briefs, context hygiene, artifact placement, and repository boundaries.
- `skills/umc-analysis-workflow/SKILL.md`: Part 1, Part 2, Part 3, text preprocessing, inference, report handoff, and verification workflow.
- `skills/umc-academic-table-formatting/SKILL.md`: academic DOCX table creation/review, compact row rules, captions, appendix prompt/keyword tables, and PDF layout checks.

## Agents

- `agents/report-docx-manager.toml`: report DOCX editing, section structure, figures, academic tables, captions, and layout-risk verification.
- `agents/report-figure-generator.toml`: report figure generation and repair, source-data checks, consistent academic styling, and DOCX figure layout verification.

## Scope Rule

Keep UMC-specific Codex components here. Do not place UMC-only skills or agents in `/Users/ujunbin/.codex` unless the user explicitly asks for a global capability.

## Maintenance

After changing skills or agents:

```bash
python3 /Users/ujunbin/.codex/scripts/check-agent-skill-links.sh --json
```

For substantial local component changes, write provenance under `.codex/logs/`.
