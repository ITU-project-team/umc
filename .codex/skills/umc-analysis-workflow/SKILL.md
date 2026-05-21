---
name: umc-analysis-workflow
description: Use for UMC analysis work under `/Users/ujunbin/project/umc`, including Part 1 index/figure work, Part 2 HLM multilevel analysis, text-preprocessing/classification pipelines, inference rounds, validity checks, report-output handoff, and analysis repository synchronization.
---

# UMC Analysis Workflow

## Trigger

Use this skill when the task concerns analysis logic, scripts, outputs, or validation in `/Users/ujunbin/project/umc`.

This includes:

- Part 1 UMC index construction, district scores, maps, LISA, Moran diagnostics, and Section 3.1 figures.
- Part 2 HLM/multilevel analysis, data preparation, EDA, model fitting, sensitivity checks, and Section 3.2 interpretation.
- Text-preprocessing and inference pipelines for UMC-related post classification.
- Validity checks that connect analysis outputs to report claims.
- Commit or push work where analysis repos and the root report repo must remain separated.

## Repository Map

Treat these as separate Git repositories when they exist, but use the active
Part 1-3 repositories as the report-sync boundary unless the user explicitly
assigns legacy/reference analysis work.

| Path | Role |
| --- | --- |
| `/Users/ujunbin/project/umc` | Root report/document repository |
| `analysis/part 1` | Part 1 UMC index, district scores, maps, and Section 3.1 figures |
| `analysis/part 2` | Part 2 HLM/multilevel analysis for Section 3.2 |
| `analysis/part 3` | Consolidated Part 3 text, Bayesian, and inference workflow for Section 3.3 |
| `analysis/01. Text_preprocessing` | Legacy/reference preprocessing repository; Part 3 data has been consolidated under `analysis/part 3` |
| `analysis/text-preprocessing` | Legacy/reference text preprocessing and classifier support repository |
| `analysis/02. baysian` | Legacy/reference Bayesian workspace; prefer `analysis/part 3/02_bayesian` for active Part 3 work |
| `analysis/03. Test-for-inference` | Legacy/reference structured inference repository; prefer `analysis/part 3/03_inference` for active Part 3 work |

Always run `git status --short --branch` inside the repository that owns the files being changed.

## General Rules

- Inspect existing scripts, README files, and outputs before changing analysis logic.
- Do not overwrite raw data, private inputs, or `.env` files.
- Keep disposable outputs in `tmp/`; keep durable outputs in the owning repo's `output/`, `docs/`, or `writing/` locations.
- If analysis outputs feed the report, update and commit the analysis repo separately from the root report repo.
- When using cmux workers, combine this skill with `$umc-cmux-worker-supervision`.
- Use worker-facing Korean instructions when communicating through visible panes, but keep code, paths, variable names, and report wording in their original language.
- For report figures, use a restrained academic style: clean lines, muted colors, concise labels, and no sentence-style explanatory footer inside or directly below the figure. Put interpretation in the body text and keep the figure caption formal.
- For report prose, combine this skill with `$umc-report-evidence-framing` when interpreting HLM, LLM platform text analysis, Bayesian updating, Digital Desert, or policy recommendations.

## Part 1: UMC Index and Spatial Figures

Use Part 1 for Section 3.1 index, district ranking, heatmap, composite map, and spatial autocorrelation figures.

Common files:

- `analysis/part 1/output/tables/seoul_umc_scores_v7_2024.csv`
- `analysis/part 1/scripts/generate_section31_figures.py`
- `analysis/part 1/output/figures/report_refresh_20260516/`
- Seoul GIS files under `analysis/part 1/data/gis/Seoul/`

Expected workflow:

1. Verify the score table and district codes.
2. Regenerate figures with the existing script instead of hand-editing images.
3. Prefer publication-style figures: muted palette, thin boundaries, legible labels, minimal decoration, and stable dimensions for DOCX insertion.
4. For spatial diagnostics, report the contiguity rule, Moran's I, permutation p-values, and LISA significance threshold.
5. Reinsert final figures into the root DOCX only after the analysis outputs are generated and checked.

Basic checks:

```bash
python3 -m py_compile "analysis/part 1/scripts/generate_section31_figures.py"
python3 "analysis/part 1/scripts/generate_section31_figures.py"
git -C "analysis/part 1" status --short --branch
```

## Part 2: HLM Multilevel Analysis

Use Part 2 for Section 3.2 analysis of individual and district characteristics.

Main scripts:

- `analysis/part 2/scripts/data_prep.py`
- `analysis/part 2/scripts/eda.py`
- `analysis/part 2/scripts/hlm_modeling.py`
- `analysis/part 2/scripts/generate_report.py`
- `analysis/part 2/scripts/regenerate_codebook_euckr.py`

Main outputs:

- `analysis/part 2/data/processed/analysis_df.csv`
- `analysis/part 2/data/processed/analysis_df.parquet`
- `analysis/part 2/output/tables/hlm_model_comparison.csv`
- `analysis/part 2/output/tables/hlm_fit_statistics.csv`
- `analysis/part 2/output/tables/hlm_policy_simulation.csv`
- `analysis/part 2/output/tables/hlm_sensitivity_summary.csv`
- `analysis/part 2/output/reports/validity_check_report.md`

### Part 2 Data Prep

Checkpoints:

- Seoul Survey 2023/2024 loaded and harmonized.
- 25 Seoul districts are present.
- `digital_use_score` is constructed from the intended service-use items.
- Level 1 variables are recoded consistently across years.
- Level 2 UMC scores are merged by district and year.
- Centering information is recorded.
- Final `analysis_df` row count, district count, and year distribution are reported.

Do not change raw survey inputs. If a script uses a local absolute path, document the required path or parameterize it in a narrow patch.

### Part 2 EDA

Checkpoints:

- Level 1 descriptive table exists and matches the report.
- Level 2 descriptive table exists and uses district-level units.
- Dependent-variable distribution is checked.
- Vulnerable-group comparisons are reported.
- Correlation checks flag high-collinearity risks before HLM modeling.

### Part 2 HLM Modeling

Use the established model sequence:

1. Model 0: null random-intercept model.
2. Model 1: Level 1 individual characteristics.
3. Model 2: Level 1 plus district-level UMC dimensions.
4. Model 3: cross-level interaction model.

Model interpretation rules:

- ICC can be small while design effect still justifies multilevel modeling.
- Level 2 effects must be interpreted cautiously when between-district variance is small.
- Distinguish individual-level differences from district-level differences.
- Do not turn observational associations into causal claims.
- Report model fit, variance components, and whether Level 2 additions materially improve fit.

### Part 2 Validity Check

Use validity checks after each model stage and before report writing.

Check:

- Exogeneity: Level 2 predictors should not accidentally include outcome-derived aggregates in the main specification.
- Affordability/contextual effects: district-level income or affordability claims must control for individual income when interpreted that way.
- Level 2 parameter count: 25 districts limit how much can be estimated.
- Residual assumptions: inspect L1/L2 residuals where feasible.
- Effect size realism: translate normalized coefficients into meaningful units.
- Causal limits: policy simulations are predicted changes under observed associations, not causal policy effects.

Basic checks:

```bash
python3 -m py_compile \
  "analysis/part 2/scripts/data_prep.py" \
  "analysis/part 2/scripts/eda.py" \
  "analysis/part 2/scripts/hlm_modeling.py" \
  "analysis/part 2/scripts/generate_report.py"

python3 - <<'PY'
import pandas as pd
from pathlib import Path
for p in [
    "analysis/part 2/output/tables/hlm_model_comparison.csv",
    "analysis/part 2/output/tables/hlm_fit_statistics.csv",
    "analysis/part 2/output/tables/hlm_policy_simulation.csv",
]:
    path = Path(p)
    if path.exists():
        df = pd.read_csv(path)
        print(path, df.shape, list(df.columns))
PY
```

## Text Preprocessing and UMC Classification

Use this for preprocessing posts and preparing UMC classification batches.

Typical repository:

- `analysis/text-preprocessing`
- `analysis/part 3/01_text_preprocessing`

Common flow:

1. Prepare input batches.
2. Run or instruct the `umc_classifier` agent where available.
3. Parse classifier responses.
4. Merge final CSV outputs.
5. Verify row counts, encoding, and failed-response cases.

When the report asks for Section 3.3 methods, agent operation, prompt details, or
reader-facing explanation of the Part 3 pipeline, automatically check the
preprocessing layer as well as the inference layer. Do not wait for the user to
name every appendix item. Public-safe appendix candidates are:

- Keyword dictionary summary: dimension, keyword count, representative terms, and
  the full dictionary file path.
- UMC relevance and dimension-classification prompt: role, core UMC test,
  six-dimension rules, over-classification filters, few-shot boundary examples,
  and output format.
- Inference prompts: abductive, forward, sequential, and judgment-synthesizer
  prompts, cleaned into role/input/rule/output sections by default.
- If the user asks for prompt text "as-is", "verbatim", or "그대로", use the
  exact source prompt files instead of summaries, preserve line breaks, and
  include source paths in the appendix.

Do not paste raw posts, post-level identifiers, local raw-data paths, or full
post-level LLM dumps into the report. If the complete 1,000+ term keyword list is
needed, suggest a separate appendix artifact instead of crowding the main DOCX.

Useful checks:

```bash
python3 -m py_compile main.py $(find src -name '*.py' -print)
python3 - <<'PY'
import yaml
from pathlib import Path
for p in ["config/seed_keywords.yaml"]:
    path = Path(p)
    if path.exists():
        yaml.safe_load(path.read_text())
        print("yaml-ok", path)
PY
```

## Inference Pipelines

Use these paths for structured post-level inference:

- `analysis/part 3/03_inference`
- `analysis/03. Test-for-inference`
- `analysis/Part 2-2`
- `analysis/Part 2-4`

Common skill families consolidated here:

- Preprocess batches: raw posts -> filtered/scored JSONL.
- Generate hypotheses: multiple reasoning agents produce candidate interpretations.
- Judge posts: load hypotheses plus context and assign accepted classifications.
- Reconcile: compare multiple pipeline outputs and adopt a conservative final classification.
- Update knowledge: append or revise category knowledge only under the repository's rules.
- Benchmark or saturation: assess reproducibility, category stability, and coverage.

Core guardrails:

- Separate hypothesis generation from judgment.
- Do not let context blocks leak into a phase that is supposed to be text-only.
- Preserve direct textual evidence and metadata.
- Record divergence, rejected alternatives, confidence, layer, UMC dimension, and absence type.
- Keep knowledge updates append-only unless the local repository explicitly defines a controlled update operation.

## Report Handoff

When analysis results are used in the root report:

1. Verify the source output in the analysis repo.
2. Update the report DOCX, figures, tables, or prose in the root repo.
3. Render or structurally inspect the DOCX when layout matters.
4. Fix figure/table references after replacing outputs.
5. Run the report-analysis lag checker from the root repo when analysis output
   may affect the report:

```bash
python3 .codex/hooks/report_analysis_lag_check.py
```

6. Commit analysis repo and root repo separately.

For DOCX checks, use `$doc` when layout matters.

## Final Verification

Before reporting completion:

- Each touched analysis repo has a clear status.
- Generated outputs match the script or table that produced them.
- Any report claim has a source table, figure, script, or validation note.
- No raw data or private files were staged.
- All temporary verification outputs were cleaned or clearly left in `tmp/`.
- For analysis/report handoffs, run
  `python3 .codex/hooks/report_analysis_lag_check.py --json` from the root repo
  and resolve or explicitly carry forward any warning-only lag notes.
- If pushing, each touched repo reports `0 0` for `HEAD...origin/main` after push.
