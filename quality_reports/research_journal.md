# Research Journal — CDD en la Formación Inicial del Profesorado

Append-only log. One entry per agent invocation or phase transition.

---

### 2026-04-26 — Project setup
**Phase:** Discovery (setup)
**Target:** `CLAUDE.md`, `.claude/references/domain-profile.md`
**Score:** N/A
**Verdict:** Project initialized for education-research field (Teacher Education / Educational Technology). Domain profile rewritten from economics default to TDC / DigCompEdu / MRCDD calibration. CLAUDE.md placeholders updated. Three clarifications resolved with user: (1) frameworks = DigCompEdu + MRCDD; (2) angle = curricular analysis (option d); (3) search languages = ES + EN.
**Report:** —

### 2026-04-26 — librarian
**Phase:** Discovery (literature)
**Target:** `quality_reports/literature/cdd_formacion_inicial/`
**Score:** N/A (creator — scored by critic)
**Verdict:** 51 entries across 7 buckets (A–G). Bucket A names six direct scooping risks (A1, A3, A4, A5, A6, A7, A8). Search interrupted by parent-session rate limit after `annotated_bibliography.md` and `references.bib`. Synthesis files (`frontier_map.md`, `positioning.md`) drafted by orchestrator from librarian's bibliography to complete the deliverable without re-running expensive web searches.
**Report:** `quality_reports/literature/cdd_formacion_inicial/annotated_bibliography.md`

### 2026-04-26 — librarian-critic
**Phase:** Discovery (review)
**Target:** `quality_reports/literature/cdd_formacion_inicial/` (4 files)
**Score:** 84/100 — PASS
**Verdict:** Above commit threshold (80), below PR threshold (90). Required follow-ups before strategy phase: (1) resolve `author = {{Various}}` placeholders in 9 .bib entries; (2) add Hsieh & Shannon (2005) and Krippendorff (2018) for content-analysis methods. Recommended Tier-1 additions: Lázaro-Cantabrana/Gisbert/Silva-Quiroz 2018, Fernández-Cruz & Fernández-Díaz 2016, Cabero & Martínez-Gimeno 2019. No escalation triggered.
**Report:** `quality_reports/literature/cdd_formacion_inicial/critic_report.md`

### 2026-04-26 — librarian (round 2)
**Phase:** Discovery (literature — focused fixes)
**Target:** `quality_reports/literature/cdd_formacion_inicial/` (annotated_bibliography.md, references.bib)
**Score:** N/A (creator)
**Verdict:** Resolved all 10 `{Various}` placeholders (9 verified and rewritten; 1 dropped — `UNIR2022_curriculum_design` unrecoverable). Surfaced and corrected 4 metadata errors from round 1: `Bordon2024_primaria_inicial` was 2026 vol 78(1) not 2024 vol 76(3); `Bordon2023_agencia_digital` was actually 2024; `Jaen2024_sagrada_familia` was published in EPSIR not *Tecnología, Ciencia y Educación*; `RELATEC2023_concept_review` was actually 2024. Added 2 methods refs (Hsieh & Shannon 2005; Krippendorff 2018) and 3 Tier 1 Spanish refs (Fernández-Cruz & Fernández-Díaz 2016; Lázaro-Cantabrana, Gisbert & Silva-Quiroz 2018; Cabero & Martínez-Gimeno 2019). Net: 51 → 54 entries; verification rate 63% → 76%; biber-compatible. New sub-bucket E.M (methods) created. `frontier_map.md` and `positioning.md` left untouched per scope.
**Report:** `quality_reports/literature/cdd_formacion_inicial/annotated_bibliography.md` §"Round 2 changelog"

### 2026-04-26 — orchestrator
**Phase:** Discovery (synthesis fix)
**Target:** `quality_reports/literature/cdd_formacion_inicial/positioning.md`
**Score:** N/A
**Verdict:** Applied librarian-critic recommendation #11 (issue 11): tightened the contribution sentence in §1 to "first post-MRCDD, two-degree, two-layer" with explicit conjunction-as-contribution clause. Resolves the contradiction the critic flagged between §1 and §7.
**Report:** —

### 2026-04-26 — strategist
**Phase:** Strategy (design memo)
**Target:** `quality_reports/strategy_memo_cdd_formacion_inicial.md` + `quality_reports/strategy/cdd_formacion_inicial/{pseudo_code,robustness_plan,falsification_tests}.md`
**Score:** N/A (creator)
**Verdict:** Delivered descriptive/measurement strategy memo (15 sections) + 3 companion artifacts. Locked-in choices: MRCDD primary + DigCompEdu benchmark, depth scale 0–3 (defended against A1–C2), three-tier sampling fallback (census → stratified → purposive), pilot-first protocol with κ ≥ 0.70, OSF pre-registration, layer-collapse fallback to one-layer framing pre-registered. 6 explicit `[ASSUMED]` flags routed to `/discover data`. INV-8 compliance enforced via explicit causal-language disavowal in §7.5–7.6.
**Report:** `quality_reports/strategy_memo_cdd_formacion_inicial.md`

### 2026-04-26 — strategist-critic
**Phase:** Strategy (review, 4 sequential phases)
**Target:** `quality_reports/strategy_memo_cdd_formacion_inicial.md` (+ companion artifacts)
**Score:** 93/100 — PASS
**Verdict:** Above PR threshold (90), below submission threshold (95). No CRITICAL issues. 2 MAJOR (M1 — MRCDD competence count 22 vs 23 contradicts domain profile; M2 — reliability protocol inconsistency between memo §6 and pseudo_code Stage 2). 7 MINOR (causal whisper, TOC underspec, power formula, multi-comparison framing, missing citations Landis & Koch + Lázaro-Cantabrana 2018 + Trujillo-Sáez). Recovery credits +12 for causal-language discipline, pre-registered layer-collapse fallback, depth-scale defense, frontier-map-risk coverage. No escalation triggered. Strategy → Coder hand-off deferred until M1, M2, and `/discover data` resolved.
**Report:** `quality_reports/strategy_memo_cdd_formacion_inicial_review.md`

### 2026-04-26 — orchestrator (strategy patch round)
**Phase:** Strategy (patch — M1 + 7 MINOR fixes)
**Target:** `domain-profile.md`, `strategy_memo_cdd_formacion_inicial.md`, `references.bib`
**Score:** N/A
**Verdict:** **M1 resolved by direct citation lookup of BOE-A-2022-8042 (PDF p. 7):** "se ha creado una nueva competencia en el Área 1, Compromiso profesional ... con lo que el Marco de Referencia de la Competencia Digital Docente que aquí se presenta tiene 23 competencias en lugar de 22." → MRCDD has 23 (strategist correct); domain profile patched (was 22). All 7 MINOR fixes applied: (m1) §8 sub-analysis 2 causal whisper rephrased; (m2) coding manual TOC §§4, 6, 7 expanded with target counts and required disambiguation pairs (Area 1↔5, 2↔3, 4↔6); (m3) Tier B power formula added explicitly (McNemar paired-proportions, with assumed values); (m4) multi-comparison policy sentence added to §7.4; (m5) Landis & Koch 1977 added to bib + memo cite; (m6) Lazaro2018_rubrica_latinoamerica woven into §6 reliability protocol; (m7) Trujillo-Sáez 2020 added to bib + memo §10 Obj 5. **M2 deferred to user — design decision pending (full double-coding vs 20%+single).** External dependency `/discover data` still pending.
**Report:** —

### 2026-04-26 — orchestrator (M2 resolved)
**Phase:** Strategy (patch — M2 reliability protocol locked-in)
**Target:** `strategy_memo_cdd_formacion_inicial.md` §6, `pseudo_code.md` Stage 2, Stage 3, `decisions/strategy_cdd_formacion_inicial.md`
**Score:** N/A
**Verdict:** User selected **Variant B** (20% double + 80% single, the field standard per Krippendorff 2018). Three operational defaults committed: B1 — a-priori stratified sampling deposited to OSF; B2 — balanced rotation across coders within (degree × layer) strata, with automatic escalation on uncertainty flags; B3 — milestone κ recalculation at 25/50/75% with halt-and-recalibrate trigger if κ < 0.70 in any area. Strategy memo §6 table rewritten with the locked-in protocol; pseudo_code Stage 2 rewritten with the implementing procedures; pseudo_code Stage 3 updated to compute κ on the cumulative double-coded set (a-priori 20% + uncertainty escalations) and to write `kappa_trajectory.csv` and `uncertainty_log.csv`. All MAJOR critic findings now resolved. Strategy phase fully approved; only `/discover data` remains as external dependency before coder phase.
**Report:** —

### 2026-04-26 — explorer
**Phase:** Discovery (data — corpus inventory)
**Target:** `quality_reports/data_exploration_cdd_formacion_inicial.md`
**Score:** N/A (creator)
**Verdict:** Pilot of 10 institutions across 5 strata. Headline findings: ~144 programmes / ~67–70 institutions (`[ASSUMED]`); no public RUCT API or export (session-based scrape required); Layer 1 retrieval 6/10 confirmed (conservative 60% / likely 85–90% after follow-up); Layer 2 retrieval 5/10 confirmed (conservative 50% / likely 75–80% — borderline against 80% Tier A trigger). Recommends Tier A with two operational adjustments. Three strategy-memo revisions flagged: (a) "online = gated" is provider-specific not modality-general (VIU public; UNIR likely gated); (b) memoria sourcing must include 8 autonomous-community quality agencies; (c) *centros adscritos* (~15 institutions) need separate stratification cell. Tooling: per-institution Python scrapers (~67 modules) using `requests` + `BeautifulSoup` + `pdfplumber`. Budget: 14 web searches + 9 web fetches.
**Report:** `quality_reports/data_exploration_cdd_formacion_inicial.md`

### 2026-04-26 — explorer-critic
**Phase:** Discovery (review, 5-point assessment adapted for document corpus)
**Target:** `quality_reports/data_exploration_cdd_formacion_inicial.md`
**Score:** 79/100 — NEEDS REVISION
**Verdict:** Below commit threshold (80). 2 CRITICAL: (C1) Pilot N=10 produces Wilson 95% CI of [24%, 76%] on the 50% Layer 2 rate — statistically insufficient to resolve Tier A vs B; (C2) Pilot under-samples 4 large CCAA (Castilian-León, Valencia, others), all private non-online providers, and centros adscritos beyond ESCUNI. 4 MAJOR: zero autonomous-community-agency probes despite explorer flagging them as required; programme universe ~144 has wide bounds (~135–185); no benchmarking against Cuevas-Monzonís / Sanz-Benito published retrieval rates; centros-adscritos × CCAA sub-analysis infeasible at Tier B. **Verdict: defer Tier A vs B decision to round-2 explorer pass with ~10 additional probes** (raising N to 17–19). Concur with explorer's three strategy-memo revisions in direction; insufficient evidence on (b). Corpus feasibility grade: **B** (feasible with named adjustments, not yet Grade A).
**Report:** `quality_reports/data_exploration_cdd_formacion_inicial_review.md`

### 2026-04-26 — strategist-critic (LIGHT review of OSF PAP)
**Phase:** Strategy (PAP fidelity check)
**Target:** `quality_reports/osf_preregistration_cdd_formacion_inicial.md`
**Score:** 80/100 — ALMOST READY (after CRITICAL patched: ~90/100 READY TO DEPOSIT)
**Verdict:** Zero design drift — every locked-in element (M1, M2, Tier B, depth 0–3, Goodlad, causal disavowal, all 21 robustness + 7 falsification by reference) reproduced exactly. **One CRITICAL: typo in cite key `@Cabero2023_competencia_digital_review` → `@Cabero2023_evaluacion_review` at 2 locations** — patched immediately by orchestrator. 5 MINOR issues all cosmetic / documentation-trail (checklist count drift 9 vs 10; hidden [ASSUMED] in §1.3; memo follow-ups m1–m7 disposition not annotated; companion artifacts deposit timing; internal repo path in §6). Hypotheses correctly framed as expected patterns with explicit "no causal interpretation" disclaimer. **Once CRITICAL patched, READY TO DEPOSIT pending the 9-item user checklist.**
**Report:** `quality_reports/osf_preregistration_cdd_formacion_inicial_review.md`

### 2026-04-26 — orchestrator (CRITICAL patch on OSF PAP)
**Phase:** Strategy (PAP — fidelity patch)
**Target:** `quality_reports/osf_preregistration_cdd_formacion_inicial.md`
**Score:** N/A
**Verdict:** Patched the CRITICAL cite-key typo: `@Cabero2023_competencia_digital_review` → `@Cabero2023_evaluacion_review` (replace_all on 2 occurrences). PAP score now ~90/100 = READY TO DEPOSIT. Remaining 5 MINOR issues left for user discretion (cosmetic).
**Report:** —

### 2026-04-26 — strategist (PAP mode — OSF pre-registration draft)
**Phase:** Strategy (PAP — OSF deposit format)
**Target:** `quality_reports/osf_preregistration_cdd_formacion_inicial.md`
**Score:** N/A (creator)
**Verdict:** ~2,400 words / 321 lines / 11 sections + Pre-Registration Checklist. Faithful re-organization of the locked-in strategy memo into OSF deposit format — no design choices re-opened. Hypotheses re-cast as "expected patterns" with explicit "no causal interpretation" disclaimers (H1: uneven coverage with Areas 2–3 > 60%, Areas 4 and 6 < 40%; H2: layer gap larger on Areas 4 and 6; H3: Primaria > Infantil on Areas 2 and 4 within paired universities). MRCDD = 23 competences cited verbatim from BOE. Reliability Variant B (B1/B2/B3) reproduced. Tier B sampling reproduced including adscritos × CCAA infeasibility caveat. 21 robustness checks + 7 falsification tests pre-registered by reference (not duplicated). 9 `[ASSUMED]` placeholders surfaced for user review before deposit (authors/affiliation, programme universe count, sampled universities, coder team, IRB, software environment).
**Report:** `quality_reports/osf_preregistration_cdd_formacion_inicial.md`

### 2026-04-27 — coder-critic (Stage 0 review, round 2 — patch verification)
**Phase:** Execution (data engineering — re-review)
**Target:** 6 sequenced patches from round 1 + new artifact integrity (174-programme universe, regenerated Tier B sample with UOC P0118+P0119 in)
**Score:** **97/100 — GREEN-LIGHT FOR DEPOSIT**
**Verdict:** Above OSF-deposit gate (≥95). All 6 round-1 patches APPLIED CORRECTLY. Two cosmetic MINORs remain (-3 total): (a) covering note understated 4th whitelist addition (UCAV alias, no net add); (b) Deviation 4 wording "tolerance allowance" was awkward — orchestrator cleaned up post-review to state +4 overshoot plainly. Universe revised 168→174 (delta +6 net: UOC×2 public-online-Cataluna, Atlántico Medio×2 private-trad-Canarias, Tecnología y Empresa×2 private-trad-Madrid). Active cells 32→34. Sample regenerated; UOC P0118+P0119 in. Reproducibility byte-identity verified. **Strikes 1/3 closed; no escalation. Coder phase fully unblocked. Stage 0 cleared for OSF deposit.** Round 2 review appended to `stage0_corpus_inventory_review.md` §"Round 2 — Patch verification".
**Report:** `quality_reports/stage0_corpus_inventory_review.md`

### 2026-04-27 — data-engineer (Stage 0 patch round 1)
**Phase:** Execution (data engineering — patch round 1)
**Target:** `inventory_reconciliation.py`, `tier_b_sample.py`, `tier_b_sample.R`, `data_engineering_environment.md`, `inventory_reconciliation_log.md`, `reproducibility_check.txt`, PAP §10 (Deviation 4 added), regenerated deposit CSVs.
**Score:** N/A (creator)
**Verdict:** Applied all 6 sequenced patches from coder-critic round 1. Recovered 4 previously-dropped legitimate institutions: UOC (added to new `PUBLIC_ONLINE_UNIS` set; sector=public, modality=online, Cataluna), Universidad del Atlántico Medio (private-traditional, Canarias), Universidad Tecnología y Empresa (private-traditional, Madrid), and UCAV alias merge (no net add). Realised universe **174 programmes** (+6 net from 168). Active stratification cells **34** (was 32). Sample regenerated against revised inventory; UOC P0118+P0119 are in the sample. New composition: 30 public / 18 private-trad / 6 private-online / 6 adscrito; 15 CCAAs; 29 Infantil + 31 Primaria; 52 presencial + 8 online. PAP §10 has 4 deviations now: RUCT fallback, N=60 cell-drop (4 cells now), Python RNG, inventory-revision (+6 / +4 over [120, 170] sanity band). Byte-reproducibility verified across two consecutive runs.
**Report:** `quality_reports/stage0_corpus_inventory_review.md` §"Round 2"

### 2026-04-27 — coder-critic (Stage 0 review, round 1)
**Phase:** Execution (data engineering — review)
**Target:** 8 scripts (`scripts/python/scrape/*.py` × 6, `scripts/python/strategy/tier_b_sample.py`, `scripts/R/strategy/tier_b_sample.R`) + 6 cleaned outputs + 12 raw passes + `data_engineering_environment.md`
**Score:** **91/100 — PASS for PR; below OSF-deposit gate (95)**
**Verdict:** Above PR threshold (90), 4 points below OSF-deposit gate (95). Two MAJOR (M1 — UOC silent classification drop; M2 — ANECA-only legitimate institutions silently dropped via `canonical_map` bottleneck; M3 — reproducibility chain documentation imprecise). Four MINOR (R `cat()`→`message()`; pandas `astype(bool)` ambiguity; TLS-bypass undocumented in env doc; educaweb noise-filter rules undocumented). Recovery +9 (strategy alignment +3, PAP coherence +3, dropped_for_n60 column +2, sample selection algorithm verified +1). All INV-14/15/16/17/18/19 PASS. PAP §10 deviations match actual outputs exactly. **One round of focused patches needed to clear OSF gate ≥95.**
**Report:** `quality_reports/stage0_corpus_inventory_review.md`

### 2026-04-27 — data-engineer (Stage 0: corpus inventory + Tier B sample)
**Phase:** Execution (data engineering — round 1)
**Target:** `scripts/python/{scrape,strategy}/`, `scripts/R/strategy/`, `data/raw/inventory_passes/`, `data/cleaned/`, `quality_reports/data_engineering_environment.md`, `quality_reports/osf_preregistration_cdd_formacion_inicial.md` §10 + checklist
**Score:** N/A (creator)
**Verdict:** Closed OSF Pre-Registration Checklist items C2 (universe count) + C3+C9 (Tier B sample). Realised universe **168 programmes** (vs `[ASSUMED]` ~144; within pre-registered [120, 170]). Tier B sample **N=60** with 30 Infantil / 30 Primaria, 30 public / 16 private-trad / 8 private-online / 6 adscrito, 16 CCAAs, 52 presencial / 8 online. Three deviations logged in PAP §10 (all user-approved): (1) RUCT scrape failed — JS-rendered pagination — fallback to cross-validation aggregate per plan §7 ladder; (2) N=60 over strict-min-2 alternative N=63 with 3 cells dropped from sample (Madrid×public×online, Murcia×public×presencial, Navarra×public×presencial); (3) Python `numpy.random.default_rng(seed=20240901)` as authoritative RNG instead of R `set.seed()` (R unavailable on machine). 8 scripts + 13 raw CSVs + 5 cleaned outputs + 1 env doc produced. Reproducibility verified byte-identical across 2 consecutive runs.
**Report:** `quality_reports/plans/2026-04-27_stage0-corpus-inventory.md` (plan); SESSION_REPORT + research_journal entries.

### 2026-04-27 — orchestrator (OSF checklist resolution C1, C4, C5, C6, C10)
**Phase:** Strategy (PAP — checklist resolution before data-engineer dispatch)
**Target:** `osf_preregistration_cdd_formacion_inicial.md` §1.2, §1.5 (new), §3.5, §6, §7.2 sub-analysis 5, deposit-files block, Pre-Registration Checklist; `CLAUDE.md` line 6; `scripts/R/strategy/power_sensitivity_table.R`; `quality_reports/strategy/cdd_formacion_inicial/power_sensitivity_table.csv`; `quality_reports/software_environment.md`
**Score:** N/A
**Verdict:** Closed 5 of 10 OSF checklist items. **C1 (authors):** 4 authors A.R.J./M.G.J./C.B.T./P.P.G., A.R.J. corresponding, all 4 same institution; full names + affiliation + email anonymized as `[ANONYMIZED — pending OSF deposit]`. **C4 (coders):** 3 coders drawn from author team (A.R.J./M.G.J./C.B.T.), language coverage Castilian (3) + Valencian (C.B.T.); Catalan/Basque/Galician *not covered* — sub-analysis 5 scope-restricted accordingly with pre-registered exclusion clause. **C5 (IRB+funding):** new §1.5 added; working position pre-registered as "no IRB needed (public documents, no human subjects)" with institution-policy + funding both `[ANONYMIZED]`. **C6 (software):** lock-protocol committed in `software_environment.md` — closed package set (tidyverse, irr, psych, boot, ggplot2, fmsb, pheatmap, scales, here, renv); concrete `renv.lock` produced at pilot start; adding any package post-lock = logged deviation. **C10 (power):** `power_sensitivity_table.csv` deposited (9-cell grid `p_d × diff`) plus reproducible R script. **Substantive correction to PAP §3.5:** the previously stated "n≈60 programme-pairs" did not match the formula (which yields 165 at p_d=0.30, diff=0.10). §3.5 rewritten to (a) reference the deposited table, (b) clarify that 60 is the Tier B *programme* sample, not the paired-test sample, (c) commit to reporting realized n_pairs post-sampling and flagging underpowered comparisons as deviations. Remaining 5 items (C2, C3+C9, C8, C7) sequenced behind RUCT scrape + pilot.
**Report:** `quality_reports/osf_preregistration_cdd_formacion_inicial.md` (post-patch); `quality_reports/software_environment.md`; `scripts/R/strategy/power_sensitivity_table.R`

### 2026-04-26 — orchestrator (Tier B locked-in + explorer revisions applied)
**Phase:** Discovery → Strategy patch (Tier B accepted as primary; 3 explorer revisions applied to memo)
**Target:** `strategy_memo_cdd_formacion_inicial.md` §3, §4, §8, §10; `positioning.md` §1, §6, §7; `decisions/strategy_cdd_formacion_inicial.md`
**Score:** N/A
**Verdict:** **User decision: adopt Tier B as primary**, skipping round-2 explorer to unblock coder phase. Memo §3 rewritten — Tier B locked-in (~60 programmes; 4-level sector × 18 CCAA × 2 modality stratification with *centros adscritos* as sector level 4); Tier A explicitly rejected on pilot evidence; Tier C reserved as final fallback below 50% retrieval. Memo §4 source priority for memorias expanded to include 8 autonomous-community agencies (AQU, ACSUG, UNIBASQ, AAC-DEVA, ACSUCYL, AQUIB, AVAP, Madri+d) between ANECA and university transparency portals. Memo §4 accessibility issues: online provider gating downgraded from modality-general to provider-specific (VIU public per pilot; UNIR gated; UCJC unconfirmed). Memo §8 sub-analysis 1 expanded to 4 sector levels (added *centros adscritos*); sub-analysis 3 (geographic) flagged as not computed within adscrito sector (cells too small at Tier B). Memo §10 Obj 1 updated — "first comprehensive census" framing replaced with "first post-MRCDD, two-degree, two-layer stratified analysis". Positioning.md §1 elevator pitch and §7 risks updated to match. Strategy decision record updated with full Tier B rationale and resolved-flag on `/discover data` dependency. **Coder phase now unblocked** — the data-engineer's first task is the full RUCT scrape + Tier B sample selection on the locked-in stratification.
**Report:** —

### 2026-04-27 12:18 — data-engineer
**Phase:** Execution -- Stage 0 (corpus inventory + Tier B sample)
**Target:** `data/cleaned/corpus_inventory.csv`, `data/cleaned/tier_b_sample_ids.csv`, `scripts/python/{scrape,strategy}/`, `scripts/R/strategy/tier_b_sample.R`, `quality_reports/data_engineering_environment.md`, `osf_preregistration_cdd_formacion_inicial.md` (deposit patch).
**Score:** N/A (pending coder-critic)
**Verdict:** Stage 0 closed with realised universe N=168 (within pre-registered [120, 170]) and Tier B sample N=60 drawn via `numpy.random.default_rng(seed=20240901)`. RUCT live scrape failed (0 parseable rows) -- fell back to cross-validation aggregate (gradomania + educaweb + ANECA + 8 autonomous-community agencies + manual adscritos override) per plan section 7. Three deviations logged in PAP §10: RUCT fallback, N=60-vs-min-2 cell-drop policy, Python-not-R RNG. C2 + C3+C9 marked [x] in OSF checklist. Verification checklist passed: every sampled programme traces to inventory, all 4 sector levels present, 17 CCAAs in universe / 16 in sample, sample reproducible across two runs.
**Report:** `data/cleaned/inventory_reconciliation_log.md`, `data/cleaned/reproducibility_check.txt`.

### 2026-04-27 13:00 — data-engineer (round 2: patch round 1 from coder-critic)
**Phase:** Execution (Stage 0 deposit patch)
**Target:** `scripts/python/scrape/inventory_reconciliation.py` + `scripts/R/strategy/tier_b_sample.R` + `data/cleaned/{corpus_inventory.csv,tier_b_sample_ids.csv,tier_b_strata_table.csv,reproducibility_check.txt,inventory_reconciliation_log.md}` + `quality_reports/{data_engineering_environment.md,osf_preregistration_cdd_formacion_inicial.md}`
**Score:** N/A (creator artifact; pending coder-critic round 2)
**Verdict:** Six patches applied per `quality_reports/stage0_corpus_inventory_review.md` "Sequenced fix list". Universe revised from 168 to 174 (recovered UOC public-online-Cataluna + Universidad del Atlántico Medio private-traditional-Canarias + Universidad Tecnología y Empresa private-traditional-Madrid + UCAV alias merge). Active cells 32 to 34. Sample IDs shifted because of inventory re-sort; new first 5 = P0003, P0004, P0009, P0011, P0018; UOC P0118+P0119 in sample. Byte-identical re-run verified. PAP §10 has 4th deviation entry; checklist updated.
**Report:** `quality_reports/stage0_corpus_inventory_review.md` (the round-1 critic report being addressed).
