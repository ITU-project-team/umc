# UMC Data Hackathon 2026

This repository is the document and coordination repository for the UMC Data Hackathon 2026 project. It brings together final reports, presentation materials, manuscript drafts, figures, and project-level documentation for the Seoul Digital Connectivity Report.

The analysis itself is split across separate nested Git repositories under `analysis/`. This root repository intentionally treats `analysis/` as an external analysis area and tracks the project-facing documents and writing artifacts.

## Project Overview

The project studies Universal Meaningful Connectivity (UMC) in Seoul. It combines district-level connectivity indicators, individual-level Seoul Survey responses, and report writing artifacts to identify digital connectivity gaps and policy-relevant vulnerable groups.

The current report focuses on:

- district-level UMC index construction and spatial diagnostics
- individual and district characteristics associated with digital service use
- interpretation of digital connectivity gaps in Seoul
- final English and Korean report artifacts for the ITU UMC Data Hackathon

## Repository Layout

```text
.
|-- docs/       # Final and dated report files, exported PDFs, and report figures
|-- config/     # Shared project configuration used by Codex and Claude workflows
|-- writing/    # Manuscript drafts, generated writing outputs, figures, and tables
|-- ppt/        # Presentation materials
|-- others/     # Administrative and supporting project files
|-- analysis/   # Separate nested analysis repositories; ignored by this root repo
|-- tmp/        # Local temporary files and backups; ignored by git
`-- README.md
```

## Main Report Artifacts

Key project-level deliverables include:

| Path | Description |
| --- | --- |
| `docs/ITU UMC Data Hackathon 2026.docx` | Current working English report file |
| `docs/UMC_report_kr_20260516.docx` | Korean report version |
| `docs/UMC_report_en.pdf` | Exported English report PDF |
| `docs/figures/` | Figure assets used in report production |
| `docs/components/` | Reusable project components for report, presentation, source-evidence, and verification workflows |
| `docs/components/umc_ppt_source_evidence_20260528.json` | PPT-first source-evidence component for mentor-feedback report revisions |
| `config/report_analysis_lag.json` | Shared Codex/Claude report-analysis sync gate configuration |
| `writing/manuscript/` | Manuscript-generation workspace and archived outputs |
| `ppt/High-Five_20260507.pptx` | Presentation deck |

## Analysis Repositories

The main analysis folders are managed as separate Git repositories:

| Folder | Remote | Role |
| --- | --- | --- |
| `analysis/part 1/` | `ITU-project-team/part1` | District-level UMC index construction and Section 3.1 figures |
| `analysis/part 2/` | `ITU-project-team/part2` | Multilevel analysis of individual and district characteristics |
| `analysis/text-preprocessing/` | `ITU-project-team/text-preprocessing` | Text preprocessing and classification support |

Because these folders are nested repositories, commit and push analysis changes from inside the relevant analysis folder. Commit report, writing, and presentation changes from this root repository.

## Working Conventions

- Keep raw data, secrets, local temporary files, and backup renders out of git.
- Use `tmp/` for disposable checks and document backups.
- Keep report-ready files under `docs/` and manuscript-generation files under `writing/`.
- When a report figure or table changes, update the source analysis repository first, then update the report artifact in this root repository.
- Before publishing, verify that the root repository and any touched analysis repository are clean and synchronized with their remotes.

## Quick Git Checks

Check the root repository:

```bash
git status --short --branch
```

Check a nested analysis repository:

```bash
git -C "analysis/part 2" status --short --branch
```

After committing and pushing, verify synchronization:

```bash
git rev-list --left-right --count HEAD...origin/main
```

The expected synchronized result is `0 0`.
