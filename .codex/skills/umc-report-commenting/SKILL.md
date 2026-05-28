---
name: umc-report-commenting
description: Use when adding, reviewing, or resolving UMC report comments, annotations, footnotes, table notes, appendix notes, or reviewer-style DOCX comments in `/Users/ujunbin/project/umc`, especially when Codex must mark an issue without rewriting report prose or must add a compact reader-facing note safely.
---

# UMC Report Commenting

Use this skill for annotation work in the UMC report workflow, especially the active draft `docs/ITU UMC Data Hackathon 2026.docx`.

## Choose the Note Type

- Use a DOCX reviewer comment when the note is for the author/editor and should not become final report text.
- Use a table note or figure note when the information is reader-facing and belongs with the display.
- Use a footnote only for source, definition, or scope clarification that would interrupt the paragraph.
- Use an inline bracketed note only in scratch drafts or when the user explicitly asks for visible inline annotations.

## Comment Rules

- Anchor comments to the smallest exact text range, table cell, caption, or figure reference that needs attention.
- Keep each comment to one issue and one requested action.
- Start comments with a short category when useful: `Evidence:`, `Formatting:`, `Source:`, `Privacy:`, or `Decision:`.
- Do not put raw posts, post IDs, private platform text, local raw-data paths, `.env` values, or secrets in comments or notes.
- Use anonymized paraphrase for Part 3 examples and privacy-sensitive evidence.
- Do not use comments to carry final interpretation. Move accepted interpretation into the body text or a compact display note.

## DOCX Comments

- Prefer `python-docx` comments when available: locate the target paragraph/run, call `Document.add_comment(runs, text, author="UMC reviewer", initials="UMC")`, and save the same document only after confirming the target.
- If the target text spans part of a run, split the run first so the comment anchors only the intended phrase.
- If the installed `python-docx` does not support comments, add comments through OOXML only after inspecting the existing `word/comments.xml` and relationship IDs.
- After adding comments, reopen the DOCX and verify comment count, anchor text, author, and comment text.
- PDF renders usually do not show Word comments; use PDF rendering only to verify visible footnotes, table notes, figure notes, and pagination.

## Reader-Facing Notes

- Keep table and figure notes compact: explain abbreviations, reference categories, model variants, source scope, or significance markers.
- Put table notes directly below the table in 8-9 pt style unless a stronger local precedent exists.
- Do not duplicate details already clear from captions, column headers, or surrounding prose.
- For Table 4-style model tables, keep reference categories and significance markers in a single compact note below the table.

## Review

1. Confirm whether the user wants reviewer comments or visible report notes.
2. Locate the exact target and avoid broad document-wide annotation.
3. Add the comment or note with privacy-safe wording.
4. Reopen or render the artifact as appropriate.
5. Report the number and location of comments or visible notes added.
