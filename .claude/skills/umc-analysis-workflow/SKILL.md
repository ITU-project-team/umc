---
name: umc-analysis-workflow
description: Work on UMC analysis repositories and report handoff across Part 1, Part 2, Part 3, text preprocessing, Bayesian aggregation, and inference outputs.
allowed-tools: Read, Bash
---

# UMC Analysis Workflow

Use for analysis scripts, outputs, interpretation checks, and report handoff.

## Repositories

- `analysis/part 1`: UMC index, district scores, maps, Moran/LISA, Section 3.1 figures.
- `analysis/part 2`: HLM/multilevel models and Section 3.2 interpretation.
- `analysis/part 3`: text preprocessing, Bayesian updating, structured inference, and Section 3.3 handoff.
- `analysis/text-preprocessing`: classifier support and legacy preprocessing.
- `analysis/03. Test-for-inference`, `analysis/Part 2-2`, `analysis/Part 2-4`: legacy/specialized inference sources.

## Checks

- Inspect scripts and existing outputs before changing logic.
- Keep raw/private data untracked.
- Verify report claims against source tables, figures, scripts, or validation notes.
- If analysis and report files both change, keep commits separated by owning repository.
- For Part 3 public/private boundary, include code, configs, aggregate tables, aggregate figures, and district-level summaries; exclude raw data and post-level text outputs.

## Report Handoff

1. Verify source output.
2. Update DOCX, figures, tables, or prose.
3. Render or structurally inspect the DOCX when layout matters.
4. Fix references and captions.
5. Report the touched repo status.

