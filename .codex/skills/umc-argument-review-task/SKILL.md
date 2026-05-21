---
name: umc-argument-review-task
description: Review argumentative coherence and cross-result consistency in the UMC Seoul report under `/Users/ujunbin/project/umc`; use when checking whether the ITU UMC theory, Part 1 district index, Part 2 HLM, Part 3 LLM/Bayesian signals, policy recommendations, and conclusion support one bounded evidence chain without overclaiming.
---

# UMC Argument Review Task

## Purpose

Act as the UMC report argument reviewer. Check whether the report reads as one integrated methodology for measuring Universal and Meaningful Connectivity in a hyper-connected city, rather than as separate Part 1, Part 2, and Part 3 outputs.

## When To Use

- The user asks for argument review, coherence review, result consistency, contradiction checks, 논증 검토, or 결과 정합성 점검 in the UMC project.
- The report needs quality control before DOCX submission or redesign.
- New Part 1, Part 2, or Part 3 outputs have been added to the report and need bridge checking.

## Source Boundaries

- Active report: `docs/ITU UMC Data Hackathon 2026.docx`.
- Design guide: `design.md`.
- Part 1 sources: `analysis/part 1/output/`.
- Part 2 sources: `analysis/part 2/output/`.
- Part 3 sources: `analysis/part 3/02_bayesian/output/`, `analysis/part 3/03_inference/`, and safe aggregate docs.
- Do not open, quote, or surface raw platform text, private text, post IDs, secrets, `.env`, or local settings.

## Decision Units

D1. Score six links as pass, weak, missing, or overclaimed:

- problem -> UMC measurement gap.
- gap -> theory/metatheory.
- theory -> operational variables and units.
- Part 1 index -> Part 2 HLM interpretation.
- Part 2 HLM -> Part 3 platform-visible signal interpretation.
- integrated results -> policy recommendations and limitations.

D2. Separate three issue types:

- Logic issue: the argument bridge is missing or contradictory.
- Evidence issue: a claim outruns the cited table, figure, model, or diagnostic.
- Writing/design issue: the report is visually or rhetorically hard to follow but the logic is sound.

D3. Check cross-result consistency:

- Part 1 district disparities must not be interpreted as causal proof of individual deprivation.
- Part 2 HLM must remain multilevel association analysis, not causal identification.
- Small ICC and limited Level 2 effects must be compatible with any place-sensitive policy claim.
- Part 3 LLM analysis must remain structured coding and platform-visible signal detection, not prevalence estimation.
- Bayesian updating must remain exploratory evidence integration, not confirmatory deprivation measurement.
- Digital Desert labels must remain provisional targeting labels, not deterministic district diagnoses.

## Procedure

P1. Build an argument map: section, main claim, evidence source, next bridge.

P2. Extract the main numeric/result claims from the report and compare them against the latest safe aggregate outputs where available.

P3. Mark unsupported claims, missing assumptions, and overclaims.

P4. For each weak link, provide a concrete rewrite instruction or bridge sentence.

P5. Produce a prioritized revision list and say which items should be edited in the DOCX now versus recorded as review notes.

## Verification

- Every main result claim has a source: theory, data, model, figure, table, diagnostic, or safe aggregate output.
- The conclusion does not introduce claims that are absent from Chapters 3 and 4.
- The policy section follows the evidence hierarchy: individual-vulnerability-centered support first, place-sensitive targeting second.
- Report wording preserves privacy boundaries and does not disclose raw platform text or post IDs.

## Output Contract

Return:

- Argument map.
- Link scores.
- Cross-result consistency findings.
- Top revision priorities.
- Suggested bridge sentences or DOCX edit instructions.
