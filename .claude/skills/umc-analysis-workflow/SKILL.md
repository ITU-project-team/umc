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
- For report figures, use a restrained academic style: clean lines, muted colors, concise labels, and no sentence-style explanatory footer inside or directly below the figure. Put interpretation in the body text and keep the figure caption formal.
- For report prose, combine this skill with `umc-report-evidence-framing` when interpreting HLM, LLM platform text analysis, Bayesian updating, Digital Desert, or policy recommendations.

## Part 3 Report Appendix Defaults

When asked to explain Section 3.3 methods, agent operation, prompt design, or
why the LLM interpretation is research-rigorous, inspect both:

- `analysis/part 3/01_text_preprocessing`
- `analysis/part 3/03_inference`

Appendix candidates should be included without requiring the user to name each
one: keyword dictionary summary, UMC relevance/dimension-classification prompt,
abductive prompt, forward prompt, sequential prompt, and judgment-synthesizer
prompt. Present them in clean role/input/rule/output tables by default.
If the user asks for prompt text "as-is", "verbatim", or "그대로", use the exact
source prompt files instead of summaries, preserve line breaks, and include
source paths in the appendix.

Do not expose raw posts, post-level identifiers, local raw-data paths, or full
post-level LLM dumps. If the full keyword dictionary is too long for the report,
include counts and representative terms in the DOCX and note the maintained
dictionary file.

## Report Handoff

1. Verify source output.
2. Update DOCX, figures, tables, or prose.
3. Render or structurally inspect the DOCX when layout matters.
4. Fix references and captions.
5. Report the touched repo status.
