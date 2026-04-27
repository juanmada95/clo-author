# Data-Engineering Environment Lock-Protocol

**Project:** CDD curricular analysis (Stage 0 corpus inventory + Tier B sample).
**Companion to:** `quality_reports/software_environment.md` (R analysis stack).
**Date:** 2026-04-27.
**Status:** OSF deposit addendum (closes Pre-Registration Checklist item C2 + C3+C9).

---

## 1. Why a separate environment file

The CDD project has two distinct execution environments:

1. **R analysis stack** (`software_environment.md`). The authoritative environment for the post-coding analysis (kappa, bootstrap CIs, layer-gap cross-tabs, paired McNemar/Wilcoxon, sub-analyses) per the OSF PAP. Pinned via `renv.lock`. Closed package set: `tidyverse`, `irr`, `psych`, `boot`, `ggplot2`, `fmsb`, `pheatmap`, `scales`, `here`, `renv`.
2. **Python data-engineering stack** (this file). The environment used by the Stage 0 scrapers (gradomania / educaweb / ANECA / 8 autonomous-community agencies / RUCT) and the reconciliation + Tier B sample-selection scripts. Required because R's `rvest` cannot reliably drive session-stateful POST forms (data-discovery report section 5).

Both environments must be pinned; this file is the Python counterpart of `software_environment.md`.

---

## 2. Closed package set (Python)

The Python environment is restricted to the following packages. Adding any package after pre-registration is a logged deviation.

| Package | Purpose |
|---|---|
| `requests` | HTTP fetching with session-cookie support (RUCT, ANECA, agency probes). |
| `beautifulsoup4` | HTML parsing for aggregator listings and result tables. |
| `lxml` | Fast XML/HTML parser backend used by BeautifulSoup. |
| `pandas` | Tabular data manipulation, CSV I/O, group-wise operations in reconciliation and sampling. |
| `numpy` | The PRNG (`numpy.random.default_rng`) used for the Tier B stratified sample. |
| `pdfplumber` | Reserved for Stage 1 layer-1 (memorias) and layer-2 (guias docentes) PDF text extraction. NOT imported by the Stage 0 scripts. |

Standard library only beyond this: `pathlib`, `logging`, `re`, `time`, `unicodedata`, `urllib3` (for warning suppression).

---

## 3. Lockfile (pip freeze, captured at scrape execution)

The exact versions used to produce `data/cleaned/corpus_inventory.csv`, `data/cleaned/tier_b_sample_ids.csv`, and the raw inventory passes in `data/raw/inventory_passes/` are pinned by this output of `pip freeze`:

```
beautifulsoup4==4.14.3
certifi==2026.4.22
charset-normalizer==3.4.7
idna==3.13
lxml==6.1.0
numpy==2.4.4
pandas==3.0.2
python-dateutil==2.9.0.post0
requests==2.33.1
six==1.17.0
soupsieve==2.8.3
typing_extensions==4.15.0
tzdata==2026.2
urllib3==2.6.3
```

Python interpreter: `Python 3.14.4` (Windows 11 Home; reproduces on any 3.11+ interpreter -- the scripts use only language features available since 3.10).

---

## 4. Reproducibility commitments

- **PRNG.** The Tier B sample is drawn via `numpy.random.default_rng(seed=20240901)` (NumPy's PCG64 generator). Re-running `scripts/python/strategy/tier_b_sample.py` against the SAME `corpus_inventory.csv` produces the same 60 programme IDs.
- **Determinism.** The reconciliation script is fully deterministic (no random component). The order of operations (sort, group, filter, drop) preserves a stable mapping from raw passes to the final inventory.
- **R cross-validation.** `scripts/R/strategy/tier_b_sample.R` encodes the same algorithm in R for code-review and pedagogical purposes. R's `set.seed(20240901)` is NOT compatible with NumPy's PCG64; the R script reproduces the algorithm but NOT the deposit's 60 IDs. The Python script is the authoritative deposit.
- **Network-dependent steps.** The scrapers (gradomania, educaweb, ANECA, 8 agencies, RUCT) depend on the live state of public web sources. Each scraper logs a `fetch_ts` (UTC) per row and falls back to documented pilot evidence (per plan section 7) if the live source is unavailable. The reconciliation step's RUCT-anchoring logic gracefully degrades to cross-validation aggregate if `ruct.csv` is empty.
- **Time budget on RUCT.** RUCT scraper has an 8-minute hard cap per call to fit within the orchestrator's 10-minute Bash tool timeout. Partial output goes to `ruct_partial.csv`; total failure leaves `ruct.csv` empty and the reconciliation log records the substitution.
- **TLS verification bypass for ANECA and RUCT.** Both `scripts/python/scrape/aneca_listado_titulos.py` and `scripts/python/scrape/ruct_scraper.py` use `requests.Session()` with `verify=False` per pilot evidence (ANECA's `*.aneca.es` certificate chain returned verification errors in pilot WebFetches; the RUCT endpoint at `educacion.gob.es` exhibits intermittent SSL handshake issues from non-Spanish IPs). The bypass is logged in each script's header. The URL is the source of authority; the bypass does not affect the integrity of the raw text downloaded (HTML content is identical with or without verification, since the public listings are unauthenticated and contain no secrets). `urllib3.disable_warnings(InsecureRequestWarning)` is called in both scripts to suppress the resulting console noise.

---

## 5. Closed-set commitment

Any change to the package set after this deposit (adding `selenium`, `playwright`, `aiohttp`, etc.) is a logged deviation in the OSF PAP section 10. The deposit's reproducibility manifest commits the project to this fixed set.

---

## 6. Lockfile location and update procedure

- **Pinned lockfile:** this file (section 3).
- **At scrape execution:** the actual `pip freeze` output is captured in this section (kept current in version control).
- **Update on each scrape execution:** when re-running the inventory pipeline, regenerate section 3 from `pip freeze` and commit the change before pushing the inventory artifacts.

---

## 7. Out-of-scope environments

- **R analysis stack** -- see `software_environment.md`.
- **LaTeX compilation stack** -- managed by `paper/latexmkrc` and TeX Live profile (Overleaf-compatible).
- **Browser-based scraping** -- the Stage 0 design avoids browser drivers entirely. Stage 1 (memorias download) and Stage 2 (guias docentes scrape) may revisit this if specific institutions block `requests`-based fetching, but that is a separate decision logged at scrape execution.
