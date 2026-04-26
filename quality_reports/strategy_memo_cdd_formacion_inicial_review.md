# Strategy Review: strategy_memo_cdd_formacion_inicial.md
**Date:** 2026-04-26
**Reviewer:** strategist-critic
**Phase severity:** Strategy (constructive)
**Score:** 93/100 — PASS
**Verdict:** No CRITICAL issues. Two MAJOR fixes are quick patches; seven MINOR fixes can be batched. Strategy → Coder hand-off can proceed once M1 and M2 are resolved.

---

## TL;DR — Critical issues at top

**No CRITICAL issues found.** Two MAJOR issues warrant attention but do not block phase advancement:

1. **MAJOR (M1):** The MRCDD competence count (23 vs 22) contradicts the domain profile (line 43 of `domain-profile.md` says 22 competences; the memo asserts 23 throughout). Must be resolved with a direct citation to `BOE-A-2022-8042` before the coding manual is drafted.
2. **MAJOR (M2):** The reliability protocol contains an internal inconsistency between full double-coding and a 20% reliability sub-sample. Memo §6 says "Reliability sample = 20% of corpus" while pseudo-code Stage 2 says "for the remaining 80%, single-coding ... is acceptable." Both can be valid designs but they produce different κ and different statistical properties. The strategy must commit to one.

---

## Phase 1: Claim Identification — PASS (no deductions)

- **Paper type:** Descriptive / Measurement (curricular content analysis). Correctly self-classified.
- **Approach:** Two-layer (Goodlad formal vs. perceived), two-degree (Infantil vs. Primaria), MRCDD-anchored directed content analysis with depth scoring (0–3) and intercoder reliability (Cohen's κ + Krippendorff's α).
- **Descriptive estimands (target):** Per-area MRCDD coverage rate; per-area mean depth; per (programme × layer × area) layer-gap categorical; paired (Infantil vs Primaria) within-university coverage and depth differences; system-level variation across the Spanish university system.
- **Treatment / control / outcome:** N/A — correctly avoided. The memo explicitly disavows treatment/control language.

Verdict: Crisp. Research question is one well-formed sentence; sub-questions framed as descriptive estimands; multi-level units of analysis with named headline unit (programme × layer × area).

---

## Phase 2: Core Design Validity — PASS w/ 2 MAJOR + 2 MINOR

### Construct validity
- Concept clearly defined: TDC as MRCDD operationalizes it; distinguished from digital literacy.
- Measure maps to concept: YES with caveat — see M1.
- Measurement error discussed: YES — §9 threats #1, #5, #7, #8.
- Alternative operationalizations considered: YES — depth-scale (0–3) is explicitly defended against A1–C2. **Strongest single methodological argument in the memo.**

### Construction and replicability
- Data sources documented: YES.
- Construction steps explicit: PARTIAL — coding manual is correctly *deferred*, but a few TOC sections (anchor count, disambiguation flowchart, depth-rubric examples) are underspecified (m2).
- Sensitivity to construction choices: YES — `robustness_plan.md` covers 21 checks.

### Validation
- Internal validation: YES — `falsification_tests.md` Tests 1–6.
- External validation: PARTIAL — Test 7 (MRCDD↔DigCompEdu cross-coding) is *optional*; for top international submission should be required.
- Discriminant validity: YES — Test 5.

### Causal-language check (INV-8)
- §1, §7.6, §7.5: PASS — disciplined disavowal with explicit list of permitted/forbidden vocabulary.
- §7.5 reasoning ("a regression would invite causal interpretation") is exemplary.
- §8 sub-analysis 2: borderline — "given digital-native delivery" tilts toward causal. **MINOR (m1)** — rephrase.

### Issues

| # | Severity | Issue |
|---|---|---|
| M1 | MAJOR | MRCDD competence count (23 vs 22) contradicts domain profile. Must be resolved against BOE-A-2022-8042. |
| M2 | MAJOR | Reliability protocol — full double-coding vs 20% sample inconsistency between memo §6 and pseudo_code Stage 2. Three operational details unspecified (timing of 20% draw, single-coder assignment rule, mid-stream κ recalculation cadence). |
| m1 | MINOR | Causal whisper in §8 sub-analysis 2 ("given digital-native delivery"). Rephrase to "(digital-native delivery context)". |
| m2 | MINOR | Coding-manual TOC §§4, 6, 7 underspecified. Add target counts (2–3 anchors per area; ≥3 worked examples per depth level; flowchart with at least Area 1↔5, 2↔3, 4↔6 disambiguation). |

### Sanity check (mandatory)
- **Sign of expected estimates:** plausible. Coverage near 60–80% on Area 2; lower on Areas 4 and 6. PASS.
- **Magnitude sense:** ~140–170 programmes × 50–70 courses × 6 areas → O(50,000–70,000) Layer-2 codable cells. 20% reliability sample = ~10,000–14,000 segments. Tractable. PASS.
- **Pattern coherence:** layer gap should be larger on Areas 4 and 6 than Areas 2 and 3. Design has resolution to detect this. PASS.
- **Cross-spec consistency:** robustness plan probes the right alternatives. PASS.

---

## Phase 3: Inference Soundness — PASS w/ 2 MINOR

### Sampling-design inference
- Tiered fallback (A: census → B: stratified ~60 → C: purposive) with quantified triggers. PASS.
- Tier B power calculation: stated but formula not in deposit. **MINOR (m3).**

### Descriptive uncertainty
- Bootstrap 95% CI with 1000 reps, resampling at programme level (correct unit). PASS.
- Distributional reporting (§7.2): explicit attention to bimodal patterns. PASS.
- System variation (SD/IQR per cell) reported as a finding. PASS.

### Multiple comparisons
- §7.4 reports McNemar / paired Wilcoxon descriptively (not as causal hypothesis test) — correct register.
- Multiple-comparison framing not stated. **MINOR (m4)** — add one sentence pre-empting methods-referee question.

### Pre-registration of sub-analyses
- §8 lists 5 sub-analyses with pre-specified expectations tied to the literature.
- Cell-size rule (≥5 programmes per cell) prevents data-mining. PASS.

### Issues

| # | Severity | Issue |
|---|---|---|
| m3 | MINOR | Tier B power calculation formula not in deposit. Add to OSF deposit before pre-registration. |
| m4 | MINOR | Multiple-comparison framing not stated. Add sentence to §7.4 noting p-values are descriptive (no adjustment because not causal hypothesis tests). |

---

## Phase 4: Polish & Completeness — PASS w/ 3 MINOR

### Citation fidelity
All required references CITED: Hsieh & Shannon (2005), Krippendorff (2018), Goodlad (1979), Sandvik et al. (2023), Instefjord & Munthe (2017), Redecker & Punie (2017), Caena & Redecker (2019), Cuevas-Monzonís (2024, 2025), Sanz-Benito et al. (2024), Peirats et al. (2018), Granados et al. (2020).

Missing or weak:
- **m5:** Landis & Koch (1977) invoked but not in citations list.
- **m6:** Lázaro-Cantabrana, Gisbert & Silva-Quiroz (2018) — librarian-critic Tier 1 #1 — not yet integrated.

### Frontier-map risks (5/5 addressed)

| # | Risk | Addressed? |
|---|---|---|
| 1 | Scooping vs Cuevas-Monzonís cluster | YES — §10 Obj 1 (post-MRCDD + both degrees + full competence space + entire degree + two layers) |
| 2 | Scooping vs Sanz-Benito | YES — §10 Obj 1 |
| 3 | Coverage feasibility | YES — three-tier sampling §3 |
| 4 | Layer collapse | YES — §9 threat #6 with 5-uni pilot **and pre-registered fallback to one-layer framing** — exemplary |
| 5 | MRCDD vs DigCompEdu coding | YES — §5 commits to MRCDD primary; hybrid coding explicitly avoided |

### Domain-profile referee objections (5/5 addressed)
- Obj 5 (digital divide / equity) is slightly thin — leans on MRCDD Area 5 and stratification but doesn't cite a non-MRCDD equity anchor. **MINOR (m7).**

### `[ASSUMED]` flags
6 explicit `[ASSUMED]` flags, all genuine. Corpus-size estimate (~140–170 programmes) flagged in 3 independent places — orchestrator can route cleanly to `/discover data`.

### Issues

| # | Severity | Issue |
|---|---|---|
| m5 | MINOR | Landis & Koch (1977) not in citations list / `references.bib`. |
| m6 | MINOR | Lázaro-Cantabrana, Gisbert & Silva-Quiroz (2018) absent from methodological grounding. |
| m7 | MINOR | Equity anchor outside MRCDD Area 5 thin. Add Trujillo-Sáez et al. (2020) or OECD TALIS in §10 Obj 5. |

### Companion artifacts
- `pseudo_code.md` — 7 stages cleanly mapped to memo. INV-14 to INV-19 explicitly cited. **GOOD.**
- `robustness_plan.md` — 21 checks across 6 domains, distinguishes "robustness" from "exploratory." **EXCELLENT.**
- `falsification_tests.md` — 7 sanity checks. Test 1 (pre-2022 documents) and Test 4 (boilerplate "TIC" mention) particularly well-targeted. **EXCELLENT.**

---

## Score build

Starting score: 100

| Deduction | Severity | Phase | Points |
|---|---|---|---|
| M1 — MRCDD competence count discrepancy | MAJOR | 2 | −5 |
| M2 — Reliability protocol inconsistency | MAJOR | 2 | −5 |
| m1 — Causal whisper in §8 sub-analysis 2 | MINOR | 2 | −1 |
| m2 — Coding manual TOC underspecified | MINOR | 2 | −2 |
| m3 — Tier B power calculation formula not in deposit | MINOR | 3 | −2 |
| m4 — Multiple-comparison framing not stated | MINOR | 3 | −1 |
| m5 — Landis & Koch (1977) not in citations | MINOR | 4 | −1 |
| m6 — Lázaro-Cantabrana, Gisbert & Silva-Quiroz (2018) missing | MINOR | 4 | −1 |
| m7 — Equity anchor thin | MINOR | 4 | −1 |
| **Total deductions** | | | **−19** |

### Recovery credits

| Credit | Why | Points |
|---|---|---|
| Causal-language disavowal exemplary (§7.5–7.6) | INV-8 not just satisfied but defended | +3 |
| Pre-registered fallback for layer collapse (§9 #6) | Plans for own potential null finding | +2 |
| Depth-scale defense (0–3 vs A1–C2) sharp | Construct validity at right level | +2 |
| All 5 frontier-map risks explicitly addressed | Discovery → Strategy hand-off respected | +2 |
| `[ASSUMED]` flags routed correctly | Orchestrator can route cleanly | +1 |
| Distinguishes robustness from exploratory | Pre-specification discipline | +1 |
| Distributional reporting (§7.2) | Beyond formulaic mean ± SE | +1 |
| **Total credits** | | **+12** |

**Final score: 100 − 19 + 12 = 93/100 — PASS**

---

## Priority recommendations

1. **[MAJOR — M1]** Verify against `BOE-A-2022-8042` whether MRCDD has 22 or 23 sub-competences. Patch the strategy memo (4 occurrences) and `domain-profile.md` (1 occurrence) so they agree. **One citation lookup.**
2. **[MAJOR — M2]** Commit the reliability protocol to either (a) full double-coding or (b) 20% reliability sample + 80% single-coded with explicit single-coder assignment rule, mid-stream κ recalculation cadence, and timing of the 20% draw (pre / during / post).
3. **[MINOR cluster]** Patch m1–m7 in a single Round-2 pass: rephrase §8 causal whisper, expand TOC §§4/6/7 with target counts, add Tier-B power formula to OSF deposit, add multiple-comparison framing sentence to §7.4, add Landis & Koch (1977) to citations, slot Lázaro-Cantabrana et al. (2018) into methodological grounding, add Trujillo-Sáez et al. (2020) to §10 Obj 5.

---

## Positive findings

1. **Causal-language discipline is exemplary.** §7.6 names words to avoid AND words permitted. §7.5 reasoning ("a regression would invite causal interpretation") is the kind of thinking a methods referee will reward.
2. **The depth-scale defense is the strongest single methodological argument.** "Why 0–3 and not A1–C2" answers a real referee objection with a substantive distinction (curriculum depth ≠ teacher attainment).
3. **Pre-registered fallback for layer collapse.** §9 threat #6 plans for the null finding — unusually mature for a strategy memo.

---

## Verdict

**PASS — 93/100. No CRITICAL issues. Two MAJOR fixes (one factual, one operational) are quick patches; seven MINOR fixes can be batched. Strategy → Coder hand-off can proceed once M1 and M2 are resolved.**

No escalation triggered. Round 1 of the strategist-critic loop; revisions within addressable scope.
