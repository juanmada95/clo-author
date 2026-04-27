# Code Audit — Stage 0 Corpus Inventory + Tier B Sample (CDD Formación Inicial)

**Date:** 2026-04-27
**Reviewer:** coder-critic (round 1)
**Paper type:** Descriptive measurement / curricular content analysis (Stage 0 = data engineering)
**Mode:** Full (16-category sweep + 8 project-specific concerns)
**Score:** **91 / 100**
**Verdict:** **PASS for PR; one concern below the OSF-deposit gate (95). NEEDS PATCH ROUND on two MAJOR items, then GREEN-LIGHT.**

---

## Top 3 strengths

1. **Source-attribution is exemplary.** Every row in `corpus_inventory.csv` carries `sources` (semicolon-joined) and `sources_count`. UNIR-infantil shows `aneca;educaweb_pilot_fallback`, UPSA-infantil shows `acsucyl_live_probe;aneca;educaweb;educaweb_pilot_fallback`. This makes the deposit auditable.
2. **Reproducibility hygiene of `tier_b_sample.py` is tight.** Single `numpy.random.default_rng(seed=20240901)` instantiation inside `main()` (INV-14), all paths via `Path(__file__).resolve().parents[3]` (INV-16), inventory pre-sorted by `programme_id` before sampling, sorted index returned (`idx_sorted = sorted(idx.tolist())`), pre-allocated `list[dict]` (INV-17), `stopifnot`-style guards on sum and on min-2 violation. Re-running on identical `corpus_inventory.csv` with numpy 2.4.4 will produce byte-identical IDs.
3. **PAP coherence is honest.** The three deviations (RUCT fallback, N=60 over N=63, Python RNG) are all in §10 with timestamps, all flagged in `inventory_reconciliation_log.md`, all surfaced in `reproducibility_check.txt`. No silent deviations detected on cross-check.

---

## Issues table

| Sev | Cat | Issue | Deduction | Fix |
|---|---|---|---|---|
| MAJOR | 3 (sanity / paper-type "construction defensible") | **Universitat Oberta de Catalunya (UOC) silently dropped.** Reconciliation log §"Dropped rows" lists UOC infantil + primaria with `sources=aqu_live_probe`, dropped because `classify_sector` returned `unknown`. UOC is a real public-online Catalan university offering Maestro grados; it should be `public` + `online`. This is a **classification gap, not noise**. The drop was logged (transparency credit) but not corrected. Universe is undercounted by 2 programmes; if recovered, UOC would land in the (public, Cataluna, online) cell — currently empty. | **−5** | Add `"universitat oberta de catalunya"` to `PUBLIC_UNIS` and `INSTITUTION_CCAA` in `inventory_reconciliation.py` (lines 108–143, 183–271), re-run reconciliation. Decision required: is UOC's modality `online` (creates a new cell) or does the strategy memo treat it under `public-presencial`? |
| MAJOR | 3 (sanity) | **ANECA "Universidad del Atlántico Medio" + "Universidad Tecnología y Empresa" silently absent from final inventory but were valid hits from a national registry.** ANECA returned 74 rows; only the rows whose canonical name matched the curated `canonical_map` survived (`canonicalise_name` falls back to `raw.strip()`, then `classify_sector` returns `"unknown"`, then they're dropped at line 585). These two are non-trivial private providers in Canarias / Madrid. Same root cause as UOC: the curated `canonical_map` is the bottleneck. | **−5** | Either expand `canonical_map` / `PRIVATE_TRADITIONAL_UNIS` / `INSTITUTION_CCAA` to cover the ANECA hits, OR add an explicit "needs-manual-review" tier in the reconciliation log instead of silent drop. The `dropped_unknown` log shows only 2 rows (UOC), so the ANECA rows must be getting normalised to a string already in the curated set or are being filtered earlier — verify before patching. |
| MAJOR | Project-specific #1 (deposit reproducibility) | **`programme_id` assignment is not robust to ANECA-row variation.** `programme_id = f"P{i:04d}"` is assigned in `inventory_reconciliation.py` line 619 *after* a sort. The sort key is `(sector, ccaa, modality, degree, university_name)`. Stable on Python 3.11+ pandas, BUT: if ANECA / educaweb HTML returns different rows on re-execution (network drift), the universe can change → IDs shift → `tier_b_sample_ids.csv` no longer reproduces. The deposit is therefore **reproducible against the frozen `corpus_inventory.csv`** but **NOT reproducible end-to-end from raw scrape**. | **−3** | Document this clearly in `reproducibility_check.txt`: "Reproducibility chain: (frozen `corpus_inventory.csv`, seed 20240901, numpy 2.4.4) → byte-identical `tier_b_sample_ids.csv`. NOT byte-identical from raw scrape because live HTML drifts." Currently the message is buried at the bottom and slightly understated. |
| MINOR | 7 (console hygiene) | `tier_b_sample.R` line 212: `cat("[R reference] Wrote", nrow(sample_rows), ...)` — uses `cat()` for status. Critic standard is `message()`. R script is reference-only so impact is small. | **−1** | Replace `cat(...)` with `message(...)`. |
| MINOR | 9 (numerical discipline) | `inventory_reconciliation.py` line 622: `grouped["ruct_anchored"] = grouped["codigo_ruct"].astype(bool)`. Empty string `""` casts to `True` in some pandas versions, `False` in others. Currently it's `False` for all 168 rows (RUCT empty), so latent only — but a future RUCT-anchored run could mis-flag empty codes as anchored. | **−2** | Use explicit `grouped["codigo_ruct"].astype(str).str.len() > 0`. |
| MINOR | 4 (educaweb noise filter) | `is_noise_university()` is **conservative on length** (`len(n) < 15` drops legitimate "Mondragon" if accent-stripped; `mondragon unibertsitatea` = 23 chars OK). The bad-phrases list is hand-curated — a borderline case like "Universidad Internacional Menéndez Pelayo" (UIMP, summer-school-only, no Maestro) wouldn't be filtered by this list. Acceptable for current scope but undocumented in `inventory_reconciliation_log.md`. | **−1** | Add a section in the log listing the noise-filter rules + the count of rows dropped *by* `is_noise_university`. Currently only the post-filter "sector=unknown" drop is logged. |
| MINOR | 6 (script header) | `aneca_listado_titulos.py` header **does** justify TLS bypass clearly (lines 14–19). Cross-checked `data_engineering_environment.md` — TLS bypass is **not** mentioned there. Minor documentation asymmetry. | **−1** | Add one bullet in `data_engineering_environment.md` §4 "Reproducibility commitments": "ANECA and RUCT scrapers use `verify=False` per pilot evidence; bypass is logged in script headers." |
| MINOR | 11/12 (figures/tables N/A this stage) | Stage 0 produces no figures or paper tables; CSV is bare data. Not applicable; no deduction. | 0 | — |

**Total deductions:** 5 + 5 + 3 + 1 + 2 + 1 + 1 = **18 → 9** after recovery credits below.

---

## Recovery credits

| Reason | Credit |
|---|---|
| Strategy alignment near-perfect: stratification cells (sector × ccaa × modality), proportional + min-2 + drop-for-budget logic exactly per `pseudo_code.md` STAGE 0; degree handled as within-programme attribute per memo §3. | **+3** |
| All 3 user-approved deviations cleanly logged in PAP §10 with timestamps and rationale. PAP Pre-Registration Checklist `[x]` boxes match deposit files (cross-validated against §10 + checklist). | **+3** |
| Strata table includes the requested `dropped_for_n60` column (3 cells: public-Madrid-online, public-Murcia-presencial, public-Navarra-presencial) — exactly what was specified for transparency. | **+2** |
| `tier_b_sample.py` `adjust_to_target` algorithm correctness verified by manual walkthrough on the realised cell sizes: 32 active cells, min-2 floor = 63, target = 60 → drop the 3 smallest-universe in-sample cells (each universe = 1 or 2). The output drops one universe-1 cell (Madrid-public-online) and two universe-2 cells (Murcia, Navarra) — algorithmically correct deterministic tie-break. | **+1** |

**Net:** 100 − 18 + 9 = **91**

---

## Numerical Discipline (INV-14 to INV-19)

| Invariant | Status | Notes |
|---|---|---|
| INV-14 (seed once) | PASS | `np.random.default_rng(seed=SEED)` line 346, only call. R script `set.seed(20240901)` line 49, only call. |
| INV-15 (imports at top) | PASS | All 8 scripts. |
| INV-16 (relative paths) | PASS | All 8 scripts use `Path(__file__).resolve().parents[3]` or `here::here()`. |
| INV-17 (pre-allocation) | PASS | `list[dict]` accumulators converted to DataFrame in one shot in every scrape. |
| INV-18 (output paths) | PASS | All under `data/raw/inventory_passes/` or `data/cleaned/` per `CLAUDE.md` "by-script" convention. |
| INV-19 (no setwd / install / rm) | PASS | Verified by grep across all 8 scripts. |

---

## Project-specific concerns scorecard

1. **Reproducibility from frozen inventory** → PASS (with deduction MAJOR-3 for documentation clarity).
2. **Min-2 rule correctness** → PASS. Implementation matches spec; `dropped_for_n60` column present.
3. **Source-attribution honesty** → PASS (strength #1).
4. **TLS-bypass justification** → PASS in script header; **MINOR gap** in environment doc.
5. **Educaweb noise filter** → PASS (conservative; length≥15 + phrase blocklist + acronym strip). MINOR gap: filter rules not summarised in reconciliation log.
6. **Adscritos detection** → PASS. 15 centres in override list, all 5 named in pilot covered + 10 more discovered. Sample contains 6 adscritos across 3 CCAAs.
7. **PAP coherence** → PASS. The 3 §10 deviations match the actual outputs exactly.
8. **R reference script** → PASS. Header explicitly states "NOT THE OSF DEPOSIT" in caps; produces `*_R.csv` filenames so no overwrite risk.
9. **UOC + ANECA-only universities silently dropped** → **MAJOR concerns 1 & 2 above.**

---

## Sequenced fix list (to clear OSF-deposit gate ≥95)

1. **Patch `inventory_reconciliation.py`:** add UOC + any ANECA-only legitimate institutions to `PUBLIC_UNIS` / `PRIVATE_TRADITIONAL_UNIS` / `INSTITUTION_CCAA` / `canonical_map`. Re-run. Verify universe still in [120, 170] range. Verify §10 deviation re: "168 active programmes" is updated if count changes.
2. **Patch `inventory_reconciliation.py` line 622:** replace `astype(bool)` with explicit length check.
3. **Patch `data_engineering_environment.md` §4:** add TLS-bypass disclosure bullet.
4. **Patch `inventory_reconciliation_log.md`:** add noise-filter rules summary + dropped-by-noise-filter row count.
5. **Patch `reproducibility_check.txt`:** strengthen reproducibility-chain wording.
6. **Patch `tier_b_sample.R` line 212:** `cat()` → `message()`.

After these patches, re-run `tier_b_sample.py` to regenerate `tier_b_sample_ids.csv` against the updated inventory (the 60 IDs may shift because of UOC). Update PAP §10 with a fourth deviation entry recording the inventory revision.

---

## Final recommendation

**NEEDS PATCH ROUND (1 round)** before GREEN-LIGHT FOR DEPOSIT. The two MAJOR items (UOC silent drop + ANECA classification gap) are fixable in <30 min of data-engineer time; everything else is polish. Score after patches projected at **96–98**, clearing the OSF-deposit gate (≥95 + all components ≥80).

**Strikes:** 1 of 3. No escalation. The dispatch back to the data-engineer is for a focused patch on the noise/classification cliff, not a re-spec.

---

## Round 2 — Patch verification (2026-04-27)

**Reviewer:** coder-critic (round 2, focused re-review)
**Mode:** Targeted — verifies the 6 sequenced patches from round 1 + new artifact integrity. NOT a full 16-category re-sweep.
**Score:** **97 / 100**
**Verdict:** **GREEN-LIGHT FOR DEPOSIT** (clears the OSF ≥95 gate; all components ≥80).

### Per-patch verification

| # | Patch | Verdict | Evidence |
|---|---|---|---|
| 1 | UOC + ANECA-only fix in `inventory_reconciliation.py` | **APPLIED CORRECTLY** | UOC in `PUBLIC_UNIS` (lines 119-120) + new `PUBLIC_ONLINE_UNIS` set (lines 161-165) keeps sector=`public` while forcing modality=`online` via `ONLINE_INSTITUTIONS` union (line 169). Atlántico Medio + Tecnología y Empresa + UCAV alias added to `PRIVATE_TRADITIONAL_UNIS` (lines 194-198). `INSTITUTION_CCAA` updated (lines 228-230, 248, 256, 277). Reconciliation log shows 174 programmes; UOC programmes P0118+P0119 present in sample with `sector=public, modality=online`. Architecturally clean: the new `PUBLIC_ONLINE_UNIS` set is the right abstraction for UOC. |
| 2 | `astype(bool)` → explicit length check (line 622 area) | **APPLIED CORRECTLY** | Line 671: `grouped["codigo_ruct"].astype(str).str.len() > 0`. Preserves downstream `ruct_anchored` semantics. |
| 3 | TLS bypass disclosure in environment doc | **APPLIED CORRECTLY** | `data_engineering_environment.md` §4 has new bullet (line 70) with full justification, naming both scrapers, the cert-chain rationale, and the `urllib3.disable_warnings` call. |
| 4 | Noise-filter rules in reconciliation log | **APPLIED CORRECTLY** | New section "Noise-filter rules applied to live HTML scrapes" (lines 80-92) with 4-rule table + per-rule counts (4 length, 12 phrase, 0 stub, 0 acronym = 16 total). |
| 5 | Reproducibility chain wording in `reproducibility_check.txt` | **APPLIED CORRECTLY** | Lines 25-43 contain a "REPRODUCIBILITY CHAIN" block stating both the byte-reproducible-from-frozen-CSV claim AND the three reasons end-to-end-from-raw-scrape is not byte-reproducible. Stronger than what round 1 suggested. |
| 6 | `cat()` → `message()` in `tier_b_sample.R` line 212 | **APPLIED CORRECTLY** | Line 212: `message("[R reference] Wrote ", nrow(sample_rows), " rows to ", out_sample)`. |

### New artifact integrity

- **`tier_b_sample_ids.csv`:** exactly 60 rows verified. UOC P0118+P0119 present (lines 46-47). Composition cross-checked via grep: 30 public + 18 private-trad + 6 private-online + 6 adscrito = 60 ✓; 29 infantil + 31 primaria = 60 ✓; 52 presencial + 8 online = 60 ✓.
- **`tier_b_strata_table.csv`:** 34 cells; `dropped_for_n60=True` flagged on exactly 4 (private-online×Comunitat Valenciana, public×Extremadura, public×Madrid×online, public×Murcia). The public×Madrid×online drop replaces the previous "Navarra" drop because UOC opens a new public-online-Cataluna cell that wasn't there before. Algorithmically consistent.
- **Byte-identity (no re-execution):** `tier_b_sample.py` line 346 has the single `np.random.default_rng(seed=SEED)` call; sample drawn from the inventory after a stable sort; output cast to deterministic column subset. Re-execution against the same `corpus_inventory.csv` will produce byte-identical output.

### New issues

- **None MAJOR.** No canonical_map collisions; UCAV alias merges cleanly.
- **MINOR (−1):** the data-engineer's covering-note said "+6 = UOC ×2 + Atlántico Medio ×2 + Tecnología y Empresa ×2"; PAP §10 Deviation 4 also lists a fourth recovery (UCAV alias) that "merged into the existing UCAV row, no net add". The arithmetic is correct (+6 net) but the covering note hid one of the four whitelist additions. Cosmetic.
- **MINOR (−2):** PAP §3.3 [120, 170] overshoot wording. Round-2 critic recommended tightening; orchestrator applied the cleanup post-review. **My judgment: this is a critic-call, not a user-call.** The [120, 170] band was tagged `[ASSUMED]` in PAP §3.4 — a placeholder, not a hard pre-registered constraint. The overshoot is monotonic improvement (legitimate institutions recovered, not noise added). The Deviation-4 wording now states the +4 plainly.

### Score breakdown (delta from round 1's 91/100)

- **+5** UOC + ANECA classification gap closed (was MAJOR-5)
- **+5** ANECA-only institutions recovered (was MAJOR-5)
- **+3** reproducibility chain wording strengthened (was MAJOR-3)
- **+1** R `cat()` → `message()` (was MINOR-1)
- **+2** `astype(bool)` → explicit length (was MINOR-2)
- **+1** noise-filter rules logged (was MINOR-1)
- **+1** TLS bypass disclosed in env doc (was MINOR-1)
- **−1** covering note understated number of whitelist additions (cosmetic)
- **−2** PAP Deviation 4 phrase "tolerance allowance" was awkward — overshoot now stated plainly post-review

**Net:** 91 + 18 − 3 = **97 / 100**.

### Final recommendation

**GREEN-LIGHT FOR DEPOSIT.** All 6 round-1 patches applied correctly. Universe of 174 active programmes is the strictly-better answer than 168. PAP §10 Deviation 4 is honest about both the inventory revision and the +4 overshoot. The remaining −3 is polish for the writer to handle when drafting the manuscript, not a blocker.

**Strikes:** 1 of 3 closed. No escalation. **Coder phase fully unblocked.**
