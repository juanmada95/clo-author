-- ============================================================================
-- Migration 002 — Analysis views
-- Implements the SQL-tractable parts of pseudo-code Stages 4–5.
-- Bootstrap CIs, Cohen's / weighted κ, and Krippendorff's α stay in R
-- (scripts/R/...) — SQL only produces the tidy inputs those scripts consume.
--
-- All views use security_invoker so the querying user's RLS applies, not the
-- view owner's — required for correct row-level scoping under Supabase auth.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Denormalised coding rows — convenient for export and ad-hoc analysis.
-- ----------------------------------------------------------------------------
create view v_coding_full
with (security_invoker = on) as
select
    c.coding_id,
    c.segment_id,
    s.programme_id,
    p.university_name,
    p.degree,
    p.sector,
    p.modality,
    p.ccaa,
    p.in_tier_b,
    s.layer,
    s.course_id,
    c.coder_id,
    cd.role        as coder_role,
    c.area_id,
    a.name_es      as area_name_es,
    c.competence_id,
    mc.code        as competence_code,
    c.depth,
    c.is_uncertain,
    c.notes,
    c.created_at
from coding c
join segment          s  on s.segment_id     = c.segment_id
join programme        p  on p.programme_id    = s.programme_id
join coder            cd on cd.coder_id       = c.coder_id
join mrcdd_area       a  on a.area_id         = c.area_id
left join mrcdd_competence mc on mc.competence_id = c.competence_id;

-- ----------------------------------------------------------------------------
-- Stage 4 — programme × layer × area aggregation.
-- Full grid: every (programme, layer) that exists in the corpus is crossed
-- with all six areas so absent areas surface as presence 0, depth 0.
-- presence = any coding with depth >= 1; depth = max depth (collapse rule).
-- ----------------------------------------------------------------------------
create view v_programme_layer_area
with (security_invoker = on) as
with programme_layer as (
    select distinct programme_id, layer from segment
),
grid as (
    select pl.programme_id, pl.layer, a.area_id
    from programme_layer pl
    cross join mrcdd_area a
),
agg as (
    select
        s.programme_id,
        s.layer,
        c.area_id,
        max((c.depth >= 1)::int)   as presence,
        max(c.depth)               as depth,
        count(*)                   as n_codings
    from coding c
    join segment s on s.segment_id = c.segment_id
    group by s.programme_id, s.layer, c.area_id
)
select
    g.programme_id,
    p.degree,
    g.layer,
    g.area_id,
    coalesce(agg.presence, 0)  as presence,
    coalesce(agg.depth, 0)     as depth,
    coalesce(agg.n_codings, 0) as n_codings
from grid g
join programme p    on p.programme_id = g.programme_id
left join agg       on agg.programme_id = g.programme_id
                    and agg.layer       = g.layer
                    and agg.area_id      = g.area_id;

-- ----------------------------------------------------------------------------
-- Stage 4 — degree × layer × area coverage (point estimates).
-- Bootstrap 95% CIs are computed in R from v_programme_layer_area.
-- ----------------------------------------------------------------------------
create view v_coverage_by_degree_layer_area
with (security_invoker = on) as
select
    degree,
    layer,
    area_id,
    avg(presence::numeric) as coverage,
    avg(depth::numeric)    as mean_depth,
    count(*)               as n_programmes
from v_programme_layer_area
group by degree, layer, area_id;

-- ----------------------------------------------------------------------------
-- Reliability helper — segments coded by two or more distinct coders.
-- Feeds Cohen's κ / weighted κ / Krippendorff's α computation in R
-- (pseudo-code Stage 3, cumulative double-coded set).
-- ----------------------------------------------------------------------------
create view v_double_coded_segment
with (security_invoker = on) as
select
    c.segment_id,
    count(distinct c.coder_id) as n_coders
from coding c
group by c.segment_id
having count(distinct c.coder_id) >= 2;
