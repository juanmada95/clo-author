# Robustness Plan — Curricular Analysis of TDC (MRCDD)

**Project:** Post-MRCDD, two-degree, two-layer curricular analysis.
**Companion to:** `quality_reports/strategy_memo_cdd_formacion_inicial.md`.
**Date:** 2026-04-26.

The main analyses (memo §7) report coverage and depth per (degree × layer × area), the four-category layer gap, and paired degree comparisons. Each robustness check probes one or more of these primary findings against an alternative analytical choice. Every check is **pre-specified** and reported in the manuscript appendix; the headline tables of the main text use the primary specification.

---

## Robustness checks — by domain

### A. Sampling robustness

| # | Check | What changes | What's preserved | What's tested |
|---|---|---|---|---|
| A1 | **Tier-A vs. Tier-B coverage** | Re-run the main analysis on the Tier-B stratified subset (~60 programmes) instead of the Tier-A census | Same coding scheme, same estimands | Whether the headline coverage estimates change qualitatively when restricting to the stratified subset. Triggered automatically if Tier B was activated; reported as a sanity check if Tier A succeeded. |
| A2 | **Public-only subset** | Restrict to public universities only | Same coding | Whether the inclusion of private/online providers (UNIR, VIU, UCJC) shifts results — these institutions are likely to be coverage outliers (one direction or the other). |
| A3 | **High-retrieval-rate subset** | Restrict to programmes where Layer-2 *guía docente* retrieval rate is ≥ 90% | Same coding | Whether incomplete *guía* corpora at some programmes pulls coverage estimates downward. |
| A4 | **Drop bilingual-only-in-regional-language documents** | Exclude programmes whose Layer-2 corpus is monolingual Catalan/Basque/Galician/Valencian | Same coding | Whether coder language coverage limits affected the headline estimates. |

### B. Coding-scheme robustness

| # | Check | What changes | What's preserved | What's tested |
|---|---|---|---|---|
| B1 | **DigCompEdu re-aggregation** | Re-aggregate codings to the 22 DigCompEdu competences via the appendix mapping table | Same underlying segment-level codings | Whether the framework choice (MRCDD vs. DigCompEdu) drives results. Substantive findings should be near-identical given near-isomorphism. |
| B2 | **Strict-presence threshold** | Define "presence" as depth ≥ 2 (developed) instead of depth ≥ 1 (mentioned) | Same depth codings | Whether the headline "X% of programmes cover area Y" depends on the loose-vs-strict threshold. Strict-presence numbers will be lower; the question is whether the *pattern* across areas is preserved. |
| B3 | **Sum-of-courses depth aggregation (Layer 2)** | Replace `max` over courses with `sum` (count of courses developing the area) — an intensity measure | Same per-course codings | Whether intensity (multiple courses) tells a different story than max-depth (one course is enough). |
| B4 | **Mean over courses (Layer 2)** | Replace `max` with `mean` over courses for depth aggregation | Same per-course codings | Whether the typical course (mean) versus the best course (max) gives different curricular characterizations. |
| B5 | **Single-coder sensitivity** | Re-run with each coder's data alone | Same data | Whether either coder's idiosyncratic codings drive results — should be near-identical given high κ. |

### C. Inclusion / exclusion robustness

| # | Check | What changes | What's preserved | What's tested |
|---|---|---|---|---|
| C1 | **With *optativas* included** | Add all *optativas* to the Layer-2 corpus | Same coding | Whether including elective courses materially changes coverage. The primary analysis excludes them because not every student takes them; this check tests whether the supply of digital-competence content is hidden in optatives. |
| C2 | **Without *Prácticum* and *TFG*** | Exclude these terminal experiences from Layer 2 | Same coding | Whether *Prácticum*/*TFG* drive coverage — these are typically terse documents with broad rubric language. |
| C3 | **Required-by-programme-type** | Re-classify courses as *básica* / *obligatoria* / *obligatoria-de-mención* and report separately | Same coding | Whether the difference between general and specialization-track required courses matters. |

### D. Layer-gap robustness

| # | Check | What changes | What's preserved | What's tested |
|---|---|---|---|---|
| D1 | **Strict layer alignment** | Re-define "both" in the layer-gap categorical to require depth ≥ 2 in BOTH layers | Same codings | Whether apparent alignment is shallow (both layers mention but neither develops). |
| D2 | **Layer-gap by area subset** | Restrict layer-gap analysis to areas where both layers have non-zero variance across programmes | Same codings | Whether headline gap rates are dominated by areas where one layer is uniformly high or low. |
| D3 | **Three-coder sub-corpus** | If a third coder is available for arbitration, re-compute layer gap using majority-vote codings on arbitrated cases | Same arbitration log | Whether arbitration choices nudge the gap rates. |

### E. Degree-comparison robustness

| # | Check | What changes | What's preserved | What's tested |
|---|---|---|---|---|
| E1 | **Unpaired comparison** | Compare Infantil and Primaria unpaired (across all programmes, not within universities offering both) | Same codings | Whether the within-university paired structure of the primary analysis is doing analytical work. |
| E2 | **Universities-with-both-degrees subset only** | Restrict the entire analysis to the subset of universities offering both degrees | Same codings | Whether single-degree institutions (some universities offer only Primaria, e.g.) shift results. |
| E3 | **Non-parametric resampling for paired difference** | Bootstrap the paired difference distribution (degree-by-degree, per area) | Same codings | Whether McNemar / Wilcoxon p-values agree with bootstrap-based inference. |

### F. Reporting robustness

| # | Check | What changes | What's preserved | What's tested |
|---|---|---|---|---|
| F1 | **Krippendorff's α reported alongside Cohen's κ** | All reliability statistics computed both ways | — | Whether the choice of statistic affects the perceived reliability story. |
| F2 | **Disagreement-rate sensitivity** | Report results both with and without disagreed segments included | Same codings | Whether unresolved disagreements bias headline estimates. |
| F3 | **No-LLM sub-corpus (if LLM-assisted pre-screening is used)** | Restrict to segments coded without LLM pre-screening | Same coding manual | Whether LLM pre-screening introduced bias into the human codings (selection effect: humans only see flagged segments). |

---

## Triggers and reporting

- **All robustness checks are pre-registered** in the OSF deposit. Failing to run any pre-registered check is itself a reportable deviation.
- **Reporting location:** Appendix tables, one per check, with a one-paragraph interpretation. The main text references the appendix and confirms whether headline conclusions hold.
- **Definition of "passing" a robustness check:** the qualitative pattern in the headline result is preserved (e.g., Area 4 remains the lowest-coverage area; the layer gap exceeds 20% in at least 3 areas). Quantitative point estimates are expected to differ.
- **If a check overturns the headline finding:** report it transparently in the discussion. Do not suppress it. If multiple checks converge on a different story, the headline should be revised.

---

## Robustness vs. exploration

The checks above are **robustness** checks — they probe pre-specified findings against alternative analytical choices.

**Exploratory analyses** (not robustness, not pre-registered) are reserved for:
- Patterns within MRCDD competences (not areas) that emerged during coding.
- Associations between coverage and university-level covariates beyond the four pre-specified sub-analyses.
- Text-level regularities (lexical patterns, pedagogical-language conventions).

Exploratory analyses, if reported, are clearly labeled as such and not advanced as findings of the study.
