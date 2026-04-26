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
