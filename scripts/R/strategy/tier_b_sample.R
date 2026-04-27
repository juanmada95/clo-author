# tier_b_sample.R
#
# Title:    Tier B stratified random sample (R reference / cross-validation
#           script). NOT the deposit script -- see header note below.
# Author:   data-engineer (CDD curricular analysis project).
# Date:     2026-04-27.
# Purpose:  Cross-validation reference: encodes the same algorithm in R as
#           the authoritative Python deposit script. Lets future analysts
#           verify the algorithm in R if they want to.
#
# IMPORTANT -- THIS SCRIPT IS NOT THE OSF DEPOSIT
# ===============================================
# The authoritative `tier_b_sample_ids.csv` is produced by
# `scripts/python/strategy/tier_b_sample.py`, which uses
# `numpy.random.default_rng(seed=20240901)`. R's `set.seed()` and
# numpy's `default_rng()` are different RNGs; running this script
# WILL NOT reproduce the deposited 60 IDs. It WILL reproduce the
# algorithm: same proportional allocation, same min-2 rule, same
# stratification logic. Use this script for code-review purposes,
# not for verifying the deposit list.
#
# A future R-only analyst who wants to reproduce the SAMPLE list (not just
# the algorithm) must port the Python script to R using a numpy-compatible
# PRNG (e.g., {numpy} via reticulate, or a manual port of PCG64), or use
# the Python script directly.
#
# Inputs:   data/cleaned/corpus_inventory.csv
# Outputs:  (none -- this is a reference script; running it would overwrite
#           the deposit. The script is set up to be sourced for inspection.)
#
# INV compliance:
#  - INV-14: set.seed(20240901) once at the top.
#  - INV-15: library() at the top.
#  - INV-16: paths via here::here().
#  - INV-17: vectorised group-wise operations (no growing loops).
#  - INV-19: no setwd(), no install.packages(), no rm(list=ls()).

# ---------------------------------------------------------------------------
# Packages -- INV-15
# ---------------------------------------------------------------------------
library(dplyr)
library(tidyr)
library(here)
library(readr)

# ---------------------------------------------------------------------------
# Reproducibility -- INV-14 (single set.seed at top)
# ---------------------------------------------------------------------------
set.seed(20240901)

# ---------------------------------------------------------------------------
# Paths -- INV-16 (relative via here::here)
# ---------------------------------------------------------------------------
inv_path     <- here::here("data", "cleaned", "corpus_inventory.csv")
out_sample   <- here::here("data", "cleaned", "tier_b_sample_ids_R.csv")
out_strata   <- here::here("data", "cleaned", "tier_b_strata_table_R.csv")
out_repro    <- here::here("data", "cleaned", "reproducibility_check_R.txt")

# Sampling parameters (must match the Python deposit script)
TARGET_N <- 60L
MIN_PER_ACTIVE_CELL <- 2L

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
proportional_allocation <- function(cells_df, target_n) {
  total <- sum(cells_df$cell_size_universe)
  cells_df$raw <- cells_df$cell_size_universe * (target_n / total)
  cells_df$floor_n <- floor(cells_df$raw)
  cells_df$rem <- cells_df$raw - cells_df$floor_n
  deficit <- target_n - sum(cells_df$floor_n)
  if (deficit > 0L) {
    ord <- order(-cells_df$rem)
    cells_df$floor_n[ord[seq_len(deficit)]] <- cells_df$floor_n[ord[seq_len(deficit)]] + 1L
  }
  cells_df$n_cell <- as.integer(cells_df$floor_n)
  cells_df
}

apply_min_per_cell <- function(cells_df, min_n) {
  for (i in seq_len(nrow(cells_df))) {
    if (cells_df$n_cell[i] < 1L) next
    target <- min(min_n, cells_df$cell_size_universe[i])
    if (cells_df$n_cell[i] < target) cells_df$n_cell[i] <- target
  }
  cells_df
}

adjust_to_target <- function(cells_df, target_n, min_n) {
  current <- sum(cells_df$n_cell)
  while (current > target_n) {
    margins <- cells_df$n_cell - pmin(min_n, cells_df$cell_size_universe)
    margins[cells_df$n_cell == 0L] <- -1L
    if (max(margins) > 0L) {
      i <- which.max(margins)
      cells_df$n_cell[i] <- cells_df$n_cell[i] - 1L
      current <- current - 1L
    } else {
      # Drop smallest in-sample cell
      in_sample <- which(cells_df$n_cell > 0L)
      if (length(in_sample) == 0L) break
      sizes <- cells_df$cell_size_universe[in_sample]
      drop_idx <- in_sample[which.min(sizes)]
      current <- current - cells_df$n_cell[drop_idx]
      cells_df$n_cell[drop_idx] <- 0L
    }
  }
  while (current < target_n) {
    zeros <- which(cells_df$n_cell == 0L)
    fitted <- FALSE
    if (length(zeros) > 0L) {
      ord <- zeros[order(-cells_df$cell_size_universe[zeros])]
      for (i in ord) {
        cell_min <- min(min_n, cells_df$cell_size_universe[i])
        if (current + cell_min <= target_n) {
          cells_df$n_cell[i] <- cell_min
          current <- current + cell_min
          fitted <- TRUE
          break
        }
      }
    }
    if (!fitted) {
      head <- cells_df$cell_size_universe - cells_df$n_cell
      head[cells_df$n_cell == 0L] <- 0L
      if (max(head) <= 0L) break
      i <- which.max(head)
      cells_df$n_cell[i] <- cells_df$n_cell[i] + 1L
      current <- current + 1L
    }
  }
  cells_df
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
inventory <- readr::read_csv(inv_path, show_col_types = FALSE)
stopifnot(nrow(inventory) > 0)

cells_df <- inventory %>%
  dplyr::group_by(sector, ccaa, modality) %>%
  dplyr::summarise(cell_size_universe = dplyr::n(), .groups = "drop") %>%
  dplyr::arrange(sector, ccaa, modality) %>%
  as.data.frame()

cells_df <- proportional_allocation(cells_df, TARGET_N)
cells_df <- apply_min_per_cell(cells_df, MIN_PER_ACTIVE_CELL)
cells_df <- adjust_to_target(cells_df, TARGET_N, MIN_PER_ACTIVE_CELL)

stopifnot(sum(cells_df$n_cell) == TARGET_N)

# Within-cell sampling -- vectorised by group_by + slice_sample.
# Note: R's `sample()` is governed by set.seed(20240901); this will NOT
# reproduce the Python deposit. The IDs drawn here are an algorithm-level
# cross-check, not the deposited sample.
sample_rows <- inventory %>%
  dplyr::left_join(
    cells_df %>% dplyr::select(sector, ccaa, modality, n_cell),
    by = c("sector", "ccaa", "modality")
  ) %>%
  dplyr::filter(!is.na(n_cell), n_cell > 0L) %>%
  dplyr::group_by(sector, ccaa, modality) %>%
  dplyr::group_modify(function(df, key) {
    n <- unique(df$n_cell)
    df %>%
      dplyr::arrange(programme_id) %>%  # deterministic pre-sort
      dplyr::slice_sample(n = min(n, nrow(df)), replace = FALSE)
  }) %>%
  dplyr::ungroup()

stopifnot(nrow(sample_rows) == TARGET_N)

# Write the cross-validation outputs (different filenames so the Python
# deposit is not overwritten).
sample_cols <- c("programme_id", "codigo_ruct", "university_name",
                 "sector", "ccaa", "modality", "degree", "centro",
                 "fallback_flag")
present_cols <- intersect(sample_cols, names(sample_rows))
readr::write_csv(sample_rows[, present_cols], out_sample)

strata_out <- cells_df %>%
  dplyr::transmute(
    sector,
    ccaa,
    modality,
    cell_size_universe,
    cell_size_sample = n_cell,
    sampling_fraction = round(n_cell / cell_size_universe, 4),
    dropped_for_n60 = n_cell == 0L
  )
readr::write_csv(strata_out, out_strata)

repro_lines <- c(
  "Reproducibility check (R reference; NOT the deposit)",
  "==================================================",
  paste0("Seed: set.seed(", 20240901, ") -- R's RNG, NOT numpy's"),
  paste0("Target N:  ", TARGET_N),
  paste0("Realised N: ", nrow(sample_rows)),
  "",
  "First 5 sampled programme_ids (R order):",
  paste0("  ", seq_len(5), ". ",
         sample_rows$programme_id[seq_len(5)], "  |  ",
         sample_rows$university_name[seq_len(5)]),
  "",
  "WARNING: This list will NOT match the Python deposit",
  "  data/cleaned/tier_b_sample_ids.csv because R's set.seed()",
  "  and numpy.random.default_rng() use different PRNG algorithms."
)
writeLines(repro_lines, out_repro)

message("[R reference] Wrote ", nrow(sample_rows), " rows to ", out_sample)
