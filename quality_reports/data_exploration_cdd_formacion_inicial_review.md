# Data Assessment Review — explorer-critic
**Date:** 2026-04-26
**Target:** `quality_reports/data_exploration_cdd_formacion_inicial.md`
**Phase:** Discovery (severity: encouraging-to-constructive — but with named pushback on critical-flag items)
**Score:** 79/100 — **NEEDS REVISION** (one round-2 explorer pass before strategist-critic locks in Tier A vs. B)

---

## Headline verdict

The explorer's report is **substantively strong** on tooling, the per-source feasibility-grade table, the 8 autonomous-community-agency flag, and the VIU counter-example. Recommendation to adopt **Tier A with two operational adjustments** is defensible **in direction**, but the **evidence base for the recommendation is thinner than the report's confident framing implies**. Three issues are genuine blockers for a Tier A lock-in; several others are MAJOR but addressable with one follow-up round.

The explorer should not be sent back to the drawing board — but should not be allowed to hand a Tier A green-light to the strategist either. Round 2: confirm the four likely-yes Layer 1 cases (the explorer's own A.2), confirm at least 2 of the 4 unconfirmed Layer 2 cases, probe at least 2 autonomous-community-agency registries, and reframe the Tier A/B decision around the legitimate pilot uncertainty.

---

## 5-point assessment table (adapted for a document corpus)

| # | Dimension | Severity | Verdict | Deduction |
|---|-----------|----------|---------|-----------|
| 1 | Measurement validity (do these documents code against the MRCDD?) | MAJOR | Partially addressed; depth-of-detail variation across documents not investigated | -8 |
| 2 | Sample selection (pilot of 10 — who's missing?) | CRITICAL | Andalusian, Castilian-León, and Madrid-only-public-uni cells under-sampled; 4 large CCAA absent; bilingual-monolingual-only cell untested | -12 |
| 3 | External validity (if 15% missing, who is missing?) | MAJOR | Asymmetric missingness (online + private + adscritos) is acknowledged but not quantified at the cell level | -5 |
| 4 | Design compatibility (does the corpus support memo-locked design choices?) | MINOR | Two-layer + degree-paired comparison supported; sub-analysis cell sizes unverified | -3 |
| 5 | Known issues from the literature | MAJOR | Cuevas-Monzonís, Sanz-Benito retrieval-rate evidence not consulted; no benchmarking of pilot rates against prior work | -7 |

**Cross-cutting deductions:**

| Issue | Severity | Deduction |
|-------|----------|-----------|
| Confidence framing on pilot N=10 retrieval rates exceeds what the data supports (50% on n=10 has a 95% CI of roughly [19%, 81%]; the report does not report this) | CRITICAL | -10 (no discussion of measurement error / sampling uncertainty) |
| "One scraper per institution × ~67 institutions" effort estimate not provided | MINOR | -2 |

**Items that PASSED (no deduction):**
- Tooling recommendation (`pdfplumber`, `requests`+`BeautifulSoup`, per-institution selectors).
- VIU counter-example to "online = gated" assumption (genuinely useful pushback).
- 8-autonomous-community-agency flag (Flag 2) — real and important addition.
- *Centros adscritos* flag (Flag 5) — correct as a structural finding.
- Per-source feasibility-grade table (§7) — strongest section.
- Bilingual-document flag (Flag 3) — well-handled.

---

## CRITICAL-1 — Pilot N=10 cannot statistically support the Tier A recommendation

The pilot reports **5/10 = 50%** confirmed Layer 2 retrieval and **6/10 = 60%** confirmed Layer 1 retrieval. The Tier A trigger is **≥ 80%**.

The report's resolution: assert that "likely actual after follow-up" is **75–80% (Layer 2)** and **85–90% (Layer 1)** — and on that basis recommend Tier A.

**Two problems:**
1. The "likely-actual" numbers are interpolations, not measurements. Wilson 95% CI on 5/10 ≈ **[24%, 76%]**. The 80% threshold is **outside** this CI on the optimistic side.
2. The conservative-vs-optimistic framing obscures the binary trigger decision. Pilot data **does not resolve** which side of 80% the true rate lies on.

**What round 2 must do:** Either (a) execute A.2 + the four unconfirmed Layer 2 cases, raising N from 10 to ~18, or (b) honestly downgrade the recommendation from "lock in Tier A" to "Tier A is plausible but round-2 evidence required."

---

## CRITICAL-2 — Pilot of 10 systematically under-samples key strata

Stated diversity claim: 4–5 large public + 1–2 private + 1–2 online + 1–2 bilingual. What was sampled:

| Cell | Sampled | Coverage |
|---|---|---|
| Catalonia (public) | UAB, UB | 2/6 = 33% |
| Madrid (public) | UCM | 1/4 = 25% |
| Andalucía (public) | US | 1/8 = 12% |
| Galicia (public) | USC | 1/3 = 33% |
| País Vasco (public) | UPV/EHU | 1/1 = 100% |
| **Castilla y León (public)** | **0/4 = 0%** | **None** |
| **Comunidad Valenciana (public)** | **0/3 = 0%** | **None** |
| All other 9 CCAA (one each) | 0/9 = 0% | None |
| Catalan-only-publishing university (UVic, UdG) | 0 | None — *despite explorer's own Flag 3 noting these are highest-risk* |
| Private non-online (UDIMA, UAX, UCV, UCAV, UPSA) | None | None |
| *Centros adscritos* | ESCUNI only | 1/~15 = 7% |

The pilot covers the **already-best-behaved** institutions. External-validity-to-the-population claim is **non-existent for** 4 large CCAA, *centros adscritos* beyond ESCUNI, traditional private non-online providers, and the highest-risk monolingual-Catalan publishing universities.

---

## MAJOR-3 — Zero autonomous-community-agency registries probed

Flag 2 correctly identifies 8 autonomous-community agencies (AQU, ACSUG, UNIBASQ, AAC-DEVA, ACSUCYL, AQUIB, AVAP, Madri+d) host *memorias* in parallel registries. Source rows for them in §7 graded **B**.

But: **the pilot probed zero of them**. Grade B is asserted on "public; 8 separate portals" — not on actual access tests. AQU Catalunya is the most important to probe (covers UAB, UB, UPC, UPF, URV, UdL, UdG, UVic, UOC). ACSUG covers all 3 Galician public universities.

---

## MAJOR-4 — Programme universe estimate has wide bounds, presented as a point

Honest range: **~135–185 programmes; ~60–80 institutions**. The point estimate of 144 implies precision the inventory does not have. This is the denominator for every retrieval-rate, coverage, and corpus-size calculation downstream.

---

## MAJOR-5 — No benchmarking against published prior inventories

Cuevas-Monzonís et al. (2024, 2025), Sanz-Benito et al. (2024), and Peirats et al. (2018) each had to do their own programme inventory and *guía docente* retrieval. The explorer's report does **not** consult what they reported. If Cuevas-Monzonís 2024 retrieved *guías* for 28 of 39 public-uni Primaria programmes (= 72%), that is a published, real-world retrieval rate at scale. Missed sanity check.

---

## MAJOR-6 — *Centros adscritos* recommendation: structurally correct, operationally infeasible at CCAA-cell level

Flag 5 + Recommendation 4: *centros adscritos* as separate sector cell. Structurally correct. But at full proportional Tier B allocation, *adscrito* cell is ~6 programmes; further stratification by CCAA yields 0–1 programmes per cell. The §8 sub-analysis "≥ 5 programmes per cell" rule cannot be satisfied for the adscrito × CCAA cross.

Recommendation correct at **sector** level; flag that **CCAA-level sub-analysis within the adscrito bucket is infeasible at Tier B**.

---

## Verdict on the explorer's three strategy-memo revisions

| Revision | Verdict |
|---|---|
| (a) "Online providers gated" → revise to provider-specific | **CONCUR.** VIU counter-evidence well-documented. Downgrade memo's `[ASSUMED]` to "online providers vary; UNIR likely gated; VIU public; UCJC unknown." |
| (b) Add 8 autonomous-community-agency registries to memoria sourcing | **CONCUR in direction; INSUFFICIENT in evidence.** Round 2 should test at least AQU and ACSUG before locking. |
| (c) *Centros adscritos* as separate stratification cell | **CONCUR at sector level; QUALIFY at CCAA level.** See MAJOR-6. CCAA × adscrito sub-analysis infeasible at Tier B. |

---

## Tier A / B / C verdict — defer

**The explorer recommends Tier A with two adjustments. I differ: defer the Tier A vs. B decision to a round-2 explorer pass.**

Specifically, the strategist should not lock in Tier A until:
1. A.2 (4 likely-yes Layer 1 cases) executed and reported.
2. 4 unconfirmed Layer 2 cases (US older years, USC, UCJC, ESCUNI per-course detail) probed.
3. At least 2 autonomous-community agencies (AQU, ACSUG) probed for *memoria* hosting.
4. Sampled-strata gap addressed by one probe each in: Castilian-León public, Valencian public, private-non-online (UDIMA or UCV).

This raises pilot from N=10 to N=17–19. Wilson 95% CI then approximately halves in width.

**Decision rule after round 2:**
- ≥ 75% Layer 2 retrieval → **Tier A** defensible.
- 50–75% → **Tier B with adscrito-sensitive stratification**.
- < 50% → **Tier C** on the table (unlikely given pilot evidence).

---

## Feasibility grade for the corpus as a whole

**Grade: B** — operationally feasible with named adjustments and one round-2 explorer pass. Infrastructure exists, access exists, tooling well-specified, but evidence base for the headline retrieval-rate claim is thinner than the report's framing implies.

Not Grade A: N=10 pilot uncertainty + un-probed autonomous-community-agency registries.
Not Grade C: sources are real, accessible, well-mapped at per-source level.

---

## Score breakdown

- Starting: 100
- CRITICAL-1 (no measurement-error discussion): **-10**
- CRITICAL-2 (pilot under-covers strata): **-12**
- MAJOR-3 (zero autonomous-community-agency probes): **-7**
- MAJOR-5 (no benchmarking against published priors): **-3**
- MAJOR-6 / Row-4 (CCAA × adscrito infeasible at Tier B): **-3**
- MINOR-7 (effort estimate missing): **-2**
- Row 1 (depth-of-detail variation across documents not investigated): **-4**
- **Final: 79/100 — NEEDS REVISION**

---

## Strike count

**Strike 1.** First explorer-critic review. Two more rounds available before three-strikes escalation to user.

---

## Files referenced

- `quality_reports/data_exploration_cdd_formacion_inicial.md` (target reviewed)
- `quality_reports/strategy_memo_cdd_formacion_inicial.md` (calibration: §3 Tier triggers, §4 corpus definition)
- `quality_reports/decisions/strategy_cdd_formacion_inicial.md` (calibration: locked-in design choices)
- `.claude/references/domain-profile.md` (calibration: official Spanish data sources)
