# Inventory Reconciliation Log

**Date:** 2026-04-27T10:50:38.743067+00:00

## Source-file row counts (raw)

| Source | Rows |
|---|---|
| `gradomania.csv` | 78 |
| `educaweb.csv` | 185 |
| `aneca.csv` | 74 |
| `aqu.csv` | 24 |
| `acsug.csv` | 6 |
| `unibasq.csv` | 6 |
| `aacdeva.csv` | 18 |
| `acsucyl.csv` | 14 |
| `aquib.csv` | 2 |
| `avap.csv` | 18 |
| `madrimasd.csv` | 27 |
| `ruct.csv` | 0 |

## RUCT outcome

**RUCT live scrape FALLBACK (per plan section 7).** The session-based POST against `https://www.educacion.gob.es/ruct/consultaestudios` returned no parseable result rows in 0/2 queries. The cross-validation aggregate (gradomania + educaweb + ANECA + 8 autonomous-community agency seeds + manual adscritos override) was used as the universe in lieu of RUCT. `codigo_ruct` is empty for all rows; programme IDs are synthetic (`P0001`-`Pxxxx`). This substitution is logged as a deviation in the OSF pre-registration deposit (PAP section 10).

## Final inventory composition

**Total programmes:** 174

### By sector

| Sector | N |
|---|---|
| public | 93 |
| private-traditional | 44 |
| adscrito | 28 |
| private-online | 9 |

### By degree

| Degree | N |
|---|---|
| primaria | 88 |
| infantil | 86 |

### By modality

| Modality | N |
|---|---|
| presencial | 162 |
| online | 12 |

### By autonomous community

| CCAA | N |
|---|---|
| Madrid | 48 |
| Cataluna | 29 |
| Andalucia | 24 |
| Comunitat Valenciana | 18 |
| Castilla y Leon | 15 |
| Canarias | 6 |
| Pais Vasco | 6 |
| Galicia | 6 |
| Aragon | 4 |
| Navarra | 4 |
| La Rioja | 2 |
| Asturias | 2 |
| Cantabria | 2 |
| Castilla-La Mancha | 2 |
| Extremadura | 2 |
| Illes Balears | 2 |
| Murcia | 2 |

## Dropped rows (sector=unknown)

0 (university, degree) candidate rows were dropped because the sector classifier did not recognise the institution name. This list is for transparency; reviewers can inspect whether any legitimate institution was missed.


## Noise-filter rules applied to live HTML scrapes

Live aggregator scrapes (educaweb, agencies) returned raw rows that include HTML-noise hits matching the `Universi...` regex but are not real institutions. These rows are filtered up-front by `inventory_reconciliation.py::is_noise_university()` before any canonicalisation, sector classification, or deduplication. Filter rules and per-rule drop counts:

| # | Rule | Description | Rows dropped |
|---|---|---|---|
| 1 | length_lt_15 | Normalised name length < 15 chars (filters stubs like 'Universidad).' and 'Universidad') | 4 |
| 2 | phrase_blocklist | Contains any of: 'para mayores de', 'mayores 25', 'mayores 30', 'mayores 40', 'tu pregunta', 'tus preguntas', 'responder a tus', 'test de orientacion', 'tu estudio' (filters senior-citizen programmes and SEO ad copy that begin 'Universidad...') | 12 |
| 3 | stub_token | Starts with 'universidad).' or 'universidad.' (filters HTML fragments where the regex captured a closing paren or period) | 0 |
| 4 | exact_acronym | Exactly equals one of: 'universidad', 'universidades', 'universitat', 'universidades.' (filters bare section headings) | 0 |
| | **Total** | | **16** |

Counts include the same row potentially filtered at multiple source passes (e.g., the same noise row in educaweb and educaweb_pilot_fallback). The post-filter `sector=unknown` drop is documented separately in the 'Dropped rows (sector=unknown)' section above; that filter operates on canonicalised institution names, not on raw HTML noise.

## Manual overrides applied

- Adscritos override list: 15 centres added per `data_exploration_cdd_formacion_inicial.md` flag 5.
- Modality collapse: `semipresencial` -> `presencial` per Tier B design (strategy memo section 3 - 2-level modality).
- Sector classification: `private-online` is reserved for VIU, UNIR, UDIMA, Isabel I; UNED is `public` (not private-online even though its modality is online).
