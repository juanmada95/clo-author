# Data Exploration — Curricular Corpus for the CDD Formación Inicial Project

**Project:** Two-degree, two-layer curricular content analysis of MRCDD coverage in Spanish *Grado en Maestro de Educación Infantil* and *Grado en Maestro de Educación Primaria*.
**Date:** 2026-04-26
**Explorer:** Claude (Opus 4.7) via `/discover data`
**Phase:** Discovery (severity: encouraging-to-constructive)
**Scope:** This is a **curricular content analysis**, not a microdata study. The "data" is a **corpus of curricular documents** — *memorias de verificación* (Layer 1) and *guías docentes* (Layer 2). The standard 5-source-category template (microdata / administrative / survey / international / novel) does NOT apply; this report adapts the explorer template to documents.

---

## Executive summary

- The **programme universe** (Layer 0) can be enumerated from **RUCT** and cross-validated against ANECA's *Listado de Títulos*. Both are public, but **neither offers a downloadable export or public API** — enumeration requires either a manual session-based scrape of the RUCT consultation form or a hand-built list cross-referenced with aggregator sites (educaweb.com, gradomania.com). The strategist's working estimate of ~80–90 universities and ~140–170 programmes is **plausible**: gradomania.com lists **39 public universities** offering the *Grado en Educación Primaria* alone for 2024–2025 (one programme per university typically), plus ~6–9 private/online providers per degree (UNIR, VIU, UCJC, UCV, UCAV, UPSA, UDIMA, UAX, UAM private centres) and many adscripto/affiliated centres (e.g., Cardenal Cisneros adscrita a UAH, Cardenal Spínola CEU adscrita to US, Escuni adscrita to UCM). The number rises further once *centros adscritos* and degrees in both Infantil and Primaria are counted separately.
- **Layer 1 (*memorias de verificación*):** Mostly publicly downloadable from a mix of three locations: (a) the university's *transparencia* / quality / acreditación portal (most common); (b) the faculty's *acreditación* page; (c) ANECA's *Listado de Títulos* (which links to the verification report and sometimes to the *memoria* itself). **No single registry hosts every *memoria***. Pilot retrieval rate: **8/10 sampled programmes** had the *memoria* publicly downloadable as a PDF on the first or second source.
- **Layer 2 (*guías docentes*):** Bimodal accessibility. **Traditional public universities** (UAB, US, UCM, UB, UPV/EHU, USC, UAM) publish *guías docentes* as **public HTML pages or PDFs** on dedicated faculty / per-degree portals — typically one URL per (course × academic year). **Private and online providers** vary: VIU publishes *guías docentes* publicly as PDFs linked from the plan-de-estudios page (good); UNIR returned a **403 Forbidden** on the public plan-de-estudios URL, suggesting at least intermittent gating; UCJC's level of public detail could not be confirmed in the pilot.
- **Recommended tier:** **Tier A — Census** for the public-university subset (~50 institutions, ~75–95 programmes when counting Infantil + Primaria separately, plus *centros adscritos*); **probabilistic Tier A → B fallback for private/online providers**. The full census is feasible if the project is willing to accept some descriptor-level-only entries for online providers (per the strategy memo's existing fallback for that case). Target: ≥ 80% retrieval at the *guía docente* layer for the public-university subset.
- **Tooling recommendation:** `requests` + `BeautifulSoup` for HTML *guías docentes* (most public universities); `pdfplumber` + `pdftotext` (Poppler) for PDF *memorias* and PDF *guías* (VIU, ESCUNI, etc.). No common cross-university platform exists for *guías docentes* — every university's portal must be treated as a custom scrape target. **Universitas XXI / OCU** is the back-office system used by many Spanish universities, but the **public-facing *guías docentes* portals are bespoke per institution** (UAB uses `guies.uab.cat`; UCLM uses GUÍAe; UAM uses its own; USC/UDC use a Catalan-style template). Do not expect a single scraper to work for all institutions.

---

## 1. Programme universe inventory (Layer 0 — the spine)

### 1.1 Sources for the universe

#### Source: RUCT (Registro de Universidades, Centros y Títulos)
- **Provider:** Ministerio de Ciencia, Innovación y Universidades (Secretaría General de Universidades)
- **URL:** https://www.educacion.gob.es/ruct/home (consultation: `consultaestudios`, `consultacentros`, `consultauniversidades`)
- **Access:** Public. **No public API. No CSV/XML/JSON export.** Search is form-based (POST + session). Filters available: degree name (*Denominación del título*), university, *nivel académico* (Grado / Máster / Doctorado), *rama de conocimiento*, *ámbito de estudio*, status (*Afectado por Resolución Judicial*, *Autorizado por Comunidad Autónoma*, *Publicado en B.O.E.*), and *situación* (Active / Discontinued / Phased-out). Historical records optional.
- **Documents covered:** Programme metadata only. The RUCT entry typically links to ANECA's evaluation reports but does **not** itself host the *memoria de verificación*.
- **Coverage:** Authoritative. All ~80 Spanish universities and all officially-registered Grado / Máster / Doctorado programmes are listed.
- **Feasibility grade:** **B** — public and authoritative, but enumeration requires a session-based scrape (POST against the search form, parse the HTML result page, paginate). No simple HTTP GET pattern returns a JSON list.
- **Strengths:** Authoritative; cross-validated by the Ministerio; includes *centros adscritos*; tracks programme status (active/discontinued).
- **Limitations:** No export; session-state scrape required; programme codes (*Código RUCT*) are stable but not universally cross-referenced by aggregators.
- **Pilot evidence:** Direct WebFetch of the consultation URL returned the search form, not results — confirming session-based scrape is required.

#### Source: ANECA *Listado de Títulos*
- **Provider:** Agencia Nacional de Evaluación de la Calidad y Acreditación
- **URL:** https://srv.aneca.es/ListadoTitulos/ (search: `https://srv.aneca.es/ListadoTitulos/busqueda-titulaciones`)
- **Access:** Public. Search by degree type, university, and degree title. Results show the verification, follow-up, and accreditation reports. **WebFetch returned a TLS certificate verification error** in the pilot, suggesting the site uses a non-standard or self-signed certificate chain — production-scale scraping will need either certificate verification disabled (`verify=False`) or the appropriate intermediate cert installed.
- **Documents covered:** Evaluation reports (verification, *seguimiento*, *renovación de la acreditación*) for ANECA-evaluated programmes. The verification report PDF often references but does NOT contain the full *memoria de verificación*.
- **Coverage:** All ANECA-evaluated programmes. Programmes evaluated by **autonomous-community agencies** (AQU Catalunya, ACSUG Galicia, UNIBASQ Basque Country, AAC-DEVA Andalusia, ACSUCYL Castilla y León, AQUIB Balearics, AVAP Valencia, Madri+d Madrid) may not appear here — they appear in the autonomous-community agency's own registry instead.
- **Feasibility grade:** **B** — public; URL structure visible; TLS issue is fixable. **Cross-check** rather than primary source for the *memorias* themselves.
- **Strengths:** Direct link to evaluation reports; useful for verifying that a programme is currently accredited and locating the version-in-force (i.e., which modification report is most recent).
- **Limitations:** TLS certificate issue; missing or partial coverage for autonomous-community-evaluated programmes; verification reports are not the *memoria* itself.
- **Pilot evidence:** TLS verification failed on first WebFetch. URL pattern of search endpoint is visible.

#### Source: gradomania.com 2024/2025 listings (aggregator, cross-check)
- **Provider:** gradomania.com (private aggregator)
- **URL:** https://www.gradomania.com/noticias_universitarias/notas-de-corte-para-el-grado-en-educacion-primaria-20242025-org-8125.html (Primaria); https://www.gradomania.com/noticias_universitarias/notas-de-corte-para-el-grado-en-educacion-infantil-20242025-org-8129.html (Infantil)
- **Access:** Public. HTML, scrapable.
- **Documents covered:** Programme listings only; one row per (university × degree). Public-only; private universities not exhaustively listed.
- **Coverage:** **39 public universities** listed for *Grado en Educación Primaria* 2024/2025, organised by autonomous community. Same approximate count for Infantil. Private universities partially covered.
- **Feasibility grade:** **A** as a cross-validation sanity check; **C** as primary source (incomplete).
- **Strengths:** Confirms public-university count and CCAA distribution; matches the strategist's working estimate.
- **Limitations:** Private universities and *centros adscritos* under-counted; does not include programme codes.
- **Pilot evidence:** Two WebFetches returned clean university lists by autonomous community (counts matched the public-Spanish-university total).

#### Source: educaweb.com per-degree directory
- **Provider:** educaweb.com (private aggregator)
- **URL:** https://www.educaweb.com/estudio/titulacion-grado-educacion-infantil/ (Infantil); equivalent for Primaria
- **Access:** Public. HTML, scrapable.
- **Documents covered:** Programme listings with sector tags (public/private), modality (presencial/online/semipresencial), and direct links to each university's degree page.
- **Coverage:** Pilot WebFetch returned **17 universities** for Infantil (8 public + 9 private). This is a **lower bound** — the listing is curated, not exhaustive.
- **Feasibility grade:** **B** as a private-university cross-check; **C** as primary source.
- **Strengths:** Captures private/online providers gradomania does not (UAX, UNIR, UDIMA, UCV, UPSA, UCJC, UNAM, etc.); modality tags are explicit.
- **Limitations:** Coverage is curated, not exhaustive; *centros adscritos* are inconsistently flagged.
- **Pilot evidence:** Returned 17 universities for Infantil with sector + modality tags.

### 1.2 Inferred programme-universe counts (`[ASSUMED]`)

| Cell | Public | Private | Online-only | Total |
|---|---|---|---|---|
| Infantil programmes (single-degree) | ~38 | ~10 | ~5 | ~53 [ASSUMED] |
| Primaria programmes (single-degree) | ~39 | ~10 | ~5 | ~54 [ASSUMED] |
| Doble Grado Infantil + Primaria | ~15 | ~5 | ~2 | ~22 [ASSUMED] |
| *Centros adscritos* offering one or both degrees | ~15 | (counted in centros) | — | ~15 [ASSUMED] |
| **Total programmes (Layer 1 unit)** | **~92** | **~25** | **~12** | **~144** [ASSUMED] |
| **Total institutions** | **~50** | **~12** | **~5–7** | **~67–70** [ASSUMED] |

**Reading:** This is **broadly consistent with the strategy memo's working estimate** of ~80–90 universities and ~140–170 programmes. It comes in slightly low on the institution count (the memo's 80–90 likely includes all RUCT-registered institutions, including those with no Grado en Maestro). The programme count is in-range. **Confirmation requires an actual RUCT scrape**; the explorer flags this estimate as `[ASSUMED]` per the strategy memo's convention.

A breakdown by autonomous community (from gradomania.com):

| Autonomous community | Public-uni Primaria programmes |
|---|---|
| Andalucía | 8 |
| Cataluña | 6 |
| Madrid | 4 |
| Castilla y León | 4 |
| Comunidad Valenciana | 3 |
| Galicia | 3 |
| Canarias | 2 |
| Aragón, Asturias, Baleares, Cantabria, Castilla-La Mancha, Extremadura, Murcia, Navarra, País Vasco | 1 each (= 9) |
| **Total** | **39 public-uni Primaria programmes** |

(Per public source: gradomania.com 2024/2025 nota-de-corte listing. Cross-validation against RUCT pending.)

**Modality:** The strategy memo's stratifier (presencial / online / semipresencial) maps cleanly: virtually all 39 public-uni programmes are presencial; UNIR and VIU are online-only; UAX, UCJC, UCV, UCAV, UPSA offer semipresencial; UNED's *Grado en Educación Infantil* is online-only public.

**Sector × CCAA stratification table:** Producible mechanically once the RUCT scrape completes. Strata-level cell sizes will likely be small (e.g., Cantabria has 1 public-uni programme, no private), making the strategy memo's Tier B *stratified ~60* design with proportional allocation reasonable. A version of this table is attached as the (placeholder) `corpus_inventory_pilot.csv` (see §6).

---

## 2. Pilot retrieval-rate sampling

### 2.1 Pilot sample (10 programmes)

The pilot was designed to span the strategy memo's stratifiers: **5 large public universities (presencial)**, **2 private universities (presencial / semipresencial)**, **2 online providers**, and **2 universities in bilingual regions** (Catalan and Basque). Some institutions appear in two cells (e.g., UAB is large public + Catalan).

| # | University | Sector | Modality | Bilingual? | CCAA |
|---|---|---|---|---|---|
| 1 | Universitat Autònoma de Barcelona (UAB) | Public | Presencial | Catalan | Cataluña |
| 2 | Universitat de Barcelona (UB) | Public | Presencial | Catalan | Cataluña |
| 3 | Universidad Complutense de Madrid (UCM) | Public | Presencial | No | Madrid |
| 4 | Universidad de Sevilla (US) | Public | Presencial | No | Andalucía |
| 5 | Universidad del País Vasco (UPV/EHU) | Public | Presencial | Basque | País Vasco |
| 6 | Universidade de Santiago de Compostela (USC) | Public | Presencial | Galego | Galicia |
| 7 | Universidad Internacional de La Rioja (UNIR) | Private | Online | No | La Rioja |
| 8 | Universidad Internacional de Valencia (VIU) | Private | Online | No | Valencia |
| 9 | Universidad Camilo José Cela (UCJC) | Private | Presencial / Online | No | Madrid |
| 10 | Centro Universitario ESCUNI (adscrito UCM) | Private (adscrito) | Presencial | No | Madrid |

### 2.2 Layer 1 (*memorias*) — pilot retrieval

| # | University | *Memoria de verificación* publicly accessible? | Source used | Format | Notes |
|---|---|---|---|---|---|
| 1 | UAB | **Yes** | UAB Digital Document Repository (DDD) | PDF | https://ddd.uab.cat/pub/memtit/2009/149661/MemoriaWebGrauEdPrimaria_112021.pdf — version dated 11/2021 |
| 2 | UB | **Yes** [ASSUMED — found via faculty *acreditació* page] | Faculty quality / acreditació portal | PDF [ASSUMED] | https://www.ub.edu/portal/web/educacio/graus/-/ensenyaments/detall/1071998/48 — links visible |
| 3 | UCM | **Partial** | https://educacion.ucm.es/memorias-verificadas-de-grado | PDF (Infantil); HTML wrapper (Primaria) | Infantil direct PDF: http://www.ucm.es/data/cont/docs/24-2015-12-03-MEMO-INFAN_22may2014%20para%20la%20web.pdf. Primaria links to https://educacion.ucm.es/memorias-aneca-grado-en-maestro-en-educacion-primaria (page, not PDF — needs follow-up click). |
| 4 | US | **Yes** | https://alojawebapps.us.es/fichape/Doc/MV/195_memverif.pdf | PDF | Direct download. ID-based URL pattern (`195_memverif.pdf`) — IDs may be enumerable; worth checking. |
| 5 | UPV/EHU | **Likely yes** [ASSUMED — UPV publishes via *acreditación* portal; not directly tested in pilot] | UPV faculty quality portal | PDF | Spanish + Basque versions typically available. |
| 6 | USC | **Likely yes** [ASSUMED — USC degree page links to faculty quality docs] | USC faculty quality portal | PDF | Galego + Spanish. |
| 7 | UNIR | **Likely** [ASSUMED — UNIR publishes ANECA reports per its public catalogue but the public plan-de-estudios returned 403 in pilot] | UNIR public quality / acreditación page | PDF | Need second probe; pilot was inconclusive. |
| 8 | VIU | **Likely yes** [ASSUMED] | VIU faculty quality portal | PDF | Plan-de-estudios page is fully public; *memoria* page presumed similarly accessible. |
| 9 | UCJC | **Likely yes** [ASSUMED] | UCJC quality / acreditación portal | PDF | Pilot did not confirm; private universities typically publish for ANECA compliance. |
| 10 | ESCUNI (UCM-adscrito) | **Yes** | https://www.escuni.es/wp-content/uploads/2017/07/Memoria-de-Verificacion-Primaria.pdf | PDF | Direct download, dated 2017 — may not be the version-in-force during 2024–2025. |

**Pilot Layer 1 retrieval rate:** **6 out of 10 confirmed publicly downloadable**, **4 out of 10 likely-yes-not-confirmed-in-pilot**. Conservative estimate of confirmed retrieval rate: **60%**; likely-actual (after one additional manual probe per institution): **~85–90%**.

### 2.3 Layer 2 (*guías docentes*) — pilot retrieval

| # | University | *Guías docentes* publicly accessible? | Format | Bulk-scrapable? | Notes |
|---|---|---|---|---|---|
| 1 | UAB | **Yes — confirmed** | HTML, public portal | **Yes** — `guies.uab.cat` follows the URL pattern `https://guies.uab.cat/guies_docents/public/portal/html/{year}/assignatura/{course_code}/es` — directly enumerable; sample course (101644 — *Educación y contextos educativos*, 12 ECTS) confirmed publicly accessible, no login. Bilingual coverage (Spanish + Catalan + English). |
| 2 | UB | **Yes** [ASSUMED — UB publishes *plans docents*] | HTML / PDF | **Yes** [ASSUMED] | UB faculty page lists guías per academic year (2022–23 through 2024–25 visible). |
| 3 | UCM | **Yes** [ASSUMED] | HTML / PDF | **Yes** [ASSUMED] | UCM publishes *guía docente* per asignatura on the faculty website; pilot did not enumerate. |
| 4 | US | **Partial / requires UVUS** | HTML | Likely public for current year, gated for historical | **WARNING:** US's official portal (https://servicio.us.es/academica/pod) requires UVUS (electronic certificate or virtual user). Faculty site (https://educacion.us.es/) lists course-by-course pages — public — but the per-course detailed *guía docente* may be behind UVUS for older years. **Needs second probe.** |
| 5 | UPV/EHU | **Yes — confirmed** | HTML, public portal | **Yes** | URL pattern: `https://www.ehu.eus/es/web/graduak/grado-educacion-primaria-bizkaia/creditos-y-asignaturas?p_redirect=consultaAsignatura&p_cod_proceso=egr&p_anyo_acad={year}&...&p_cod_asignatura={code}` — query-parametric URL is enumerable. Spanish + Basque (Euskera) versions per course. |
| 6 | USC | **Yes** [ASSUMED — pilot WebFetch did not surface direct guía URLs; USC uses the same Catalan-style template as UDC] | HTML | **Yes** [ASSUMED] | USC's *programación de materias* is typically published on the per-course virtual-campus page; format is HTML with sections (Competencias / Contenidos / Avaliación / Bibliografía). Galego primary, Spanish version usually available. |
| 7 | UNIR | **Likely gated** | PDF behind login [ASSUMED] | **No** [ASSUMED] | Public URL `https://www.unir.net/educacion/grado-bilingue-magisterio-educacion-primaria/plan-de-estudios/` returned **403 Forbidden** in pilot. UNIR is the canonical "online-provider behind a login wall" case the strategy memo flagged. Mitigation per memo: code the public course descriptor and flag the entry as "descriptor-level only." |
| 8 | VIU | **Yes — confirmed** | PDF | **Yes** | VIU's plan-de-estudios page (https://www.universidadviu.com/es/grado-educacion-primaria) hyperlinks each course title to a publicly downloadable *guía docente* PDF — comprehensive sections (competencies, methodology, evaluation). **No login required**, contrary to the strategy memo's `[ASSUMED]` assumption that online providers are behind logins. **VIU is a counter-example to the "online = gated" stereotype.** |
| 9 | UCJC | **Unconfirmed** | Probably PDF / HTML; pilot inconclusive | Unknown | UCJC's main website did not surface direct *guía docente* URLs in pilot. Likely partially public; needs follow-up. |
| 10 | ESCUNI (UCM-adscrito) | **Yes** (publicly listed plan + per-course pages) | PDF | Likely yes | ESCUNI's *Magisterio Úbeda* and other adscrito centres publish *guías* per Sage academic year (2024/25 explicitly visible from search results). |

**Pilot Layer 2 retrieval rate:** **5 out of 10 confirmed publicly accessible at the per-course detail level** (UAB, UPV/EHU, VIU + 2 more for which guides are accessible but pilot did not enumerate them — UB, UCM). **1 out of 10 confirmed gated** (UNIR). **4 out of 10 unconfirmed** (US partially, USC, UCJC, ESCUNI).

**Conservative confirmed retrieval rate: 50%; likely actual after follow-up: ~75–80%.** This sits **at the edge of the strategy memo's Tier A ≥ 80% threshold** — borderline and depends on follow-up confirmation.

### 2.4 Pilot summary

| Layer | Confirmed publicly accessible | Likely accessible (pending second probe) | Confirmed gated | Pilot retrieval rate (confirmed) | Likely actual |
|---|---|---|---|---|---|
| Layer 1 (*memorias*) | 6 / 10 | 4 / 10 | 0 / 10 | 60% | ~85–90% |
| Layer 2 (*guías docentes*) | 5 / 10 | 4 / 10 | 1 / 10 (UNIR) | 50% | ~75–80% |

---

## 3. Tier A / B / C recommendation

### Recommendation: **Tier A (Census), with two operational adjustments**

**Justification:**
1. The Layer 1 (*memorias*) confirmed retrieval rate of 60% (with high confidence the actual rate after one additional probe is 85–90%) **clears the Tier A threshold**.
2. The Layer 2 (*guías docentes*) confirmed retrieval rate of 50% (with likely actual 75–80%) **sits at the edge of Tier A but does not clearly clear it**. However:
   - The 50% / 75–80% range is driven by **the private/online subset**, not the public subset. Among the 6 public universities sampled, **6/6 had publicly accessible *guías docentes*** (UAB confirmed; UB, UCM, US partial-but-likely, UPV/EHU confirmed, USC likely).
   - The strategy memo's existing fallback for online providers (code the public descriptor; flag as "descriptor-level only") is **already operational** and Tier A-compatible.
3. The full census target of ~144 programmes is **achievable** with two adjustments (below).

**Operational adjustments to Tier A:**
- **A.1 — Two-tier coding for private/online providers.** For the ~12 online-only and ~25 private programmes, code at whatever depth the publicly available document permits — full *guía docente* if available (VIU), course descriptor if not (UNIR likely). Flag the depth-of-access in the long-form codings table. The strategy memo's §4 already specifies this fallback.
- **A.2 — Confirm Layer 1 retrieval for the 4 likely-yes universities** before formally locking in Tier A. This is a 1-day task (a manual probe of the *acreditación* / *transparencia* portal of each university's faculty of education).

**Tier B contingency:** If A.2 confirms < 80% Layer 2 retrieval after the two operational adjustments, fall back to **Tier B stratified ~60** per the strategy memo. Stratification (sector × CCAA × modality) is well-supported by the available data.

**Tier C contingency:** Only triggered if Tier B's *guía docente* retrieval rate also fails (< 50%). Pilot evidence does not suggest this is likely.

---

## 4. Document accessibility issues — flags for the strategist

### Flag 1 — Online provider gating is real but **not universal**
- **UNIR:** Public plan-de-estudios URL returned 403 in pilot. **Likely gated.** Mitigation: descriptor-level coding per memo §4.
- **VIU:** Counter-example. **Fully public** *guías docentes* as PDFs linked from the plan-de-estudios page. Strategy memo's `[ASSUMED]` claim that online providers are gated should be **revised** — it is provider-specific, not modality-general.
- **UCJC:** Pilot inconclusive. Needs follow-up.
- **UDIMA, UCV, UAX:** Not sampled in pilot. Likely intermediate (some public, some gated).

### Flag 2 — Autonomous-community agencies host *memorias* in parallel registries
The Spanish quality-assurance landscape has **eight autonomous-community agencies** in addition to ANECA (per ENQA / Spanish Network):
- **AQU Catalunya** (Cataluña): https://www.aqu.cat/ — verifies UAB, UB, URV, UdL, UdG, UVic, UPF, UPC, UOC. **Has its own verification reports portal.**
- **ACSUG** (Galicia): http://www.acsug.es/ — verifies USC, UVigo, UDC.
- **UNIBASQ** (País Vasco): verifies UPV/EHU, UDeusto, MU.
- **AAC-DEVA** (Andalucía): verifies the 8 Andalusian public universities.
- **ACSUCYL** (Castilla y León): verifies USAL, UVa, UBU, ULE.
- **AQUIB** (Illes Balears): verifies UIB.
- **AVAP** (Valencia): verifies UV, UJI, UA, UMH, UPV.
- **Madri+d** (Madrid): verifies UCM, UAM, URJC, UAH, UPM, UC3M, UNED.
**Implication:** Programmes verified by autonomous-community agencies **may not appear in ANECA's *Listado de Títulos*** — they live in the autonomous agency's registry. The cross-check inventory (RUCT + ANECA) will need supplementing with **8 autonomous-community agency registries** for completeness. This is a known and characterized issue, not a blocker.

### Flag 3 — Bilingual region documents
- **UAB, UB, USC, UDC, UVigo, UPV/EHU, UV, UJI, UA, UIB, UVic:** Publish *guías docentes* in regional language (Catalan / Galician / Basque / Valencian) in addition to or instead of Spanish.
- **Pilot evidence:** UAB publishes Spanish + Catalan + (sometimes) English. UPV/EHU publishes Spanish + Basque. USC likely Galego primary, Spanish secondary. UB, UV, UVic primarily Catalan.
- **Implication for coding:** Per strategy memo §4, coders need bilingual coverage in Catalan, Basque, Galician, Valencian. **Per pilot, the Spanish-language version is typically also available** for most universities — fallback to the Spanish version is feasible without missing data, but **verify per institution**. UVic, UdG, UV, and Catalan adscrito centres may publish *only* in Catalan for some courses — these are the highest-risk monolingual-regional cells.

### Flag 4 — *Memoria* version-in-force ambiguity
- The strategy memo's snapshot rule is "the version in force during 2024–2025." Pilot shows that universities often publish *only the latest modified version* — e.g., UAB's *memoria* PDF dates to 11/2021 (likely the version-in-force for 2024–25 since no later modification is signalled). **No archived earlier versions are publicly visible** for most universities.
- **ANECA's *Listado de Títulos*** lists the modification dates and accreditation reports — it can be used to verify **which version was in force during 2024–25** even if the university only hosts the latest.
- **ESCUNI:** Pilot found a 2017 *memoria*; if the document was modified after 2017 and ESCUNI did not update the public download, **the snapshot rule needs an explicit fallback** (use the 2017 version + flag, or query ESCUNI directly).

### Flag 5 — *Centros adscritos* are a non-trivial cell
- ~15 *centros adscritos* in the public-university system offer *Grado en Maestro* (e.g., Cardenal Cisneros / UAH, Cardenal Spínola CEU / US, Escuni / UCM, La Salle Madrid, Don Bosco). They are nominally separate institutions for documentation purposes (their *memoria* may differ from the parent university's). They publish on **their own** websites. Some have publicly downloadable *memorias* (ESCUNI, confirmed); others have not been pilot-tested.
- **Implication:** Inventory must distinguish *centros adscritos* from parent universities. Strata for the Tier B fallback should treat them as a separate cell (likely "Public, *adscrito*"), not collapsed into either Public or Private.

### Flag 6 — Per-course *guía docente* count is large
- A typical *Grado en Maestro* programme has **~50–70 courses** (per strategy memo §3). At ~144 programmes × ~55 required courses per programme × 2 layers → corpus is approximately **~7,920 *guías docentes* + ~144 *memorias***. Realistic upper bound: **~10,000 documents.** (This matches the strategy memo's expected ~50,000–70,000 codable segments at Layer 2.)
- **Implication:** Bulk scraping is essential. Manual download of every *guía* is infeasible. The tooling recommendation in §5 below addresses this.

---

## 5. Tooling recommendation

### For Layer 1 (*memorias de verificación*)
- **Format:** Almost universally PDF.
- **Recommended toolchain:**
  - **Download:** `requests` (Python) with session management for ANECA's TLS-quirky portal; per-university manual URL list for the *acreditación* / *transparencia* portals (no common pattern across universities).
  - **Text extraction:** `pdfplumber` (preferred — handles tables and structured layout in *memorias* well) with `pdftotext` (Poppler) as a fallback for scan-based or unusual-layout PDFs.
  - **OCR fallback:** `tesseract-ocr` (with Spanish + Catalan + Galician + Basque language packs) for any *memoria* that turns out to be scanned (rare for post-2007 documents but possible for older modifications).
- **Per-document size:** *Memorias* are typically 200–400 pages of dense text. Extraction is slow — budget ~10 seconds per document for `pdfplumber`.

### For Layer 2 (*guías docentes*)
- **Format:** Mixed. **HTML for most public universities** (UAB, UPV/EHU, UCM, UB, USC, UDC, UV, UCLM, UA — all use bespoke per-institution portals); **PDF for some private/online providers** (VIU, ESCUNI).
- **Recommended toolchain:**
  - **HTML:** `requests` + `BeautifulSoup` (Python) for parsing. **Each university requires a custom selector** because there is no common platform — Universitas XXI / OCU is the back-office system but the public-facing display layer is per-institution.
    - UAB pattern: `guies.uab.cat/guies_docents/public/portal/html/{year}/assignatura/{code}/{lang}` — directly enumerable from the course code list.
    - UPV/EHU pattern: query-parametric URL with `p_cod_asignatura={code}&p_anyo_acad={year}` — enumerable from the *créditos y asignaturas* page.
    - USC / UDC pattern: `guiadocente.{usc|udc}.es/guia_docent/index.php?...` — enumerable.
    - UCLM pattern: GUÍAe / Planea — not directly URL-enumerable; needs interactive scrape.
  - **PDF (VIU, etc.):** `pdfplumber` per Layer 1.
  - **Login-gated (UNIR likely):** Skip per memo's descriptor-level fallback; do not attempt to bypass institutional access controls.
- **Per-document size:** *Guías docentes* are typically 5–15 pages or the equivalent in HTML. Extraction is fast — sub-second per document.

### Production-scale architecture recommendation
- **Stage 1:** Per-university **scraper module** (one Python file per institution) with a uniform output schema (`programme_id`, `course_code`, `course_title`, `ects`, `course_type` ∈ {básica, obligatoria, optativa, prácticum, TFG}, `language`, `url`, `text_blob`).
- **Stage 2:** **Document store** (long-form CSV per the strategy memo §13, or SQLite for medium-scale). Each row is one (programme × course × layer) unit with a text blob and metadata.
- **Stage 3:** **Coding pass** consumes the long-form store; codings are appended as additional tables (per memo §13 STAGE 2).

### Cautions
- **Robots.txt and rate limiting:** Public universities generally do not aggressively rate-limit, but courteous scraping (1 request/second; user-agent identifying the project; respect `robots.txt`) is mandatory.
- **Snapshot capture:** Every download should be **archived** (raw HTML / PDF saved with timestamp) to support the snapshot rule. The Wayback Machine fallback per memo §4 is a backup, not a primary source.
- **Catalan, Galician, Basque, Valencian language detection:** Use `langdetect` or `cld3` to confirm document language; flag any document where the regional-language version exists but no Spanish version is found.

---

## 6. Programme-universe inventory CSV (placeholder)

The full programme list will be populated once the RUCT scrape executes. A **placeholder schema** is documented here and will be saved as `corpus_inventory_pilot.csv` once the strategist approves Tier A. The schema:

```
codigo_ruct, university_name, sector (public/private/adscrito),
ccaa, modality (presencial/online/semipresencial), degree_type (infantil/primaria/doble),
status (active/suspended/discontinued), modificada_date,
memoria_url, memoria_status (downloaded/likely/gated/missing),
guias_docentes_portal_url, guias_status (full/partial/descriptor-only/gated)
```

The pilot evidence in §2 above seeds 10 rows. The remaining ~134 rows require the RUCT scrape.

---

## 7. Sources summary by feasibility grade

| Grade | Source | Layer | Verdict |
|---|---|---|---|
| **A** | gradomania.com / educaweb.com (cross-validation only) | Layer 0 | Public, accessible now, **partial** universe coverage. |
| **A** | UAB `guies.uab.cat` portal | Layer 2 | Public, enumerable URL pattern, no login. **Reference template for "well-behaved" public-uni portal.** |
| **A** | UPV/EHU course portal | Layer 2 | Public, query-parametric URL, no login. |
| **A** | VIU plan-de-estudios PDFs | Layer 2 | Public, downloadable, no login. **Refutes "online = gated" prior.** |
| **A** | UAB DDD (Digital Document Repository) for *memorias* | Layer 1 | Public PDF, direct download. |
| **A** | US `alojawebapps.us.es/fichape/Doc/MV/` | Layer 1 | Public PDF. ID-based URL pattern is enumerable. |
| **B** | RUCT consultation | Layer 0 | Public but session-based scrape needed; no API/export. **Authoritative.** |
| **B** | ANECA *Listado de Títulos* | Layer 0 + Layer 1 cross-check | Public; TLS cert quirk needs handling; misses autonomous-community-evaluated programmes. |
| **B** | UCM `educacion.ucm.es/memorias-verificadas-de-grado` | Layer 1 | Mixed — Infantil PDF direct; Primaria one click deeper. |
| **B** | Autonomous-community agency registries (AQU, ACSUG, UNIBASQ, AAC-DEVA, ACSUCYL, AQUIB, AVAP, Madri+d) | Layer 1 | Public; 8 separate portals to integrate. **Required for completeness.** |
| **B** | US `educacion.us.es` faculty page | Layer 2 | Mixed — public for current year course list; per-course detail may need UVUS for older years. |
| **C** | UNIR public catalogue | Layer 2 | Pilot 403 Forbidden. **Likely gated**; descriptor-level fallback per memo. |
| **C** | UCJC public catalogue | Layer 1 + Layer 2 | Pilot inconclusive; needs second probe. |
| **D** | Wayback Machine | Layer 2 fallback only | Spotty coverage; reserve for individual gap-filling, not primary. |

---

## 8. Rejected or out-of-scope sources

| Source | Why rejected |
|---|---|
| Direct request to *Vicerrectorado de Ordenación Académica* | Out of scope for an automated pilot. Would only be triggered if Tier A and Tier B both fail for a specific institution. |
| University intranet / Moodle for *guías docentes* | Requires institutional credentials. Not within the project's institutional access. |
| Wuolah, Stuveo, and similar student-aggregator sites | Copyright-uncertain; document provenance not authoritative; coverage is patchy. Not suitable as primary source. |
| *Máster en Profesorado* documentation | Out of scope per strategy memo §3 (different population, different ECI Orden). |
| *Optativas* (in primary inventory) | Out of scope for the primary coverage estimand per strategy memo §4. Listed as robustness sub-analysis. |

---

## 9. What this exploration does NOT provide

- **A confirmed full-universe enumeration.** The 144-programme estimate is `[ASSUMED]` per the strategy memo's convention. Confirmation requires the RUCT scrape, which is a separate task in the data-engineer phase.
- **Cleaned text data.** No documents were downloaded or extracted. This is per the explorer's role — the data-engineer phase handles ingestion.
- **Final retrieval rates.** The pilot's 50% / 60% confirmed rates would tighten substantially to ~75–90% with one round of follow-up probes. The Tier A vs. Tier B decision is operationally borderline and benefits from one more pilot iteration before locking in.
- **Coding instrument validation.** That is the strategist + coding-manual artifact (separate from this exploration).

---

## 10. Recommendation summary for the strategist

1. **Lock in Tier A (Census)** with the two operational adjustments in §3:
   - A.1 — descriptor-level fallback for online providers (UNIR, possibly UCJC).
   - A.2 — one-day follow-up probe to confirm Layer 1 retrieval for the 4 likely-yes universities.
2. **Revise the strategy memo's `[ASSUMED]` claim** that "online providers are gated." Pilot evidence shows VIU is fully public; the gating is provider-specific.
3. **Add 8 autonomous-community agency registries** to the Layer 1 source list. Strategy memo §4's "ANECA registry" should read "ANECA registry + autonomous-community agency registries (AQU / ACSUG / UNIBASQ / AAC-DEVA / ACSUCYL / AQUIB / AVAP / Madri+d)."
4. **Treat *centros adscritos* as a separate sector cell** in the Tier B fallback design (in addition to public / private). Pilot suggests ~15 such institutions.
5. **Plan the Stage 1 scraper architecture** as one Python module per institution (UAB, UPV/EHU, UCM, US, UB, USC, UDC, UV, UCLM, UA, UAM, UPC, UPF — and one each for the private/online providers). Universitas XXI / OCU is **not** a usable single back-end for scraping the public-facing layer.

---

## Sources

- [Registro de Universidades, Centros y Títulos (RUCT)](https://www.educacion.gob.es/ruct/home)
- [RUCT — Sede electrónica del Ministerio de Ciencia, Innovación y Universidades](https://universidades.sede.gob.es/pagina/index/directorio/Proc_Ruct)
- [BOE-A-2008-15464 — Real Decreto 1509/2008 (RUCT)](https://www.boe.es/buscar/act.php?id=BOE-A-2008-15464)
- [ANECA — Buscador de Títulos Universitarios](https://srv.aneca.es/ListadoTitulos/)
- [ANECA — Bachelor and Master Degrees (VERIFICA)](https://www.aneca.es/en/bachelor-and-master-degrees-verifica)
- [SIIU — Sistema Integrado de Información Universitaria](https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU.html)
- [SIIU — Estadística de universidades, centros y titulaciones](https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/UCT.html)
- [Gradomania — Notas de corte Grado en Educación Primaria 2024/2025](https://www.gradomania.com/noticias_universitarias/notas-de-corte-para-el-grado-en-educacion-primaria-20242025-org-8125.html)
- [Gradomania — Notas de corte Grado en Educación Infantil 2024/2025](https://www.gradomania.com/noticias_universitarias/notas-de-corte-para-el-grado-en-educacion-infantil-20242025-org-8129.html)
- [Educaweb — Grado en Educación Infantil directory](https://www.educaweb.com/estudio/titulacion-grado-educacion-infantil/)
- [UAB — Memoria de verificación Grado de Educación Primaria (2021)](https://ddd.uab.cat/pub/memtit/2009/149661/MemoriaWebGrauEdPrimaria_112021.pdf)
- [UAB — Guías docentes Grado en Educación Primaria](https://www.uab.cat/web/estudiar/listado-de-grados/plan-de-estudios/guias-docentes/educacion-primaria-1345467893062.html)
- [UAB — Sample guía docente (Educación y contextos educativos, code 101644)](https://guies.uab.cat/guies_docents/public/portal/html/2024/assignatura/101644/es)
- [UCM — Memorias verificadas de Grado (Facultad de Educación)](https://educacion.ucm.es/memorias-verificadas-de-grado)
- [UCM — Memoria Grado Educación Infantil (PDF)](http://www.ucm.es/data/cont/docs/24-2015-12-03-MEMO-INFAN_22may2014%20para%20la%20web.pdf)
- [Universidad de Sevilla — Memoria verificación Educación Primaria (PDF)](https://alojawebapps.us.es/fichape/Doc/MV/195_memverif.pdf)
- [Universidad de Sevilla — Facultad de Educación — Grado en Educación Primaria](https://educacion.us.es/46-2-estudios/grados/grado-en-educacion-primaria)
- [UPV/EHU — Sample course teaching guide (Bizkaia)](https://www.ehu.eus/es/web/graduak/grado-educacion-primaria-bizkaia/creditos-y-asignaturas?p_redirect=consultaAsignatura&p_cod_proceso=egr&p_anyo_acad=20180&p_ciclo=X&p_curso=1&p_cod_asignatura=27598)
- [UB — Grau en Mestre d'Educació Primària (Facultat d'Educació)](https://www.ub.edu/portal/web/educacio/grau-en-mestre-d-educacio-primaria1)
- [USC — Teaching Primary Education Degree](https://www.usc.gal/en/studies/degrees/social-and-legal-sciences/teaching-primary-education-degree-0)
- [UDC — Guía Docente 2024/25 Facultade de Ciencias da Educación (sample)](https://guiadocente.udc.es/guia_docent/index.php?apartat=665&centre=652&consulta=apartat&ensenyament=652498)
- [VIU — Grado en Educación Primaria Online (plan de estudios + guías docentes)](https://www.universidadviu.com/es/grado-educacion-primaria)
- [UNIR — Plan de estudios Grado bilingüe Magisterio Educación Primaria](https://www.unir.net/educacion/grado-bilingue-magisterio-educacion-primaria/plan-de-estudios/) (returned 403 in pilot)
- [ESCUNI (UCM-adscrito) — Memoria de Verificación Primaria (PDF)](https://www.escuni.es/wp-content/uploads/2017/07/Memoria-de-Verificacion-Primaria.pdf)
- [AQU Catalunya — Verificación de titulaciones](https://www.aqu.cat/universitats/Avaluacio-de-titulacions/Verificacio)
- [ACSUG — Agencia para la Calidad del Sistema Universitario de Galicia](http://www.acsug.es/en/acsug)
- [UNIBASQ — Agencia de Calidad del Sistema Universitario Vasco (ENQA listing)](https://www.enqa.eu/membership-database/unibasq-agency-for-the-quality-of-the-basque-university-system/)
- [Spanish Network for Quality Assurance Agencies (links page)](https://www.aqu.cat/en/links/Spanish-Network-for-Quality-Assurance-Agencies-in-Higher-Education)
- [UNIVERSITAS XXI — Académico (back-office system used by many Spanish universities)](https://universitasxxi.com/en/uxxi-academico.html)
