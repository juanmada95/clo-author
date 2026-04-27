# Software Environment — CDD en la Formación Inicial del Profesorado

**OSF Pre-Registration Checklist item C6.** Companion artifact to `osf_preregistration_cdd_formacion_inicial.md` §3.5.

This document is a **lock-protocol commitment**, not a today's lockfile. Specific package versions are pinned at **pilot start** (not at pre-registration draft time), recorded here, and the resulting `renv.lock` is deposited as the OSF addendum file `software_environment_lockfile.json` (renv → JSON export). Updating this file after pilot start is itself a logged deviation in PAP §10.

---

## 1. Language and runtime

| Component | Target | Locked at | Lock evidence |
|---|---|---|---|
| **R** | 4.4.x (release branch) | Pilot start | `R.version` snapshot in `renv.lock` |
| **OS reproducibility** | Any POSIX-or-Windows host with R 4.4.x — analysis is OS-independent (no system calls, no platform-specific I/O) | — | `sessionInfo()` output deposited |

**Note:** Python is *not* part of the analysis stack. Python is used only for the data-engineer's web-scraping toolchain (`requests`, `BeautifulSoup`, `pdfplumber`); scraper environment is pinned separately in `data_engineering_environment.md` (deposited at scrape start).

## 2. Required R packages — pre-registered set

The following packages are pre-registered as the analysis stack. The set is closed: any package added during analysis is a logged deviation (PAP §10).

| Package | Purpose (per pseudo_code.md / PAP) | Target version |
|---|---|---|
| `tidyverse` (incl. `dplyr`, `tidyr`, `purrr`, `readr`, `stringr`) | Data manipulation, I/O, transformation | latest stable at pilot start |
| `irr` | Cohen's κ (binary), weighted κ (ordinal depth) | latest stable |
| `psych` | Krippendorff's α (`ICC` and reliability statistics, robustness) | latest stable |
| `boot` | Bootstrap 95% CI on coverage / depth aggregates (1000 reps, programme-level resampling) | latest stable |
| `ggplot2` | Coverage heatmaps, depth plots | latest stable |
| `fmsb` | Radar plots (per (degree × layer × area)) | latest stable |
| `pheatmap` | Heatmaps (alternative / cross-validation against ggplot2 + scales) | latest stable |
| `scales` | Heatmap scaling, palette management | latest stable |
| `here` | Path management (no `setwd()` per INV-16/INV-19) | latest stable |
| `renv` | Project-local package management; produces `renv.lock` for deposit | latest stable |

## 3. Lock procedure — to be executed at pilot start

The following procedure is committed to. Output of step 4 is the deposit artifact.

```r
# 1. Activate project-local library
renv::init(bare = TRUE)

# 2. Install pre-registered packages from CRAN
install.packages(c(
  "tidyverse", "irr", "psych", "boot",
  "ggplot2", "fmsb", "pheatmap", "scales",
  "here", "renv"
))

# 3. Snapshot to renv.lock
renv::snapshot()

# 4. Export sessionInfo() for the deposit
sink("software_environment_sessionInfo.txt")
sessionInfo()
sink()

# 5. Hash-stamp the lockfile for OSF deposit
tools::md5sum("renv.lock")
```

## 4. Reproducibility commitments

- **Single-machine rule.** Pilot lock and main-coding analysis must run on the *same* lockfile. Switching machines mid-analysis triggers a `renv::restore()` from the locked file and a `sessionInfo()` re-snapshot for cross-validation.
- **No `install.packages()` in scripts** (per INV-19). All package management goes through `renv::restore()` at session start.
- **No `library()` after the top of a script** (per INV-15). Loaded once, at the top.
- **No absolute paths** (per INV-16). All paths via `here::here(...)`.
- **`set.seed()` once at the top of every stochastic script** (per INV-14). Project-wide seed: `20240901`. Used by:
  - `tier_b_sample.R` (sample selection)
  - `reliability_subsample.R` (a-priori 20% reliability sample, PAP §6 B1)
  - `bootstrap_ci.R` (1000 reps for coverage/depth confidence intervals)

## 5. Deposit checklist (at pilot start)

- [ ] `renv.lock` produced and committed.
- [ ] `software_environment_sessionInfo.txt` produced and committed.
- [ ] MD5 hashes of both files added to this document, §6 below.
- [ ] OSF addendum filed: `software_environment_lockfile.json` = `renv.lock` (renamed for OSF clarity).

## 6. Hashes (filled at pilot start)

| File | MD5 | Date |
|---|---|---|
| `renv.lock` | `[pending pilot start]` | — |
| `software_environment_sessionInfo.txt` | `[pending pilot start]` | — |

---

**Document status:** lock-protocol committed; concrete package versions to be locked at pilot start. Until then, treat the package list in §2 as the closed pre-registered set; no analysis package may be added without a logged deviation.
