---
name: umc-report-evidence-framing
description: Use when editing UMC report prose that interprets HLM, LLM platform text analysis, Bayesian updating, Digital Desert, or policy recommendations; keeps claims at the level supported by the evidence.
allowed-tools: Read, Bash
---

# UMC Report Evidence Framing

Use this skill for report-facing wording in `/Users/ujunbin/project/umc`.

## Source of Truth

- Active draft: `docs/ITU UMC Data Hackathon 2026.docx`
- Term dictionary: `docs/style/umc_report_evidence_terms.json`
- HLM source tables: `analysis/part 2/output/tables/`
- Part 3 aggregate sources: `analysis/part 3/02_bayesian/output/tables/` and `analysis/part 3/03_inference/`

## Core Framing Rules

- Keep the ITU UMC framework, critical realism, and multilayer design.
- Present HLM as hierarchical linear model based multilevel association analysis or explanatory decomposition, not causal identification.
- Make the central HLM message explicit: individual-level vulnerabilities dominate digital usage disparities in Seoul; district-level indicators are contextual conditions and targeting aids.
- Use place-sensitive targeting or place-sensitive intervention for policy, except where discussing the literature distinction between people-based and place-based approaches.
- Present LLM analysis as platform-visible lived-experience signal detection. The LLM is a structured coding assistant, not an autonomous evidence source.
- Treat prompts as codebook-like classification criteria. They improve consistency but do not replace human validation.
- Do not invent precision, recall, F1-score, Cohen's kappa, Krippendorff's alpha, robustness statistics, or validation sample sizes.
- Explain Bayesian updating as exploratory evidence integration between administrative indicators and platform-visible signals, not confirmatory estimation of deprivation prevalence.
- Keep Digital Desert as a provisional, non-deterministic targeting label; do not imply that districts themselves cause deprivation.

## Required First-Use Explanations

- HLM: hierarchical linear model, a model that separates individual-level and district-level factors in nested data.
- LLM: large language model, used here as a structured coding assistant for classifying platform text against predefined criteria.
- Bayesian updating: a method for revising prior information with new evidence; here it is used exploratorily to connect administrative indicators with platform-visible signals.

## Preferred Policy Structure

1. Individual-vulnerability-centered support: low-education older adults, older single-person households, groups with low digital service-use experience, and residents with low offline access.
2. Place-sensitive targeting: use the UMC composite index and dimension scores to identify where vulnerable individuals may be reached more efficiently, without treating low district scores as causal proof.
3. Capability, safety, and affordability support: device access, digital-service training, security and fraud-prevention capacity, telecom affordability, and help with complex public apps.
