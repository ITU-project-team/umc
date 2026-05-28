---
name: umc-academic-table-formatting
description: Use when creating, editing, or reviewing UMC report DOCX academic tables, especially Table 4-style HLM/model-result tables, compact evidence tables, and appendix prompt/keyword tables.
allowed-tools: Read, Bash
---

# UMC Academic Table Formatting

Use for report-facing tables in `/Users/ujunbin/project/umc`, especially `docs/ITU UMC Data Hackathon 2026.docx`.

When the user asks for tables like "Table 4", use `Table 4. HLM Estimation Results` in `docs/ITU UMC Data Hackathon 2026.docx` as the visual reference.

## Rules

- Tables are evidence displays, not prose containers.
- Keep rows compact: short labels, compact wording, small font, zero paragraph spacing, and tight cell margins.
- Put interpretation in body text or a note, not in long table cells.
- Keep captions formal and attached to the table. Avoid captions stranded at page bottoms.
- Do not use nested or decorative tables.

## DOCX Defaults

- Dense numeric tables and Table 4-style model tables: Arial `8 pt`; short descriptive tables: `9-9.5 pt`.
- Cell paragraphs: `0 pt` before/after, single spacing.
- Vertical alignment: center for short/numeric cells, top only for unavoidable prose-heavy cells.
- Cell margins: top/bottom `30-50 twips`; left/right `60-90 twips`.
- Header row: bold, compact, gray fill, high contrast, no blank line.
- Avoid fixed tall rows; remove empty cell paragraphs.

## Table 4 Model-Result Pattern

- Use for HLM, regression, and comparable multi-model result tables unless the table has a stronger local precedent.
- Caption: centered `Caption` style, italic report caption text, immediately above the table.
- Table: near full text width, `List Table 1 Light` when working in the active DOCX; otherwise reproduce its visible effect.
- Columns: `Variable` plus model columns. For four models, use about `30% / 21% / 16% / 16% / 16%`; keep the first column wide enough for variable labels and center model estimates.
- Header: gray fill (`D9D9D9` or matching theme shade), bold centered labels, double top/bottom rules.
- Body: first column left aligned; model-result columns centered; Arial `8 pt`; no paragraph spacing.
- Group rows: use short labels such as `Level 1: Individual characteristics`, `Level 2: District characteristics`, and `Retained interactions`; leave model cells blank, keep the group label bold, and separate major groups with horizontal double rules.
- Borders: keep vertical separators visible and thin; use double horizontal rules at the table top, below the header, above major group rows, and at the table bottom.
- Emphasis: preserve sparse yellow highlighting only when the source table or user explicitly marks estimates for emphasis; do not invent highlights.
- Notes: put reference categories, model variants, and significance markers in a compact `9 pt` note below the table, not inside body cells.

## Width Patterns

- Numeric/statistical tables: narrow numeric columns and a wider label column.
- Table 4-style model tables: first column about `30%`; model columns split by content length, with the widest model column around `20-21%` if needed.
- Prompt tables: label `25-30%`, content `70-75%`.
- Keyword appendix tables: count column `10-12%` maximum; representative terms get the widest column.
- If a cell wraps beyond about three visual lines, shorten it or move detail to a note/artifact.

## Compact Content

- Use noun phrases instead of sentence prose in cells.
- Use concise headers such as `SD`, `Min`, and `Max`; define them in notes.
- Left-align text columns, center short categorical columns, and right- or decimal-align numeric/model-result columns.
- Repeat only the true header row. Do not mark body rows as repeat headers.
- Avoid `cantSplit` on every body row; reserve it for headers, group rows, or very short tables.

## Appendix Rules

- Prompt tables summarize role/input/rule/output by default. If the user explicitly asks for prompts "as-is", "verbatim", or "그대로", insert the exact source prompt text in the appendix, preserve line breaks, add source path/version metadata, and use compact font/table spacing.
- Keyword tables show counts and representative terms only.
- Full prompts and dictionaries belong in maintained appendix artifacts with path/date/version metadata.
- Never include raw posts, post IDs, post-level LLM dumps, local raw-data paths, or private data in report tables.

## Pagination Rules

- Detect report tables by body-order traversal: a caption matching `Table N.` or `Appendix Table A#.` immediately followed by a table. Skip figure-layout tables.
- Set captions to keep with the following table.
- After PDF render, flag continuation pages with `<=3` rows or mostly blank space.
- Do not insert manual page breaks before tables unless the break prevents an orphan caption or broken table.

## Review

1. Check caption number and title.
2. Check page split and orphaned captions.
3. Find rows made tall by prose, repeated labels, blank paragraphs, or large font.
4. Render to PDF and inspect visually.
5. Keep disposable render files under `tmp/` and clean them before reporting.
