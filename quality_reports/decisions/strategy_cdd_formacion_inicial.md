# Decision Record — Strategy Phase: TDC Curricular Analysis

**Date:** 2026-04-26
**Phase:** Strategy (design memo)
**Status:** Approved — strategist-critic PASS (93/100). Round 2 patch pending for 2 MAJOR + 7 MINOR issues before coder phase activates.

---

## Decision

Adopt a **descriptive / measurement** design — content analysis of curricular documents — with the following locked-in choices:

- **Coding grid:** MRCDD primary (6 areas × N sub-competences — **N pending verification of M1**), DigCompEdu as secondary benchmark via mapping table.
- **Coding approach:** Directed content analysis (Hsieh & Shannon, 2005). Codes supplied a priori from the framework.
- **Depth scale:** **0–3** (absent / mentioned / developed / assessed) — explicitly chosen over MRCDD's A1–C2 because the latter describes *teacher attainment*, not *curriculum depth* (mapping table appended).
- **Layers (Goodlad framework):** Layer 1 = *memoria de verificación* (formal); Layer 2 = *guía docente* (perceived). Operational layer (classroom practice) explicitly out of scope; ideological layer (BOE/LOMLOE) treated as legal context, not coded data.
- **Sampling — three-tier fallback:**
  - Tier A: all-Spain census (~140–170 programmes) — primary plan.
  - Tier B: stratified sample of ~60 programmes (sector × autonomous community × modality) — fallback if Tier A document retrieval rate < 80%.
  - Tier C: purposive sample of largest providers — fallback if Tier B also fails.
- **Snapshot:** academic year 2024–2025 (most recent fully completed year).
- **Intercoder reliability target:** Cohen's κ ≥ 0.70 per area, ≥ 0.80 overall (Krippendorff 2018; Landis & Koch 1977).
- **Pilot:** 5 universities × 2 degrees × 2 layers = 20 cells; 2–3 iterations of the coding manual to reach κ targets.
- **Pre-registration:** OSF deposit before pilot finalization of the coding manual.

## Alternatives considered (and why rejected)

| Alternative | What it would have looked like | Why rejected |
|---|---|---|
| **MRCDD A1–C2 depth scale** | Code each competence at A1–C2 progression level | A1–C2 measures teacher attainment, not curriculum depth. Risk of coder confusion (assessing the document as if it were a teacher). 0–3 scale chosen instead, with mapping table for European audience. |
| **Hybrid MRCDD/DigCompEdu coding** | Code simultaneously to both grids | Librarian-critic flagged hybrid coding as intercoder-reliability risk. Adopted MRCDD primary + DigCompEdu mapping table instead. |
| **All-Spain census without fallback** | Commit to 100% population coverage | Document-accessibility variation across universities makes 100% unrealistic. Three-tier fallback locked in instead. |
| **Single-layer (memoria only)** | Skip *guías docentes* | Loses the formal-vs-perceived gap (the project's main analytical leverage). Only adopted as fallback if layer collapse turns out to be empirically real (§9 threat #6). |
| **Sentence-level coding unit** | Code at sentence rather than paragraph | Pilot will determine the right unit (memo §5). Sentence is more granular but increases coding burden ~5x. |

## Sub-decisions made within the chosen frame

- **Aggregation rule for Layer 2 (guía docente):** `max` over courses per (degree × competence). A competence developed in *any* course counts as part of the perceived curriculum. `mean` and `sum` are robustness checks (`robustness_plan.md` B3, B4).
- **Course inclusion criteria (primary):** all *básicas* + *obligatorias*. *Optativas* included only if degree-specific justification (per-programme rule). *Prácticum* and *TFG* with separate coding rules.
- **Sub-analyses pre-specified (5):** public vs private; geographic (autonomous community); traditional vs online providers (UNIR, VIU, UCJC); subject-area (language/STEM/social/Prácticum/TFG); cohort/year stratification if available.
- **Multiple-comparison policy:** no formal correction. Justification: p-values reported descriptively to characterize paired-difference magnitude relative to chance variation, NOT as tests of causal hypotheses.
- **Equity / digital-divide framing:** addressed primarily via MRCDD Area 5 + stratification sub-analyses. Anchor citation outside MRCDD pending (m7).

## Key assumptions (must hold for the design to deliver)

1. *Memorias* and *guías docentes* are accessible at scale for a workable subset of Spanish universities (`[ASSUMED]` — pending `/discover data`).
2. The MRCDD's six areas can be operationalized as a coding scheme with two coders reaching κ ≥ 0.70 per area.
3. *Memoria* and *guía docente* layers contain enough variation in language to make the gap between them meaningful (layer-collapse risk; piloted at 5 universities; pre-registered fallback if it fails).
4. Document-vs-practice gap (the *guía docente* states intentions; teaching practice may differ) is acceptable as a limitation framed as scope.

## What would invalidate the strategy

- If the corpus turns out to be < 30 programmes accessible at any tier — design becomes infeasible.
- If pilot fails to reach κ ≥ 0.70 per area after 3 manual iterations — coding scheme needs structural revision.
- If layer collapse is empirically confirmed (memoria and guía docente identical at competence level) — fall back to one-layer framing per §9 threat #6.
- If a comprehensive post-MRCDD curricular analysis is published in 2026 before this study completes — re-evaluate scope and contribution.

## Required follow-ups before coder phase activates

Per `strategy_memo_cdd_formacion_inicial_review.md`:

**MAJOR (must resolve):**
- [x] **M1 — RESOLVED 2026-04-26.** Verified against `BOE-A-2022-8042` (PDF p. 7): "se ha creado una nueva competencia en el Área 1, Compromiso profesional ... con lo que el Marco de Referencia de la Competencia Digital Docente que aquí se presenta tiene 23 competencias en lugar de 22." MRCDD has **23 competences**. Strategy memo retained (was correct). `domain-profile.md` patched (was wrong; said 22).
- [x] **M2 — RESOLVED 2026-04-26 (user decision).** Variant **B** committed: 20% double-coded + 80% single-coded with three locked-in operational details:
   - **B1 (timing):** 20% reliability sample drawn a priori before main coding begins, stratified random across (degree × layer), deposited as part of the OSF pre-registration package.
   - **B2 (single-coder assignment):** Two trained coders share the 80% via balanced rotation across (degree × layer) strata (~50/50). Uncertainty flags ("boundary case" or "ambiguous") trigger automatic escalation to the second coder; per-coder uncertainty-flag rate is tracked and reported.
   - **B3 (mid-stream κ recalculation):** κ recalculated at 25%, 50%, 75% completion milestones on the cumulative double-coded set. If κ in any area falls below 0.70 at any milestone, all coding halts, the manual is reviewed, affected segments recoded, and a deviation logged for the OSF deposit.
   Variant A (full double-coding) was rejected on budget grounds (≈ 50,000–70,000 codable segments at Layer 2 makes 2× coder cost prohibitive). Variant B is the field standard per Krippendorff (2018).

**MINOR (recommended single-pass batch fix):**
- [ ] m1. Rephrase §8 sub-analysis 2 ("given digital-native delivery" → "(digital-native delivery context)").
- [ ] m2. Expand coding-manual TOC §§4, 6, 7 with target counts.
- [ ] m3. Add Tier-B power calculation formula to OSF deposit.
- [ ] m4. Add multiple-comparison framing sentence to §7.4.
- [ ] m5. Add Landis & Koch (1977) to citations list and `references.bib`.
- [ ] m6. Add Lázaro-Cantabrana, Gisbert & Silva-Quiroz (2018) to methodological grounding.
- [ ] m7. Add Trujillo-Sáez et al. (2020) or OECD TALIS to §10 Obj 5.

**External dependency:**
- [x] **`/discover data` — RESOLVED 2026-04-26.** Explorer pilot of N=10 institutions across 5 strata produced Layer 1 retrieval 6/10 (60% conservative / 85–90% likely) and Layer 2 retrieval 5/10 (50% conservative / 75–80% likely). Wilson 95% CI on the Layer 2 rate is [24%, 76%], statistically insufficient to support the Tier A trigger of ≥80%. **User decision (2026-04-26): adopt Tier B as primary** — stratified random sample of ~60 programmes drawn from the universe of ~144, stratified on sector (4 levels including *centros adscritos*) × CCAA × modality. Three explorer revisions applied to memo: (1) "online providers gated" downgraded to provider-specific (VIU public, UNIR gated, UCJC unconfirmed); (2) memoria source priority list expanded to include 8 autonomous-community evaluation agencies (AQU, ACSUG, UNIBASQ, AAC-DEVA, ACSUCYL, AQUIB, AVAP, Madri+d); (3) *centros adscritos* (~15 institutions) promoted to a separate sector level in the stratification, with the caveat that adscrito × CCAA sub-analysis is infeasible at Tier B (cells of 0–1 programmes). Positioning.md §1 and §7 updated to reflect "first post-MRCDD, two-degree, two-layer stratified analysis" framing instead of "first comprehensive census" framing — conjunction-of-qualifiers contribution argument holds at Tier B scope. Tier C (purposive) remains as final fallback if Tier B retrieval falls below 50% in the data-engineer's main pull.

## Score

- strategist-critic: **93/100 — PASS** (above PR threshold 90; below submission threshold 95).
- Phase: Strategy → Coder activation deferred until M1, M2, and `/discover data` resolved.
