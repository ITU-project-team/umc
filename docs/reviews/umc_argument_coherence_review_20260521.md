# UMC Argument Coherence Review - 2026-05-21

## Scope

This review applies a UMC-specific version of the Korean urban argument-review workflow to the current project. It checks whether the report's problem framing, theory, Part 1 district index, Part 2 HLM results, Part 3 text/Bayesian signals, and policy interpretation support one another without overstating the evidence.

Sources checked:

- `docs/ITU UMC Data Hackathon 2026.docx`
- `analysis/part 1/output/figures/report_refresh_20260516/fig05_lisa_moran_stats_2024.csv`
- `analysis/part 2/output/tables/hlm_model_comparison.csv`
- `analysis/part 2/output/reports/validity_check_report.md`
- `analysis/part 3/02_bayesian/output/tables/table4_dim_summary.csv`
- `analysis/part 3/02_bayesian/output/tables/region_dimension_report_notes.json`
- `analysis/part 3/02_bayesian/output/tables/region_dimension_sensitivity_summary.csv`

No raw platform text, post IDs, private local settings, or `.env` material were reviewed or reproduced.

## Argument Map

The main chain is coherent:

1. Seoul is already highly connected in aggregate, so the relevant problem is not simple access/non-access but uneven, meaningful connectivity across districts and dimensions.
2. The UMC framework translates that problem into six dimensions: Connectivity, Available for Use, Affordability, Devices, Digital Skills, and Safety.
3. Part 1 shows district-level multidimensional variation and defines the bottom-five districts as provisional Digital Deserts for targeting, not as fixed identities.
4. Part 2 shows that individual vulnerabilities remain central. District-level infrastructure-side variables provide context but do not replace individual-level explanation.
5. Part 3 adds platform-visible lived-experience signals and Bayesian diagnostics as exploratory interpretation, not prevalence measurement or causal proof.
6. The policy conclusion therefore works best when it combines individual-vulnerability-centered support with dimension-specific, place-sensitive targeting.

## Link Scores

| Link | Assessment | Note |
|---|---|---|
| Problem -> UMC measurement gap | Strong | The report consistently argues that aggregate connectivity hides lower-level variation. |
| UMC theory -> six-dimensional operationalization | Strong | The dimensions used in Part 1, Part 2, and Part 3 are aligned. |
| Part 1 -> Part 2 | Strong with boundary | Part 1 identifies district conditions; Part 2 correctly treats district variables as contextual predictors rather than causal proof. |
| Part 2 -> Part 3 | Strong with boundary | Part 3 is framed as exploratory signal interpretation compatible with HLM, not as a direct test of HLM coefficients. |
| Integrated results -> policy | Mostly strong | The combined policy frame is coherent, but a few expressions need narrower wording to avoid overstating spatial clustering or older Part 2 results. |

## Coherence Findings

### F1. Stale Part 2 validity report conflicts with current HLM outputs

Severity: High for project-level consistency; low for the active DOCX if the DOCX follows the current table.

The current HLM comparison table reports the infrastructure-side cross-level interactions as statistically non-significant:

- `score_Infrastructure_n:elderly`: p = 0.312
- `score_Available_for_Use_n:elderly`: p = 0.394
- `score_Affordability_n:elderly`: p = 0.081
- `score_Infrastructure_n:low_edu`: p = 0.215

Evidence: `analysis/part 2/output/tables/hlm_model_comparison.csv` lines 58-63.

However, `analysis/part 2/output/reports/validity_check_report.md` still contains an older interpretation in which `wifi_total_n x elderly` and `conn_n x low_edu` are treated as significant. Evidence: lines 124-140, 208-216, and 240.

Action: treat the validity report as stale or regenerate it from the current HLM table before using it for any further report edits.

### F2. Part 3 district-dimension counts require stage-specific labeling

Severity: Medium; directly fixable in the active DOCX.

The Part 3 outputs contain two valid counts from different aggregation stages. The basic Y-by-dimension count sums to `7,421`:

- Connection Quality: 730
- Availability for Use: 536
- Affordability: 587
- Devices: 1,455
- Digital Skills: 2,322
- Safety & Security: 1,791

Evidence: `analysis/part 3/02_bayesian/output/tables/table2_gu_dim_counts.csv` line 27 and `analysis/part 3/02_bayesian/output/tables/table4_dim_summary.csv` lines 1-7.

The later mapping-sensitivity output records `7,454` all-weighted mapped assignments after administrative-dong candidate expansion and weighting. Evidence: `analysis/part 3/02_bayesian/output/tables/region_dimension_sensitivity.csv`.

Action: label the DOCX counts by stage: `7,421` for the basic unweighted district-dimension summary and `7,454` for the all-weighted mapped sensitivity specification. Do not replace every `7,454` mechanically.

### F3. LISA wording should distinguish composite clustering from dimension-level global Moran results

Severity: Medium; interpretive precision issue.

The current report states that adjacent areas display similar patterns in some UMC dimensions and refers to spatial autocorrelation by dimension. The LISA output shows a statistically significant global Moran result for the composite index (`p = 0.005`), but the six dimension-level global Moran p-values are not significant (`p = 0.234` to `0.627`).

Evidence: `analysis/part 1/output/figures/report_refresh_20260516/fig05_lisa_moran_stats_2024.csv` lines 1-8.

Action: phrase the result as composite-index clustering plus selected local dimension clusters, not citywide dimension-level spatial autocorrelation.

### F4. Digital Desert clustering should explicitly separate the northern cluster from Guro-gu

Severity: Medium-low; wording issue.

The bottom-five Digital Desert group includes Jungnang-gu, Dobong-gu, Gangbuk-gu, Guro-gu, and Nowon-gu. The northern Low-Low cluster is Dobong-gu, Gangbuk-gu, Nowon-gu, and Jungnang-gu, while Guro-gu is a separate southwestern low-score case. The report mostly handles this correctly, but a few summary sentences can be read as if all five districts are in northern Seoul.

Action: use wording such as "four of the five provisional Digital Desert districts form a northern cluster, while Guro-gu appears as a separate southwestern low-score case."

### F5. Part 3 sensitivity results are coherent and should be retained

Severity: No inconsistency.

The current report says 149 of 150 district-dimension cells retain the same direction across mapping-sensitivity specifications. The sensitivity summary confirms this; the only sign-unstable cell is Guro-gu Connectivity.

Evidence: `analysis/part 3/02_bayesian/output/tables/region_dimension_sensitivity_summary.csv` lines 40, 67, 107, 125, 149-150.

Action: retain the current sensitivity framing. It is correctly presented as exploratory platform-visible deviation, not prevalence.

### F6. One stale Digital Skills sentence conflicts with current Part 3 outputs

Severity: Medium; directly fixable in the active DOCX.

One report sentence stated that Gangseo-gu had a negative Digital Skills shift despite a high measured value. Current outputs show the opposite pattern: Gangseo-gu has a positive Digital Skills shift of about `+0.606` percentage points and a measured Digital Skills score of `0.340`, not a high measured value.

Evidence: `analysis/part 3/02_bayesian/output/tables/region_dimension_sensitivity_summary.csv` line 24 and `analysis/part 1/output/tables/seoul_umc_scores_v7_2024.csv` line 16.

Action: remove or rewrite the stale duplicate sentence. Keep the current Digital Skills pattern centered on Jungnang-gu, Gangnam-gu, and Gwanak-gu as described in the immediately preceding paragraph.

## Recommended Bridge Sentences

Use these as guardrails for further prose edits:

- "The Part 1 index identifies where district conditions differ, while Part 2 shows that these differences do not explain most individual digital-use variation; district scores are therefore used as targeting context rather than causal explanations."
- "Part 3 does not test the HLM directly; it adds platform-visible situations that help interpret how the vulnerabilities identified in Part 2 become observable in everyday service-navigation contexts."
- "The provisional Digital Desert label refers to a multidimensional targeting profile, not a claim that districts cause deprivation."
- "The spatial evidence supports a northern inter-district coordination strategy for the Low-Low cluster, while Guro-gu should be treated as a separate southwestern low-score case."

## Revision Priority

1. Regenerate or archive the stale Part 2 validity report before future analysis handoff.
2. Distinguish Part 3 count stages in the DOCX: `7,421` for the basic unweighted dimension summary and `7,454` for all-weighted mapped sensitivity.
3. Narrow LISA wording to composite-index clustering and selected local dimension clusters.
4. Clarify the Digital Desert geography in summary and policy paragraphs.
5. Remove the stale Gangseo-gu Digital Skills sentence.
6. Keep all Part 3 examples anonymized and paraphrased; do not introduce raw post text into the report or review artifacts.
