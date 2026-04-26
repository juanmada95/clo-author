# Strategy Memo — Curricular Analysis of TDC in Spanish Initial Teacher Training

**Project:** Post-MRCDD, two-degree, two-layer curricular analysis of how the Spanish *Grado en Maestro de Educación Infantil* and *Grado en Maestro de Educación Primaria* develop Teacher Digital Competence.
**Date:** 2026-04-26
**Strategist:** Claude (Opus 4.7) via `/strategize`
**Phase:** Strategy (severity: constructive)
**Paper type:** **Descriptive / Measurement** (curricular content analysis). No causal estimand; no treatment; no comparison group in the inferential sense. Comparisons are **between curricular layers** (*memoria* vs. *guía docente*) and **between degrees** (Infantil vs. Primaria) within a measurement-design frame.

**Companion artifacts (same project folder under `quality_reports/strategy/cdd_formacion_inicial/`):**
- `pseudo_code.md` — analytical pipeline pseudo-code
- `robustness_plan.md` — sensitivity and robustness checks
- `falsification_tests.md` — sanity / falsification checks for the coding instrument

---

## 1. Research question (one sentence)

> **To what extent and at what depth do the *memorias de verificación* (formal curriculum) and the *guías docentes* (perceived curriculum) of Spanish *Grado en Maestro de Educación Infantil* and *Grado en Maestro de Educación Primaria* programmes integrate the six areas and twenty-three competences of the *Marco de Referencia de la Competencia Digital Docente* (MRCDD; Resolución de 4 de mayo de 2022, BOE-A-2022-8042), and where do systematic gaps appear — between the two layers, between the two degrees, and across the Spanish university system?**

This is a **descriptive measurement question**. It does not ask "what causes" anything; it asks "how much, where, and where are the gaps."

### Sub-questions (descriptive estimands)

- **SQ1 (Coverage):** What proportion of the MRCDD's six areas (and twenty-three competences) appears in each (*degree* × *layer*) combination, by university and in aggregate?
- **SQ2 (Depth):** Conditional on appearance, at what coded depth (0 = absent, 1 = mentioned, 2 = developed, 3 = assessed) is each area integrated?
- **SQ3 (Layer gap, per Goodlad):** For each (*university* × *degree* × *area*), is the area present in the *memoria* only, the *guía docente* only, both, or neither — and what is the depth differential when both are present?
- **SQ4 (Degree gap):** Within universities offering both degrees, how do Infantil and Primaria compare on coverage and depth, area by area?
- **SQ5 (System variation):** How does coverage/depth vary across the Spanish university system, and is that variation patterned by sector (public vs. private), modality (in-person vs. online), or autonomous community?

---

## 2. Unit(s) of analysis

The design is **multi-level**. Each level has a distinct unit and aggregation rule.

| Level | Unit | Description | `n` (per `[ASSUMED]` working estimate) |
|---|---|---|---|
| 0 | Institution | University (e.g., UAB, UCM, Universidad de Sevilla) | ~80–90 institutions [ASSUMED] |
| 1 | Degree programme | Distinct accredited programme: Infantil and/or Primaria, per institution | ~140–170 programmes [ASSUMED] |
| 2 | Curricular layer | Within a programme: the *memoria de verificación* (1 document) and the set of *guías docentes* (many) | 2 layers × N programmes |
| 3 | Course (*asignatura*) | Layer-2 only: each subject in the programme's plan of studies | ~50–70 courses per Grado [ASSUMED] |
| 4 | Codable text segment | Paragraph or bullet inside a *memoria* section (Layer 1) or inside a *guía docente* field (Layer 2) | many per document |
| 5 | Code application | A (segment, MRCDD area, MRCDD competence, depth, coder) tuple | thousands |

**Primary unit for descriptive estimands:** the **(programme × layer × MRCDD area)** triple. SQ1–SQ4 estimands are computed at this level, then aggregated up to (degree × layer × area) for headline tables and down to (programme × layer × area × competence) for detailed appendix material.

**Aggregation rule for Layer 2:** A programme's *guía docente*-layer coverage of an area is the **maximum depth** over all its courses for that area (not the mean). Justification: a competence developed in even one course is part of the perceived curriculum the programme delivers. We additionally report the **count of courses touching the area** as a secondary intensity measure.

**Note:** Heatmaps and radar plots aggregate to (programme × area) and (degree × area) respectively. A long-form coded dataset (one row per code application, Level 5) is the canonical analytical artifact; everything else is derived by aggregation.

---

## 3. Population and sampling frame

### Target population

All Spanish degree programmes accredited as either:
- *Grado en Maestro de Educación Infantil* (under Real Decreto 1393/2007 + Orden ECI/3854/2007), or
- *Grado en Maestro de Educación Primaria* (under Real Decreto 1393/2007 + Orden ECI/3857/2007),

and listed in **RUCT** (Registro de Universidades, Centros y Títulos), as of 2026-09-01 (the snapshot date). Both public and private universities are included; both in-person and online modalities are included; both single- and dual-degree (PEP — *Programa de Estudios Paralelos*) configurations are included.

**Exclusions:**
- *Máster en Profesorado* (Secondary). Different population, different ECI Orden, different framework.
- *Grados* in non-Spanish-system institutions (e.g., UNED Costa Rica branch).
- Discontinued programmes whose last cohort graduated before academic year 2024–2025.

### Sampling decision — Tier B (locked-in 2026-04-26 after data-discovery round)

**Tier B — stratified random sample of ~60 programmes** is the locked-in primary design, chosen on evidence after a 10-institution pilot reported in `quality_reports/data_exploration_cdd_formacion_inicial.md` (and reviewed at 79/100 NEEDS REVISION in `quality_reports/data_exploration_cdd_formacion_inicial_review.md`). The pilot's measured Layer 2 retrieval rate is 5/10 = 50% with Wilson 95% CI [24%, 76%] — the 80% Tier A trigger sits above the upper bound of the CI, so the census recommendation is not statistically supportable from the pilot. The strategist (orchestrator) decision in consultation with the user: choose Tier B up-front rather than expand the pilot.

| Tier | Coverage | Status | Justification |
|---|---|---|---|
| **B — Stratified random sample of ~60 programmes** (primary) | ~60 programmes drawn proportionally from a 4-level sector × 18-level CCAA × 2-level modality cross-tabulation of the universe (~144 programmes [ASSUMED] pending the data-engineer's full RUCT scrape). Sector levels: (1) public, (2) private-traditional, (3) private-online, (4) *centros adscritos* — promoted to a sector level per `data_exploration_cdd_formacion_inicial_review.md` MAJOR-6, since adscritos have distinct *memorias* from their parent universities. | **Locked-in.** | Pilot retrieval evidence does not support Tier A. Tier B is the field-standard fallback and supports all primary estimands at adequate power (see formula below). |
| **A — Census of all RUCT-listed programmes** | All ~144 (~135–185 with bounds) | **Rejected on evidence.** | Pilot N=10 produced Wilson 95% CI [24%, 76%] on Layer 2 retrieval; 80% threshold is outside this CI on the optimistic side. The "first comprehensive census" framing is replaced with "first post-MRCDD, two-degree, two-layer stratified analysis" — the conjunction-of-qualifiers contribution argument still holds. |
| **C — Purposive subset of all public unis + 3 largest private/online** | ~50 programmes | **Final fallback.** | Triggered only if Tier B's actual retrieval rate during the data-engineer's main pull falls below 50% — i.e., if the optimistic 75–80% pilot interpolation turns out to overstate the population rate. The 50% trigger is below the pilot's conservative 50% estimate, so this contingency is unlikely to fire but is reserved for transparency. |

**Power calculation (Tier B):** McNemar's test for paired proportions:
$$n = \frac{(z_{\alpha/2} + z_{\beta})^2 \cdot p_d (1 - p_d)}{(p_2 - p_1)^2}$$
where $p_1, p_2$ are the area-presence proportions in Infantil and Primaria respectively, $p_d$ is the discordant-pair rate, $z_{\alpha/2} = 1.96$, $z_{\beta} = 0.84$. Assuming baseline coverage $p_1 = 0.50$ (mid-range per the literature), target detectable difference $p_2 - p_1 = 0.10$, and discordant-pair rate $p_d = 0.30$ (moderate within-university paired correlation), required $n \approx 60$ matched university-pairs offering both degrees. The exact assumed values and a sensitivity table will be deposited with the OSF pre-registration.

**Stratification cells.** With 4 sector levels × 18 CCAA × 2 modality, the unrestricted cross has 144 cells, of which most are empty (e.g., online + Ceuta = 0). After collapsing empty cells, the active stratification cross has ~30–35 cells. Proportional allocation of n=60 across active cells gives ~2 programmes per cell on average; cells with < 2 programmes are oversampled to a minimum of 2 (with the deficit absorbed from the largest cells), so every active stratum is represented.

**Centros adscritos warning** (per `data_exploration_cdd_formacion_inicial_review.md` MAJOR-6): the adscrito × CCAA cell at proportional allocation yields 0–1 programmes per CCAA. **Sub-analysis 3 (geographic) is therefore not computed within the adscrito sector** — adscritos are reported as a sector-level summary only.

`[ASSUMED]` Total N ≈ 144 programmes (range 135–185 with bounds), ~67–70 institutions. Confirmation requires the data-engineer's full RUCT scrape as the first task of the coder phase; until then, the stratification is implementable on the pilot's universe estimate, with re-balancing once the scrape completes.

### Snapshot

- **Academic year:** **2024–2025** (most recent fully completed year for which all *guías docentes* are stable).
- **`[ASSUMED]`** *Memorias* corpus: **last *memoria modificada* in force as of 2024–2025**. If a programme's *memoria* was modified during 2024–2025, code the version that governed the academic year (typically the one effective on 2024-09-01).
- **Snapshot rationale:** matches Sandvik et al. (2023) and Cuevas-Monzonís et al. (2024, 2025); ensures replicability and rules out post-snapshot changes contaminating the corpus.

---

## 4. Documents coded — the corpus

### Layer 1 — *Memoria de verificación* (formal curriculum, per Goodlad)

- **Definition:** the official document submitted to ANECA (or the autonomous community's evaluation agency) for accreditation, version in force during academic year 2024–2025.
- **Source priority:** (1) ANECA registry (covers nationally-evaluated programmes); (2) **autonomous-community evaluation agency** for programmes verified by the regional agency rather than ANECA — AQU Catalunya, ACSUG (Galicia), UNIBASQ (País Vasco), AAC-DEVA (Andalucía), ACSUCYL (Castilla y León), AQUIB (Illes Balears), AVAP (Comunitat Valenciana), Madri+d (Comunidad de Madrid); (3) university transparency portal; (4) university website downloads section; (5) direct request to the *Vicerrectorado de Ordenación Académica*. The 8 autonomous-community agencies are added per `data_exploration_cdd_formacion_inicial_review.md` MAJOR-3 — ANECA does not cover programmes verified by the regional agencies, so for ~9 of the most-likely-coded universities (e.g., the Catalan and Galician public systems) the regional agency is the primary source, not the fallback.
- **Sections to code:** typically *Competencias Generales*, *Competencias Específicas*, *Competencias Transversales*, *Planificación de Enseñanzas* (módulos and materias), and *Sistemas de Evaluación*. Other sections (resources, justification, governance) are out-of-scope for digital-competence coding but are read for context.
- **Unit of analysis at this layer:** **degree programme**. One *memoria* per programme.

### Layer 2 — *Guías docentes* (perceived curriculum, per Goodlad)

- **Definition:** the per-academic-year syllabus document for an individual course (*asignatura*), governing teaching in 2024–2025.
- **Course inclusion criteria:**
  - **Include all required courses:** *básicas* + *obligatorias* (per the *memoria*'s plan of studies). These constitute the curriculum every graduate completes.
  - **Include *Prácticum* and *TFG*:** code with a separate sub-protocol because their *guías docentes* are typically less detailed; code based on the rubric/competences explicitly listed.
  - **Optativas:** by default **exclude** from the primary coverage estimand. Sub-analysis: include *optativas* whose title or description suggests digital-competence content (e.g., "TIC aplicadas a la educación", "Tecnología educativa") and report a separate **"with-optatives"** coverage estimate as a robustness check (see `robustness_plan.md`).
- **Source priority:** (1) university course-catalogue portal; (2) faculty website; (3) direct PDF download; (4) Wayback Machine if the 2024–2025 version was replaced.
- **`[ASSUMED]`** *Guías docentes* are systematically published. The librarian flagged that public universities reliably publish them; private/online providers vary. Pilot will quantify the retrieval rate.
- **Unit of analysis at this layer:** **course**, aggregated to programme.

### Out-of-scope layers

- **Operational curriculum** (what is actually taught in the classroom): explicitly out-of-scope. Acknowledged as a limitation; framed as the natural follow-up.
- **Ideological curriculum** (BOE/LOMLOE/Orden ECI): not coded; cited as legal context in the introduction and the methods section.

### Document accessibility — known issues `[ASSUMED]`

- *Guías docentes* of online universities are **provider-specific in accessibility** (revised per data-discovery 2026-04-26): **VIU publishes guías docentes openly** as PDFs directly downloadable from the plan-de-estudios page (refutes the prior assumption); **UNIR is gated** (HTTP 403 confirmed in the pilot) — institutional email request OR descriptor-level coding flagged as "descriptor-level only"; **UCJC is unconfirmed** in the pilot — to be probed in the data-engineer's full pull. For any provider where guías are gated and institutional access is unavailable, code the publicly-available course descriptor and flag the entry as "descriptor-level only".
- Some *memorias* are only available as the *última versión modificada* without an archived earlier version. Mitigation: snapshot is unambiguous (in force during 2024–2025); only one version per programme is coded.
- Bilingual programmes (Catalan, Basque, Galician, Valencian) publish *guías docentes* in the regional language. Mitigation: coders include readers competent in each regional language; or use the Spanish-language version when both are published; flag any monolingual-regional-only documents.

---

## 5. Coding scheme — operationalizing MRCDD as a coding instrument

This is the **central methodological contribution**. The coding manual is a separate artifact; this section specifies its design.

### Primary grid — MRCDD

The MRCDD (Resolución 4 mayo 2022, BOE-A-2022-8042; @INTEF2022_mrcdd) defines:
- **6 areas:** (1) Compromiso profesional; (2) Recursos digitales; (3) Enseñanza y aprendizaje; (4) Evaluación y retroalimentación; (5) Empoderamiento del alumnado; (6) Desarrollo de la competencia digital del alumnado.
- **23 competences** distributed across the 6 areas.
- **6 progression levels** (A1, A2, B1, B2, C1, C2) per competence.

Each codable segment is assigned to **at most one area** (primary) and **at most one competence within that area** (specific). Multi-area segments are coded once per area (i.e., the same segment can be tagged in Area 2 AND Area 4) when both are clearly invoked; the coding manual specifies the disambiguation rules.

### Secondary grid — DigCompEdu (European benchmark)

The MRCDD is operationally aligned with DigCompEdu (Redecker & Punie 2017; @Redecker2017_digcompedu) but the 22 DigCompEdu competences and the 23 MRCDD competences are not in one-to-one correspondence. The strategy:
- Code primarily against MRCDD.
- Provide a **MRCDD ↔ DigCompEdu mapping table** in an appendix (constructed from INTEF's official documentation plus the analytical mapping in @Caena2019_aligning), so that European readers can re-aggregate the findings to the DigCompEdu structure.

### Coding approach — directed content analysis

Per @HsiehShannon2005_qca, this is **directed content analysis**: the framework supplies the codes a priori; coders apply them to text. This is the same methodological grammar used by @Sandvik2023_norway_ecte_curriculum and @Instefjord2017_norway_curriculum.

**Inferential register:** the coder applies an MRCDD code when the segment **explicitly invokes** the area (verbatim or paraphrased) **or when it describes an activity, competence, or assessment that operationalizes the area**. The coding manual provides:
- One **anchor example** per area drawn from a coded *memoria* or *guía docente*.
- Three **boundary cases** per area (one clear-positive, one clear-negative, one ambiguous-with-decision-rule).
- A **disambiguation flowchart** for segments that could plausibly fall into more than one area.

### Depth scoring

For each (document, MRCDD area) pair where the area is present, code depth on a **0–3 ordinal scale**:

| Depth | Label | Operational definition |
|---|---|---|
| 0 | Absent | Area is not referenced in the document |
| 1 | Mentioned | Area is named or alluded to but no specific learning outcome, activity, or content is specified |
| 2 | Developed | Area is named AND tied to specific learning outcomes, content blocks, or pedagogical activities in the document |
| 3 | Assessed | All criteria for level 2 are met AND the document specifies an evaluation procedure (assessment criteria, rubric, weighted contribution to the course grade) tied to the area |

**Why 0–3 and not A1–C2:** the MRCDD's six progression levels describe *teacher* attainment, not *curriculum* depth. Trying to map curriculum text to teacher-level CEFR-style descriptors invites coder confusion (the librarian-critic flagged this as an intercoder reliability risk). The 0–3 scale mirrors the Bloom-like progression mention → development → assessment that is meaningful for documents. The strategy is to report the simple 0–3 scale primarily and provide an appendix mapping to A1–C2 for readers who need it.

**Aggregation:** at the programme × layer × area level, the depth score is the **maximum** across all coded segments (Layer 1) or all coded courses (Layer 2). Aggregation to the (degree × area) level uses the **mean** across programmes within the degree, with bootstrap confidence intervals.

### Coding manual — required table of contents

The strategist drafts the manual's TOC; the manual itself is produced before the coder phase activates.

```
Coding Manual — MRCDD Curricular Analysis of Initial Teacher Training in Spain
 1. Purpose, scope, and snapshot
 2. Documents and units of analysis
 3. The MRCDD grid: 6 areas × 23 competences (full text reproduced from INTEF 2022)
 4. Anchor examples per area
       — Target: 2–3 anchor examples per area (per Sandvik et al. 2023; Hsieh
         & Shannon 2005), drawn from coded memorias and guías. Single anchors
         risk coder over-fixation on a single salient case.
 5. Boundary cases per area
       — Target: per area, one clear-positive + one clear-negative + one
         ambiguous-with-decision-rule. Boundary cases drive the disambiguation
         in §6 below.
 6. Disambiguation flowchart for multi-area segments
       — Required disambiguation pairs (the historically tricky ones in
         MRCDD/DigCompEdu coding):
           (a) Area 1 (Compromiso profesional) ↔ Area 5 (Empoderamiento del
               alumnado): when a segment refers to teacher reflection AND
               student inclusion.
           (b) Area 2 (Contenidos digitales) ↔ Area 3 (Enseñanza y
               aprendizaje): when a segment refers to creating digital
               resources for teaching activity.
           (c) Area 4 (Evaluación y retroalimentación) ↔ Area 6 (Desarrollo
               de la competencia digital del alumnado): when a segment
               refers to assessing student digital outputs.
       — Decision rules: prefer the more specific area; use the activity verb
         (verb test); when both are explicit, code in both areas (multi-area
         segment).
 7. Depth scoring rubric (0–3) with worked examples
       — Target: ≥3 worked examples per depth level (1 from a Layer-1 memoria
         + 2 from Layer-2 guías docentes, mixing degree and subject area).
       — Field convention (per Sandvik et al. 2023, Hsieh & Shannon 2005).
 8. Special protocols
   8.1 Prácticum and TFG
   8.2 Optativas (when included in robustness)
   8.3 Bilingual / regional-language documents
   8.4 Descriptor-level-only entries (online providers without full guías)
 9. MRCDD ↔ DigCompEdu mapping table
10. Coder workflow: software, tagging conventions, version control of codings
11. Disagreement resolution protocol (arbitration; logged disagreement rate)
12. Pilot iterations: change log of the manual through pilot rounds
```

### Pilot

- **Sample:** 5 universities × 2 degrees × 2 layers = 20 (programme × layer) cells, with the Layer-2 cells aggregating across all required courses in those programmes. Universities chosen to span (public + private), (peninsular + insular), (Castilian-only + bilingual region), and (in-person + online).
- **Coders:** 2 independent coders, blind to each other's codings.
- **Iteration target:** Cohen's κ ≥ 0.70 per area on the pilot, computed at the (segment × area-presence) level. If any area falls below 0.70, revise the manual (sharpen the anchor example or boundary cases) and re-pilot that area.
- **Number of iterations expected:** 2–3 (per @Krippendorff2018_content_analysis, two-round iteration is typical).
- **Pilot output:** finalized coding manual (frozen version, deposited to OSF before main coding begins).

---

## 6. Intercoder reliability protocol

| Element | Specification |
|---|---|
| **Number of coders** | Minimum 2; preferred 3 (so that majority arbitration is possible without third-party intervention). |
| **Coder profile** | Researchers familiar with the MRCDD and Spanish initial teacher training; trained on the manual; blind to each other's codings during the reliability sample. |
| **Reliability statistic** | **Cohen's κ** for binary presence (per area), **weighted κ** (linear weights) for ordinal depth (0–3). Per @Krippendorff2018_content_analysis, also report **Krippendorff's α** with ordinal metric as a robustness check, since α handles missing data and >2 coders gracefully. |
| **Threshold (per area)** | κ ≥ 0.70 (per @LandisKoch1977_kappa "substantial agreement" threshold and @Krippendorff2018_content_analysis). The COMDID Iberoamerican benchmark by @Lazaro2018_rubrica_latinoamerica reports per-dimension κ in this range, validating the threshold for Spanish-language teacher digital competence instruments. |
| **Threshold (overall)** | κ ≥ 0.80 across the full coding (per Krippendorff 2018). |
| **Coding-protocol variant** | **B — 20% double + 80% single (with operational details locked-in below).** Variant A (full double-coding of the entire corpus) was considered but rejected on budget grounds (≈ 50,000–70,000 codable segments at Layer 2 alone makes 2× coder cost prohibitive). Variant B is the field standard (Krippendorff 2018) and is realistic at a 1.2× single-coder budget. |
| **B1 — Timing of the 20% reliability sample** | Drawn **a priori** (before main coding begins), via stratified random sampling across (degree × layer) cells with proportional allocation. The sample IDs are deposited as part of the OSF pre-registration package, so the reliability subset is fixed before any code is applied. |
| **B2 — Single-coder assignment in the 80% non-doubled set** | Two trained coders share the single-coded corpus by **alternating rotation balanced across (degree × layer) strata** — each coder owns ~50% of the single-coded segments, with neither coder concentrated in any single (degree × layer) cell. **Uncertainty flag rule:** any segment a single coder marks as "boundary case" or "ambiguous" is **automatically escalated** to the second coder for independent coding; the resulting double-coded entry feeds into a per-coder uncertainty-rate tracker (reported in the methods). |
| **B3 — Mid-stream κ recalculation cadence** | κ is recalculated at **25%, 50%, and 75% completion milestones** of the main coding, computed on the cumulative double-coded segments available at each milestone (i.e., the a-priori 20% reliability sample plus any uncertainty-flagged escalations to that point). **If κ in any area falls below 0.70 at any milestone, all coding halts**, the manual is reviewed against the disagreement log, recalibrated if necessary, the affected segments are recoded, and a deviation is logged for the OSF deposit. |
| **Disagreement resolution** | Each disagreement is logged with the segment text and the two codings; resolved by (a) discussion to consensus when both coders agree on a re-reading; (b) arbitration by a third coder when consensus fails. The **unresolved disagreement rate** is reported in the methods section. |
| **Reporting** | A reliability table in the manuscript: κ per area, weighted κ for depth per area, Krippendorff's α overall, the cumulative κ trajectory across the three milestones, the per-coder uncertainty-flag rate, the disagreement rate, and the number of arbitrated cases. |

---

## 7. Analytical strategy — descriptive and comparative

All analyses are **descriptive measurement**. No causal language. Comparisons are between curricular layers and degrees, framed as documented differences in measured curricular content, not as effects of treatments.

### 7.1 Coverage statistics

- **Per area, per layer, per degree:** proportion of programmes coding ≥ 1 (presence) and proportion coding ≥ 2 (developed) for each MRCDD area.
- **Per competence:** the same, at the 23-competence resolution. Reported in an appendix table.
- **Per university:** programme-level coverage table (one row per (university × degree × layer)). Reported in supplementary material.
- **Output artifacts:** coverage tables (six rows × 4 columns per degree); heatmaps (university × area, faceted by degree × layer); radar plots (degree × area, separate for each layer).

### 7.2 Depth analysis

- **Per (degree × layer × area):** mean depth (0–3 scale), with **bootstrap 95% CI** (resampling programmes with replacement, 1000 reps; one-sided lower bound reported when the question is "is depth above the 'mentioned' floor").
- **Per (degree × layer × area):** distribution of depth across programmes (histogram or density). This matters because mean masks bimodal distributions (a few programmes assess; most just mention).
- **Comparison:** depth difference between Infantil and Primaria within paired universities (paired Wilcoxon, with effect-size r); depth difference between *memoria* and *guía docente* within paired (university × degree) (paired Wilcoxon).

### 7.3 Layer gap (Goodlad — formal vs. perceived)

For each (university × degree × area), construct a four-level categorical:
- *Memoria* only (formal commitment without perceived implementation)
- *Guía docente* only (perceived implementation without formal commitment — typically arises when a *memoria* is generic but courses pick up the slack)
- Both (aligned)
- Neither

Report the cross-tabulation per area, with proportions. The **headline gap statistic per area** is `P(Memoria-only) + P(Guía-only)` — the rate of misalignment.

### 7.4 Degree gap (Infantil vs. Primaria)

- **Within universities offering both degrees:** paired comparisons per area (presence + depth). Report McNemar's test for paired binary presence and paired Wilcoxon for paired depth, **descriptively** — the p-value is reported as a measure of whether the observed difference exceeds chance variation in the paired structure, not as a hypothesis test of a causal effect.
- **Across universities:** unpaired comparison as a sensitivity check.
- **Multiple-comparison policy:** no formal correction (Bonferroni / Benjamini-Hochberg / Holm) is applied. Justification: p-values throughout this analysis are reported descriptively, to characterize the magnitude of paired differences relative to chance variation in the paired structure — not as tests of causal hypotheses. The 6 areas × 2 layers × 2 degrees comparison space generates ~24 paired tests, but each is reported as a measurement-level descriptor with its own confidence interval, not as a screening procedure for true positives.

### 7.5 System variation

- **Between-programme heterogeneity within (degree × area):** report standard deviation of presence and depth, plus the interquartile range. A high SD signals systematic between-university variation that is itself a finding.
- **Stratification:** report coverage stratified by (a) sector (public vs. private), (b) modality (in-person vs. online), (c) autonomous community. Pre-specified in §8.
- **No regression of coverage on institutional characteristics is run as a primary analysis.** A regression would invite causal interpretation. If included as exploratory material in an appendix, frame strictly as descriptive associations.

### 7.6 No causal claim

The manuscript will **not** use language like "causes," "effect of," "impact of," "explains," or "predicts" in connection with these descriptive findings. Permitted language: "associated with," "varies by," "is more prevalent in," "documented gap between," "differs across."

---

## 8. Pre-specified sub-analyses

Pre-declared to forestall post-hoc selection. All sub-analyses are descriptive and use the same coverage / depth / layer-gap estimands as the main analysis.

| # | Sub-analysis | Stratum | Pre-specified expectation (from literature) |
|---|---|---|---|
| 1 | Public vs. private vs. *centros adscritos* | Sector (4 levels: public, private-traditional, private-online, adscritos) | No strong prior between public and private (literature mixed: B5, B7). *Centros adscritos* (~15 institutions) reported as a separate sector summary — they have distinct *memorias* from their parent universities and are promoted from the prior public/private dichotomy per `data_exploration_cdd_formacion_inicial_review.md` MAJOR-6. |
| 2 | In-person vs. online | Modality | Online providers vary by institution (per the data-discovery revision: VIU is fully open; UNIR is gated; UCJC unconfirmed). Per-area pattern: may be higher on Areas 2 and 3 — resources, teaching — (digital-native delivery context), and may be lower on Areas 1 and 4. |
| 3 | Geographic — autonomous community | 17 communities + Ceuta + Melilla | Catalonia (where COMDID was developed; Lázaro-Cantabrana cluster) plausibly higher; rural-region universities (Extremadura, Castilla-La Mancha) plausibly lower. **Not computed within the adscrito sector** — adscrito × CCAA cells are too small (0–1 programmes) at Tier B, per `data_exploration_cdd_formacion_inicial_review.md` MAJOR-6. |
| 4 | Subject area within Layer 2 | Course type: language/literacy / STEM / social sciences / arts / *Prácticum* / *TFG* | EFL courses higher (per @Cuevas2025_curriculum_efl); arts and social sciences likely lower |
| 5 | Bilingual region documents | Documents in Catalan / Basque / Galician / Valencian | Sensitivity to coder language competence; reported separately |

Sub-analyses are reported in the manuscript appendix; only sub-analyses 1–4 may appear in the main results section, and only if the cell sizes after stratification permit meaningful comparison (rule of thumb: ≥ 5 programmes per cell).

---

## 9. Validity threats and mitigation

Adapted from a causal-design template to a measurement-design frame.

| # | Validity dimension | Threat | Mitigation |
|---|---|---|---|
| 1 | **Construct validity** | Does the coding scheme capture the MRCDD construct of digital competence? | (a) Pilot with two independent coders to κ ≥ 0.70 per area; (b) coding manual reviewed by an external expert (Lázaro-Cantabrana cluster member, INTEF representative, or domain colleague); (c) MRCDD ↔ DigCompEdu mapping table for triangulation; (d) anchor and boundary examples per area documented in the manual. |
| 2 | **Sample selection bias** | Universities that publish *guías docentes* may correlate with higher TDC commitment, biasing coverage estimates upward. | (a) Report retrieval rate per university; (b) sensitivity analysis excluding low-availability institutions; (c) if Tier-A census is achieved, this threat is muted because non-publication is itself a coverage failure (a programme that does not publish *guías docentes* fails the perceived-curriculum dimension by construction). |
| 3 | **Document–practice gap** | The *guía docente* is what is *intended*; what is *taught* may differ. | Explicitly framed as out-of-scope in the methods; treated as a **scope limitation** in the discussion; positioned as motivation for a follow-up study with classroom observations or student interviews. |
| 4 | **Temporal validity** | Academic year 2024–2025 may not generalize. | (a) Snapshot framing; (b) discussion of regulatory stability (the MRCDD is locked-in; the *Grado en Maestro* curriculum has not been substantially revised since the LOMLOE secondary legislation); (c) suggest replication in 2027–2028 once any LOMLOE-driven revisions stabilize. |
| 5 | **Coder bias** | Coders' own TDC priors may affect coding (e.g., a coder who is a digital enthusiast may over-attribute presence). | (a) Blind double coding; (b) coder training to manual; (c) intercoder reliability monitoring; (d) record coder demographics/training in the methods. |
| 6 | **Layer collapse** | If *memorias* and *guías docentes* are largely identical at the digital-competence level, the two-layer design loses analytical leverage. | (a) Pilot 5 universities first (per discovery decision); (b) if the layer gap is consistently zero, pre-register a fallback framing as a one-layer comparative study with the layer-equivalence finding itself reported. |
| 7 | **Coding granularity drift** | Coders may converge on the manual's anchor examples and miss boundary cases. | Mid-coding calibration meeting (after ~25% of corpus); re-test on a small sample; recalibrate. |
| 8 | **Missing-by-design vs. missing-by-omission** | A *guía docente* without explicit MRCDD references could mean (a) the area is not part of the course OR (b) the document author chose not to mention it. | The coding instrument cannot distinguish (a) from (b) within the document. This is acknowledged as a measurement limitation; framed via the inference rule that codings are about **document content**, not **teacher intent**. |

---

## 10. Top 5 anticipated referee objections

Drawn from the domain profile's field-specific referee concerns and the frontier map's named risks. Each gets a one-paragraph pre-planned response.

### Objection 1 — "What's the contribution beyond Cuevas-Monzonís et al. (2024, 2025) and Sanz-Benito et al. (2024)?"

**Pre-planned response:** The differentiation is the **conjunction** of five qualifiers: post-MRCDD (rules out Peirats 2018 and Granados 2020), both degrees (rules out Cuevas-Monzonís cluster which restricts to Primaria), full competence space (rules out Sanz-Benito which restricts to digital inclusion), entire degree (rules out Cuevas-Monzonís restriction to EFL), two layers (no Spanish precedent codes both *memoria* and *guía docente*). Each qualifier alone is not novel; the conjunction is. The introduction states this explicitly with a differentiation table; the methods cite the precedents as methodological scaffolds (we adopt @Sandvik2023_norway_ecte_curriculum's Goodlad-mediated three-level frame and @Instefjord2017_norway_curriculum's curriculum-document analysis). The framing is "first post-MRCDD, two-degree, two-layer **stratified** analysis" — the design samples ~60 programmes from the universe of ~144 via stratified random sampling (Tier B; see §3), not a census. The conjunction-of-qualifiers contribution holds at this scope — none of the named precedents covers the full grid even within their narrower programme sets.

### Objection 2 — "Is the curricular analysis based on the *memoria*, the *guía docente*, or actual classroom practice?"

**Pre-planned response:** Both *memoria* (formal) and *guía docente* (perceived); classroom practice is explicitly out-of-scope. The Goodlad scaffold is invoked precisely to make this distinction. The two-layer design is not a substitute for classroom observation; it is the upstream measurement that classroom-observation work needs as a baseline. We frame this as the natural follow-up.

### Objection 3 — "How do you justify Cohen's κ ≥ 0.70 and how did you achieve it?"

**Pre-planned response:** The threshold follows @Krippendorff2018_content_analysis and Landis & Koch (1977) (substantial agreement). The pilot iterates the coding manual until κ ≥ 0.70 per area; the reliability sample (20% of the main corpus) re-tests after final coding. We report κ per area, weighted κ for depth per area, Krippendorff's α overall, the disagreement rate, and the number of arbitrated cases — full transparency on coder agreement, not just a single headline number.

### Objection 4 — "Why analyze only Spanish degrees? What about international comparison?"

**Pre-planned response:** The MRCDD is a Spain-specific instrument; analyzing Spanish curricula against it is the natural unit. International comparison is provided structurally via the **DigCompEdu mapping table** (appendix), so European readers can re-aggregate findings to the European framework. The Norwegian precedents (@Sandvik2023_norway_ecte_curriculum, @Instefjord2017_norway_curriculum) are the methodological comparators. Adding an Iberoamerican comparison is mentioned as a possible follow-up but not required for the present contribution.

### Objection 5 — "What about the digital divide / equity dimension?"

**Pre-planned response:** Equity and inclusion are partially internal to the framework: MRCDD Area 5 (*Empoderamiento del alumnado*) explicitly addresses inclusion. The sub-analysis by sector (public vs. private), modality, and autonomous community surfaces system-level inequities in curricular supply. We anchor the broader digital-divide framing in the post-COVID Spanish education evidence (@TrujilloSaez2020_panorama documents the magnitude of the divide that ITE is supposed to remediate) and in the inclusion-curricular-analysis line (@SanzBenito2024_inclusion_digital; @SanzBenito2023_inclusion_review). The present study's contribution is positioned as the supply-side measurement against which these divide claims can be triangulated. Equity is not the central frame, and we are explicit about that.

---

## 11. Falsification / sanity checks

Adapted to a measurement design — what should NOT show up if the coding instrument is well-constructed?

A full enumeration is in `falsification_tests.md`. The headline checks:

1. ***Memorias* dated before 2022** (if any are encountered as historical context) should NOT show explicit MRCDD area labels. If they do, the manual is over-flexible — the MRCDD post-dates them.
2. **Courses in clearly non-digital subjects with no instrumental-tech component** (e.g., a pure musicology *guía*, a Latin-language *guía*) should code as zero on most areas. A non-zero coding here triggers a manual re-check.
3. **Logical bound:** for each (university × degree), the *memoria*-coded coverage of any area should be **weakly bounded above** by the union of *guía docente* coverages across courses. If the *memoria* commits to an area that no course implements, that is a meaningful finding (commitment gap); if the union of courses covers an area the *memoria* does not commit to, that is also meaningful (emergent coverage). But both directions should be **substantively explainable** when they arise.
4. **Synonym test:** the manual should code "TIC", "tecnologías de la información y la comunicación", "digital", "tecnología educativa", and "competencia digital" as candidates for area presence — but only when paired with substantive content. Pilot includes a check that pure "TIC" mention without substantive content codes as level-1 (mentioned), not level-2 (developed).

---

## 12. Pre-registration recommendation

**Recommended platform:** **OSF** (Open Science Framework). Natural fit for descriptive / observational designs in education research; lower friction than AsPredicted or AEA registry; supports document deposit (the coding manual itself) alongside the registration.

**What to pre-register:**
- The research questions and descriptive estimands (sections 1 and 7 of this memo).
- The corpus snapshot (academic year 2024–2025, *memoria* version-in-force).
- The sampling decision (Tier A / B / C tiered fallback).
- The coding manual (frozen version, post-pilot, deposited as a project file).
- The intercoder reliability target (κ ≥ 0.70 per area, ≥ 0.80 overall).
- Pre-specified sub-analyses (section 8).
- Falsification checks (section 11 + `falsification_tests.md`).

**When to pre-register:** **after pilot completion and manual finalization**, **before** main coding begins. This timing is the OSF norm: register what you will analyze, freeze it, then analyze.

**What stays exploratory (not pre-registered):** any descriptive associations between coverage and institutional covariates beyond the four pre-specified sub-analyses; visualizations; supplementary appendices.

---

## 13. Implementation pseudo-code

A concise sketch is given here; the full pipeline is in `pseudo_code.md`.

```
INPUT:
  - RUCT inventory of Grado en Maestro programmes [/discover data output]
  - Corpus of memorias (PDF) [Layer 1]
  - Corpus of guías docentes (PDF / HTML) [Layer 2]
  - Coding manual (frozen, post-pilot)

STAGE 1 — Document ingestion and preprocessing
  for each document d in corpus:
    extract_text(d)              # PDF: pdftotext / pdfminer; HTML: BeautifulSoup
    normalize_unicode(d)
    segment(d)                   # paragraph-level for memorias; field-level for guías
    save to long-form corpus table

STAGE 2 — Coding (human; optional LLM-assisted pre-screening flagged as such)
  for each segment s in corpus:
    for each coder c in {1, 2}:
      assign(s, MRCDD_area, MRCDD_competence, depth in {0,1,2,3})
    log to codings table: (segment_id, coder_id, area, competence, depth, timestamp)

STAGE 3 — Reliability
  compute Cohen's kappa per area (binary presence)
  compute weighted Cohen's kappa per area (ordinal depth)
  compute Krippendorff's alpha overall
  resolve disagreements (consensus → arbitration); log resolutions

STAGE 4 — Aggregation
  for each (programme p, layer L, area a):
    presence(p, L, a) = max over segments/courses of presence
    depth(p, L, a)    = max over segments/courses of depth
  for each (degree D, layer L, area a):
    coverage(D, L, a) = mean over programmes of presence
    mean_depth(D, L, a) = mean over programmes of depth
    bootstrap 95% CI (1000 reps)

STAGE 5 — Comparative analyses
  layer_gap(p, D, a)  = categorical: memoria-only / guía-only / both / neither
  degree_gap          = paired comparison per area, within (university × area) pairs
  system_variation    = SD and IQR per (D, L, a) across programmes
  sub-analyses        = stratified by sector / modality / community / subject

STAGE 6 — Outputs
  coverage tables (per area; per competence in appendix)
  heatmaps (university × area, faceted by degree × layer)
  radar plots (degree × area, by layer)
  layer-gap cross-tabulations
  paired-comparison tables
  reliability table

STAGE 7 — Falsification / sanity
  run falsification_tests.md checks
  log results
```

**Tooling (recommended; not blocking):** R 4.4+ for analysis (`tidyverse`, `irr` for κ, `boot` for bootstrap, `ggplot2` + `fmsb` for radar, `pheatmap` for heatmaps). Coding can use a lightweight tagging interface (NVivo, Atlas.ti, or a custom long-form spreadsheet); the long-form CSV is the canonical output regardless of tool.

---

## 14. Required-before-coding checklist

Before the coder phase activates and main coding begins:

- [ ] **`/discover data` completed.** Corpus inventoried; retrieval rate quantified per layer; Tier A / B / C decision triggered. Currently `[ASSUMED]` — must be resolved.
- [ ] **Coding manual finalized.** Drafted, expert-reviewed, piloted, frozen. Separate artifact (not part of this memo). Required TOC in §5 above.
- [ ] **Pilot completed with κ ≥ 0.70 per area** on the 5-university × 2-degree × 2-layer pilot subset.
- [ ] **OSF pre-registration submitted** (recommended; not strictly required by the journal but strongly recommended by the strategist).
- [ ] **Coder team in place:** minimum 2 (preferred 3); training session completed; access to corpus and tagging interface configured.
- [ ] **Bilingual coder coverage confirmed** for any documents in Catalan / Basque / Galician / Valencian; or fallback to Castilian-language version pre-specified.
- [ ] **Tier B / C contingency activated only if Tier A pilot shows *guía docente* retrieval < 80%.**

---

## 15. What this strategy memo does NOT cover

For the orchestrator's awareness:

- **Coding manual content.** Specified as a separate artifact; TOC given here.
- **Ethics / data protection.** All documents are public-domain institutional documents; no human subjects. A brief ethics statement in the manuscript suffices; no IRB needed for document analysis of public curricular materials. (Coder demographic reporting, if collected, is the only datapoint requiring ethical handling.)
- **Statistical software environment.** Recommended R but not specified at the package level; the coder phase will lock this in.
- **Visualization design.** Specified at the level of "heatmaps, radar plots, coverage tables"; the writer phase will lock in concrete figure designs.
- **Manuscript structure.** Out-of-scope for the strategy memo; the writer phase will produce it.

---

## Citations used in this memo

@INTEF2022_mrcdd; @BOE2022_mrcdd; @Redecker2017_digcompedu; @Caena2019_aligning;
@Goodlad1979_curriculum_inquiry; @Sandvik2023_norway_ecte_curriculum; @Instefjord2017_norway_curriculum;
@HsiehShannon2005_qca; @Krippendorff2018_content_analysis; @LandisKoch1977_kappa;
@Lazaro2018_rubrica_latinoamerica; @TrujilloSaez2020_panorama;
@Cuevas2025_curriculum_efl; @Cuevas2024_tpack_primary; @SanzBenito2024_inclusion_digital;
@Peirats2018_planes_estudios; @Granados2020_profesorado_tic;
@SanzBenito2023_inclusion_review;
@BOE2007_RD1393; @BOE2007_ECI3854_infantil; @BOE2007_ECI3857_primaria; @LOMLOE2020.

---

## Score self-check (advisory; not a self-score)

This memo addresses every section of the descriptive / measurement template in the `/strategize` skill, plus the user-supplied 14-section structure. `[ASSUMED]` flags are placed wherever data feasibility is unverified. Companion artifacts (`pseudo_code.md`, `robustness_plan.md`, `falsification_tests.md`) are produced. The strategist-critic will score this independently.
