# OSF Pre-Registration — Curricular Analysis of Teacher Digital Competence in Spanish Initial Teacher Training (Post-MRCDD)

**Deposit type:** Pre-registration of a descriptive content-analysis study (observational, non-experimental).
**Platform:** Open Science Framework (OSF).
**Date drafted:** 2026-04-26.
**Pre-registration status:** *Draft for user review prior to OSF submission.* See the **Pre-Registration Checklist** at the end of this document for `[ASSUMED]` placeholders that must be resolved before deposit.
**Companion artifacts (project files to be deposited alongside this document):**
- `strategy_memo_cdd_formacion_inicial.md` — full strategy memo (authoritative; this PAP is the commitment-device extract).
- `pseudo_code.md` — analytical pipeline (7 stages).
- `robustness_plan.md` — 21 pre-specified robustness checks.
- `falsification_tests.md` — 7 instrument-validation / sanity checks.
- `data_exploration_cdd_formacion_inicial.md` — corpus inventory and pilot retrieval evidence.
- `software_environment.md` — R analysis-stack lock-protocol (deposited; concrete `renv.lock` to follow at pilot start).
- `data_engineering_environment.md` — Python data-engineering-stack lock-protocol (deposited 2026-04-27; closes Pre-Registration Checklist C2 + C3+C9).
- `power_sensitivity_table.csv` — pre-registered McNemar power-sensitivity grid (deposited; reproducible from `scripts/R/strategy/power_sensitivity_table.R`).
- `corpus_inventory.csv` — realised programme universe (deposited 2026-04-27; **revised same day to 174 active programmes** after coder-critic round-1 review; closes C2; revision logged as Deviation 4 in §10).
- `tier_b_sample_ids.csv` — Tier B 60-programme stratified sample (deposited 2026-04-27; **regenerated same day** against the revised 174-programme inventory; reproducible from `scripts/python/strategy/tier_b_sample.py`; closes C3+C9).
- `tier_b_strata_table.csv` — companion strata cross-tabulation showing universe-vs-sample allocation per cell.
- `inventory_reconciliation_log.md` — disagreements between sources, manual overrides applied, RUCT scrape outcome.
- `coding_manual_v1.0.pdf` — frozen post-pilot coding manual *(to be deposited before main coding begins; not yet produced).*
- `reliability_subsample_ids.csv` — the a-priori 20% reliability sample IDs *(to be deposited with the random seed and stratification cells).*

---

## 1. Study Information

### 1.1 Title

**Curricular Coverage and Depth of the *Marco de Referencia de la Competencia Digital Docente* (MRCDD) in Spanish Initial Teacher Training: A Two-Degree, Two-Layer Stratified Content Analysis of *Memorias de Verificación* and *Guías Docentes* (Academic Year 2024–2025).**

### 1.2 Authors and affiliations

- **A.R.J.** — `[ANONYMIZED — single institution; full name, affiliation, and email pending OSF deposit]` (corresponding author).
- **M.G.J.** — `[ANONYMIZED — same institution as A.R.J.]`
- **C.B.T.** — `[ANONYMIZED — same institution as A.R.J.]`
- **P.P.G.** — `[ANONYMIZED — same institution as A.R.J.]`

*(All four authors share a single institutional affiliation. Full names, institutional details, and contact emails are intentionally anonymized in the draft and will be filled in before the OSF deposit is submitted.)*

### 1.3 Description

This pre-registration commits the study to a stratified, post-MRCDD content analysis of how Spanish *Grado en Maestro de Educación Infantil* and *Grado en Maestro de Educación Primaria* programmes integrate the six areas and twenty-three competences of the *Marco de Referencia de la Competencia Digital Docente* (MRCDD; Resolución de 4 de mayo de 2022, BOE-A-2022-8042; @INTEF2022_mrcdd) into two distinct curricular layers — the formal *memoria de verificación* and the perceived *guías docentes* (per the @Goodlad1979_curriculum_inquiry framework). The study targets a stratified random sample of approximately 60 programmes from a `[ASSUMED]` universe of ~144 RUCT-listed programmes, snapshot academic year 2024–2025. It produces coverage and depth estimates per (degree × layer × MRCDD area), documents the **layer gap** between formal commitment and perceived implementation, and makes **paired within-university comparisons** between Infantil and Primaria. The contribution is the **conjunction** of five qualifiers: post-MRCDD, two-degree, two-layer, full competence space, and stratified national scope — a combination not present in any prior Spanish curricular study.

### 1.4 Hypotheses (expected patterns, not causal hypotheses)

This is a **descriptive measurement design**. We pre-state expected patterns drawn from the literature, with the explicit understanding that the pre-registration commits to **reporting the test**, not to defending any particular outcome. No causal interpretation is intended.

- **H1 (System-level coverage is uneven across MRCDD areas).** Coverage of MRCDD Areas 2 (*Recursos digitales*) and 3 (*Enseñanza y aprendizaje*) will exceed 60% of programmes at the *guía docente* layer, while Area 4 (*Evaluación y retroalimentación*) and Area 6 (*Desarrollo de la competencia digital del alumnado*) will fall below 40%. *(Anchored in the saturated Spanish literature: @Cabero2023_evaluacion_review; @Cuevas2024_tpack_primary; @Cuevas2025_curriculum_efl.)*
- **H2 (Layer gap is larger on outcome-oriented areas).** The misalignment between the *memoria* layer and the *guía docente* layer — operationalized as `P(memoria-only) + P(guía-only)` — will be larger on Areas 4 and 6 than on Areas 2 and 3. Formal commitment is expected to outpace perceived implementation on assessment and student-outcome competences.
- **H3 (Within universities offering both degrees, Primaria coverage exceeds Infantil on operational areas).** In the paired within-university subsample, Primaria will show higher coverage than Infantil on Areas 2 and 4. *(Anchored in @Cuevas2024_tpack_primary's Primaria-focused finding pattern and the broader observation that Infantil curricula are more developmental than instrumental-tech in orientation.)*

Each H_i is pre-stated as an **expected pattern**. The study will report each test descriptively with a confidence interval; no claim of causation will be made regardless of the outcome.

### 1.5 Ethics and funding

- **Ethics / IRB.** This study analyzes only **public curricular documents** (*memorias de verificación* registered with ANECA / autonomous-community evaluation agencies, and *guías docentes* published on university course catalogues). It involves **no human subjects, no personal data, and no intervention**. The author team's working position is therefore that no IRB approval is required. Whether the authors' institution requires a formal "no aplica" exemption letter from its own ethics committee is `[ANONYMIZED — institution policy pending; exemption letter or self-declaration to be confirmed before OSF deposit is finalized]`.
- **Funding.** `[ANONYMIZED — funding source pending OSF deposit. If a competitive grant supports the study, the grant code will be cited here at deposit time; if the study is self-funded, that will be declared.]`
- **Conflicts of interest.** None declared. (Confirmed at deposit time.)

---

## 2. Design Plan

### 2.1 Study type

**Observational — content analysis of public curricular documents.**

This is **not** a randomized experiment, **not** a quasi-experimental observational study (no treatment / control contrast in the inferential sense), and **not** an instrumental-variables design. The design is a **stratified cross-sectional content analysis** of curricular documents, with **paired within-university** and **paired within-programme** comparisons used as a measurement-design feature, not as causal-inference identification.

### 2.2 Blinding

Coders are **blind to each other's codings** on the reliability subset (see §6). Coders are not blind to document identity (the *memoria* and *guía docente* are by nature institutionally identifiable), but no inferential outcome is conditioned on coder identity.

### 2.3 Study design

- **Cross-sectional snapshot** at academic year 2024–2025.
- **Two-layer:** Layer 1 = formal *memoria de verificación* (one document per programme); Layer 2 = perceived *guías docentes* (~50–70 required courses per programme). Operational and ideological layers are explicitly out of scope.
- **Two-degree:** *Grado en Maestro de Educación Infantil* and *Grado en Maestro de Educación Primaria*.
- **Coding grid:** MRCDD primary (6 areas × 23 competences); DigCompEdu (@Redecker2017_digcompedu) as benchmark via an appendix mapping table.
- **Comparisons:** between layers (within programme), between degrees (within university — paired), and across the system.

### 2.4 Randomization

The only randomized component is the **20% reliability subsample**, which is drawn **a priori** (Variant B per strategy memo §6) via stratified random sampling across (degree × layer) cells. The random seed (`set.seed(20240901)`) and the resulting sample IDs will be deposited as the project file `reliability_subsample_ids.csv` **before** main coding begins.

The Tier B stratified sample of ~60 programmes is also drawn via stratified random sampling across the active sector × CCAA × modality cells of the universe. The seed, strata, and resulting programme IDs are deposited as `tier_b_sample_ids.csv`.

**RNG note (deposit correction, 2026-04-27).** Sample selection was executed via Python `numpy.random.default_rng(seed=20240901)`; the deposited `tier_b_sample_ids.csv` is the authoritative sample list. R analysis (κ, bootstrap, etc.) per `software_environment.md` uses `set.seed(20240901)` independently. The R reference script `scripts/R/strategy/tier_b_sample.R` encodes the same sampling algorithm but uses R's RNG; it cross-validates the algorithm but does NOT reproduce the deposited 60 IDs. See `data_engineering_environment.md` §4 for full reproducibility commitments.

---

## 3. Sampling Plan

### 3.1 Existing data

**No.** The corpus does not yet exist. It will be collected via web scraping of public university portals, the autonomous-community evaluation agencies, and the ANECA *Listado de Títulos*.

### 3.2 Explanation of existing data

Not applicable.

### 3.3 Data collection procedures

Per strategy memo §3 (sampling) and §4 (corpus), and per the data-exploration report:

1. **Layer 0 (programme universe):** Scrape RUCT (`https://www.educacion.gob.es/ruct/home`) via session-based POST against the consultation form; cross-validate against ANECA *Listado de Títulos*, gradomania.com 2024/2025 listings, and educaweb.com per-degree directory. Output: `corpus_inventory.csv` enumerating all `Grado en Maestro de Infantil` and `Grado en Maestro de Primaria` programmes active in academic year 2024–2025.
2. **Tier B sample selection:** Stratified random sample of ~60 programmes drawn from the universe via proportional allocation across active cells of a 4-level sector (public / private-traditional / private-online / *centros adscritos*) × 18-level CCAA × 2-level modality cross-tabulation. Cells with < 2 programmes are oversampled to a minimum of 2 (with the deficit absorbed from the largest cells), so every active stratum is represented.
3. **Layer 1 (*memorias de verificación*):** Download the version in force during 2024–2025 from a prioritized source list — (i) ANECA *Listado de Títulos*; (ii) autonomous-community evaluation agency (AQU Catalunya, ACSUG, UNIBASQ, AAC-DEVA, ACSUCYL, AQUIB, AVAP, Madri+d) for programmes verified by the regional agency; (iii) university transparency portal; (iv) university website downloads section; (v) direct request to the *Vicerrectorado de Ordenación Académica*.
4. **Layer 2 (*guías docentes*):** For each programme, scrape the per-course catalogue and download the *guía docente* for every required course (*básicas* + *obligatorias* + *Prácticum* + *TFG*). *Optativas* are excluded from the primary corpus and included only as a robustness check (B C1; see `robustness_plan.md`). For providers where guías are gated (e.g., UNIR — confirmed 403 in pilot), code the publicly available course descriptor and flag the entry as **descriptor-level only**.

### 3.4 Sample size

**Tier B target: ~60 programmes.** Drawn from the `[ASSUMED]` universe of ~144 programmes (range 135–185 with bounds), pending confirmation by the data-engineer's full RUCT scrape.

### 3.5 Sample size rationale

McNemar's test for paired proportions (per strategy memo §3):

$$n_{\text{pairs}} = \frac{(z_{\alpha/2} + z_{\beta})^2 \cdot p_d (1 - p_d)}{(p_2 - p_1)^2}$$

With $z_{\alpha/2} = 1.96$ ($\alpha = 0.05$, two-sided) and $z_{\beta} = 0.84$ (80% power), the required *matched-pair* sample size as a function of the within-university discordant-pair rate $p_d$ and the detectable difference $p_2 - p_1$ is the pre-registered sensitivity table at `power_sensitivity_table.csv` (deposited; reproducible from `scripts/R/strategy/power_sensitivity_table.R`). At anchor parameters $p_d = 0.30$ and $p_2 - p_1 = 0.10$ the formula yields $n_{\text{pairs}} = 165$ paired programmes. At $p_d = 0.30$ and $p_2 - p_1 = 0.15$, $n_{\text{pairs}} = 74$.

**Relationship to the Tier B sample size.** The Tier B target of ~60 *programmes* is a stratification target for descriptive coverage and depth estimation (the primary estimand) and is not equal to $n_{\text{pairs}}$. The *paired* analysis is restricted to universities in the Tier B sample whose institution also offers the complementary degree (Infantil ↔ Primaria) within the sample; the realized $n_{\text{pairs}}$ is determined post-sampling, pre-coding, and is reported transparently. The pre-registered sensitivity table commits the project to **reporting which detectable differences the realized $n_{\text{pairs}}$ supports at 80% power**, instead of claiming a single "powered for X" headline. Should the realized $n_{\text{pairs}}$ fall below the threshold to detect substantively meaningful differences (e.g., $\geq 0.15$), the paired analysis is reported as **descriptively underpowered** and the deviation is logged in §10.

### 3.6 Stopping rule

Data collection is complete when **either** (a) all sampled programmes have been processed, **or** (b) the realized retrieval rate at the *guía docente* layer falls below 50%, in which case the **Tier C fallback** is triggered (purposive subset of all public universities + 3 largest private/online providers, ~50 programmes; see strategy memo §3). Tier C activation is a logged deviation.

---

## 4. Variables

### 4.1 Manipulated variables

**None.** This is an observational design.

### 4.2 Measured variables (primary)

Per strategy memo §7:

- **Coverage** — binary presence (0/1) per (programme × layer × MRCDD area). Aggregation rule: `presence(programme, layer, area) = max` over all coded segments (Layer 1) or all required courses (Layer 2).
- **Depth** — ordinal 0–3 per (programme × layer × MRCDD area), where 0 = absent, 1 = mentioned, 2 = developed, 3 = assessed. Aggregation rule: `depth(programme, layer, area) = max` over segments/courses. *(The 0–3 scale is defended in strategy memo §5 against MRCDD's A1–C2, which describes teacher attainment, not curriculum depth.)*
- **Layer-gap categorical** — per (programme × degree × area), one of: *memoria-only*, *guía-only*, *both*, *neither*. The headline gap statistic per area is `P(memoria-only) + P(guía-only)`.

### 4.3 Measured variables (secondary)

- **Competence-level coverage and depth** at the 23-competence resolution (appendix table).
- **Number of courses touching the area** per (programme × area) at Layer 2 — an intensity measure used in robustness check B B3.
- **Per-coder uncertainty-flag rate** — see §6 (Reliability Protocol).

### 4.4 Indices and aggregation

- (Programme × layer × area) is the primary unit for descriptive estimands.
- (Degree × layer × area) is the headline-table aggregation: `coverage(D, L, a) = mean over programmes` of presence; `mean_depth(D, L, a) = mean over programmes` of depth; both reported with **bootstrap 95% CI** (1000 reps, resampling at the programme level).
- (Competence × layer × degree) reported in appendix tables.

---

## 5. Coding Scheme

This is the central methodological commitment of the pre-registration.

### 5.1 Framework

- **Primary:** MRCDD (BOE-A-2022-8042; @INTEF2022_mrcdd). 6 areas × 23 competences. Verified count of 23 competences per the BOE PDF (the BOE establishes "el Marco de Referencia de la Competencia Digital Docente que aquí se presenta tiene 23 competencias en lugar de 22").
- **Secondary:** DigCompEdu (@Redecker2017_digcompedu). 22 competences. Used as a European benchmark via the **MRCDD ↔ DigCompEdu mapping table** (appendix), constructed from INTEF's official documentation plus @Caena2019_aligning.

### 5.2 MRCDD areas (the six)

1. Compromiso profesional.
2. Recursos digitales.
3. Enseñanza y aprendizaje.
4. Evaluación y retroalimentación.
5. Empoderamiento del alumnado.
6. Desarrollo de la competencia digital del alumnado.

### 5.3 Coding approach

**Directed content analysis** (@HsiehShannon2005_qca): the framework supplies the codes a priori; coders apply them to text. Each codable segment is assigned to **at most one area** as primary and **at most one competence within that area**. Multi-area segments are coded once per area when both are clearly invoked, per the disambiguation flowchart in the coding manual.

**Inferential register:** the coder applies an MRCDD code when the segment **explicitly invokes** the area (verbatim or paraphrased) **OR** when it describes an activity, competence, or assessment that operationalizes the area.

### 5.4 Depth scale (0–3)

| Depth | Label | Operational definition |
|---|---|---|
| 0 | Absent | Area is not referenced in the document |
| 1 | Mentioned | Area is named or alluded to but no specific learning outcome, activity, or content is specified |
| 2 | Developed | Area is named AND tied to specific learning outcomes, content blocks, or pedagogical activities |
| 3 | Assessed | All criteria for Level 2 are met AND the document specifies an evaluation procedure (assessment criteria, rubric, weighted contribution to the course grade) tied to the area |

### 5.5 Coding manual

The coding manual is a **separate artifact**, finalized post-pilot, and **deposited as a project file before main coding begins**. The manual's required Table of Contents is in strategy memo §5 (12 sections including the disambiguation flowchart for the historically tricky pairs: Area 1 ↔ Area 5, Area 2 ↔ Area 3, Area 4 ↔ Area 6). The manual will be frozen in version `coding_manual_v1.0.pdf` before the OSF deposit is finalized.

### 5.6 Pilot

5 universities × 2 degrees × 2 layers = 20 (programme × layer) cells. Two independent blind coders. Iterate the manual (target: 2–3 iterations per @Krippendorff2018_content_analysis) until Cohen's κ ≥ 0.70 per area on the pilot subset. Re-pilot any area falling below 0.70.

---

## 6. Reliability Protocol

Per strategy memo §6 — locked-in **Variant B** (2026-04-26 user decision; see `quality_reports/decisions/strategy_cdd_formacion_inicial.md`).

| Element | Specification |
|---|---|
| **Number of coders** | **3** — A.R.J., M.G.J., C.B.T. (drawn from the author team). Meets the *preferred* level of the PAP, enabling majority arbitration on disagreements without recourse to a third party. |
| **Coder profile** | Members of the author team; familiar with the MRCDD and Spanish initial teacher training; trained on the coding manual; blind to each other's codings on the reliability subset. Specific academic qualifications (rank, doctoral status, prior coding experience) `[ANONYMIZED — to be filled at OSF deposit]`. |
| **Language coverage** | **Castilian Spanish** — all three coders. **Valencian** — C.B.T. only. **Catalan, Basque (Euskera), Galician** — *not covered* by the current coder team. Sensitivity sub-analysis 5 (PAP §7.2) is therefore restricted to (a) the *Valencian-language* corpus subset (coded by C.B.T.) and (b) Castilian-language parallel versions of documents originally published in Catalan / Basque / Galician where the issuing university provides both. Documents available *only* in Catalan / Basque / Galician without a Castilian parallel are excluded from the bilingual sensitivity analysis and the exclusion is logged as a pre-registered scope limit (deposited in §10 below at deposit time). |
| **Reliability statistic** | Cohen's κ for binary presence (per area); weighted κ (linear weights) for ordinal depth (0–3) per area; Krippendorff's α (ordinal metric) overall as a robustness statistic. |
| **Threshold (per area)** | κ ≥ 0.70 (per @Krippendorff2018_content_analysis "substantial agreement"; @LandisKoch1977_kappa). The COMDID Iberoamerican benchmark by @Lazaro2018_rubrica_latinoamerica reports per-dimension κ in this range, validating the threshold for Spanish-language teacher digital competence instruments. |
| **Threshold (overall)** | κ ≥ 0.80 across the full coding. |
| **Variant** | **B — 20% double + 80% single** (operational details B1, B2, B3 below). Variant A (full double-coding) was rejected on budget grounds (~50,000–70,000 codable segments at Layer 2 alone makes 2× coder cost prohibitive). |

### B1 — Timing of the 20% reliability sample

Drawn **a priori**, before main coding begins, via **stratified random sampling** across (degree × layer) cells with proportional allocation. The sample IDs and the random seed are deposited as `reliability_subsample_ids.csv` as part of the OSF deposit. This commits the reliability subset *before* any code is applied.

**RNG note (deposit correction, 2026-04-27).** The reliability subsample is drawn in R using `set.seed(20240901)` from within the R analysis stack (`software_environment.md`). The Tier B programme sample (PAP §3) is drawn separately in Python using `numpy.random.default_rng(seed=20240901)`; the two seeds happen to share the integer value but are applied to different PRNGs and operate on different sampling frames (programmes vs. coded segments). The deposited `tier_b_sample_ids.csv` and (forthcoming) `reliability_subsample_ids.csv` are each authoritative for their respective sampling step. See `data_engineering_environment.md` §4.

### B2 — Single-coder assignment in the 80% non-doubled set

Two trained coders share the single-coded corpus by **alternating rotation balanced across (degree × layer) strata** (~50/50 within each cell). **Uncertainty flag rule:** any segment a single coder marks as "boundary case" or "ambiguous" is **automatically escalated** to the second coder for independent coding. The resulting double-coded entry feeds into a per-coder uncertainty-rate tracker (reported in the methods section).

### B3 — Mid-stream κ recalculation

κ is recalculated at **25%, 50%, and 75% completion milestones** of the main coding, computed on the cumulative double-coded set (the a-priori 20% reliability sample plus uncertainty-flag escalations to that point). **If κ in any area falls below 0.70 at any milestone, all coding halts**, the manual is reviewed against the disagreement log, recalibrated if necessary, the affected segments are recoded, and a deviation is logged in §10 below.

### Disagreement resolution

Each disagreement is logged with the segment text and the two codings; resolved by (a) discussion to consensus when both coders agree on a re-reading; (b) arbitration by a third coder when consensus fails. The unresolved disagreement rate is reported in the methods section.

---

## 7. Analysis Plan

### 7.1 Primary descriptive analyses

Per strategy memo §7.1–7.5; full pseudo-code in `pseudo_code.md`.

- **Coverage tables, heatmaps, radar plots** per (degree × layer × MRCDD area) and per competence.
- **Depth analysis** with bootstrap 95% CI (1000 reps, programme-level resampling).
- **Layer-gap cross-tabulation** per area (4 categories: memoria-only / guía-only / both / neither) and headline gap rate `P(memoria-only) + P(guía-only)`.
- **Paired within-university comparisons** between Infantil and Primaria: McNemar's test for paired binary presence; paired Wilcoxon signed-rank for paired ordinal depth.
- **System variation** per (degree × layer × area): SD and IQR across programmes.

### 7.2 Pre-specified sub-analyses

Per strategy memo §8 (5 sub-analyses with literature-anchored expectations):

1. **Sector** (4 levels: public / private-traditional / private-online / *centros adscritos*).
2. **Modality** (in-person vs. online; provider-specific given pilot evidence — VIU public, UNIR gated, UCJC unconfirmed).
3. **Geography** (autonomous community); **not computed within the *adscrito* sector** because cell sizes are too small at Tier B (see strategy memo §3).
4. **Subject area within Layer 2** (language/literacy / STEM / social sciences / arts / *Prácticum* / *TFG*).
5. **Bilingual region documents** — restricted to (a) the Valencian-language subset (coder C.B.T.) and (b) Castilian-language parallel versions of documents originally in Catalan / Basque / Galician where universities publish both. The original-language-only Catalan / Basque / Galician corpus is excluded from this sub-analysis as a pre-registered scope limit driven by coder team language coverage (see §6).

Sub-analyses appear in the manuscript appendix; sub-analyses 1–4 may appear in the main results section if cell sizes after stratification permit meaningful comparison (≥ 5 programmes per cell).

### 7.3 Multiple-comparison policy

**No formal multiple-comparison correction (Bonferroni, Holm, or Benjamini-Hochberg) is applied.** Justification: p-values throughout this analysis are reported **descriptively**, to characterize the magnitude of paired differences relative to chance variation in the paired structure — **not** as tests of causal hypotheses. Each comparison is reported as a measurement-level descriptor with its own confidence interval, not as a screening procedure for true positives. Per strategy memo §7.4, this policy is pre-registered explicitly so reviewers cannot interpret it as post-hoc.

### 7.4 Causal-language policy

The manuscript will **not** use language like "causes," "effect of," "impact of," "explains," or "predicts" in connection with these descriptive findings. Permitted language: "associated with," "varies by," "is more prevalent in," "documented gap between," "differs across." Per strategy memo §7.6.

### 7.5 Robustness checks

All 21 robustness checks in `robustness_plan.md` are pre-registered. They span: sampling (A1–A4), coding-scheme (B1–B5), inclusion/exclusion (C1–C3), layer-gap (D1–D3), degree-comparison (E1–E3), and reporting (F1–F3) robustness. **Failing to run any pre-registered check is itself a reportable deviation.** Reporting location: appendix tables, one per check, with a one-paragraph interpretation.

---

## 8. Falsification / Sanity Checks

All 7 instrument-validation checks in `falsification_tests.md` are pre-registered as part of the planned analysis pipeline (Stage 7 of `pseudo_code.md`):

1. **Temporal sanity** — pre-2022 documents must not invoke MRCDD-specific labels.
2. **Substantive sanity** — clearly non-digital courses must code as zero on most areas.
3. **Logical bound** — *memoria* coverage should be substantively reconcilable with the union of *guía* coverage; off-diagonal observations are the layer gap and must be re-examined to confirm they are not coding errors.
4. **Synonym handling** — pure boilerplate "TIC" or "competencia digital" mention without substantive content must code as depth 1 (mentioned), not depth 2 (developed).
5. **Inter-area discrimination** — segments coded into ≥ 4 areas with depth ≥ 2 must be < 5% of all coded segments.
6. **Reliability stability over time** — Cohen's κ must not drop more than 0.10 across the first/middle/last thirds of the coding sessions.
7. **DigCompEdu re-aggregation consistency** — re-aggregated MRCDD codings (mapped to DigCompEdu) must show κ ≥ 0.70 against direct DigCompEdu coding on the pilot subcorpus *(optional but recommended)*.

Failures and remediations are logged in §10 below.

---

## 9. Timeline

| Phase | Activity | Approx. duration |
|---|---|---|
| 1 | RUCT scrape + Tier B sample selection (data-engineer) | ~2 weeks |
| 2 | Full corpus retrieval (~67 institutions × custom scrapers; per-institution scraper modules per `data_exploration_cdd_formacion_inicial.md` §5) | ~6–8 weeks |
| 3 | Coding pilot (5 universities × 2 degrees × 2 layers; iterate manual to κ ≥ 0.70 per area) | ~3–4 weeks |
| 4 | OSF deposit lock — freeze coding manual, deposit reliability subsample IDs, submit pre-registration | ~1 week |
| 5 | Main coding (~60 programmes × 50–70 courses × 6 areas) | ~3–4 months |
| 6 | Analysis (Stages 3–7 of `pseudo_code.md`) | ~6 weeks |
| 7 | Writing + internal review | ~3 months |
| **Total** | RUCT scrape → manuscript | **~12–15 months** |

---

## 10. Deviations Log

*(Empty at submission. Deviations from this pre-registration will be logged here with date, deviation, and rationale. The orchestrator commits to logging any deviation **before** the affected analysis is reported in the manuscript.)*

| Date | Section | Deviation | Rationale |
|---|---|---|---|
| 2026-04-27 | §3.3 (data collection) | RUCT scrape returned 0 parseable result rows on 2026-04-27 (the consultation form's POST endpoint accepted the request but the response did not contain a result table the heuristic parser could read; likely the form requires JavaScript-rendered pagination). The programme universe was therefore built from the cross-validation aggregate (gradomania + educaweb + ANECA + 8 autonomous-community agencies + manual adscritos override). | Per plan §7 fallback ladder. **User explicitly approved this fallback on 2026-04-27.** Realised universe: 168 active programmes, within the pre-registered [120, 170] range. `codigo_ruct` is empty for all rows; programme IDs are synthetic (`P0001`-`P0168`). The substitution does not affect downstream coding (the unit of analysis remains the (programme × layer × area) triple, not the RUCT code). Re-attempting the RUCT scrape with a JS-rendering driver (selenium/playwright) is a future-work option logged in `data_engineering_environment.md` §7. |
| 2026-04-27 | §2.4 (randomization) | Tier B realised N = 60 (PAP target) instead of "~60 with every active cell receiving min-2 draws". With 32 active cells in the realised universe, strict min-2 forces N ≥ 63. To deliver exactly N = 60, three low-information cells (Madrid×public×online, Murcia×public×presencial, Navarra×public×presencial — all small cells with universe size 1-2) were dropped from the SAMPLE (they remain in the universe). | Pragmatic resolution of the tension between PAP "~60" and "min-2-per-active-cell". **User explicitly chose N=60 over the strict-min-2 alternative N=63 on 2026-04-27** after orchestrator recommended N=63; the rationale was preserving the PAP-headline target. The min-2 rule holds for every cell that receives any draw; cells dropped are documented in `tier_b_strata_table.csv` with `dropped_for_n60 = TRUE`. Universe coverage in the descriptive estimands is not affected (those use the universe inventory, not the sample). |
| 2026-04-27 | §2.4 (randomization) | Sample selection executed via Python `numpy.random.default_rng(seed=20240901)` rather than R `set.seed(20240901)`. | The R analysis stack is unavailable on the data-engineering machine; the Python script is the authoritative deposit and the R reference script (`scripts/R/strategy/tier_b_sample.R`) is provided only for algorithmic cross-validation. R-based downstream analysis (κ, bootstrap, sub-analyses) uses `set.seed(20240901)` independently. See `data_engineering_environment.md` §4. |
| 2026-04-27 | §3.3 (data collection) | Inventory revised after coder-critic round-1 review: added Universitat Oberta de Catalunya (UOC; public-online, Cataluna), Universidad del Atlántico Medio (private-traditional, Canarias), Universidad Tecnología y Empresa (private-traditional, Madrid), and Universidad Católica Santa Teresa de Jesús de Ávila (alias of UCAV; private-traditional, Castilla y León) — institutions previously dropped because the curated `canonical_map` did not recognise their names, even though they appear in ANECA's national registry and / or AQU's Catalan probe. **Realised universe revised from 168 to 174 active programmes** (delta +6: +2 UOC, +2 Atlántico Medio, +2 Tecnología y Empresa; the UCAV alias merged into the existing UCAV row, no net add). The number of active stratification cells rose from 32 to 34 (UOC opens a new public-online-Cataluna cell; Atlántico Medio adds a private-traditional-Canarias-presencial cell). Min-feasible-N under strict min-2 rose from 63 to 67; with TARGET_N held at 60 (per Deviation 2), 4 low-information cells are now dropped from the sample (vs. 3 previously). The 60 Tier B sample IDs shifted as a consequence of the inventory revision (re-sort changes row positions, which propagate through the deterministic per-cell sampling indices). New IDs in `tier_b_sample_ids.csv` (regenerated 2026-04-27 second run; UOC P0118+P0119 are in the sample). Old 168-row / 60-ID outputs were not preserved (clean re-deposit; superseded by this revision). | Critic-driven correction. The change strictly improves universe coverage by recovering legitimate institutions previously dropped on classification grounds, not on substantive grounds. The recovered institutions all offer Maestro-Infantil and/or Maestro-Primaria grados in 2024-2025 and are listed in ANECA's `srv.aneca.es/ListadoTitulos` registry and/or the relevant autonomous-community agency probe. **The 174-programme realised universe is +4 above the [120, 170] sanity-check band stated in PAP §3.4** (which was tagged `[ASSUMED]` and described as "approximate" in strategy memo §3 — a placeholder estimate, not a hard constraint). The overshoot direction is monotonic improvement: 4 legitimate programmes recovered, no noise added. Truncating back to ≤170 would require dropping legitimate programmes, which is methodologically worse than honest disclosure. |

---

## 11. Citations

Same set as strategy memo §"Citations used in this memo". Full bibliographic detail in `quality_reports/literature/cdd_formacion_inicial/references.bib`.

@INTEF2022_mrcdd; @BOE2022_mrcdd; @Redecker2017_digcompedu; @Caena2019_aligning;
@Goodlad1979_curriculum_inquiry; @Sandvik2023_norway_ecte_curriculum; @Instefjord2017_norway_curriculum;
@HsiehShannon2005_qca; @Krippendorff2018_content_analysis; @LandisKoch1977_kappa;
@Lazaro2018_rubrica_latinoamerica; @TrujilloSaez2020_panorama;
@Cuevas2025_curriculum_efl; @Cuevas2024_tpack_primary; @Cabero2023_evaluacion_review;
@SanzBenito2024_inclusion_digital; @SanzBenito2023_inclusion_review;
@Peirats2018_planes_estudios; @Granados2020_profesorado_tic;
@BOE2007_RD1393; @BOE2007_ECI3854_infantil; @BOE2007_ECI3857_primaria; @LOMLOE2020.

---

## Pre-Registration Checklist — `[ASSUMED]` items for user review before deposit

The following placeholders must be reviewed and resolved by the user before this document is submitted to OSF:

- [x] **Author team identified** — 4 authors (A.R.J., M.G.J., C.B.T., P.P.G.), single common institution, A.R.J. corresponding (per §1.2). **Names, institution, and email** intentionally anonymized in the draft; to be filled in before submission to OSF.
- [x] **Programme universe count** — realised count is **174 active programmes** (revised 2026-04-27 from 168 after coder-critic round-1 review; +6 from recovering UOC + 3 ANECA-only legitimate institutions previously dropped on classification grounds — see §10 Deviation 4). The strategy memo's `[ASSUMED]` ~144 estimate is replaced by this count; the revised count is +4 above the pre-registered [120, 170] ceiling, documented as a minimal deviation from monotonic-improvement. RUCT scrape unavailable on 2026-04-27 (form returned no parseable result rows); the universe is built from the cross-validation aggregate (gradomania + educaweb + ANECA + 8 autonomous-community agencies + manual adscritos override) per plan section 7 fallback ladder. This substitution is logged as a deviation in §10. Deposit file: `data/cleaned/corpus_inventory.csv`. Reconciliation log: `data/cleaned/inventory_reconciliation_log.md`.
- [x] **Specific universities sampled in Tier B** — drawn 2026-04-27 via Python `numpy.random.default_rng(seed=20240901)` against the realised 174-programme universe (revised count after coder-critic round 1). **Realised N = 60 programmes** across 30 of the 34 active stratification cells (4 low-information cells dropped from the sample to maintain N=60 + min-2-per-cell-in-sample; up from 3 dropped in the 168-universe pre-revision draw because UOC opens a new public-online-Cataluna cell and Atlántico Medio adds a private-traditional-Canarias cell). Sample composition: 30 public, 18 private-traditional, 6 private-online, 6 adscrito; 15 CCAAs represented; 29 Infantil + 31 Primaria; 52 presencial + 8 online. UOC (P0118 + P0119) is in the sample. First 5 sampled IDs: P0003, P0004, P0009, P0011, P0018. Deposit file: `data/cleaned/tier_b_sample_ids.csv`. Strata table: `data/cleaned/tier_b_strata_table.csv`. Reproducibility check: `data/cleaned/reproducibility_check.txt`.
- [x] **Coder team identified** — 3 coders (A.R.J., M.G.J., C.B.T.), drawn from the author team (per §6). Language coverage: Castilian (all three) + Valencian (C.B.T.); Catalan / Basque / Galician *not covered* — bilingual sub-analysis 5 scope-restricted accordingly. Specific academic qualifications anonymized in the draft; to be filled in before OSF submission.
- [x] **Ethics / IRB and funding declared in §1.5** — both as `[ANONYMIZED — pending OSF deposit]`. Working position pre-registered: no IRB needed (no human subjects); the existence of an institutional exemption letter and the funding source will be filled in before submission.
- [x] **Software environment lock-protocol committed** — full lock procedure deposited as `software_environment.md`. Pre-registered closed package set: `tidyverse`, `irr`, `psych`, `boot`, `ggplot2`, `fmsb`, `pheatmap`, `scales`, `here`, `renv`. Concrete versions and `renv.lock` deposited at pilot start; adding any package after that is a logged deviation.
- [ ] **Coding manual `coding_manual_v1.0.pdf`** — to be produced post-pilot and deposited before main coding begins. The required TOC is in strategy memo §5.
- [ ] **Reliability subsample IDs `reliability_subsample_ids.csv`** — to be generated and deposited before main coding begins, using the pre-registered seed.
- [x] **Tier B sample IDs `tier_b_sample_ids.csv` deposited** — see the previous "Specific universities sampled in Tier B" item; the same 60-row deposit file closes both checklist references (formerly C3 and C9).
- [x] **Power sensitivity table `power_sensitivity_table.csv` deposited** — 9-cell table over $p_d \in \{0.20, 0.30, 0.40\}$ × $p_2-p_1 \in \{0.05, 0.10, 0.15\}$ produced from the pre-registered formula in §3.5. Reproducible from `scripts/R/strategy/power_sensitivity_table.R`.

Once each item is resolved, this checklist becomes the deposit's reproducibility manifest.
