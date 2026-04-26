# Pseudo-code — Curricular Analysis Pipeline (TDC / MRCDD)

**Project:** Post-MRCDD, two-degree, two-layer curricular analysis.
**Companion to:** `quality_reports/strategy_memo_cdd_formacion_inicial.md`.
**Date:** 2026-04-26.

This is **specification-level pseudo-code**, not implementable code. The coder will operationalize it.

---

## Conventions

- `<programme>` = an accredited Grado en Maestro de Infantil OR Primaria offered by a university (1 of ~140–170 [ASSUMED]).
- `<layer>` ∈ {memoria, guia}.
- `<area>` ∈ {1..6} per MRCDD.
- `<competence>` ∈ {1..23} per MRCDD, nested in areas.
- `<depth>` ∈ {0,1,2,3} (absent / mentioned / developed / assessed).
- `<coder>` ∈ {1, 2, [3 if available]}.
- All file paths are relative to the project root via `here()` or `pathlib.Path`.

---

## STAGE 0 — Inventory the corpus (depends on `/discover data`)

```
INPUT: RUCT scrape / API pull
OUTPUT: corpus_inventory.csv
        columns: programme_id, university, sector (public/private),
                 modality (in-person/online), autonomous_community,
                 degree (Infantil/Primaria), memoria_url, memoria_version,
                 num_courses_expected, courses_url

procedure inventory_corpus():
    raw = pull_RUCT()                   # API or scrape; cache locally
    filtered = filter(raw,
                     degree in {Infantil, Primaria},
                     legislation in {RD 1393/2007, ECI/3854/2007, ECI/3857/2007},
                     active_in_2024_2025)
    write filtered to corpus_inventory.csv
    log: total programmes, by-degree breakdown, by-sector breakdown

assertion: every programme has memoria_url OR is flagged as "memoria not retrievable"
```

---

## STAGE 1 — Document ingestion and preprocessing

```
INPUT: corpus_inventory.csv, downloaded PDFs and HTML files
OUTPUT: corpus_segments.csv (long form: one row per codable segment)
        columns: segment_id, programme_id, layer, course_id (NA for memoria),
                 section, segment_text, language, retrieval_status

procedure ingest_layer1_memorias():
    for each programme p in corpus_inventory:
        download p.memoria_url to data/raw/memorias/{programme_id}.pdf
        text = extract_text_pdf(memoria_pdf)         # pdftotext or pdfminer
        text = normalize_unicode(text)
        sections = identify_sections(text,
                                     {"Competencias", "Planificación",
                                      "Evaluación", "Módulos", "Materias"})
        for each section in sections:
            segments = paragraph_split(section)
            for each segment in segments:
                write row: (segment_id, programme_id, layer="memoria",
                            course_id=NA, section=name, text, language)

procedure ingest_layer2_guias():
    for each programme p in corpus_inventory:
        course_list = scrape_course_catalogue(p.courses_url)
        course_list = filter(course_list,
                             tipo in {"básica", "obligatoria"})           # required only
        course_list = course_list ∪ filter(course_list, tipo == "Prácticum")
        course_list = course_list ∪ filter(course_list, tipo == "TFG")
        for each course in course_list:
            download course.guia_url
            text = extract_text(course.guia_url)                          # PDF or HTML
            segments = field_split(text,
                                   {"Competencias", "Resultados de aprendizaje",
                                    "Contenidos", "Metodología", "Evaluación"})
            for each segment in segments:
                write row with layer="guia", course_id

assertion: retrieval_status logged for every (programme, course) pair
            (retrieved / login_required / not_found / language_unsupported)
```

---

## STAGE 2 — Coding

```
INPUT: corpus_segments.csv, coding manual (frozen post-pilot)
OUTPUT: codings.csv (long form: one row per coding application)
        columns: coding_id, segment_id, coder_id, area, competence,
                 depth, timestamp, notes

procedure assign_segments_to_coders():
    # Locked-in protocol (Variant B per strategy_memo §6):
    # 20% double-coded a priori + 80% single-coded with rotation,
    # uncertainty-flag escalation, and milestone κ recalculation.

    set.seed(20240901)                                # INV-14: snapshot date

    # B1 — A priori sampling
    reliability_subset = stratified_random_sample(
                            corpus_segments,
                            strata = (degree, layer),
                            fraction = 0.20)
    deposit reliability_subset to OSF                 # pre-registration package

    # Double-code the reliability subset
    for each segment in reliability_subset:
        assign to coder_1 AND coder_2                 # full double coding (20%)

    # B2 — Single-code the remainder with rotation
    remainder = corpus_segments \ reliability_subset
    rotated = balanced_rotation_assignment(
                  remainder,
                  coders = {coder_1, coder_2},
                  balance_across = (degree, layer))   # ~50/50 within each cell
    for each segment in rotated:
        assign to its assigned single coder

    # B2 — Uncertainty-flag escalation rule
    procedure on_uncertainty_flag(segment, primary_coder):
        # Triggered whenever a single coder marks a segment
        # as "boundary case" or "ambiguous"
        secondary_coder = the other coder
        assign segment to secondary_coder
        log to uncertainty_escalation_log
        # Resulting double coding feeds into the κ recalc.

procedure milestone_kappa_recalculation():
    # B3 — Recompute κ at 25%, 50%, 75% completion of MAIN coding
    for milestone in {0.25, 0.50, 0.75}:
        wait_until(fraction_of_main_coding_complete >= milestone)
        cumulative_double_coded = reliability_subset
                                 ∪ uncertainty_escalations_to_date
        for each area in 1..6:
            kappa[area, milestone] = cohen_kappa(...)
        if any kappa[area, milestone] < 0.70:
            HALT all coding
            review manual against disagreement_log
            recalibrate manual if needed
            recode affected segments
            log deviation to OSF_deviations.md
        else:
            continue coding

procedure llm_assisted_prescreen [OPTIONAL, FLAGGED]:
    # If used: an LLM (e.g., GPT-4 or Claude) flags segments LIKELY to invoke
    # an MRCDD area. Human coders then code the flagged segments, plus a
    # random sample of unflagged segments to estimate the LLM's recall.
    # MUST BE FLAGGED in the methods section if used.
    # MUST report LLM's precision/recall against human coding on a holdout.

procedure code_segment(segment, coder):
    # Coder reads segment, applies manual:
    #   1. Determine if any MRCDD area is invoked.
    #   2. If yes, assign to area(s) — at most one competence per area.
    #   3. Assign depth (0/1/2/3) per the rubric.
    #   4. If single-coder mode AND segment is a boundary/ambiguous case,
    #      raise on_uncertainty_flag(segment, coder).
    #   5. Log notes for any boundary case.
    # Output: 0 or more (area, competence, depth) tuples per (segment, coder).
    write to codings.csv
```

---

## STAGE 3 — Reliability

```
INPUT: codings.csv, restricted to the cumulative double-coded set
       (= a-priori 20% reliability subsample + uncertainty-flag escalations)
OUTPUT: reliability_table.csv (final), kappa_trajectory.csv (milestones)

procedure compute_reliability(double_coded_set):
    for each area in 1..6:
        # Binary presence reliability
        presence_coder1[area] = vector of {0,1} per segment in double_coded_set
        presence_coder2[area] = vector of {0,1} per segment in double_coded_set
        kappa_presence[area] = cohen_kappa(presence_coder1, presence_coder2)
        # Ordinal depth reliability (where both coders mark presence)
        depth_coder1[area] = vector of {1,2,3}
        depth_coder2[area] = vector of {1,2,3}
        weighted_kappa_depth[area] = cohen_kappa_weighted(depth_coder1, depth_coder2,
                                                         weights="linear")
    krippendorff_alpha_overall = krippendorff_alpha(double_coded_set, metric="ordinal")
    disagreement_rate = count(disagreements) / count(double_coded_set)
    return (kappa_presence, weighted_kappa_depth, krippendorff_alpha_overall,
            disagreement_rate)

# Called from milestone_kappa_recalculation in STAGE 2 at 25/50/75%
# Final call after main coding completes:
final_reliability = compute_reliability(all_double_coded_segments)
write final_reliability to reliability_table.csv
write per-milestone kappa to kappa_trajectory.csv
write per-coder uncertainty-flag rate (B2) to uncertainty_log.csv

assertion: final kappa_presence[area] >= 0.70 for ALL areas
           AND no milestone halt was unresolved;
           else BLOCK and re-pilot.
```

---

## STAGE 4 — Aggregation

```
INPUT: codings.csv (post-reliability resolution)
OUTPUT: programme_layer_area.csv (one row per (programme, layer, area))
        columns: programme_id, degree, layer, area,
                 presence (0/1), depth (0..3),
                 num_courses_touching_area (NA for memoria),
                 num_segments_coding_area

procedure aggregate_to_programme_layer_area():
    for each (programme, layer, area):
        # Layer 1 (memoria): collapse over segments
        # Layer 2 (guia): collapse over courses (which collapse over segments)
        if layer == "memoria":
            relevant_codings = codings where programme_id, layer, area match
            presence = max(presence over relevant_codings)        # 0 or 1
            depth = max(depth over relevant_codings)              # 0..3
            num_segments = count(relevant_codings where presence==1)
        else:  # layer == "guia"
            for each course c in programme:
                course_presence[c] = max(presence over codings(c, area))
                course_depth[c] = max(depth over codings(c, area))
            presence = max(course_presence) over c
            depth = max(course_depth) over c
            num_courses_touching_area = sum(course_presence > 0)
        write row

procedure aggregate_to_degree_layer_area():
    for each (degree, layer, area):
        progs = programmes where degree, layer match
        coverage(degree, layer, area) = mean(presence over progs)
        mean_depth(degree, layer, area) = mean(depth over progs)
        # Bootstrap 95% CI
        for b in 1..1000:
            resampled = sample(progs, replace=TRUE)
            cov_b[b] = mean(presence over resampled)
            depth_b[b] = mean(depth over resampled)
        ci_coverage = quantile(cov_b, [0.025, 0.975])
        ci_depth = quantile(depth_b, [0.025, 0.975])
        write to degree_layer_area.csv
```

---

## STAGE 5 — Comparative analyses

```
procedure layer_gap_analysis():
    for each (programme, degree, area):
        m = presence in memoria layer
        g = presence in guia layer
        category[programme, degree, area] =
            "both"        if m==1 and g==1
            "memoria_only" if m==1 and g==0
            "guia_only"    if m==0 and g==1
            "neither"      if m==0 and g==0
    cross_tab = tabulate categories per area
    layer_gap_rate[area] = P(memoria_only) + P(guia_only)
    write layer_gap_table.csv

procedure degree_gap_analysis():
    for each university u offering both degrees:
        for each (layer, area):
            paired data: (presence_Infantil[u, layer, area],
                          presence_Primaria[u, layer, area])
    for each (layer, area):
        mcnemar_test on paired binary presence
        wilcoxon_signed_rank on paired depth
        report: median paired difference, effect-size r
    write degree_gap_table.csv
    # Note: p-values reported descriptively, not as causal hypothesis tests.

procedure system_variation():
    for each (degree, layer, area):
        sd = sd(presence over programmes)
        iqr_depth = IQR(depth over programmes)
    write system_variation.csv

procedure sub_analyses():
    for stratifier in {sector, modality, autonomous_community, course_subject}:
        for each (degree, layer, area, stratum_value):
            if n_programmes_in_stratum >= 5:
                report coverage, depth, with bootstrap CI
            else:
                report n only, suppress estimate
    write sub_analyses.csv
```

---

## STAGE 6 — Outputs (figures and tables)

```
procedure produce_outputs():
    # Coverage tables (main text)
    table_coverage_per_degree_layer_area     # 6 areas × 4 cells (2 degrees × 2 layers)
    table_depth_per_degree_layer_area        # same shape, with CI
    table_layer_gap_per_area                 # 6 rows × 5 cols (4 categories + gap rate)
    table_degree_paired_comparison           # per area, paired stats

    # Coverage tables (appendix)
    table_competence_level_coverage          # 23 competences × 4 cells

    # Heatmaps
    heatmap_university_x_area_facet_degree_layer
        # x = area (1..6), y = university, fill = depth, facet = degree × layer

    # Radar plots
    radar_per_degree_layer
        # 6 axes (areas), one polygon per layer (memoria vs. guia overlaid),
        # separate plot per degree (Infantil, Primaria)

    # Reliability
    table_reliability                        # κ per area + overall Krippendorff α

    save to: paper/tables/ and paper/figures/
    # Per INV-13: scripts export bare tabular environments;
    # paper main.tex wraps them with threeparttable / talltblr.
```

---

## STAGE 7 — Falsification / sanity (see `falsification_tests.md`)

```
procedure run_falsification():
    test_1_pre_2022_memoria_no_mrcdd_label   # if any pre-2022 memoria exists
    test_2_non_digital_subjects_zero_coding
    test_3_logical_bound_memoria_vs_guia_union
    test_4_synonym_substantive_paired_check
    write falsification_results.csv
```

---

## Reproducibility constraints (per content-invariants.md)

- INV-14: `set.seed(20240901)` once at the top of the main analysis script (date = the snapshot date).
- INV-15: All packages loaded at top.
- INV-16: All paths via `here::here()` (R) or `pathlib.Path` (Python).
- INV-17: No growing vectors in loops; pre-allocate or vectorize.
- INV-18: Outputs to `paper/tables/`, `paper/figures/`, and `data/cleaned/` per by-script organization.
- INV-19: No `setwd()`, no `rm(list=ls())`, no `install.packages()` in scripts.

---

## Hand-off to coder

The coder receives:
1. This pseudo-code.
2. The frozen coding manual (separate artifact).
3. The `corpus_inventory.csv` from `/discover data`.
4. The reliability target (κ ≥ 0.70 per area).
5. The output schema for `paper/tables/` and `paper/figures/`.

The coder produces R/Python scripts, runs them, exports tables and figures, and hands the outputs back for the writer to incorporate.
