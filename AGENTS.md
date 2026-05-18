# UMC Project Instructions

This file is the project-local operating contract for `/Users/ujunbin/project/umc`.

## Local Components

- Use project-local Codex skills before global fallbacks:
  - `$umc-cmux-worker-supervision`
  - `$umc-analysis-workflow`
  - `$umc-report-evidence-framing`
- Claude-facing project components live under `.claude/`.
- Codex-facing project components live under `.codex/`.
- UMC-specific skills, agents, and routing notes should stay project-local unless they are genuinely reusable across `/Users/ujunbin/project`, `/Users/ujunbin/knowledge`, `/Users/ujunbin/research`, and `/Users/ujunbin/resource`.

## Worker Orchestration

- Use functional worker labels, not decorative names:
  - `보고서 DOCX 담당`
  - `Part 1 분석 총괄`
  - `Part 2 분석 총괄`
  - `Part 3 분석 총괄`
  - `검증 담당`
- Give compact briefs with exact paths, scope boundary, evidence source, and expected output.
- Continue the leader loop after delegation: read worker results, judge sufficiency, verify important claims, and issue the next bounded instruction.

## Repository Boundaries

- Root repo: report, docs, writing, project-level coordination.
- Nested analysis repos own their own code and outputs:
  - `analysis/part 1`
  - `analysis/part 2`
  - `analysis/part 3`
  - `analysis/text-preprocessing`
  - legacy/specialized inference folders under `analysis/`.
- Commit and push from the repository that owns the changed files.
- Do not stage raw data, secrets, `.env`, local settings, or private platform text.

## Artifact Hygiene

- Use `tmp/` for disposable render/check outputs.
- Use clear durable locations such as `docs/`, `writing/`, or each analysis repo's `output/`.
- Do not delete or move existing user files without explicit approval.
- For DOCX work, preserve the active file path unless the user changes it.

## Current Report Context

- Active draft: `docs/ITU UMC Data Hackathon 2026.docx`
- Literature folder: `paper/`
- Part 3 consolidated repo: `analysis/part 3`
- Report evidence-framing term dictionary: `docs/style/umc_report_evidence_terms.json`
