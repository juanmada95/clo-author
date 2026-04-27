"""
tier_b_sample.py

Title:    Tier B stratified random sample (60 programmes) for the CDD
          curricular analysis (Stage 0 deposit artifact).
Author:   data-engineer (CDD curricular analysis project).
Date:     2026-04-27.
Purpose:  Draws the OSF-pre-registered Tier B sample of 60 programmes via
          stratified random sampling across active sector x CCAA x modality
          cells, with proportional allocation and the min-2-per-active-cell
          rule. This Python implementation is the AUTHORITATIVE deposit
          script for `tier_b_sample_ids.csv` -- the R reference script in
          `scripts/R/strategy/tier_b_sample.R` is for cross-validation
          only and uses a different RNG (R's `set.seed`) so it will NOT
          reproduce these exact IDs (it reproduces the algorithm, not the
          deposit).

Inputs:   data/cleaned/corpus_inventory.csv
Outputs:  data/cleaned/tier_b_sample_ids.csv
          data/cleaned/tier_b_strata_table.csv
          data/cleaned/reproducibility_check.txt

Algorithm (per strategy memo section 3 + plan section 3.4):
  1. Load corpus_inventory.csv.
  2. Identify ACTIVE cells = (sector x ccaa x modality) cells with >= 1
     programme. Note: degree is NOT a stratifier per the memo; it is a
     within-programme attribute. The (sector x ccaa x modality) cross has
     4 x 18 x 2 = 144 cells, of which ~30-35 are active.
  3. Proportional allocation: per-active-cell n_cell =
     round(60 * cell_size / total_universe).
  4. Min-2 rule: bump every active cell to n_cell >= 2 (capped at the cell
     size if the cell has < 2 programmes).
  5. Adjust to sum to exactly 60: deduct from cells with the largest
     surplus (n_cell - 2) until sum == 60; or add to the largest cells
     if sum < 60. Adjustments preserve the min-2 constraint.
  6. Within each cell, sample n_cell programmes without replacement using
     numpy.random.default_rng(seed=20240901).
  7. Write tier_b_sample_ids.csv (60 rows), tier_b_strata_table.csv
     (per-cell allocation), and reproducibility_check.txt (first 5 IDs).

INV compliance:
  - INV-14: numpy RNG seeded EXACTLY ONCE at the top of main().
  - INV-15: imports at top.
  - INV-16: pathlib.Path.
  - INV-17: pre-allocated lists/arrays.
  - INV-19: no setwd / install.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
INV_PATH = PROJECT_ROOT / "data" / "cleaned" / "corpus_inventory.csv"
OUT_DIR = PROJECT_ROOT / "data" / "cleaned"
OUT_SAMPLE = OUT_DIR / "tier_b_sample_ids.csv"
OUT_STRATA = OUT_DIR / "tier_b_strata_table.csv"
OUT_REPRO = OUT_DIR / "reproducibility_check.txt"

SEED = 20240901
# Pre-registration target: "~60 programmes" (strategy memo section 3; PAP
# section 3.4) with min-2-per-active-cell rule. With 32 active cells in the
# realised universe, strict min-2 forces N >= 63 (since 32 cells x 2 = 64,
# minus 1 because one cell has only 1 programme in its universe). To deliver
# exactly N=60 (per orchestrator deliverable spec), the algorithm:
#   - Computes proportional allocation.
#   - Bumps to min-2 where feasible.
#   - When sum > TARGET_N, deducts from cells with the largest surplus
#     (n_cell - min(2, cell_size)) until sum == TARGET_N. Some cells may
#     end up at n_cell = 0, i.e., excluded from the sample. The min-2
#     constraint is enforced ONLY for cells that receive >= 1 draw (a
#     cell with n_cell = 0 is "not in sample", not "violating min-2").
# This keeps N=60 fixed and satisfies "min-2 for every cell in the sample"
# at the cost of dropping a small number of low-information cells from the
# sample. The dropped cells are documented in tier_b_strata_table.csv with
# cell_size_sample = 0 and a `dropped_for_n60` flag.
TARGET_N = 60
MIN_PER_ACTIVE_CELL = 2

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("tier_b")


# ---------------------------------------------------------------------------
# Sampling functions
# ---------------------------------------------------------------------------
def proportional_allocation(
    universe_sizes: pd.Series, target_n: int
) -> pd.Series:
    """Apportion target_n across cells in proportion to cell size."""
    total = int(universe_sizes.sum())
    raw = universe_sizes * (target_n / total)
    floors = np.floor(raw).astype(int)
    remainders = raw - floors
    deficit = target_n - int(floors.sum())
    if deficit > 0:
        # Distribute the remaining seats to the cells with the largest
        # fractional remainders.
        order = remainders.sort_values(ascending=False).index
        for cell in order[:deficit]:
            floors.loc[cell] += 1
    return floors.astype(int)


def apply_min_per_active_cell(
    n_cell: pd.Series, universe_sizes: pd.Series, min_n: int
) -> pd.Series:
    """Bump every cell with allocation >= 1 to at least min_n (capped at
    cell size). Cells with allocation 0 are left at 0 -- they are
    candidates to be dropped from the sample if the budget is tight.
    """
    bumped = n_cell.copy()
    for cell in bumped.index:
        if bumped.loc[cell] < 1:
            continue  # leave at 0; may be brought in later if budget allows
        target = min(min_n, int(universe_sizes.loc[cell]))
        if bumped.loc[cell] < target:
            bumped.loc[cell] = target
    return bumped.astype(int)


def adjust_to_target(
    n_cell: pd.Series,
    universe_sizes: pd.Series,
    target_n: int,
    min_n: int,
) -> pd.Series:
    """Adjust n_cell so its sum equals target_n while respecting min_n
    on cells that remain in the sample.

    Cells with n_cell = 0 are excluded from the sample (and from the
    min-n constraint). Cells with n_cell >= 1 must satisfy
    n_cell >= min(min_n, cell_size).

    Algorithm:
      Phase 1: bring as many cells in at min_n as the budget allows
               (smallest cells first, prioritising stratum coverage).
      Phase 2: if budget remaining, distribute extras to cells in
               proportion to their universe size (preserving min_n).
      Phase 3: if budget short (sum > target_n), remove draws from cells
               with surplus (n - min_n) > 0; if no surplus exists, zero
               out the smallest in-sample cells (dropping them from the
               sample) until budget == target_n.
    """
    n = n_cell.copy().astype(int)
    current = int(n.sum())

    # Phase 3 (over-allocation -> remove)
    while current > target_n:
        # Try first: remove from cells with surplus n > min_floor.
        margins = pd.Series(
            {
                cell: n.loc[cell] - min(min_n, int(universe_sizes.loc[cell]))
                for cell in n.index
            }
        )
        # Restrict to in-sample cells (n > 0).
        margins = margins[n > 0]
        if (margins > 0).any():
            cell = margins.idxmax()
            n.loc[cell] -= 1
            current -= 1
            continue
        # No cell has surplus above its min; we must drop a cell.
        in_sample = n[n > 0]
        if in_sample.empty:
            break
        # Drop the smallest in-sample cell (lowest universe size; tiebreak
        # by alphabetical cell key for determinism).
        cell_sizes_in_sample = universe_sizes[in_sample.index]
        cell_to_drop = sorted(
            cell_sizes_in_sample.items(),
            key=lambda kv: (kv[1], str(kv[0])),
        )[0][0]
        current -= int(n.loc[cell_to_drop])
        n.loc[cell_to_drop] = 0

    # Phase 2 (under-allocation -> add)
    while current < target_n:
        # Prefer to bring in cells currently at 0 (broaden coverage), but
        # only if their min-n requirement fits within the remaining budget.
        zeros = n[n == 0]
        if not zeros.empty:
            # Pick the largest zero cell (highest universe size).
            zero_sizes = universe_sizes[zeros.index].sort_values(ascending=False)
            for cell in zero_sizes.index:
                cell_min = min(min_n, int(universe_sizes.loc[cell]))
                if current + cell_min <= target_n:
                    n.loc[cell] = cell_min
                    current += cell_min
                    break
            else:
                # No zero cell fits; fall through to incrementing existing.
                head = universe_sizes - n
                head = head[(head > 0) & (n > 0)]
                if head.empty:
                    break
                cell = head.idxmax()
                n.loc[cell] += 1
                current += 1
            continue
        # No zero cells; increment the cell with most headroom (n < universe).
        head = universe_sizes - n
        head = head[(head > 0) & (n > 0)]
        if head.empty:
            break
        cell = head.idxmax()
        n.loc[cell] += 1
        current += 1

    return n.astype(int)


def stratified_sample(
    inventory: pd.DataFrame, n_cell: pd.Series, rng: np.random.Generator
) -> pd.DataFrame:
    """Within each cell, sample n_cell rows without replacement.

    `inventory` MUST be sorted deterministically (we sort by programme_id
    above) so the sample is fully reproducible from (seed, sorted-input).
    """
    sampled_rows: list[pd.DataFrame] = []
    for cell, k in n_cell.items():
        sector, ccaa, modality = cell
        cell_rows = inventory[
            (inventory["sector"] == sector)
            & (inventory["ccaa"] == ccaa)
            & (inventory["modality"] == modality)
        ]
        # Deterministic order by programme_id before drawing.
        cell_rows = cell_rows.sort_values("programme_id").reset_index(drop=True)
        if k <= 0:
            continue
        if k >= len(cell_rows):
            picked = cell_rows.copy()
        else:
            idx = rng.choice(len(cell_rows), size=k, replace=False)
            idx_sorted = sorted(idx.tolist())
            picked = cell_rows.iloc[idx_sorted].copy()
        sampled_rows.append(picked)
    if not sampled_rows:
        return pd.DataFrame(columns=inventory.columns)
    return pd.concat(sampled_rows, ignore_index=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load inventory ------------------------------------------------------
    inventory = pd.read_csv(INV_PATH, encoding="utf-8")
    log.info("Loaded inventory: %d programmes", len(inventory))

    if inventory.empty:
        raise RuntimeError("corpus_inventory.csv is empty; cannot sample.")

    # Validate required columns
    required = {"programme_id", "sector", "ccaa", "modality", "degree", "university_name"}
    missing = required - set(inventory.columns)
    if missing:
        raise RuntimeError(f"Inventory missing columns: {missing}")

    # 2. Identify active cells -----------------------------------------------
    # Stratification: sector x ccaa x modality (degree is NOT a stratifier).
    cells = (
        inventory.groupby(["sector", "ccaa", "modality"])
        .size()
        .rename("cell_size_universe")
    )
    n_active = (cells > 0).sum()
    log.info(
        "Active cells: %d (out of 4 x 18 x 2 = 144 possible).", int(n_active)
    )

    # Compute the minimum-feasible N implied by min-2-on-every-active-cell
    # (informational only; we do NOT raise the target to this value -- we
    # accept dropping low-information cells to stay at TARGET_N=60).
    min_2_floor_full = int(
        cells.apply(lambda x: min(MIN_PER_ACTIVE_CELL, int(x))).sum()
    )
    log.info(
        "Min-feasible N if every active cell receives min-%d: %d",
        MIN_PER_ACTIVE_CELL, min_2_floor_full,
    )
    if min_2_floor_full > TARGET_N:
        log.warning(
            "Min-feasible-N (%d) > TARGET_N (%d). The algorithm will drop "
            "low-information cells from the sample to keep N=%d. Cells "
            "dropped will appear in tier_b_strata_table.csv with "
            "cell_size_sample=0.",
            min_2_floor_full, TARGET_N, TARGET_N,
        )

    # 3. Proportional allocation ---------------------------------------------
    raw_alloc = proportional_allocation(cells, TARGET_N)
    log.info("Proportional allocation sum: %d", int(raw_alloc.sum()))

    # 4. Min-2 rule ----------------------------------------------------------
    bumped = apply_min_per_active_cell(raw_alloc, cells, MIN_PER_ACTIVE_CELL)
    log.info(
        "After min-%d-per-cell-with-allocation rule: sum = %d",
        MIN_PER_ACTIVE_CELL, int(bumped.sum()),
    )

    # 5. Adjust to exactly TARGET_N -----------------------------------------
    n_cell = adjust_to_target(bumped, cells, TARGET_N, MIN_PER_ACTIVE_CELL)
    log.info("After adjustment to TARGET_N=%d: sum = %d", TARGET_N, int(n_cell.sum()))

    if int(n_cell.sum()) != TARGET_N:
        raise RuntimeError(
            f"Failed to allocate exactly {TARGET_N} draws "
            f"(allocated {int(n_cell.sum())}). Investigate adjust_to_target."
        )

    # Verify min-2 constraint (only on cells that received >= 1 draw;
    # cells with k=0 are excluded from the sample and therefore from the
    # min-2 rule by construction).
    for cell, k in n_cell.items():
        if k == 0:
            continue
        cell_size = int(cells.loc[cell])
        target = min(MIN_PER_ACTIVE_CELL, cell_size)
        if k < target:
            raise RuntimeError(
                f"Min-{MIN_PER_ACTIVE_CELL} rule violated at {cell}: "
                f"k={k}, cell_size={cell_size}"
            )

    # 6. Draw sample ---------------------------------------------------------
    # INV-14: numpy RNG seeded EXACTLY ONCE here.
    rng = np.random.default_rng(seed=SEED)
    sample = stratified_sample(inventory, n_cell, rng)
    log.info("Sample size: %d", len(sample))

    if len(sample) != TARGET_N:
        raise RuntimeError(
            f"Sample size {len(sample)} != target {TARGET_N}."
        )

    # 7. Write tier_b_sample_ids.csv ----------------------------------------
    sample_cols = [
        "programme_id", "codigo_ruct", "university_name", "sector",
        "ccaa", "modality", "degree", "centro", "fallback_flag",
    ]
    sample_out = sample[[c for c in sample_cols if c in sample.columns]].copy()
    sample_out.to_csv(OUT_SAMPLE, index=False, encoding="utf-8")
    log.info("Wrote %d sampled programmes to %s", len(sample_out), OUT_SAMPLE)

    # 8. Write tier_b_strata_table.csv ---------------------------------------
    strata_table = (
        cells.reset_index()
        .merge(
            n_cell.rename("cell_size_sample").reset_index(),
            on=["sector", "ccaa", "modality"],
            how="left",
        )
    )
    strata_table["cell_size_sample"] = strata_table["cell_size_sample"].fillna(0).astype(int)
    strata_table["sampling_fraction"] = (
        strata_table["cell_size_sample"] / strata_table["cell_size_universe"]
    ).round(4)
    strata_table["dropped_for_n60"] = strata_table["cell_size_sample"] == 0
    strata_table = strata_table.sort_values(
        ["sector", "ccaa", "modality"]
    ).reset_index(drop=True)
    strata_table.to_csv(OUT_STRATA, index=False, encoding="utf-8")
    log.info(
        "Wrote strata table (%d active cells) to %s",
        len(strata_table), OUT_STRATA,
    )

    # 9. Reproducibility check -----------------------------------------------
    first5 = sample_out.head(5)["programme_id"].tolist()
    cells_in_sample = int((n_cell > 0).sum())
    cells_dropped = int((n_cell == 0).sum())
    repro_lines = [
        "Reproducibility check -- Tier B sample selection",
        "================================================",
        f"Seed: numpy.random.default_rng(seed={SEED})",
        f"Inventory file:  data/cleaned/corpus_inventory.csv",
        f"Inventory size:  {len(inventory)} programmes",
        f"Target N (PAP):  {TARGET_N}",
        f"Min per cell-in-sample: {MIN_PER_ACTIVE_CELL}",
        f"Active cells (universe): {int(n_active)}",
        f"Cells in sample:         {cells_in_sample}",
        f"Cells dropped from sample: {cells_dropped}",
        f"Min-feasible N if every active cell received min-2: {min_2_floor_full}",
        f"Realised N:      {len(sample_out)}",
        "",
    ]
    if cells_dropped > 0:
        repro_lines.append(
            f"NOTE: With {int(n_active)} active cells, strict min-2-per-active-cell "
            f"would force N >= {min_2_floor_full}. To deliver TARGET_N=60 (PAP), "
            f"{cells_dropped} low-information cells were dropped from the "
            "sample (cell_size_sample=0 in tier_b_strata_table.csv). The "
            "min-2 rule holds for every cell that receives any draw. "
            "Programmes in dropped cells remain in the universe inventory "
            "but are not in this Tier B sample. This is documented in the "
            "strata table for full transparency."
        )
        repro_lines.append("")
    repro_lines.append("First 5 sampled programme_ids (for PAP quotation):")
    for i, pid in enumerate(first5, 1):
        row = sample_out.iloc[i - 1]
        repro_lines.append(
            f"  {i}. {pid}  |  {row['university_name']}  |  "
            f"{row['sector']}  |  {row['ccaa']}  |  "
            f"{row['modality']}  |  {row['degree']}"
        )
    repro_lines.append("")
    repro_lines.append(
        "To verify reproducibility: re-run "
        "scripts/python/strategy/tier_b_sample.py from a clean Python "
        "session against the SAME corpus_inventory.csv. The same 60 "
        "programme IDs must be produced (the algorithm is fully "
        "deterministic given the seed and the sorted inventory)."
    )
    repro_lines.append("")
    repro_lines.append("REPRODUCIBILITY CHAIN")
    repro_lines.append("")
    repro_lines.append(
        "The deposit artifacts (corpus_inventory.csv, tier_b_sample_ids.csv,"
    )
    repro_lines.append(
        "tier_b_strata_table.csv) are byte-reproducible from THIS frozen"
    )
    repro_lines.append(
        "corpus_inventory.csv with seed 20240901 and numpy 2.4.4 on Python 3.11+."
    )
    repro_lines.append(
        "Re-running tier_b_sample.py from this exact corpus_inventory.csv on a"
    )
    repro_lines.append("different machine will produce identical 60 IDs.")
    repro_lines.append("")
    repro_lines.append(
        "The deposit is NOT byte-reproducible end-to-end from raw scrape, because:"
    )
    repro_lines.append(
        "1. RUCT scrape returned 0 rows on 2026-04-27 (JS-rendered pagination);"
    )
    repro_lines.append(
        "   future runs may succeed and add ~10-30 codigo_ruct values."
    )
    repro_lines.append(
        "2. ANECA / educaweb / autonomous-community agency HTML drifts over time"
    )
    repro_lines.append(
        "   (institutions added, removed, restructured between academic years)."
    )
    repro_lines.append(
        "3. Live HTTP fetches are subject to network conditions, TLS cert refresh,"
    )
    repro_lines.append("   and rate limiting.")
    repro_lines.append("")
    repro_lines.append(
        "The frozen corpus_inventory.csv (committed at deposit time) is the"
    )
    repro_lines.append(
        "authoritative anchor for all downstream analysis. Future scrapes are"
    )
    repro_lines.append("documented as deviations in PAP Section 10.")
    OUT_REPRO.write_text("\n".join(repro_lines), encoding="utf-8")
    log.info("Wrote reproducibility check to %s", OUT_REPRO)


if __name__ == "__main__":
    main()
