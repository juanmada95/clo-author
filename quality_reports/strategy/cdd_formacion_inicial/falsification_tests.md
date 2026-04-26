# Falsification / Sanity-check Tests — Curricular Analysis of TDC (MRCDD)

**Project:** Post-MRCDD, two-degree, two-layer curricular analysis.
**Companion to:** `quality_reports/strategy_memo_cdd_formacion_inicial.md`.
**Date:** 2026-04-26.

In a measurement design, "falsification" means testing whether the **coding instrument** behaves correctly on cases where the answer is known a priori. These are sanity checks for the manual and the coder team, not falsification tests for a causal hypothesis. They are pre-specified and run on the corpus as part of stage 7 of the analytical pipeline (see `pseudo_code.md`).

A failure on any falsification test triggers a manual revision and (if the test fails after revision) a re-pilot. Falsification results are reported in the methods section to demonstrate instrument behavior.

---

## Test 1 — Temporal sanity: pre-2022 documents should not invoke MRCDD-specific labels

**Logic.** The MRCDD entered force on 4 May 2022 (Resolución 4 mayo 2022, BOE-A-2022-8042; @BOE2022_mrcdd). Any document predating that date cannot reference the MRCDD's six-area structure or its specific area names.

**Procedure.**
- Identify any *memoria* or *guía docente* in the corpus dated before 2022-05-04.
- For each such document, check whether the codings include explicit MRCDD area labels (e.g., "Área 4: Evaluación y retroalimentación").
- Expected: zero such codings on pre-2022 documents.

**Pass criterion.** Zero false-positive MRCDD-label codings on pre-2022 documents.

**Failure response.** If false positives appear, the manual is over-flexible: it is conflating MRCDD-specific language with the generic INTEF *Marco Común* (2017) language, or with TPACK / DigCompEdu language. Revise the manual to require explicit MRCDD invocation or post-2022 publication date for the strictest area-label code; coders re-train.

**Note.** This test only applies if the corpus includes pre-2022 documents (e.g., older *memorias modificadas* still in force). If all coded documents are post-2022, this test is inapplicable; document that fact in the methods.

---

## Test 2 — Substantive sanity: clearly non-digital courses should code as zero on most areas

**Logic.** A *guía docente* for a course with no plausible digital component should code as 0 on most MRCDD areas. Coding any area with depth ≥ 2 on such a course flags an over-permissive coder or over-broad anchor.

**Procedure.**
- Identify a hand-curated set of "clearly non-digital" courses across the corpus. Examples:
  - A pure-content musicology course with no instrument-tech.
  - A Latin or classical-language course.
  - A pure-content philosophy-of-education course where the *guía* makes no mention of digital tools.
  - A history-of-education course covering the pre-digital era.
- The set must be hand-curated by the coding team using the *guía docente* descriptions; no a priori list is possible because course content varies by university.
- Expected: most areas code as 0; if any area codes as ≥ 1, it must be MRCDD Area 1 (*Compromiso profesional*) and only at depth 1 (mentioned), since transversal digital-citizenship language might appear even in non-digital courses.

**Pass criterion.** ≥ 80% of "clearly non-digital" courses code as 0 on Areas 2–6. Any depth-2 or depth-3 code on Areas 2–6 triggers a manual re-check.

**Failure response.** If many such courses code as ≥ 2 on Areas 2–6, the manual's anchors are too permissive — coders are reading transversal-competence language as area-specific commitment. Revise anchors and boundary cases.

**Note.** The set of "clearly non-digital" courses is itself documented in the methods so reviewers can replicate the test.

---

## Test 3 — Logical bound: memoria coverage should be substantively reconcilable with guía-union coverage

**Logic.** The *memoria* describes the formal commitments of the programme; the *guías docentes* describe how individual courses operationalize them. Two patterns are meaningful:
- **Commitment gap:** the *memoria* commits to area X but no *guía* implements it (formal-only coverage). This is a finding in itself.
- **Emergent coverage:** the *memoria* does not commit to area X but multiple *guías* implement it. This is also a finding.

**Procedure.**
- For each (programme, degree, area), compute:
  - `M(p, a)` = presence in *memoria* layer (0/1)
  - `G_union(p, a)` = `1` if ANY course in the programme codes presence on area `a`, else 0.
- Cross-tabulate `M(p, a)` vs. `G_union(p, a)` per area. The four cells map to the layer-gap categorical.
- Expected: most (programme, area) cells should fall in (1,1) or (0,0). The off-diagonal cells (1,0) and (0,1) are the gaps.

**Pass criterion.** This test does not have a pass/fail threshold — its purpose is to surface the pattern. The check is **substantive plausibility**: every off-diagonal observation should be re-examined by a coder to confirm the coding (rather than reflecting a coding error).

**Failure response.** If a (1,0) or (0,1) observation traces to a coding error (e.g., the *memoria* did invoke the area but the coder missed it), correct the coding and document the correction in the resolution log.

---

## Test 4 — Synonym handling: pure mention of "TIC" without substance must code as level 1, not level 2

**Logic.** The Spanish curriculum literature is awash in transversal "TIC" language — "competencia digital y TIC" appears as boilerplate in many *memorias* without any specific commitment. The depth scale (memo §5) requires depth 2 to be tied to specific learning outcomes, content, or activities. A pure boilerplate mention should code at depth 1 (mentioned).

**Procedure.**
- During the pilot, hand-construct a small set of "boilerplate-only" segments — ones that mention "TIC" or "competencia digital" but have no specific outcome, content, or activity attached.
- Code them through the manual; verify they code as depth 1.
- Run the same check on a random 20-segment sample drawn from the main corpus during the reliability sample.

**Pass criterion.** ≥ 90% of boilerplate-only segments code as depth 1 (not 2 or 3).

**Failure response.** Coders are conflating mention with development. Revise the depth rubric's worked examples; re-train.

---

## Test 5 — Inter-area discrimination: a segment cannot fully code into all six areas

**Logic.** A single short segment that codes into all six MRCDD areas with depth ≥ 2 is almost certainly a coding artifact (the coder is treating "digital competence" as an undifferentiated whole rather than disambiguating the areas).

**Procedure.**
- Count segments where ≥ 4 areas are coded with depth ≥ 2 by a single coder.
- Inspect these segments manually.
- Expected: these are rare, and when they occur, the segment is genuinely a multi-area summary statement (e.g., a *memoria* paragraph listing all the digital outcomes of the programme).

**Pass criterion.** Multi-area-deep codings on a single short segment are < 5% of all coded segments and survive manual inspection.

**Failure response.** If many segments are coded into all six areas, coders are not disambiguating. Revise the disambiguation flowchart in the manual.

---

## Test 6 — Reliability stability over time

**Logic.** Coder agreement should not drift downward as the coding proceeds (which would suggest fatigue or inconsistent application).

**Procedure.**
- Compute Cohen's κ on the first 25%, the middle 50%, and the last 25% of the coded segments (chronologically by coding session).
- Expected: κ stable across the three windows.

**Pass criterion.** κ in any window does not drop below 0.65 (relaxed threshold within a window) and does not drop by more than 0.10 across windows.

**Failure response.** Mid-coding calibration meeting; re-train; re-code the post-drop window.

---

## Test 7 — DigCompEdu re-aggregation consistency check

**Logic.** Because the MRCDD is operationally aligned with DigCompEdu, re-aggregating MRCDD codings to the DigCompEdu structure (via the appendix mapping table) should produce coverage estimates that are not wildly different from a hypothetical direct DigCompEdu coding.

**Procedure.**
- On the pilot subcorpus only, conduct a direct DigCompEdu coding by one coder (in addition to the MRCDD coding).
- Compare the re-aggregated MRCDD codings (mapped to DigCompEdu) against the direct DigCompEdu codings. Compute Cohen's κ.

**Pass criterion.** κ ≥ 0.70 between re-aggregated MRCDD and direct DigCompEdu on the pilot subcorpus.

**Failure response.** Either the mapping table is misaligned (revise it) or one of the two frameworks is being coded systematically differently from the other (revise the manual). Either way, the methods section must report the alignment.

**Note.** This test is **optional** but recommended: it adds substantial credibility for European reviewers who are more familiar with DigCompEdu than with MRCDD.

---

## Reporting

All falsification tests are reported in the manuscript:
- Tests 1–6 in the **methods section** (a "Coding-instrument validation" subsection).
- Test 7 in an **appendix** if conducted.
- Failures and the resulting manual revisions are documented in the OSF deposit's change log.

A test that **passes** is reported as a sentence: "The coding instrument passed test X; depth-2 codings on clearly non-digital courses did not exceed 10% of cases." A test that **fails and was remediated** is reported with the failure and the fix. A test that **fails and could not be remediated** is reported as a limitation and triggers escalation to the strategist (and, if needed, to the user) before main coding proceeds.
