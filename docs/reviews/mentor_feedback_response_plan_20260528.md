# Mentor Feedback Response Plan

Date: 2026-05-28

Scope: latest working report, `docs/ITU UMC Data Hackathon 2026.docx`.

## User Decisions

- Key Results should prioritize result interpretation over numeric dashboards.
  Use numbers only where they clarify the claim.
- For Part 2, foreground the substantive finding that district-level effects
  are very small and individual vulnerability dominates; avoid leading with
  the ICC value.
- Use visual subheadings in Sections 1.1 and 1.2 rather than numbered
  subheadings.
- Add a 5G base-station choropleth or equivalent geospatial figure.
- For Part 2, the current DOCX/code model with three Level-2 UMC dimensions is
  the reference model.
- For Part 3, include a template results table rather than claiming final
  results before the workflow is complete.
- 독자가 읽기 편하도록 보고서 내용을 풀어서 설명
-- 예시: Before the topic model and LLM classification material, add short definitions
  of topic model, seed list, prompt, and the three interpretive lenses.

Do not use raw platform text, post IDs, private row-level records, local
settings, secrets, or `.env` material.

## Work Allocation

| Owner | Path / Section | Task | Output |
| --- | --- | --- | --- |
| `report-docx-manager` | `docs/ITU UMC Data Hackathon 2026.docx` | Rebuild report flow, restructure Key Results, add visual subheadings in 1.1/1.2, place Part 3 template results table. | DOCX edit plan, then report edits after approval/assignment. |
| `report-figure-generator` | `docs/figures/` and Part 1 handoff outputs | Convert the approved 5G base-station evidence into a report-ready choropleth figure with academic styling. | Figure asset, caption draft, and source note for DOCX insertion. |
| `part1-analysis-manager` | `analysis/part 1`, report Sections 2.3.1 and 3.1 | Clarify composite score meaning, SKT source wording, affordability wording, and produce/add 5G base-station choropleth plan. | Figure-generation task list and report-ready source notes. |
| `part2-analysis-manager` | `analysis/part 2`, report Section 3.2 | Use current DOCX/code model; revise HLM wording toward association/decomposition, small district-level effects, and age/over-65 interpretability caution. | Section 3.2 wording plan and optional diagnostics list. |
| `part3-analysis-manager` | `analysis/part 3`, report Section 3.3 | Add topic model, seed list, prompts, lenses, bounded categories, removal-rate, selection-bias, and template-results explanations without raw text exposure. | Section 3.3 structure and template table specification. |
| `project-verifier` | Root repo and touched analysis paths | Verify source references, privacy boundaries, dirty-state separation, and figure/table/report consistency. | Findings-first verification note. |

## Planned Report Changes

### Key Results

- Replace number-heavy dashboard framing with three narrative findings:
  district UMC gaps are visible, individual vulnerabilities dominate digital
  usage disparities, and place-sensitive targeting policy will be good
- Keep the ICC or related figures as supporting detail only.
- Clarify the composite score as a relative Seoul-within-district measure: an
  equally weighted mean of six normalized dimension scores, not an absolute UMC
  attainment level.
- For the third finding, explicitly state which analysis supports it: Part 1
  spatial/index patterns plus Part 3 platform-visible signals, interpreted
  cautiously with Part 2's weak district-level effects.

### Sections 1.1 and 1.2

- Break long paragraphs into visual subheaded blocks.
- Section 1.1 should separate UMC framing, evidence transferability, critical
  realism, and the brief motivating example.
- Section 1.2 should separate district UMC measurement, HLM decomposition,
  platform-visible text signals, and Bayesian evidence integration.
- Do not introduce `1.1.1` or `1.2.1` numbering unless the report style is
  later changed.

### Section 2.3.1

- Reorder bar charts high-to-low for easier reading.
- Add a 5G base-station choropleth or equivalent map early in the Seoul context
  section to introduce the geospatial dimension before Analysis 1.
- Use the PPT-first component for source wording: cellular base-station data
  from Spectrum Resource Mgmt System, with district matching and
  population-adjusted density logic.

### Section 3.1.1

- Define SKT as SK Telecom on first use.
- Explain the data source using the PPT-first component: SKT Telecom Data via
  Korean Public Data Portal, Seoul 2023-2024, including mobile data use,
  online service days, and fee delinquency rate.
- Keep the current affordability construction, but clarify that average income
  is the resource-side contextual proxy and arrears/fee delinquency is the more
  direct burden-side indicator.

### Section 3.2.1 and 3.2.2

- State that retained interactions were theory-guided and pre-specified around
  policy-relevant vulnerability mechanisms, not selected after searching for
  significance.
-- 이 부분 구체적으로 2장에서 다룬 사실로 변수 구성함
- Use the current DOCX/code three-dimension Level-2 model as the reference.
- Replace phrasing that foregrounds the numeric ICC with: district-level
  contextual effects are very small in the present model, while individual
  vulnerabilities dominate digital usage disparities. -> 구체적으로 어떤 취약성이 주도하는지 설명!!
- Add caution that age and the over-65 indicator are structurally related; 한국은 고령 정책 기준이 65세 이상임


### Section 3.3

- Clarify figure labels such as B and C in the surrounding text and caption.
- Explain bounded classification categories before using the term.
- Replace vague phrasing such as "posts classified as related" with the exact
  classification relation: posts classified by the LLM coding procedure as UMC
  relevant under the predefined criteria.
- Explain how formulas below Table 5 connect Part 1 UMC priors, Part 2
  cautious interpretation, and Part 3 platform-visible signals.
- Rewrite removal rates as analytic text-sample exclusions due to inaccessible
  body text, not as substantive moderation or deletion behavior by the
  platform.
- Add the selection-bias caveat: people with severe access issues may be less
  able to use the online platform, so platform-visible signals underrepresent
  the most excluded groups.
-- 종합적인 프레임으로서의 가치 재언급
- Include a template result table showing the planned row/column structure and
  interpretation type, without exposing raw posts or claiming completed final
  results.

## Suggested Template Table

| District / group | UMC dimension | Prior indicator signal | Platform-visible signal | Expected interpretation | Status |
| --- | --- | --- | --- | --- | --- |
| Example district or cluster | Connectivity / Affordability / Devices / Skills / Safety | Low / medium / high relative UMC score | Aggregate classified-signal direction only | How the signal would qualify or illustrate the quantitative result | Template pending final aggregation |

Use anonymized aggregates or placeholders only until final Part 3 outputs are
approved for publication.

## Implementation Sequence

1. Protect existing root changes by keeping DOCX/PDF edits and new paper PDFs
   separate from this planning/component work.
2. Generate or update the 5G choropleth in the Part 1 repo, then hand a
   report-ready figure path to `report-figure-generator` and the root report
   workflow.
3. Revise the report body in this order: Key Results, 1.1/1.2, 2.3.1,
   3.1.1, 3.2.1-3.2.2, 3.3.
4. Add the Part 3 template table and explicitly mark it as template/planned
   results if final aggregation is not yet ready.
5. Render the DOCX and check layout, captions, figure order, and table
   readability.
6. Run read-only verification for source claims, privacy boundaries, and
   analysis-to-report consistency.

## Open Risks

- The 5G choropleth requires careful source-path and output-path handling in
  the Part 1 nested repo.
- Adding a new 5G figure may require figure-number and cross-reference cleanup
  in the DOCX. Current figure numbering should be checked before insertion.
- Current root repo already has unrelated modified DOCX/PDF files and new
  paper PDFs; keep these changes separated from component/plan commits.
- Part 3 template content must not drift into fabricated results. Keep status
  labels explicit until final outputs are available.
- HLM language must not imply causality or overstate district-level effects.
