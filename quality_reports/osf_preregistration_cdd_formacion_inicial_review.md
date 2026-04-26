# Strategy Review: osf_preregistration_cdd_formacion_inicial.md
**Date:** 2026-04-26
**Reviewer:** strategist-critic (LIGHT fidelity check)
**Scope:** Re-organization fidelity to locked-in design (memo + decision record) + OSF deposit-readiness. Not a re-litigation of design.
**Score:** 80/100 — **ALMOST READY** (1–2 small patches)
**Verdict:** One CRITICAL fix (cite-key typo) → READY TO DEPOSIT pending the 9-item user checklist.

---

## Phase 1: What's the Claim?

- **Paper type:** Descriptive / Measurement (curricular content analysis).
- **Approach:** Stratified two-degree, two-layer content analysis of MRCDD coverage and depth in Spanish initial teacher training (2024–2025).
- **Document under review:** OSF pre-registration draft (321 lines, 11 sections + Pre-Registration Checklist).

---

## Phase 2: Fidelity to Locked-in Design

**Verdict: HIGH FIDELITY.** Every locked-in element is reproduced without drift.

| Locked-in element | Memo / Decision Record | PAP location | Match |
|---|---|---|---|
| MRCDD = 23 competences (M1) | Decision record M1; memo §5 | §1.3, §5.1 with BOE citation verbatim | EXACT |
| Variant B reliability (M2) | Decision record M2; memo §6 | §6 with B1, B2, B3 reproduced | EXACT |
| Tier B sampling (~60 programmes) | Memo §3 | §3.4, §3.6, §2.4 | EXACT |
| 4-level sector × 18 CCAA × 2 modality | Memo §3 | §3.3 step 2 | EXACT |
| Adscrito × CCAA infeasible | Memo §3, §8 sub-analysis 3 | §7.2 sub-analysis 3 | EXACT |
| Depth scale 0–3 (defended vs. A1–C2) | Decision record; memo §5 | §4.2, §5.4 | EXACT |
| Goodlad two-layer frame | Memo §4 | §2.3, §1.3 | EXACT |
| Causal-language disavowal | Memo §7.6 | §7.4 with permitted/prohibited language | EXACT |
| H1, H2, H3 as expected patterns (not causal) | (New formalization, consistent with memo §1) | §1.4 with explicit disclaimer | EXACT |
| 7 falsification + 21 robustness pre-registered by reference | Memo §11; companion artifacts | §7.5, §8 | EXACT |
| Power calculation reproduced | Memo §3 | §3.5 | EXACT |

**No drift from the locked-in design.** All three M1, M2, and Tier B locked-in choices are reproduced without alteration.

---

## Phase 3: OSF Deposit Format Compliance

All 11 sections present and operational. Format is fully OSF-compliant. The two extension sections (Coding Scheme §5, Reliability Protocol §6) are appropriate for a content-analysis pre-registration and follow the Krippendorff (2018) convention.

---

## Phase 4: Issues Found

### Issue 4.1 — CRITICAL: Citation key mismatch (`@Cabero2023_competencia_digital_review`)

- **Location:** §1.4 (in H1 anchor); §11 citations.
- **Severity:** CRITICAL (-10).
- **Problem:** Cited key `@Cabero2023_competencia_digital_review` does not resolve in `references.bib`. Actual key is `@Cabero2023_evaluacion_review` (title: "Evaluación de la competencia digital docente: Instrumentos, resultados y propuestas. Revisión sistemática de la literatura"). On compile, biber will print `[Cabero2023_competencia_digital_review?]` in the rendered OSF deposit.
- **Why CRITICAL:** Affects H1 — the headline pre-registered hypothesis — and the missing anchor will be visible in the public OSF deposit. **Fix is one-line: replace at both occurrences.**

### Issue 4.2 — MINOR: `[ASSUMED]` checklist count drift (9 vs. 10)

- **Location:** Pre-Registration Checklist.
- **Severity:** MINOR (-2).
- **Problem:** User's brief stated "9 `[ASSUMED]` items"; checklist contains 10. Extra item is the **Power sensitivity table** — genuinely a deposit artifact rather than an `[ASSUMED]` strategic placeholder. Re-label or restructure the checklist to distinguish "[ASSUMED] strategic placeholders" (5–6 items) from "deposit artifacts to generate" (3–4 items).

### Issue 4.3 — MINOR: Hidden `[ASSUMED]` not surfaced in checklist

- **Location:** §1.3 (mention of "~144 RUCT-listed programmes").
- **Severity:** MINOR (-2).
- **Problem:** The §1.3 mention does NOT carry an `[ASSUMED]` flag, even though the same number elsewhere does. Cosmetic.

### Issue 4.4 — MINOR: Memo m1, m4, m5, m6, m7 disposition not annotated in PAP

- **Location:** Inferable across §3.5 (m3 RESOLVED) and §7.3 (m4 RESOLVED).
- **Severity:** MINOR (-2).
- **Problem:** Spot-check of the PAP's citations confirms m5 (Landis & Koch), m6 (Lázaro-Cantabrana), m7 (Trujillo-Sáez) are all cited; m2 (TOC expansion) lives in the memo §5 referenced by pointer. **Net: substantively reflected.** Documentation-trail concern only.

### Issue 4.5 — MINOR: Companion artifacts not yet produced

- **Location:** §1; checklist items 7, 8, 9.
- **Severity:** MINOR (-2).
- **Problem:** PAP correctly notes that `coding_manual_v1.0.pdf`, `reliability_subsample_ids.csv`, `tier_b_sample_ids.csv`, `power_sensitivity_table.csv` are "to be deposited." Per OSF norms (and per memo §12), pre-registration is finalized AFTER pilot completion and manual finalization. **Acceptable** as documented.

### Issue 4.6 — MINOR: Decision record reference path inside the PAP

- **Location:** §6.
- **Severity:** MINOR (-2).
- **Problem:** Cross-references internal repo path that won't resolve from a public OSF deposit. **Cosmetic** — the lock-in date and rationale are already inlined.

---

## Summary

- **Score:** 100 − 10 − 2 − 2 − 2 − 2 − 2 = **80/100**
- **Verdict:** **80–89 ALMOST READY.**
- **Critical issues (must fix before deposit):** 1 — citation key fix.
- **Major issues:** 0.
- **Minor issues:** 5 — all cosmetic / documentation-trail.

The single CRITICAL issue is a one-character fix but it is in the headline H1 anchor and in the deposited bibliography, so it must be patched before OSF lock. Once patched, this PAP is **READY TO DEPOSIT** pending the user checklist.

## Priority Recommendations

1. **[CRITICAL]** Replace `@Cabero2023_competencia_digital_review` with `@Cabero2023_evaluacion_review` at both occurrences. (1-minute fix.)
2. **[MINOR]** Re-label or restructure the Pre-Registration Checklist to distinguish "[ASSUMED] strategic placeholders" from "deposit artifacts to generate."
3. **[MINOR]** Add a one-line disposition note for memo MINOR follow-ups m1–m7.

## Positive Findings

1. **Zero design drift.** Every locked-in element from memo and decision record reproduced without alteration. **Highest-fidelity translation possible.**
2. **Hypotheses correctly framed as expected patterns.** §1.4 explicitly disclaims causal interpretation. Reviewers cannot mistake this for a causal-test pre-registration.
3. **PAP correctly self-positions as commitment device, not encyclopedia.** §7.5 wisely pre-registers all 21 robustness checks by reference. The "failing to run any pre-registered check is itself a reportable deviation" sentence is a strong commitment.
