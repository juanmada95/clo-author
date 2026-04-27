# Plan — Stage 0 (Corpus Inventory + Tier B Sample) for the CDD Curricular Analysis

**Status:** DRAFT — awaiting user approval.
**Plan target:** Closes OSF Pre-Registration Checklist items **C2** (universe count) and **C3+C9** (`tier_b_sample_ids.csv`). Unblocks C8 (reliability subsample).
**Agents to dispatch:** `data-engineer` (creator) + `coder-critic` (reviewer).
**Estimated agent time:** 2.5–3.5 hours of agent work.
**Save copy to:** `quality_reports/plans/2026-04-27_stage0-corpus-inventory.md` after approval.

---

## 1. Context

The strategy phase locked in **Tier B** (~60 programmes, stratified across 4-level sector × 18-CCAA × 2-modality cells with min-2-per-active-cell rule, seed `20240901`). The OSF pre-registration commits to depositing both `corpus_inventory.csv` (the universe) and `tier_b_sample_ids.csv` (the sample) before any document retrieval begins. Three pre-registered artifacts on the deposit timeline depend on this stage:

- **C2** — replace `[ASSUMED]` ~144-programme estimate with the realized RUCT count; log a deviation in PAP §10 if the realized count differs substantially.
- **C3+C9** — `tier_b_sample_ids.csv` with the seed, strata, and 60 programme IDs.
- **C8** — `reliability_subsample_ids.csv` (20% of the *coded segments*, drawn AFTER Tier B sample is fixed AND AFTER document retrieval defines the segment universe; this plan does **not** produce C8 yet).

Without this stage, the data-engineer cannot proceed to Layer 1/2 retrieval (Stages 1a/1b of `pseudo_code.md`), and the OSF deposit cannot be finalized.

## 2. Goal

Produce, in this session:

1. **`data/cleaned/corpus_inventory.csv`** — every active 2024–2025 *Grado en Maestro de Educación Infantil* and *Grado en Maestro de Educación Primaria* programme in Spain, classified by (sector, CCAA, modality) per the locked-in Tier B stratification cells. Schema per `pseudo_code.md` STAGE 0.
2. **`data/cleaned/tier_b_sample_ids.csv`** — the 60 programmes drawn via stratified random sampling (`set.seed(20240901)`, proportional allocation, min-2-per-active-cell rule).
3. **`data/cleaned/tier_b_strata_table.csv`** — companion: cell-by-cell counts of the universe and the allocation to the sample (transparency artifact for the OSF deposit).
4. **`scripts/python/scrape/...`** + **`scripts/R/strategy/tier_b_sample.R`** — reproducible scripts.
5. **PAP updates** to mark C2 + C3+C9 closed, deposit the new artifacts, and (if needed) log the deviation in §10.

## 3. Approach — two-pass enumeration + stratified sample

### 3.1 Stack

| Component | Language | Justification |
|---|---|---|
| Web scraping (HTML, session-based forms) | **Python 3.11+** (`requests`, `BeautifulSoup4`, `lxml`) | Pilot recommendation (`data_exploration_cdd_formacion_inicial.md` §5); R's `rvest` cannot drive session-stateful forms reliably. |
| Inventory reconciliation (merge / dedupe / classify) | Python (`pandas`) | Same toolchain as the scrape; avoids language-context switch. |
| Tier B sample selection | **R 4.4+** (`tidyverse`, `here`, base `sample()`) | Per `software_environment.md`, R is the analysis stack; the sample-selection step is part of analysis (must be reproducible from the PAP-locked seed). |

The Python scraping stack will be pinned in a parallel companion artifact `data_engineering_environment.md` (Python lockfile to follow at scrape execution).

### 3.2 Two-pass enumeration

**Pass 1 — Cross-validation aggregation (cheap, fast, partial coverage).** Scrape four public aggregators in parallel:

- `gradomania.com` — public-uni Primaria + Infantil 2024/2025 nota-de-corte listings (39 + ~38 public-uni rows).
- `educaweb.com` — Infantil + Primaria per-degree directories (mix of public + private + online; modality tags explicit).
- 8 autonomous-community quality agencies (AQU, ACSUG, UNIBASQ, AAC-DEVA, ACSUCYL, AQUIB, AVAP, Madri+d) — programmes verified by each agency.
- ANECA *Listado de Títulos* (with TLS workaround per pilot) — central registry cross-check.

Output: `data/raw/inventory_passes/{gradomania,educaweb,aqu,acsug,...}.csv`. Schema per source (raw, pre-reconciliation).

**Pass 2 — RUCT authoritative scrape.** Session-based POST against the RUCT consultation form (`https://www.educacion.gob.es/ruct/consultaestudios`), filtered to:

- *Nivel académico* = Grado.
- *Denominación del título* contains "Maestro Educación Infantil" OR "Maestro Educación Primaria" (separate queries, paginated).
- *Situación* = Active (not discontinued, not phased-out).
- Snapshot academic year = 2024–2025.

Pagination via session cookies. Courteous rate-limit (1 req/s). Output: `data/raw/inventory_passes/ruct.csv` with `codigo_ruct`, `denominacion`, `universidad`, `centro` (distinguishes adscritos), `ccaa`, `modalidad`, `situacion`, `fecha_modificacion`, `fecha_publicacion_boe`.

### 3.3 Reconciliation

Python script `inventory_reconciliation.py`:

1. Read all `data/raw/inventory_passes/*.csv`.
2. Use RUCT `codigo_ruct` as the canonical key. Anchor on RUCT for everything that appears there.
3. For programmes appearing in cross-validation passes but NOT in RUCT (likely none, but a check): flag and investigate.
4. For each row, classify into (sector × CCAA × modality):
   - **Sector** — 4-level: `public` (50 traditional public unis), `private-traditional` (UCV, UPSA, UCJC, UCAV, UAX, etc.), `private-online` (UNIR, VIU, UDIMA, plus UNED's online modality), `adscrito` (centros adscritos — detected via RUCT's `centro` field where it differs from the parent `universidad`, plus a manual override list seeded from pilot evidence: ESCUNI, Cardenal Cisneros, Cardenal Spínola CEU, La Salle Madrid, Don Bosco, etc.).
   - **CCAA** — direct from RUCT's `ccaa` field.
   - **Modality** — direct from RUCT, with educaweb.com as cross-check; default to `presencial` where missing.
5. Output: `data/cleaned/corpus_inventory.csv`, plus a reconciliation log `data/cleaned/inventory_reconciliation_log.md` documenting any disagreement between RUCT and cross-validation passes.

### 3.4 Tier B stratified sample (R)

`scripts/R/strategy/tier_b_sample.R`:

```r
# 1. Load corpus_inventory.csv via here::here()
# 2. set.seed(20240901)  -- pre-registered seed (PAP §6 B1)
# 3. Cross-tabulate (sector × CCAA × modality × degree) and identify ACTIVE cells.
#    Compute target_n = 60.
# 4. Proportional allocation: per-active-cell n_cell = round(60 * cell_size / total).
# 5. Min-2 rule: bump every active cell to at least n_cell = 2.
#    If sum(n_cell) > 60, deduct from the cells with largest n_cell - 2 surplus
#    until sum == 60. If sum(n_cell) < 60, add to the largest cells until == 60.
# 6. Within each cell, sample(n_cell) without replacement.
# 7. Write tier_b_sample_ids.csv with columns:
#      programme_id, codigo_ruct, university_name, sector, ccaa, modality, degree
# 8. Write tier_b_strata_table.csv with columns:
#      sector, ccaa, modality, cell_size_universe, cell_size_sample, sampling_fraction
# 9. Write reproducibility_check.txt: print first 5 sampled programme_ids
#    so the PAP can quote them and any re-execution can verify.
```

### 3.5 PAP / docs updates after artifacts produced

1. Mark C2 [x] in PAP checklist with the realized count. If the realized count is outside [120, 170], log a deviation in PAP §10.
2. Mark C3+C9 [x] in PAP checklist with the deposit-file paths and the universe-count → sample-size proportion.
3. Update `project_cdd_formacion_inicial.md` memory with realized counts.
4. Append research journal entry + SESSION_REPORT entry per `logging.md`.

## 4. Files to create or modify

**Scripts (all reproducible, no absolute paths, INV-15/16/17/19 compliant):**
- `scripts/python/scrape/gradomania_aggregator.py`
- `scripts/python/scrape/educaweb_aggregator.py`
- `scripts/python/scrape/agencias_autonomicas.py` (8 agencies — one module, dispatched per-agency)
- `scripts/python/scrape/aneca_listado_titulos.py`
- `scripts/python/scrape/ruct_scraper.py`
- `scripts/python/scrape/inventory_reconciliation.py`
- `scripts/R/strategy/tier_b_sample.R`

**Data outputs:**
- `data/raw/inventory_passes/gradomania.csv`
- `data/raw/inventory_passes/educaweb.csv`
- `data/raw/inventory_passes/{aqu,acsug,unibasq,aacdeva,acsucyl,aquib,avap,madrimasd}.csv` (8 files)
- `data/raw/inventory_passes/aneca.csv`
- `data/raw/inventory_passes/ruct.csv`
- `data/cleaned/corpus_inventory.csv`
- `data/cleaned/inventory_reconciliation_log.md`
- `data/cleaned/tier_b_sample_ids.csv`
- `data/cleaned/tier_b_strata_table.csv`
- `data/cleaned/reproducibility_check.txt`

**Documentation:**
- `quality_reports/data_engineering_environment.md` (Python env lock-protocol; mirrors `software_environment.md`).
- Updates to `quality_reports/osf_preregistration_cdd_formacion_inicial.md` (deposit-files block + checklist + §10 if needed).
- Update to memory `project_cdd_formacion_inicial.md`.
- Append entries to `quality_reports/research_journal.md` and `SESSION_REPORT.md`.

## 5. Verification

The plan is complete when ALL of the following hold:

- [ ] `corpus_inventory.csv` has between 120 and 170 rows (ensures the realized count is in the pre-registered range).
- [ ] Every row has all 7 required columns populated (no NAs in `codigo_ruct`, `sector`, `ccaa`, `modality`, `degree`).
- [ ] Sector distribution: at least one row in each of the 4 sector levels (public, private-traditional, private-online, adscrito).
- [ ] Degree distribution: roughly balanced across Infantil and Primaria (within 70/30 either way).
- [ ] CCAA distribution: at least 15 of the 17 autonomous communities + Ceuta/Melilla represented (some communities may have zero programmes — Cantabria etc.; Ceuta/Melilla likely zero for Maestro grados).
- [ ] `tier_b_sample_ids.csv` has exactly 60 rows.
- [ ] Every row in `tier_b_sample_ids` traces back to a row in `corpus_inventory` via `codigo_ruct`.
- [ ] Min-2-per-active-cell rule satisfied (every active stratum cell has ≥ 2 programmes in sample).
- [ ] Re-running `tier_b_sample.R` from a clean R session reproduces the exact 60 IDs (seed reproducibility).
- [ ] Cross-validation: gradomania's 39 public-uni Primaria programmes are all present in `corpus_inventory.csv`.
- [ ] `coder-critic` score ≥ 80 on the produced scripts.

## 6. Out of scope of this plan

- Layer 1 *memoria* PDF downloads (Stage 1a — separate plan; ~6–8 weeks per OSF PAP §9).
- Layer 2 *guías docentes* HTML/PDF downloads (Stage 1b — separate plan; per-institution scraper modules for the 60 sampled universities only, not all ~67–70 institutions).
- Reliability subsample IDs (C8 — drawn AFTER segment ingestion completes, not now).
- Coding manual freeze (C7 — post-pilot artifact).
- The pilot itself.

## 7. Risks and fallbacks

| Risk | Likelihood | Mitigation |
|---|---|---|
| RUCT session scrape fails (form structure changed, IP blocked, etc.) | Medium | Fall back to cross-validation aggregate (Pass 1 only) as the universe. Log the substitution as a PAP §10 deviation: "RUCT scrape unavailable; universe enumerated from gradomania + educaweb + 8 autonomous-community agencies + ANECA, with manual centros-adscritos override list." Realized count likely undercount by 5–10 programmes (mostly adscritos). |
| ANECA TLS certificate verification fails (per pilot) | High | Use `requests.Session()` with `verify=False` AND log this in the script header so reviewers know the source was verified to be ANECA via URL pattern even if certificate validation was bypassed. (This is acceptable for a public read-only data source where the URL itself is the authority.) |
| Realized universe count materially outside [120, 170] | Low | Log deviation in PAP §10. Re-examine the strategy memo's [ASSUMED] estimate. The Tier B target stays at 60 either way — proportional allocation handles the change. |
| One stratum has 1 programme (impossible to draw 2) | Medium | The strategy memo already specifies: cells with < 2 programmes are oversampled to a minimum of 2 (with the deficit absorbed from the largest cells). The script implements this. If a stratum has exactly 1 programme, n_cell = 1 (cannot exceed the universe). |
| Centros adscritos detection is incomplete | Medium | Combine RUCT's `centro` field with a manual override list seeded from pilot evidence (ESCUNI, Cardenal Cisneros, Cardenal Spínola CEU, La Salle Madrid, Don Bosco, plus discovery during scraping). Document the list in `inventory_reconciliation_log.md`. |
| Rate-limiting / IP blocking during scrape | Low | 1 req/s rate-limit; user-agent identifies the project; respect robots.txt. If blocked, switch to a different source or wait. |
| Bilingual programme naming variation ("Mestre", "Magisterio", "Maestro"...) | High | Normalize via a canonical map: `Mestre|Mestra|Magisterio|Maestro Educación|Maestro de Educación` → unified key. Document in script. |

## 8. Critical files to read before implementing

- `quality_reports/strategy_memo_cdd_formacion_inicial.md` §3 (sampling) and §4 (corpus).
- `quality_reports/strategy/cdd_formacion_inicial/pseudo_code.md` STAGE 0.
- `quality_reports/data_exploration_cdd_formacion_inicial.md` §1, §4 (Flag 5: adscritos), §5 (tooling), §7 (sources by feasibility).
- `quality_reports/osf_preregistration_cdd_formacion_inicial.md` §3 (sampling plan), §6 (reliability protocol → seed).
- `quality_reports/software_environment.md` (R stack — Tier B sample script must comply).
- `.claude/rules/content-invariants.md` (INV-14 set.seed, INV-15 packages-at-top, INV-16 no absolute paths, INV-19 prohibited functions).

## 9. Dispatch and review

1. **Dispatch:** `data-engineer` agent with this plan as its brief. The agent reads the critical files in §8, builds the scripts in §4, runs them, and produces the data artifacts.
2. **Run the scripts:** Pass 1 (cross-validation aggregators) → Pass 2 (RUCT) → Reconciliation → Tier B sample selection. If any pass fails, follow the §7 fallback ladder.
3. **Review:** `coder-critic` evaluates the scripts against the §5 verification list and INV-14/15/16/17/19. Score must be ≥ 80 to commit.
4. **Patch round (if needed):** Up to 3 critic-fix rounds per `agents.md`. Escalate to user if not converged after 3.
5. **Verify:** Run the verification checklist (§5) end-to-end. Compile the inventory CSV and sample CSV; spot-check a handful of rows manually.
6. **PAP + docs update:** Apply the §3.5 updates to PAP, memory, research journal, SESSION_REPORT.
7. **Hand-off:** Tier B sample IDs locked. Phase 2 (per-institution scraper modules for the 60 sampled programmes) becomes the next plan.

## 10. End-of-session deliverables

When this plan executes successfully, the user has:
- A reproducible enumeration of the universe (with reconciliation log so disagreements between sources are documented).
- A locked-in random sample of 60 programmes, drawn from the pre-registered seed, deposited in OSF format.
- Two new OSF checklist items closed (C2, C3+C9).
- A clear path to C8 (reliability subsample) and to per-institution scraping (Stages 1a/1b).
- All artifacts ready for the OSF deposit on the same day if the user wants to submit.
