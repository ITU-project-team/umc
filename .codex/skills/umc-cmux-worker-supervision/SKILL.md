---
name: umc-cmux-worker-supervision
description: Use when work in `/Users/ujunbin/project/umc` is coordinated through cmux worker panes, especially when assigning report, Part 1, Part 2, text-preprocessing, git, or document-verification work and the leader must keep worker roles, context, artifacts, and repository boundaries clear.
---

# UMC cmux Worker Supervision

## Trigger

Use this skill when the active root is `/Users/ujunbin/project/umc` and any of these are true:

- The task is split across cmux worker panes.
- A worker pane needs to be named, renamed, refreshed, or reassigned.
- A report, DOCX, figure, table, or analysis output is being edited or verified.
- Git work spans the root UMC repo and one or more nested analysis repos.
- Temporary renders, backups, reports, or verification outputs may be created.

Do not use this skill for unrelated workspaces or single-command tasks that do not involve UMC worker coordination.

## First Checks

1. Confirm the current root is `/Users/ujunbin/project/umc`.
2. Inspect the live cmux layout before addressing workers:

```bash
cmux tree --workspace workspace:1
```

3. Check the relevant Git repositories before editing or committing:

```bash
git status --short --branch
git -C "analysis/part 1" status --short --branch
git -C "analysis/part 2" status --short --branch
git -C "analysis/text-preprocessing" status --short --branch
```

4. Identify the durable output location before creating files. Use `tmp/` only for disposable checks, renders, and backups.

## Worker Naming

Use functional role names, not decorative or personality-based names.

Preferred visible pane labels:

- `보고서 DOCX 담당`
- `Part 1 분석 총괄`
- `Part 2 분석 총괄`
- `Part 3 분석 총괄`
- `Text preprocessing 담당`
- `Git/배포 담당`
- `검증 담당`

Rename panes with:

```bash
cmux rename-tab --workspace workspace:1 --surface surface:<n> '<role label>'
```

After renaming, verify with:

```bash
cmux tree --workspace workspace:1
```

## Default Worker Assignments

Before sending work to a pane, map the visible worker label to an explicit
agent name and owning path. Re-check `cmux tree --workspace workspace:1` first;
surface IDs can drift, so the role label and agent name are authoritative.

Observed `workspace:1` assignment as of 2026-05-28. Verify live state before
using any surface ID; the leader surface is not an assignment target.

| Visible worker label | Current surface | Assigned agent | Primary owning path | Primary skills/rules |
| --- | --- | --- | --- | --- |
| `검증 담당 · project-verifier` | `surface:1` | `project-verifier` | touched root or nested repo paths | read-only verification; findings first; no edits |
| `보고서 DOCX 담당 · report-docx-manager` | `surface:2` | `report-docx-manager` | `docs/ITU UMC Data Hackathon 2026.docx` | `umc-report-evidence-framing`, `umc-academic-table-formatting`, `umc-report-handoff`, `doc` |
| `Part 3 분석 총괄 · part3-analysis-manager` | `surface:3` | `part3-analysis-manager` | `analysis/part 3` | `umc-analysis-workflow`, `umc-report-evidence-framing`; no raw/private text or post IDs |
| `Part 1 분석 총괄 · part1-analysis-manager` | `surface:4` | `part1-analysis-manager` | `analysis/part 1` | `umc-analysis-workflow`, `umc-report-handoff`; protect raw data and Part 1 nested repo boundary |
| `Part 2 분석 총괄 · part2-analysis-manager` | `surface:6` | `part2-analysis-manager` | `analysis/part 2` | `umc-analysis-workflow`, `umc-report-evidence-framing`, `umc-report-handoff`; HLM as association analysis |

When renaming panes, include both the worker label and assigned agent:

```bash
cmux rename-tab --workspace workspace:1 --surface surface:<n> '<worker label> · <agent-name>'
```

When briefing a worker, the first line should restate the assignment:

```text
[역할 지정] 이 패널의 담당 agent는 `<agent-name>`입니다.
```

Do not assign report DOCX edits to an analysis agent. Do not assign raw-data,
private-text, or post-level inspection to a report or verification worker.

## Parallel Subagents

Bounded parallel subagents are allowed by default for independent side checks
inside the assigned worker boundary unless the user or leader says otherwise.
Use them to split clearly separable verification, file inspection, or
implementation subtasks.

Rules:

- The worker remains responsible for integrating and judging subagent results.
- Parallel subtasks must have disjoint files, sections, scripts, outputs, or
  read-only evidence targets.
- Do not send raw data, private platform text, post IDs, secrets, `.env` files,
  or local settings into subagent prompts.
- For write tasks, state the owned file path or module for each subagent and
  forbid reverting or overwriting other workers' edits.
- For verification tasks, keep subagents read-only and require findings-first
  output with exact files, commands, or rendered pages checked.
- Report which subagents were used, what each checked or changed, and what the
  worker verified directly before returning to the leader.

## Worker Briefs

Send bounded briefs. Do not paste long transcript history into a worker.

Every worker instruction should include:

- Current file path or repo path.
- Exact section, table, figure, script, or output being checked.
- Scope boundary: read-only, edit allowed, or report-only.
- Evidence source: files, tables, rendered pages, logs, or command output.
- Expected return format: concise findings plus exact files/sections checked.
- Explicit permission that bounded parallel subagents are allowed for
  independent side checks, unless this specific task forbids it.

When a worker is likely holding stale context or nearing context pressure, instruct it to save a short status note or clear context before the new task.

Always submit the message after `cmux send`:

```bash
cmux send --workspace workspace:1 --surface surface:<n> '<brief>'
cmux send-key --workspace workspace:1 --surface surface:<n> Enter
```

Then read back the screen if the task depends on the worker actually starting:

```bash
cmux read-screen --workspace workspace:1 --surface surface:<n> --lines 40
```

## Leader Loop

The leader owns the workflow until the task is closed.

1. Assign a bounded task.
2. Confirm the worker received it.
3. Monitor completion.
4. Read and judge the worker result.
5. Verify important claims directly when feasible.
6. Send the next bounded instruction or put the worker on standby.

Do not treat delegation as completion. Report to the user only after the worker result has been reviewed and any important claims have been checked.

For report/DOCX tasks, the leader acts as orchestrator and verifier:

- Use the relevant analysis worker to verify source truth, result tables, prompt files, and pipeline steps.
- Use `$umc-report-handoff` when analysis-worker evidence must become DOCX comments, table notes, prose instructions, or report-worker briefs.
- Use `보고서 DOCX 담당` or `검증 담당` to inspect rendered pages, captions, tables, figures, and appendix placement.
- Integrate worker findings only after checking the key paths or rendered output directly.
- When the user asks to put a prompt "as-is" or "verbatim" into an appendix, do not replace it with a role/input/rule/output summary. Insert the exact source prompt text and preserve line breaks, while still excluding raw posts, private text, and post-level dumps.
- For report figures, do not add sentence-style explanatory footers inside the image or as one-line notes directly below it. Put interpretation in the body text, caption, or formal table note.

## Repository Boundaries

The root repo and analysis repos are separate Git repositories.

- Root UMC repo: `/Users/ujunbin/project/umc`
  - Tracks report, writing, docs, PPT, and project-level files.
  - Ignores `analysis/`.
- Part 1 repo: `/Users/ujunbin/project/umc/analysis/part 1`
  - Tracks Part 1 UMC index construction and Section 3.1 figure outputs.
- Part 2 repo: `/Users/ujunbin/project/umc/analysis/part 2`
  - Tracks HLM/multilevel analysis for Section 3.2.
- Text preprocessing repo: `/Users/ujunbin/project/umc/analysis/text-preprocessing`
  - Tracks text preprocessing and classification support.

Commit from the repository that owns the changed files. If a task changes both analysis outputs and a report artifact, commit the analysis repo and the root repo separately.

Before push, verify each touched repo:

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
```

After push, the expected synchronization result is:

```text
0 0
```

## Artifact Hygiene

Keep generated files tidy.

- Use `tmp/` for disposable renders, OCR output, DOCX unzip checks, screenshots, and one-off verification files.
- Use a clear backup folder such as `tmp/docs/backups/` for dated document backups.
- Keep durable outputs in the owning repo's established output folder, for example `docs/`, `writing/`, or `analysis/<part>/output/`.
- Do not scatter backups or temporary render pages in main folders.
- Remove disposable render/check folders before final reporting unless the user explicitly asks to keep them.
- Do not delete or move existing user files without explicit approval.

## Approval Boundaries

Proceed autonomously for normal inspection, bounded worker instructions, README/doc edits, non-destructive verification, commits, and pushes when the user explicitly asks for that flow.

Pause for approval before:

- Deleting or moving existing user files.
- Rewriting raw data or private inputs.
- Resetting, restoring, or discarding changes not made by the current task.
- Broadening a worker's scope beyond the assigned analysis/report boundary.
- Taking externally visible actions that were not requested.

## Final Report Checklist

Before reporting completion:

- Current worker labels are role-based and match ownership.
- Workers that were assigned have either reported completion or are explicitly on standby.
- Important worker claims were checked directly where feasible.
- Disposable files were cleaned.
- The touched Git repos are clean or clearly reported as dirty.
- Any commits/pushes include commit hashes and repository names.
- Any residual risk or skipped verification is stated plainly.
