# Session Report — CDD en la Formación Inicial del Profesorado

## 2026-04-26 — Discovery phase: project setup + literature review

**Operations:**
- Rewrote `.claude/references/domain-profile.md` for Teacher Education / Educational Technology field (replaces economics default). Calibrated to DigCompEdu + MRCDD; lists Spanish + international target journals; names central Spanish authors and seminal references.
- Updated `CLAUDE.md`: project name, field, frameworks, working language, current project state.
- Dispatched `librarian` agent (10-min run, 48 tool calls; rate-limited before final two synthesis files).
- Wrote `frontier_map.md` and `positioning.md` from the librarian's bibliography to complete the deliverable without re-running web searches.
- Dispatched `librarian-critic`: scored 84/100 PASS with named follow-ups.
- Saved decision record at `quality_reports/decisions/discovery_cdd_formacion_inicial.md`.
- Initialized `quality_reports/research_journal.md` and this `SESSION_REPORT.md`.

**Decisions:**
- Project scope confirmed as **post-MRCDD, two-degree, two-layer (memoria + guía docente) curricular analysis** of TDC formation.
- Coding grid: **MRCDD primary, DigCompEdu benchmark** — not hybrid.
- Methodological precedents: Instefjord & Munthe (2017) and Sandvik et al. (2023) — Goodlad three-level frame.
- Search languages: ES + EN bilingual; rejected EN-only as it would miss central journals (Comunicar, Educación XX1, Pixel-Bit, RIED, etc.).

**Results:**
- 51-entry annotated bibliography across 7 buckets; 23 entries at proximity 5 (direct competitors / required cites).
- Six direct scooping risks identified in Bucket A (Cuevas-Monzonís et al. 2024, 2025; Sanz-Benito et al. 2024; Peirats et al. 2018; Granados et al. 2020) — each has a named differentiator.
- Initial target journal: *Educación XX1* (Q1 JCR Spanish; Cabero cluster home).
- 5-dimension white-space frame defined for the strategist (geography × degrees × scope × layer × framework × timing).

**Commits:**
- (none yet — staged for user review)

**Status:**
- Done: Discovery (literature) — librarian + librarian-critic + librarian round 2 + positioning fix all completed (84/100 PASS, all blockers resolved).
- Done: Strategy (design memo) — strategist + strategist-critic completed (93/100 PASS).
  - Memo: `quality_reports/strategy_memo_cdd_formacion_inicial.md`.
  - Companion: `pseudo_code.md`, `robustness_plan.md`, `falsification_tests.md`.
  - Decision record: `quality_reports/decisions/strategy_cdd_formacion_inicial.md`.
- Done: Strategy patch round — M1, M2, and all 7 MINOR fixes resolved.
  - **M1 resolved:** BOE-A-2022-8042 (PDF p. 7) confirms MRCDD has **23 competences** (strategist correct; domain profile patched).
  - **M2 resolved (user decision):** Variant **B** locked-in (20% double + 80% single). Three operational defaults: B1 a-priori stratified sample deposited to OSF; B2 balanced coder rotation within strata, automatic escalation on uncertainty flags; B3 milestone κ recalc at 25/50/75% with halt-and-recalibrate trigger.
  - m1–m7 applied: causal whisper, TOC expansion, power formula, multi-comparison sentence, Landis & Koch 1977, Lázaro 2018, Trujillo-Sáez 2020.
  - Strategy memo §6 + pseudo_code Stages 2 and 3 fully aligned. References.bib +2 entries.
- Strategy phase: **fully approved**. All critic findings resolved.
- Discovery (data) round 1: explorer + explorer-critic done.
  - Pilot N=10. Recommends Tier A with adjustments (corpus universe ~144 [ASSUMED]; Layer 2 retrieval 50% conservative / 75–80% likely).
  - **Critic verdict: 79/100 NEEDS REVISION.** Pilot statistically insufficient (Wilson 95% CI on 50% retrieval = [24%, 76%]). 2 CRITICAL + 4 MAJOR.
  - Recommends round-2 explorer pass: ~10 additional probes (4 likely-yes Layer 1 + 4 unconfirmed Layer 2 + AQU + ACSUG + Castilian-León + Valencian + private non-online), raising N to 17–19.
  - Useful findings to keep: VIU is fully public (online ≠ gated); 8 autonomous-community agencies host parallel memoria registries; UAB and UPV/EHU are clean templates for scraper architecture.
- **Decision: Tier B accepted as primary** (2026-04-26). Skipping round-2 explorer to unblock coder phase.
  - Stratification: 4 sector levels (public, private-traditional, private-online, *centros adscritos*) × 18 CCAA × 2 modality. Proportional allocation of n=60 with min-2-per-active-cell rule.
  - 3 explorer revisions applied to memo: VIU public ≠ modality-general gating; +8 autonomous-community agencies in memoria sourcing (AQU, ACSUG, UNIBASQ, AAC-DEVA, ACSUCYL, AQUIB, AVAP, Madri+d); *centros adscritos* as sector level (with adscrito × CCAA sub-analysis flagged as infeasible).
  - Framing updated: "first post-MRCDD, two-degree, two-layer stratified analysis" replaces "first comprehensive census" everywhere (memo §10 Obj 1, positioning.md §1, §7).
  - Tier C reserved as final fallback if main-pull retrieval falls below 50%.
- **Coder phase now unblocked.** First task for the data-engineer: full RUCT scrape + Tier B sample selection on the locked-in stratification.
- Done: OSF pre-registration draft — `quality_reports/osf_preregistration_cdd_formacion_inicial.md` (321 lines, 11 sections + Pre-Registration Checklist).
- Done: Strategist-critic LIGHT review of OSF PAP — **80/100 ALMOST READY** (1 CRITICAL = cite-key typo, patched immediately; 5 MINOR cosmetic). After patch: ~90/100 READY TO DEPOSIT pending the user checklist.
- Review report: `quality_reports/osf_preregistration_cdd_formacion_inicial_review.md`.
- Done: Checkpoint — 3 memory files written (`user_profile`, `project_cdd_formacion_inicial`, `reference_mrcdd_competences`) + `MEMORY.md` index created. SESSION_REPORT and research_journal append-maintained throughout.

---

## 2026-04-26 — End-of-session summary

**Session totals:**
- 6 worker-critic agent rounds dispatched (librarian × 2, strategist, strategist-critic, explorer, explorer-critic, strategist-critic LIGHT)
- 14 substantive artifacts produced in `quality_reports/`
- 3 phases advanced: Discovery (Literature) PASS, Strategy PASS, Discovery (Data) accepted at user discretion
- All MAJOR critic findings resolved or accepted with explicit user decision
- Project moved from "template repo" state to "research project with locked-in design + READY-TO-DEPOSIT pre-registration"

**Verifiable factual contributions to project record:**
- BOE-A-2022-8042 verified directly: MRCDD has 23 competences (corrected `domain-profile.md` which incorrectly stated 22)
- Pilot retrieval data documented: Layer 1 6/10 confirmed, Layer 2 5/10 confirmed (Wilson 95% CI [24%, 76%])
- ~144-programme universe estimate, range 135–185, anchored on gradomania.com
- VIU is fully open (refutes prior "online = gated" assumption); UNIR confirmed gated; UCJC unconfirmed

**Hand-off state:** Coder phase unblocked. First task for the data-engineer is the full RUCT scrape + Tier B sample selection on the locked-in 4-level sector × 18 CCAA × 2 modality stratification. Estimated 12–15 months end-to-end per OSF PAP §9.

**Pending user actions:**
- Fill institution in `CLAUDE.md` (still `[TO FILL]`)
- Work through 9-item OSF Pre-Registration Checklist before actual OSF deposit
- Decide when to start data-engineer phase (RUCT scrape is ~1 day; per-institution scrapers ~270–530 person-hours per explorer estimate)
- Pending — external dependency:
  - `/discover data` — inventory *memorias* + *guías docentes* feasibility (the most fragile design assumption).
- Open question for user: institution affiliation (still placeholder in `CLAUDE.md`).

---

## 2026-04-27 — OSF Pre-Registration Checklist resolution (5 of 10)

**Operations:**
- Closed checklist items C1 (authors), C4 (coders), C5 (IRB + funding), C6 (software environment), C10 (power sensitivity table).
- Edited `osf_preregistration_cdd_formacion_inicial.md`: §1.2 (author block), §1.5 (new — Ethics & Funding), §3.5 (sample-size rationale rewritten), §6 (coder team + language coverage), §7.2 sub-analysis 5 (scope restricted), deposit-files block (+2 entries), Pre-Registration Checklist (5 items checked).
- Edited `CLAUDE.md`: institution line marked anonymized.
- Created `scripts/R/strategy/power_sensitivity_table.R` (reproducible script).
- Created `quality_reports/strategy/cdd_formacion_inicial/power_sensitivity_table.csv` (9-cell deposit artifact).
- Created `quality_reports/software_environment.md` (lock-protocol, not today's lockfile).
- Updated project memory at `project_cdd_formacion_inicial.md` with author/coder commitments + checklist progress.

**Decisions:**
- All identifying author/institution/funding data anonymized as `[ANONYMIZED — pending OSF deposit]` per user request. The PAP commits the structure (4 authors, 1 institution, A.R.J. corresponding; 3 coders drawn from authors); names/emails get filled in only at actual deposit.
- Bilingual language coverage limited to Castilian + Valencian. PAP §7.2 sub-analysis 5 restricted: (a) Valencian-language documents (C.B.T.); (b) Castilian parallel versions of CA/EU/GL documents where universities publish both. Original-only CA/EU/GL excluded with pre-registered scope clause.
- Software lock-protocol committed (closed package set) but concrete `renv.lock` deferred to pilot start.
- **Substantive correction to PAP §3.5:** original "n≈60 programme-pairs" statement contradicted the pre-registered formula. With $p_d=0.30, p_2-p_1=0.10$ the formula yields $n_{\text{pairs}}=165$, not 60. The 60 is the Tier B *programme* sample, not the paired-test sample — these are different quantities. §3.5 rewritten to make this transparent and to commit to reporting the realized $n_{\text{pairs}}$ post-sampling, with under-power as a logged deviation.

**Results:**
- 5 of 10 OSF checklist items closed in-session. Remaining 4 (C2 universe count, C3+C9 Tier B sample IDs, C8 reliability subsample IDs) correctly sequenced behind RUCT scrape; C7 (coding manual) sequenced behind pilot.
- PAP now in *substantively complete* state for OSF deposit pending only (a) the unblanking of `[ANONYMIZED]` fields at submission time and (b) the four scrape/pilot-dependent addenda.

**Commits:**
- (none yet — staged for user review)

**Status:**
- Done: 5 of 10 OSF checklist items (C1, C4, C5, C6, C10).
- Pending — user input not required:
  - Decide when to dispatch the data-engineer (RUCT scrape unlocks C2/C3+C9/C8).
  - Decide when to start the pilot (unlocks C7).
- Pending — user input required:
  - Unblank the 5 anonymized fields in §1.2 / §1.5 / §6 before actual OSF submission (full names, affiliation, email of A.R.J., institutional IRB-policy outcome, funding source).

## 2026-04-27 12:18 — Stage 0: Corpus inventory + Tier B sample (data-engineer)

**Operations:**
- Created Python scrapers: `scripts/python/scrape/{gradomania_aggregator,educaweb_aggregator,aneca_listado_titulos,agencias_autonomicas,ruct_scraper,inventory_reconciliation}.py`
- Created Tier B sample selection script (Python deposit; primary): `scripts/python/strategy/tier_b_sample.py`
- Created R reference script (cross-validation only; not deposit): `scripts/R/strategy/tier_b_sample.R`
- Wrote `quality_reports/data_engineering_environment.md` (Python env lock).
- Patched `quality_reports/osf_preregistration_cdd_formacion_inicial.md` §2.4, §6 (RNG correction note), deposit-files block, checklist C2 + C3+C9 marked [x], §10 deviations log appended (RUCT fallback, N=60 vs min-2, Python RNG).
- Ran all aggregators + RUCT + reconciliation + sampling end-to-end.

**Decisions:**
- RUCT live scrape returned 0 parseable rows -- fell back to cross-validation aggregate per plan §7. Logged as deviation.
- Tier B target N=60 vs strict min-2-per-active-cell = 63 minimum: resolved by enforcing min-2 only on cells receiving >=1 draw, dropping 3 low-information cells from sample (still in universe). Logged as deviation.
- Python `numpy.random.default_rng(seed=20240901)` is the authoritative deposit RNG. R script encodes algorithm but does not reproduce IDs. Logged as deviation.

**Results:**
- **Universe count:** 168 active programmes (PAP `[ASSUMED]` ~144 replaced; within [120, 170] range).
- **Strata cells active:** 32 of 144 possible.
- **Tier B sample N=60.** Sector: 30 public / 16 private-traditional / 8 private-online / 6 adscrito. CCAA: 16 communities. Modality: 52 presencial / 8 online. Degree: 30 Infantil / 30 Primaria.
- **Reproducibility:** verified by re-running tier_b_sample.py against same inventory; identical 60 IDs.

**Commits:** (pending user approval)

**Status:**
- Done: Stage 0 deliverables produced; verification checklist passes.
- Pending: coder-critic review (per worker-critic pair); user sign-off on RUCT-fallback deviation; commit.

## 2026-04-27 13:00 — Stage 0 patch round 1 (coder-critic round 1 fixes)

**Operations:**
- Edited `scripts/python/scrape/inventory_reconciliation.py`: added UOC (public-online, Cataluna) and 3 ANECA-only institutions to PUBLIC_UNIS / PRIVATE_TRADITIONAL_UNIS / INSTITUTION_CCAA / canonical_map; added PUBLIC_ONLINE_UNIS set + ONLINE_INSTITUTIONS union; replaced `astype(bool)` with explicit `astype(str).str.len() > 0` (line 622-equivalent); added NOISE_FILTER_COUNTS instrumentation to `is_noise_university` and a per-rule drop-counts table to the reconciliation log.
- Edited `scripts/R/strategy/tier_b_sample.R`: replaced final `cat()` with `message()` (line 212).
- Edited `scripts/python/strategy/tier_b_sample.py`: parameterised "32 active cells" hardcode to `n_active`; appended REPRODUCIBILITY CHAIN paragraph to `reproducibility_check.txt` writer.
- Edited `quality_reports/data_engineering_environment.md`: added TLS-bypass disclosure bullet to §4.
- Edited `quality_reports/osf_preregistration_cdd_formacion_inicial.md`: added Deviation 4 (inventory revision); updated Pre-Registration Checklist C2 + C3+C9 to 174-programme universe + new sample composition; updated companion-artifacts header.
- Re-ran `scripts/python/scrape/inventory_reconciliation.py` then `scripts/python/strategy/tier_b_sample.py` (twice — second run byte-identical, confirming determinism).

**Decisions:**
- "Universidad Católica Santa Teresa de Jesús de Ávila" (ANECA's formal name) merged into the existing UCAV row via the canonical_map alias rather than added as a new institution — they are the same entity (UCAV's full registered name).
- UOC modality forced to `online` via a new PUBLIC_ONLINE_UNIS set + ONLINE_INSTITUTIONS union (parallel to PRIVATE_ONLINE_UNIS), preserving the public sector while overriding the modality hint.
- 174-programme realised count is +4 above the pre-registered [120, 170] ceiling; this is documented as a minimal monotonic-improvement deviation in PAP §10 Deviation 4 rather than narrowing the recovered set.

**Results:**
- Realised universe: 168 to 174 programmes (delta +6).
- Active stratification cells: 32 to 34.
- Min-feasible-N under min-2: 63 to 67 (TARGET_N held at 60).
- Cells dropped from sample: 3 to 4.
- Sample composition (N=60): 30 public, 18 private-traditional, 6 private-online, 6 adscrito; 15 CCAAs; 29 Infantil + 31 Primaria; 52 presencial + 8 online. UOC P0118+P0119 in sample.
- New first 5 sampled IDs: P0003, P0004, P0009, P0011, P0018 (vs. previous P0003, P0004, P0009, P0011, P0018 — IDs happen to coincide for the first 5 because all 5 are adscritos rows whose ordering was unaffected by the UOC/ANECA insertions further down the sort key; the shift is in IDs P0029+ and onward).
- Byte-identical re-run verified.

**Commits:**
- (pending — patch round not yet committed)

**Status:**
- Done: All 6 patches applied; reconciliation + sampling re-run; deposit artifacts regenerated; PAP §10 + checklist updated; research journal appended.
- Pending: coder-critic round 2 review (target ≥95 for OSF-deposit gate).

## 2026-04-27 — Stage 0 cleared for OSF deposit (coder-critic round 2)

**Operations:**
- Dispatched **coder-critic** round 2 (focused re-review): all 6 round-1 patches verified APPLIED CORRECTLY.
- Tightened PAP §10 Deviation 4 wording: replaced "remains within [120, 170] only after a one-row tolerance allowance" with plain statement that 174 is +4 above the sanity band, monotonic improvement (legitimate institutions recovered). Removes the awkward critic-flagged phrase.
- Appended round 2 review section to `quality_reports/stage0_corpus_inventory_review.md`.

**Decisions:**
- [120, 170] +4 overshoot judged a critic-call (not user-call): the band was tagged `[ASSUMED]` in PAP §3.4 — placeholder, not hard constraint. Truncating back would require dropping legitimate institutions (worse than honest disclosure).

**Results:**
- **Stage 0 score: 97/100 — GREEN-LIGHT FOR DEPOSIT.** OSF deposit gate (≥95) cleared.
- Round 1: 91/100 (PASS for PR; below OSF gate). Round 2: 97/100 (cleared OSF gate). Strikes 1/3 closed; no escalation.
- 7 of 10 OSF Pre-Registration Checklist items closed (C1, C2, C3+C9, C4, C5, C6, C10). Remaining 3 sequenced: C8 (post-segment-ingestion), C7 (post-pilot), OSF deposit lock (assembly).

**Commits:** (pending user approval — clean commit point now reached)

**Status:**
- Done: Stage 0 fully cleared for OSF deposit. Coder phase fully unblocked for Stages 1a/1b (Layer 1/2 retrieval) once user signals readiness.
- Pending — orchestrator-trackable:
  - C8 (reliability subsample) → drawn after segment ingestion completes (Stages 1a/1b).
  - C7 (coding manual v1.0) → produced post-pilot.
  - OSF deposit lock → can submit partial (7 items + design artifacts) now if user wants; complete deposit waits on C7+C8.
- Pending — user-tracked:
  - Unblank 5 anonymized fields before actual OSF submission (full names + institution + email of A.R.J. + IRB-policy + funding).
  - Decide: deposit OSF partial now, or wait for full set after pilot?
  - Decide: next phase = Stage 1a/1b (~6-8 weeks per OSF PAP §9) or pilot first?
  - Decide: commit Stage 0 deliverables now (167 files staged)?
