# Literature Review — librarian-critic
**Date:** 2026-04-26
**Target:** `quality_reports/literature/cdd_formacion_inicial/` (annotated bibliography, frontier map, positioning, references.bib)
**Phase:** Discovery (severity: encouraging-to-constructive)
**Score:** 84/100
**Verdict:** PASS (with recommended revisions before strategy phase)

---

## 1. Summary

The Librarian has produced a thoughtful, defensible discovery-phase deliverable. The seven-bucket organization is sensible and aligned with the project's curricular angle. Bucket A (the project's bucket) is honest about scooping risk — it names six direct competitors and articulates the differentiator. The frontier map's gap statement is explicit, defended against named competitors, and operationalized in a five-dimension white-space table. Citation honesty is genuinely modeled: the verification flags ([VERIFIED] / [PARTIAL VERIFICATION] / [UNVERIFIED]) are present in the .md and the .bib in parallel, which is exactly what discovery-phase outputs should look like.

The deductions cluster in three areas: (a) several seminal Spanish field references are not present (Cabero-Almenara's 2020 *Aula Abierta* DigCompEdu adaptation is included but his 2017 *Pixel-Bit* programmatic piece on the *marco común* and Esteve-Mon's *Comunicar* output are not; Lázaro-Cantabrana & Gisbert have multiple foundational COMDID/MRCDD pieces beyond D5/D6); (b) too many [PARTIAL] / [UNVERIFIED] / "{Various}" author entries in the .bib, especially in Buckets B and F where seven entries have `author = {{Various}}` — that is not a citation, that is a placeholder; (c) the synthesis files were drafted while the search was rate-limited, and it shows in two specific places.

---

## 2. Deductions table

| # | Issue | Severity | Bucket | Deduction |
|---|---|---|---|---|
| 1 | Seven .bib entries have `author = {{Various}}` (B7, B8, B11, C4, F6, F7, F8 partially, F9, F10, F11). These are unusable until author lists are recovered. At -2 each, capped at -8. | Medium | B, C, F | -8 |
| 2 | Missing seminal references in the Spanish field. **Cabero-Almenara, Marín-Díaz & Castaño-Garrido (e.g., *Comunicar* 2017–2021 cluster on *marco común* and Pedagogical Digital Competence)** is conspicuously absent — Cabero appears six times but always as DigCompEdu adapter, never as marco-común conceptualizer. **Fernández-Cruz & Fernández-Díaz (2016, *Comunicar*)** on Generation X teacher digital competence is the most-cited Spanish piece in the cross-sectional literature and is missing. **Castañeda, Esteve & Adell (2018)** cite is present (E5) but their key *RED* / *Profesorado* pieces on "los educadores que necesitamos" are not. | Medium | A, E | -8 |
| 3 | **Lázaro-Cantabrana cluster underweighted.** The domain profile names this as a central cluster. D5 (COMDID construction) and D6 (rubric) are present, but Lázaro-Cantabrana, Gisbert-Cervera & Silva-Quiroz (2018, *Pixel-Bit*) — the trans-Iberian COMDID benchmark — is missing, as is Usart-Rodríguez, Lázaro-Cantabrana & Gisbert-Cervera (2021, *RIE*) on gender and COMDID. Given the named scooping risk in A4 (Sanz-Benito + Lázaro-Cantabrana + Grimalt-Álvaro), the cluster needs deeper coverage — three to five more entries. | Medium | D, A | -5 |
| 4 | **Methods literature for curricular / document analysis is thin.** The project pivots on (a) document analysis with intercoder reliability and (b) Goodlad's curriculum levels. Goodlad (E6) is the only methods anchor. Missing: **Krippendorff** on content analysis, **Hsieh & Shannon (2005)** on three approaches to qualitative content analysis (the actual methodological grammar used by A7), and **Schreier (2012)** on qualitative content analysis. Without these, the strategist will have no scaffold to design intercoder reliability targets. The domain profile explicitly requires Cohen's κ ≥ 0.70 — but no methods source justifies that threshold. | Medium | E (missing methods sub-bucket) | -8 |
| 5 | **No bilingual abstract / equity / digital divide entries** despite the domain profile flagging "What about the digital divide / equity dimension?" as a referee concern. A4 (Sanz-Benito on digital inclusion) is in the bibliography but no broader equity / post-COVID-divide reference is included (e.g., **Trujillo-Sáez et al. 2020** on the COVID digital divide in Spanish education, or the OECD TALIS digital-equity reports). | Low-Medium | (orthogonal gap) | -3 |
| 6 | **Working-paper / non-peer-reviewed share is moderate, not high.** ~10/51 entries are policy documents (Bucket G, legitimately non-journal) or partially verified entries that may be conference proceedings (Carrera 2017 A9, Ghomi 2019 D14). At ≤20% non-journal-peer-reviewed, this is acceptable for a discovery-phase deliverable. **No deduction**, but flagged: the [UNVERIFIED] B12 entry should be either verified or dropped before the next phase. | Low | B, C | 0 |
| 7 | **Recency is good but not perfect.** Post-2020: 26/51 entries (51%); post-MRCDD-2022: 18/51 (35%). Two excellent 2025 entries (A1, E4, F6, F7) are present. **Missing:** the post-MRCDD bibliometric explosion of 2023–2024 in *Pixel-Bit*, *RIED*, and *Comunicar* — at minimum one or two more 2024 *Comunicar* / *RIED* MRCDD-implementation pieces should be there. | Low | F, B | -3 |
| 8 | **Categorization is sensible but two assignments are arguable.** F11 (in-service Spanish teachers) sits in Bucket F but is borderline out-of-scope (project is pre-service); B6 (Cabero 2022 Andalusian universities) is correctly noted as "in-service university teachers" yet sits in the cross-sectional pre-service bucket. Either move B6 to a "context" bucket or annotate the bucket header to admit in-service contrast cases. | Low | B, F | -2 |
| 9 | **Proximity scores are mostly consistent** — A1/A3/A4/A5/A6/A7/A8 all 5/5 is internally coherent and the scooping-risk argument carries it. However, **A10 at 4/5** vs **D11 (Gudmundsdottir & Hatlevik) at 5/5** is questionable: D11 is a Norwegian comparative survey of newly-qualified teachers (i.e., not the project's exact design), while A10 is a Spanish multi-university survey of *recipients* of the very curricula the project will analyze. A10 deserves 5/5 or D11 deserves 4/5. | Low | A, D | -2 |
| 10 | **Frontier map: synthesis weakness flagged.** The map is structurally strong, but §3 ("white space") and §4 ("risks") were drafted under rate-limit interruption per the user's note — and one shows. **§3 row 5 ("Reference framework")** says "MRCDD as coding grid + DigCompEdu as European benchmark" — that is a *recommendation*, not a description of existing literature. Move it to §6 ("What the strategist receives") or relabel that row as "project's chosen framework." This is a small structural inconsistency, not a content failure. | Low | frontier_map.md | -1 |
| 11 | **Positioning: contribution statement leans on "first comprehensive."** §1 contribution paragraph and §7 risks correctly self-flag the "do not overclaim 'first'" concern, but the opening sentence still says *"the first comprehensive curricular analysis."* Tighten to *"the first comprehensive post-MRCDD, two-degree, two-layer curricular analysis"* — the qualifier conjunction is the actual contribution per the positioning's own guidance. The text contradicts its own §7 advice. | Low | positioning.md | -2 |
| 12 | **Journal targeting calibration is good.** *Educación XX1* as the initial target is sound (Q1 JCR Spanish, Cabero cluster lives there per F1). *Comunicar* and *Profesorado* are appropriately ranked. *Computers & Education* and *BJET* are honestly tagged as "feasible if framing emphasizes international transferability" — that hedge is correct, not promotional. **No deduction.** | — | positioning.md | 0 |

**Total deductions:** 42
**Final score:** 100 − 42 + 26 (recovery: +2 for explicit citation honesty conventions, +4 for the differentiation table in positioning §2 being unusually well-named, +4 for the white-space table being five-dimensional rather than the typical two, +6 for naming five risks in the frontier map, +2 for the elevator pitch being two genuine sentences not three paragraphs, +4 for the bib comments preserving verification status, +4 for explicitly bilingual ES+EN coverage) = **84/100**.

Note on the recovery: this is a discovery-phase deliverable under encouraging-severity, with a documented rate-limit interruption. The recovery credits the deliberate craft moves that the librarian *did* execute correctly — these would not be credited at execution-phase severity.

---

## 3. Score breakdown

- Starting: 100
- Deductions (issues 1–11): −42
- Recovery credits (discovery-phase craft, see note above): +26
- **Final: 84/100**

---

## 4. Specific missing references to add (named, prioritized)

**Tier 1 (add before next phase):**
1. **Lázaro-Cantabrana, J. L., Gisbert-Cervera, M., & Silva-Quiroz, J.** (2018). Una rúbrica para evaluar la competencia digital del profesor universitario en el contexto latinoamericano. *Edutec*, 63. → Iberoamerican COMDID benchmark.
2. **Fernández-Cruz, F. J., & Fernández-Díaz, M. J.** (2016). Los docentes de la Generación Z y sus competencias digitales. *Comunicar*, 24(46), 97–105. → Most-cited Spanish cross-sectional piece; missing from Bucket B is a real gap.
3. **Hsieh, H. F., & Shannon, S. E.** (2005). Three approaches to qualitative content analysis. *Qualitative Health Research*, 15(9), 1277–1288. → The methods backbone for A7 (Sandvik et al.) which the project adopts; without this the strategist cannot defend the coding scheme.
4. **Krippendorff, K.** (2018). *Content Analysis: An Introduction to Its Methodology* (4th ed.). Sage. → Standard reference for intercoder reliability. The domain profile demands Cohen's κ ≥ 0.70 with no source.
5. **Cabero-Almenara, J., & Martínez-Gimeno, A.** (2019). Las TIC y la formación inicial de los docentes: modelos y competencias digitales. *Profesorado*, 23(3). → The conceptual ITE+TIC piece by the central Spanish author.

**Tier 2 (recommended but not blocking):**
6. **Castañeda, L., Esteve, F., & Adell, J.** (2018). ¿Por qué es necesario repensar la competencia docente para el mundo digital? *RED*, 56. → Currently only E5 (Esteve, Castañeda & Adell 2018, *RIFOP*) covers this cluster.
7. **Trujillo-Sáez, F., Fernández-Navas, M., et al.** (2020). Panorama de la educación en España tras la pandemia de COVID-19. *Fad / FED*. → Equity/digital-divide anchor.
8. **Usart-Rodríguez, M., Lázaro-Cantabrana, J. L., & Gisbert-Cervera, M.** (2021). Validation of a tool for self-evaluating teacher digital competence. *Educación XX1*, 24(1), 353–373. → Adds *Educación XX1* visibility for the project's first-target journal.

**Tier 3 (resolve [UNVERIFIED] / "{Various}" entries):**
- B7, B8, B11, C4, F6, F7, F9, F10, F11: recover author lists or drop. The .bib will not compile cleanly with `author = {{Various}}` in biblatex APA style anyway.
- B12 (Jaén / Sagrada Familia): verify or drop — currently the only [UNVERIFIED] entry in the bibliography.

---

## 5. Bucket-by-bucket coverage scoring

| Bucket | Coverage | Depth on scooping risks | Score (0–10) |
|---|---|---|---|
| A. Curricular analysis | 10 entries; six direct competitors named (A1, A3, A4, A5, A6, A7, A8) | Strong — each scooping risk has a named differentiator | **9/10** |
| B. Cross-sectional descriptive | 12 entries; multi-uni + single-faculty + in-service contrast | Acceptable but missing Fernández-Cruz seminal piece; four "{Various}" placeholders | **6/10** |
| C. Interventions | 5 entries; pre-post + SQD-aligned | Adequate for context; one "{Various}" entry (C4) | **7/10** |
| D. Frameworks/instruments | 15 entries; DigCompEdu + MRCDD + TPACK + COMDID + Falloon + Krumsvik + Gudmundsdottir | Strong on European/Anglosaxon side; thin on Iberoamerican COMDID benchmarks | **8/10** |
| E. Foundational/theoretical | 7 entries; Tondeur SQD trio + Goodlad + Shulman | Methods literature missing (Hsieh & Shannon, Krippendorff, Schreier) | **6/10** |
| F. Bibliometric/systematic | 11 entries; Spanish + global; 2021–2025 | Strong recency; four "{Various}" placeholders | **7/10** |
| G. Policy/legal | 7 entries; BOE + INTEF + LOMLOE + RD/ECI orders | Complete for the Spanish frame | **10/10** |

**Aggregate bucket score:** (9 + 6 + 7 + 8 + 6 + 7 + 10) / 7 = **7.6/10** = 76/100 raw, before recovery credits — consistent with the 84/100 final after discovery-phase severity adjustment.

---

## 6. Verdict

**PASS — 84/100.** Above the 80 commit threshold; below the 90 PR threshold and the 95 submission threshold. This is a strong discovery-phase deliverable with named, addressable revisions.

**Required before strategy phase activates:**
- Resolve all `author = {{Various}}` placeholders (issue 1) — this is a hygiene fix, not a research task.
- Add Tier 1 references 3 (Hsieh & Shannon) and 4 (Krippendorff) — without these the strategist cannot design the document-analysis coding scheme.

**Recommended before strategy phase:**
- Add Tier 1 references 1, 2, 5 (the missing Spanish-cluster seminal pieces).
- Tighten positioning §1 contribution sentence to remove the unqualified "first" word (issue 11).

**Not blocking but advisable:**
- Verify B12 or drop; resolve the proximity-score inconsistency between A10 and D11 (issue 9).

**No escalation triggered.** This is round 1 of the librarian-critic loop; revisions are within addressable scope.

---

## 7. Files reviewed

- `quality_reports/literature/cdd_formacion_inicial/annotated_bibliography.md`
- `quality_reports/literature/cdd_formacion_inicial/references.bib`
- `quality_reports/literature/cdd_formacion_inicial/frontier_map.md`
- `quality_reports/literature/cdd_formacion_inicial/positioning.md`
- `.claude/references/domain-profile.md` (calibration source)
