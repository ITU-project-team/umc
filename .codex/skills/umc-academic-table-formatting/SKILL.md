---
name: umc-academic-table-formatting
description: Use when creating, editing, or reviewing academic tables in UMC report DOCX files, especially to keep row height compact, captions consistent, and appendix prompt/keyword tables readable.
---

# UMC Academic Table Formatting

Use this skill for report-facing tables in `/Users/ujunbin/project/umc`, especially `docs/draft_20260518.docx`.

## Core Rules

- Treat tables as academic evidence displays, not prose containers.
- Keep rows as narrow as readability allows: short labels, compact wording, small font, zero paragraph spacing, and tight cell margins.
- Put interpretation in the body text or a note below the table, not inside long table cells.
- Keep captions formal, centered, and directly attached to the table. Do not leave a caption orphaned at the bottom of a page.
- Prefer one clean table over nested tables or decorative styling.

## DOCX Compactness Defaults

When editing with `python-docx`, apply these defaults unless the existing table style clearly requires otherwise:

- table font: `8 pt` for dense numeric tables, `8.5 pt` for model tables, and `9-9.5 pt` only for short descriptive tables;
- paragraph spacing inside cells: `0 pt` before and after;
- line spacing: single;
- vertical alignment: center for short/numeric cells, top only for unavoidable prose-heavy cells;
- cell margins: top/bottom about `30-50 twips`, left/right about `60-90 twips`;
- row height: do not use large fixed heights; allow auto/at-least behavior and remove empty paragraphs;
- header: bold, compact, high contrast, and no extra blank line;
- notes: smaller than table body, directly after the table.

## Width Patterns

- Numeric/statistical tables: narrow numeric columns, wider label column.
- Model tables: first column about `34-40%`; model columns evenly split.
- Two-column prompt tables: label `25-30%`, content `70-75%`.
- Keyword appendix tables: count column no more than `10-12%`; representative terms get the widest column.
- If a cell wraps past about three visual lines, shorten the wording or move detail to a note or appendix artifact.

## Content Compression

Before changing row height mechanically, reduce table text:

- Replace sentence prose with noun phrases.
- Use abbreviations only when already defined in the report.
- Use concise headers such as `SD`, `Min`, and `Max`; define them in notes rather than forcing multi-line headers.
- Left-align text columns, center short categorical columns, and right- or decimal-align numeric/model-result columns.
- Move repeated constraints to a shared note instead of repeating them across rows.
- For appendix prompt tables, use role/input/rule/output summaries by default. If the user explicitly asks for prompts "as-is", "verbatim", or "그대로", insert the exact source prompt text in the appendix, preserve line breaks, add source path/version metadata, and use compact font/table spacing.
- For keyword dictionaries, show counts and representative terms only. Full dictionaries belong in a maintained artifact path with version/date metadata.
- Do not paste raw posts, post IDs, full post-level LLM dumps, local raw-data paths, or private data into report tables.

## Pagination Rules

- Detect actual report tables by body-order traversal: a caption paragraph matching `Table N.` or `Appendix Table A#.` immediately followed by a table. Skip figure-layout tables.
- Set caption paragraphs to `keep_with_next` and `keep_together`.
- Repeat only the true header row. Do not mark body rows as repeat headers.
- Avoid `cantSplit` on every body row; reserve no-split behavior for headers, group rows, or very short tables.
- After PDF render, flag continuation pages with `<=3` remaining rows or mostly blank space. Compress, rebalance, or move to appendix/landscape instead of accepting an orphan continuation.
- Use manual page breaks only to prevent orphan captions or broken tables, not as a default before every table.

## Review Checklist

1. Confirm the caption number and title.
2. Check whether the table can fit on one page or whether the split is acceptable.
3. Look for rows made tall by long prose, repeated labels, blank paragraphs, or oversized font.
4. Check that header, grid, font size, and alignment are consistent with adjacent tables.
5. Render DOCX to PDF and visually inspect the table pages.
6. Clean disposable render files under `tmp/` before reporting.

## When To Edit Existing Tables

Edit existing report tables only when the user asks for document changes or when the current task explicitly concerns table layout. Otherwise, report findings and update the relevant skill or agent instructions.
