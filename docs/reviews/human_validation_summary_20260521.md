# Human Validation Layer for UMC Text Classification

Date: 2026-05-21

## Purpose

The first-stage LLM classification is treated as structured coding output, not
as final ground truth. To make the platform-visible signal analysis auditable,
the current `Y` and `N` labels were separated into exhaustive internal review
files before any human-audited Bayesian rerun.

## Baseline

- Classified source rows: 131,792
- LLM `Y` rows prepared for full human review: 7,136
- LLM `N` rows prepared for full human review: 122,509
- LLM `?` rows retained for later adjudication: 2,147

## Review Files

Internal files:

- `analysis/part 3/data/processed/human_validation/human_validation_y_full.csv`
- `analysis/part 3/data/processed/human_validation/human_validation_n_full.csv`
- `analysis/part 3/data/processed/human_validation/chunks/Y/`
- `analysis/part 3/data/processed/human_validation/chunks/N/`
- `analysis/part 3/data/processed/human_validation/human_validation_manifest.json`

The full files are also split into 5,000-row chunks to support distributed
human review. The `Y` file has 2 chunks; the `N` file has 25 chunks.

Management artifacts:

- `analysis/part 3/01_text_preprocessing/docs/human_validation_protocol_20260521.md`
- `docs/reviews/human_validation_file_index_20260521.json`

The generator now refuses to write reviewer files outside the ignored
`data/processed/` boundary, removes stale chunk files before rerun, records
excluded labels, and records source duplicate statistics in the manifest.

## Reviewer Fields

Each row preserves the original LLM label and provides blank human-review
columns:

- `llm_umc_related`, `llm_umc_dimensions`, `llm_problem_group`
- `human_umc_related`, `human_umc_dimensions`, `human_problem_group`
- `reviewer_id`, `review_notes`

The final human label should be written into the `human_*` columns without
overwriting the original `llm_*` columns.

## Report-Safe Boundary

The reviewer files are internal validation artifacts. They include an internal
join key and a 300-character review excerpt to allow human checking, but these
row-level fields must not be copied into public report outputs. The report
should describe only the validation design, aggregate counts, and the effect of
human-audited labels on district-dimension Bayesian results after rerun.

## Report Wording

Suggested wording for Section 3.3:

> To make the first-stage LLM coding auditable, all posts classified as related
> (`Y`, 7,136 rows) and unrelated (`N`, 122,509 rows) were separated into
> exhaustive internal human-review files. The review layer preserves the
> original LLM relevance label, dimension assignment, and problem summary while
> adding separate human-decision columns. Review files include only the
> row-level information needed for internal checking and are not reproduced in
> the report. Public reporting is limited to aggregate validation counts and to
> the stability of Bayesian district-dimension results after human-audited
> labels are incorporated.
