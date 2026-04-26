# Decision Record — Discovery Phase: TDC in Initial Teacher Training

**Date:** 2026-04-26
**Phase:** Discovery (literature)
**Status:** Approved — librarian-critic PASS (84/100)

---

## Decision

Frame the project as a **comprehensive, post-MRCDD, two-degree, two-curricular-layer analysis** of how the Spanish *Grado en Maestro de Educación Infantil* and *Grado en Maestro de Educación Primaria* develop Teacher Digital Competence, mapped against the **MRCDD (Resolución 4 mayo 2022, BOE-A-2022-8042)** as primary coding grid and **DigCompEdu (Redecker & Punie, 2017)** as European benchmark. Adopt **Goodlad's curriculum-levels frame** (ideological / formal / perceived / operational) operationalized as BOE & LOMLOE → *memoria de verificación* → *guía docente*. Methodological precedents: **Instefjord & Munthe (2017, T&TE)** and **Sandvik, Smørdal & Østerud (2023, SJER)**.

## Alternatives considered (and why rejected)

| Alternative | What it would have looked like | Why rejected |
|---|---|---|
| **(a) Measure trainee TDC level** (descriptive cross-section) | Survey of self-perceived TDC across universities | Bucket B is saturated (12+ direct precedents); novelty bar in this lane is now very high. The user explicitly chose option (d) — curricular analysis — over options (a)–(c) in the discovery interview. |
| **(b) Evaluate a training intervention** (pre-post / quasi-experimental) | Run a TDC training module and measure effects | Single-site, small-N designs dominate the existing intervention literature (C1–C5); requires field access to a specific cohort that is not currently set up. Scope misfit with the user's chosen angle. |
| **(c) Compare across institutions / countries** | Comparative survey design | Useful framing addition but too broad as primary frame. Will be partially absorbed via the "all-Spain" dimension and the Norwegian methodological precedents. |
| **(d) Analyze how the curriculum forms TDC** (chosen) | Document analysis of *memoria* + *guía docente* layers | Selected by the user. The frontier map (§3) shows a defensible white space along five dimensions simultaneously: post-MRCDD timing, both degrees, full curricular scope (not a subject or competence subset), two layers, MRCDD/DigCompEdu coding. |

## Sub-decisions made within the chosen frame

- **Coding grid:** MRCDD primary, DigCompEdu benchmark — not a hybrid (the librarian-critic flagged hybrid coding as an intercoder-reliability risk).
- **Curricular layers:** *Memoria de verificación* (formal) + *guía docente* (perceived). The classroom-practice (operational) layer is out of scope; the BOE/LOMLOE (ideological) layer is treated as legal context, not coded data.
- **Population:** Spanish *Grado en Maestro* providers. Geographic scope (all-Spain vs. defensible subset) deferred to the strategist.
- **Search languages:** Bilingual ES + EN — non-negotiable given the field's structure (Spanish journals like *Comunicar*, *Educación XX1*, *Pixel-Bit* are central and absent from anglosaxon-only searches).
- **Reference framework citations required:** DigCompEdu (Redecker & Punie 2017), MRCDD (BOE-A-2022-8042 + INTEF 2022), TPACK (Mishra & Koehler 2006), Goodlad (1979).

## Key assumptions (must hold for the question to be answerable)

1. *Memorias de verificación* are accessible (publicly available via ANECA registry / RUCT / university websites) for a workable subset of Spanish universities.
2. *Guías docentes* are systematically published (most public universities do this; some private universities are less consistent).
3. The MRCDD's six areas and twenty-three competences can be operationalized as a coding scheme that two independent coders can apply with Cohen's κ ≥ 0.70.
4. The *memoria* and *guía docente* layers contain enough variation in language to make the gap between them meaningful (the librarian-critic flagged "layer collapse" as a risk to pilot before committing).

## What would invalidate the chosen frame

- If a comprehensive post-MRCDD curricular analysis turns out to already exist (a 2025–2026 *Educación XX1* / *Comunicar* article we missed). **Mitigation:** the librarian-critic flagged Tier 1 missing references; recheck the 2024–2026 Spanish journals before committing to the strategy memo.
- If *memorias* and *guías docentes* turn out to be largely identical at the digital-competence level. **Mitigation:** pilot 3–5 universities before final design (named in `frontier_map.md` §4).
- If the 2026 update of LOMLOE secondary legislation changes the *Grado en Maestro* requirements (and thus the whole curriculum corpus). **Mitigation:** snapshot the current academic year; treat any subsequent update as a follow-up study.

## Required follow-ups before strategy phase activates

Per `critic_report.md` §6:

- [ ] Resolve all `author = {{Various}}` placeholders in `references.bib` (B7, B8, B11, C4, F6, F7, F9, F10, F11) — hygiene fix; biber will not compile with these.
- [ ] Add **Hsieh & Shannon (2005)** and **Krippendorff (2018)** to the methods sub-bucket — required for designing the coding scheme.
- [ ] Verify B12 (Jaén / Sagrada Familia) or drop.

Recommended (non-blocking):

- [ ] Add Tier 1 missing references: Lázaro-Cantabrana, Gisbert & Silva-Quiroz (2018); Fernández-Cruz & Fernández-Díaz (2016); Cabero & Martínez-Gimeno (2019).
- [ ] Tighten the contribution statement in `positioning.md` §1.
- [ ] Reconcile A10 vs. D11 proximity scores.

## Score

- librarian-critic: **84/100 — PASS** (above commit threshold 80, below PR threshold 90).
- Phase: Discovery → Strategy can activate once required follow-ups are resolved.
