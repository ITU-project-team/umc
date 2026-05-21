# UMC Human Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reproducible human-validation procedure for the 14만 keyword-candidate to `Y/N/?` UMC classification pipeline, then rerun Bayesian outputs only after verified label corrections are applied.

**Architecture:** Keep original LLM labels immutable and write human decisions into separate validation artifacts. Build an internal reviewer CSV with minimal text snippets for human review, convert reviewed rows into a correction table, then create an audited classified CSV for downstream Bayesian reruns. Public/report-facing outputs must remain aggregate and must not expose raw text, post IDs, nicknames, or URLs.

**Tech Stack:** Python, pandas, pytest, CSV/JSON manifests, existing UMC Part 3 scripts under `analysis/part 3/01_text_preprocessing` and `analysis/part 3/02_bayesian`.

---

## Baseline Checked On 2026-05-21

- `analysis/part 3/data/processed/phase03_parsed/*.csv`: 3,004 parsed files, 149,484 raw parsed rows.
- `analysis/part 3/data/processed/02_keyword_filtered.csv`: 149,733 keyword-filtered candidate rows.
- `analysis/part 3/02_bayesian/data/processed/03_umc_classified.csv`: 131,792 classified safe-metadata rows.
- Current safe classified distribution: `Y=7,136`, `N=122,509`, `?=2,147`.
- Current Bayesian signal count is not 14만. It is the district-dimension evidence derived from `Y` rows and dimensions.

## File Structure

- Create `analysis/part 3/01_text_preprocessing/docs/human_validation_protocol.md`
  - Human codebook, reviewer instructions, decision labels, adjudication rule, privacy boundary.
- Create `analysis/part 3/01_text_preprocessing/scripts/build_human_validation_set.py`
  - Joins parsed labels to keyword-filtered text internally and writes reviewer workbooks under ignored `data/validation/`.
- Create `analysis/part 3/01_text_preprocessing/scripts/apply_human_validation.py`
  - Applies reviewed labels to produce `data/validation/03_umc_classified_human_audited.csv` and a manifest.
- Create `analysis/part 3/01_text_preprocessing/tests/test_human_validation.py`
  - Unit tests for sampling, correction application, label validity, and privacy-safe public manifest generation.
- Optionally modify `analysis/part 3/02_bayesian/scripts/phase_a/build_safe_dong_inputs.py`
  - Add an explicit `--classified-csv` input only if rerunning Bayesian from the audited CSV cannot be handled cleanly through the existing `--parsed-glob` and `--source-csv` interface.

## Human Validation Design

Use three validation strata, because validating only current `Y` rows measures precision but misses false negatives.

1. **Y precision audit**
   - Recommended first pass: all `Y` rows if reviewer capacity allows, because current `Y` is 7,136.
   - If capacity is limited: at least 1,200 stratified `Y` rows by district and dimension, with minimum cell coverage for sparse district-dimension cells.

2. **Ambiguous `?` resolution**
   - Review all 2,147 `?` rows.
   - Final human labels must be `Y` or `N`; keep a separate `human_uncertain` flag only when adjudication cannot resolve.

3. **False-negative audit from `N`**
   - Sample at least 1,500 `N` rows.
   - Oversample high-risk `N` rows where keyword dimensions suggest UMC relevance, problem summaries are non-empty, or matched keywords are from connectivity/security/cost categories.
   - Include a small uniform random `N` sample to estimate residual false-negative risk.

## Reviewer CSV Contract

Internal reviewer files may include text excerpts, but they must stay under ignored `data/validation/`.

Required columns:

- `review_id`: stable anonymized row key for reviewer workflow.
- `dbId`: internal join key; never copy into public outputs.
- `gu`, `regionName`, `createdAt`: context for checking geography/time if needed.
- `text_excerpt`: title plus content, normalized and truncated to 300 characters.
- `llm_umc_related`, `llm_umc_dimensions`, `llm_problem_group`: original model labels.
- `human_umc_related`: blank before review; allowed final values `Y`, `N`, `?`.
- `human_umc_dimensions`: official English dimension names, comma-separated, blank or `-` for `N`.
- `human_problem_group`: Korean short summary for `Y` or `?`, `관련없음` for `N`.
- `reviewer_id`: reviewer initials or role label.
- `review_notes`: short reason for label changes.

Public-safe manifests must exclude `dbId`, `text_excerpt`, `title`, `content`, `articleUrl`, writer fields, and raw post text.

## Task 1: Freeze Baseline And Privacy Boundary

**Files:**
- Create: `analysis/part 3/01_text_preprocessing/docs/human_validation_protocol.md`
- Read: `analysis/part 3/01_text_preprocessing/.claude/agents/umc_classifier.md`
- Read: `analysis/part 3/02_bayesian/docs/dong_reanalysis_plan.md`

- [ ] **Step 1: Write the protocol document**

Include these sections exactly:

```markdown
# UMC Human Validation Protocol

## Scope

This protocol validates the first-stage UMC relevance labels (`Y`, `N`, `?`) and six-dimension assignments generated from keyword-matched Danggeun posts.

## Privacy Boundary

Reviewer workbooks are internal only. Report-facing files must not contain raw post text, post IDs, article URLs, writer nicknames, or full row-level LLM dumps.

## Human Judgment Rule

`Y` means the post's primary concern is a digital connectivity barrier, digital access condition, digital cost burden, device barrier, digital skill barrier, or online safety/security threat. `N` means digital terms are absent, peripheral, or only tools/background. `?` is allowed only during first review and must be adjudicated before audited Bayesian reruns.

## Dimension Names

Use only: Connection Quality; Availability for Use; Affordability; Devices; Digital Skills; Safety & Security.

## Adjudication

Rows changed by reviewers, all `?` rows, and a 20 percent overlap sample are adjudicated by a second reviewer. Final labels are stored separately from original LLM labels.
```

- [ ] **Step 2: Verify the protocol has no raw examples**

Run:

```bash
rg -n "dbId|articleUrl|writer_|text_excerpt|title|content" analysis/part 3/01_text_preprocessing/docs/human_validation_protocol.md
```

Expected: only privacy-boundary references, no row-level examples.

## Task 2: Build Human Validation Set

**Files:**
- Create: `analysis/part 3/01_text_preprocessing/scripts/build_human_validation_set.py`
- Test: `analysis/part 3/01_text_preprocessing/tests/test_human_validation.py`
- Outputs: `analysis/part 3/data/validation/human_validation_sample.csv`
- Outputs: `analysis/part 3/data/validation/human_validation_manifest.json`

- [ ] **Step 1: Implement sampler inputs and label normalization**

The script must accept:

```bash
python scripts/build_human_validation_set.py \
  --parsed-glob "data/processed/phase03_parsed/*.csv" \
  --source-csv "data/processed/02_keyword_filtered.csv" \
  --output-dir "data/validation" \
  --seed 20260521 \
  --y-mode census \
  --n-sample 1500
```

Implementation requirements:

- Read parsed CSVs with `dbId`, `umc_related`, `umc_dimensions`, `problem_group`.
- Drop exact duplicate `dbId` rows after recording duplicate counts.
- Join to source rows by `dbId`.
- Build `text_excerpt` from `title` and `content`, truncated to 300 characters.
- Normalize labels to `Y`, `N`, `?`; fail on other non-empty values.

- [ ] **Step 2: Implement validation strata**

Sampling rules:

- Include all `Y` rows when `--y-mode census`.
- Include all `?` rows.
- Include `--n-sample` rows from `N`, split 70 percent high-risk and 30 percent uniform random.
- High-risk `N` is defined by multiple keyword-family matches, connectivity/security/cost keyword-family matches, non-empty LLM dimensions other than `-`, or `problem_group` not equal to `관련없음`.

- [ ] **Step 3: Write reviewer CSV and manifest**

Reviewer CSV columns must match the reviewer contract above. Manifest must include:

```json
{
  "source_rows": 149733,
  "parsed_files": 3004,
  "parsed_rows": 149484,
  "review_rows": 0,
  "review_y_rows": 0,
  "review_q_rows": 0,
  "review_n_rows": 0,
  "random_seed": 20260521
}
```

The `review_*` values must be computed from actual outputs, not hard-coded.

- [ ] **Step 4: Test sampler**

Run:

```bash
cd "analysis/part 3/01_text_preprocessing"
pytest tests/test_human_validation.py -q
python scripts/build_human_validation_set.py --output-dir data/validation --seed 20260521 --y-mode sample --y-sample 50 --n-sample 50
```

Expected:

- Tests pass.
- Reviewer CSV exists.
- Manifest exists.
- Reviewer CSV contains text only under ignored `data/validation/`.

## Task 3: Human Review Workflow

**Files:**
- Output: `analysis/part 3/data/validation/human_validation_sample.reviewed.csv`
- Output: `analysis/part 3/data/validation/human_validation_adjudicated.csv`

- [ ] **Step 1: First reviewer pass**

Reviewer fills only:

- `human_umc_related`
- `human_umc_dimensions`
- `human_problem_group`
- `reviewer_id`
- `review_notes`

Allowed values:

- `human_umc_related`: `Y`, `N`, `?`
- `human_umc_dimensions`: official dimension names separated by commas; `-` for `N`
- `human_problem_group`: Korean summary for `Y` or `?`; `관련없음` for `N`

- [ ] **Step 2: Second reviewer overlap**

Second reviewer independently reviews:

- All rows where human label differs from LLM label.
- All original `?` rows.
- 20 percent random overlap from unchanged `Y` rows.
- 20 percent random overlap from sampled `N` rows.

- [ ] **Step 3: Adjudication**

Adjudicator writes final columns:

- `final_umc_related`
- `final_umc_dimensions`
- `final_problem_group`
- `adjudication_reason`

No Bayesian rerun should use rows lacking final labels.

## Task 4: Apply Corrections Without Overwriting Original Labels

**Files:**
- Create: `analysis/part 3/01_text_preprocessing/scripts/apply_human_validation.py`
- Output: `analysis/part 3/data/validation/03_umc_classified_human_audited.csv`
- Output: `analysis/part 3/data/validation/human_validation_corrections.csv`
- Output: `analysis/part 3/data/validation/human_validation_apply_manifest.json`

- [ ] **Step 1: Implement correction application**

Run:

```bash
python scripts/apply_human_validation.py \
  --source-csv "data/processed/02_keyword_filtered.csv" \
  --reviewed-csv "data/validation/human_validation_adjudicated.csv" \
  --output-csv "data/validation/03_umc_classified_human_audited.csv"
```

Requirements:

- Preserve original LLM columns with `llm_` prefixes.
- Write final labels into `umc_related`, `umc_dimensions`, `problem_group`.
- Keep source metadata needed for downstream joins: `dbId`, `gu`, `regionName`, `createdAt`.
- Do not write raw text into the audited classified CSV.
- Write a corrections table containing only rows where final label differs from LLM label.

- [ ] **Step 2: Compute validation metrics**

Manifest metrics:

- LLM vs human precision for sampled `Y`.
- Estimated false-negative rate for sampled `N`.
- Resolution distribution for original `?`.
- Dimension exact-match agreement.
- Reviewer overlap agreement and Cohen's kappa where overlap exists.

## Task 5: Rerun Bayesian With Audited Labels

**Files:**
- Read: `analysis/part 3/02_bayesian/scripts/phase_a/build_safe_dong_inputs.py`
- Read: `analysis/part 3/02_bayesian/scripts/phase_b/participation_density_dong.py`
- Read: `analysis/part 3/02_bayesian/scripts/phase_c/region_dimension_sensitivity.py`
- Output: `analysis/part 3/02_bayesian/data/validation_rerun/`
- Output: `analysis/part 3/02_bayesian/output/validation_rerun/`

- [ ] **Step 1: Copy audited label input into a rerun-only directory**

Do not overwrite current `data/processed/03_umc_classified.csv` until the rerun is accepted.

- [ ] **Step 2: Run safe dong input builder against audited labels**

Preferred command after adding an explicit input option:

```bash
cd "analysis/part 3/02_bayesian"
python3 scripts/phase_a/build_safe_dong_inputs.py \
  --classified-csv "../data/validation/03_umc_classified_human_audited.csv" \
  --output-dir "data/validation_rerun"
```

If no `--classified-csv` option is added, convert audited rows into parsed-label-compatible CSVs in `data/validation/phase03_parsed_audited/` and pass `--parsed-glob`.

- [ ] **Step 3: Rerun density and region-dimension sensitivity**

Run with validation output directories so current baseline is preserved:

```bash
UMC_LIVING_POP_DIR="../../02. baysian/data/raw/생활인구_행정동" \
UMC_DOWNLOAD_MISSING_LIVING_POP=0 \
UMC_ALLOW_MISSING_POP_KEYS=1 \
python3 scripts/phase_b/participation_density_dong.py

python3 scripts/phase_c/region_dimension_sensitivity.py
```

Expected checks:

- All classified rows match dong candidates unless documented.
- Exact living-pop key loss remains documented.
- `region_dimension_sensitivity.csv` has 450 rows.
- `region_dimension_sensitivity_summary.csv` has 150 rows.

## Task 6: Compare Baseline Versus Human-Audited Results

**Files:**
- Create: `analysis/part 3/02_bayesian/scripts/phase_c/compare_human_validation_rerun.py`
- Output: `analysis/part 3/02_bayesian/output/validation_rerun/human_validation_impact_summary.csv`
- Output: `analysis/part 3/02_bayesian/output/validation_rerun/human_validation_impact_notes.md`

- [ ] **Step 1: Compare label counts**

Report:

- Original and audited `Y/N/?` counts.
- Original and audited six-dimension counts.
- District-dimension cells with changed `y_weight`.

- [ ] **Step 2: Compare posterior shifts**

Report:

- District-dimension cells whose posterior shift sign changes.
- Top 10 absolute changes in `shift_pp`.
- Whether the main reported key findings remain stable.

- [ ] **Step 3: Decide report update rule**

Update the report only when one of these conditions holds:

- A key finding's sign changes.
- A top district-dimension result changes rank materially.
- Human validation shows low precision or high false-negative risk requiring a methods caveat.

## Task 7: Report Integration

**Files:**
- Modify: `docs/ITU UMC Data Hackathon 2026.docx`
- Create or update: `docs/reviews/human_validation_summary_20260521.md`

- [ ] **Step 1: Add methods paragraph**

Add a short methods note that human validation audited first-stage UMC relevance and dimension assignment before Bayesian aggregation.

- [ ] **Step 2: Add results caveat only if needed**

If audited rerun is stable, state that key region-dimension patterns are robust to human validation. If unstable, report the affected district-dimension cells explicitly.

- [ ] **Step 3: Keep report public-safe**

Do not include raw post text, post IDs, article URLs, writer fields, or reviewer workbook rows in the DOCX.

## Verification Checklist

- [ ] Original LLM classified CSV remains recoverable.
- [ ] Human-reviewed files with text stay under ignored `data/validation/`.
- [ ] Public manifests contain no raw text or post IDs.
- [ ] Final audited classified CSV has only safe metadata and labels.
- [ ] Bayesian rerun uses audited labels through an explicit input path.
- [ ] Baseline vs audited comparison quantifies whether findings changed.
- [ ] Root report and nested analysis repos are committed separately only after user approval.
