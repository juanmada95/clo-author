-- ============================================================================
-- Migration 001 — Core schema
-- Project: Competencia Digital Docente en la Formación Inicial del Profesorado
-- Purpose: Relational store for the MRCDD curricular-coding pipeline
--          (Stages 0–5 of quality_reports/strategy/.../pseudo_code.md).
--
-- Entity model:
--   programme  ── has many ──▶ segment ── coded by ──▶ coding (per coder, per area)
--   mrcdd_area ── has many ──▶ mrcdd_competence
--   coder      ── makes ─────▶ coding / coding_assignment
--
-- All coding is long-form: one `coding` row per (segment, coder, area).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Enumerated domains (categorical values observed in data/cleaned/*.csv)
-- ----------------------------------------------------------------------------
create type degree_type      as enum ('infantil', 'primaria');
create type doc_layer        as enum ('memoria', 'guia');
create type sector_type      as enum ('public', 'private-traditional', 'private-online', 'adscrito');
create type modality_type    as enum ('presencial', 'online');
create type coder_role       as enum ('lead', 'coder');
create type coding_mode      as enum ('double', 'single', 'escalation');
create type retrieval_status as enum ('pending', 'retrieved', 'login_required', 'not_found', 'language_unsupported');

-- ----------------------------------------------------------------------------
-- MRCDD reference framework (BOE-A-2022-8042): 6 areas, 23 competences.
-- Seeded in migration 20260709120300_reference_seed.sql.
-- ----------------------------------------------------------------------------
create table mrcdd_area (
    area_id  smallint primary key check (area_id between 1 and 6),
    name_es  text not null,
    name_en  text not null
);
comment on table mrcdd_area is 'The six MRCDD / DigCompEdu competence areas.';

create table mrcdd_competence (
    competence_id smallint  primary key check (competence_id between 1 and 23),
    area_id       smallint  not null references mrcdd_area (area_id),
    code          text      not null unique,           -- e.g. '1.1'
    name_es       text      not null,
    -- Composite target so `coding` can enforce competence-belongs-to-area.
    unique (competence_id, area_id)
);
comment on table mrcdd_competence is 'The 23 MRCDD competences, nested within areas. MRCDD adds one competence in Area 1 vs DigCompEdu''s 22.';

-- ----------------------------------------------------------------------------
-- Coders. auth_user_id links a Supabase auth user to a coder for RLS.
-- coder_id kept small and human-facing (1, 2, [3]) to match the pseudo-code.
-- ----------------------------------------------------------------------------
create table coder (
    coder_id     smallint    primary key check (coder_id > 0),
    display_name text        not null,
    role         coder_role  not null default 'coder',
    auth_user_id uuid        unique references auth.users (id) on delete set null,
    active       boolean     not null default true,
    created_at   timestamptz not null default now()
);
comment on table coder is 'Human coders. Link auth_user_id after inviting the user to the project so RLS can scope their codings.';

-- ----------------------------------------------------------------------------
-- Programmes (corpus_inventory.csv). One row per accredited degree programme.
-- ----------------------------------------------------------------------------
create table programme (
    programme_id    text          primary key,          -- 'P0001'
    codigo_ruct     text,
    university_name text          not null,
    sector          sector_type   not null,
    ccaa            text          not null,
    modality        modality_type not null,
    degree          degree_type   not null,
    centro          text,
    sources         text,
    sources_count   integer,
    ruct_anchored   boolean       not null default false,
    fallback_flag   text,
    in_tier_b       boolean       not null default false, -- membership in the n=60 stratified sample
    created_at      timestamptz   not null default now()
);
comment on column programme.in_tier_b is 'TRUE for the 60 programmes in the Tier B primary analysis sample (tier_b_sample_ids.csv).';

create index programme_degree_idx   on programme (degree);
create index programme_sector_idx   on programme (sector);
create index programme_ccaa_idx     on programme (ccaa);
create index programme_tier_b_idx   on programme (in_tier_b) where in_tier_b;

-- ----------------------------------------------------------------------------
-- Segments (corpus_segments): one codable unit of text.
-- Layer 1 = memoria (course_id NULL); Layer 2 = guia docente (course_id set).
-- ----------------------------------------------------------------------------
create table segment (
    segment_id       text            primary key,        -- e.g. 'P0001-M-0001'
    programme_id     text            not null references programme (programme_id) on delete cascade,
    layer            doc_layer       not null,
    course_id        text,                                -- NULL for memoria
    section          text,
    segment_text     text            not null,
    language         text            not null default 'es',
    retrieval_status retrieval_status not null default 'retrieved',
    created_at       timestamptz     not null default now(),
    -- A memoria segment belongs to no course.
    constraint segment_memoria_no_course check (layer <> 'memoria' or course_id is null)
);
comment on table segment is 'Long-form corpus: one row per codable text segment, per pseudo-code Stage 1.';

create index segment_programme_idx on segment (programme_id);
create index segment_layer_idx     on segment (layer);
create index segment_course_idx    on segment (programme_id, course_id) where course_id is not null;

-- ----------------------------------------------------------------------------
-- Coding assignments (Stage 2): which coder is responsible for which segment,
-- and whether the segment is in the a-priori reliability (double-coded) subset.
-- ----------------------------------------------------------------------------
create table coding_assignment (
    assignment_id       bigint      generated always as identity primary key,
    segment_id          text        not null references segment (segment_id) on delete cascade,
    coder_id            smallint    not null references coder (coder_id),
    mode                coding_mode not null,
    in_reliability_subset boolean   not null default false,
    assigned_at         timestamptz not null default now(),
    unique (segment_id, coder_id)
);
comment on table coding_assignment is 'Variant B assignment plan: 20% double-coded reliability subset + 80% single with uncertainty escalation.';

create index coding_assignment_coder_idx on coding_assignment (coder_id);

-- ----------------------------------------------------------------------------
-- Codings (Stage 2 output): one row per (segment, coder, area).
-- depth: 0 absent · 1 mentioned · 2 developed · 3 assessed.
-- At most one competence per area per coder per segment.
-- ----------------------------------------------------------------------------
create table coding (
    coding_id     bigint      generated always as identity primary key,
    segment_id    text        not null references segment (segment_id) on delete cascade,
    coder_id      smallint    not null references coder (coder_id),
    area_id       smallint    not null references mrcdd_area (area_id),
    competence_id smallint,
    depth         smallint    not null check (depth between 0 and 3),
    is_uncertain  boolean     not null default false,  -- B2 uncertainty flag → escalation
    notes         text,
    created_at    timestamptz not null default now(),
    updated_at    timestamptz not null default now(),
    unique (segment_id, coder_id, area_id),
    -- When a competence is given it must belong to the coded area (MATCH SIMPLE:
    -- skipped when competence_id is NULL, i.e. area-only codings).
    foreign key (competence_id, area_id)
        references mrcdd_competence (competence_id, area_id)
);
comment on table coding is 'One coding application per (segment, coder, area) per pseudo-code Stage 2.';

create index coding_segment_idx    on coding (segment_id);
create index coding_coder_idx      on coding (coder_id);
create index coding_area_idx       on coding (area_id);
create index coding_uncertain_idx  on coding (is_uncertain) where is_uncertain;

-- ----------------------------------------------------------------------------
-- Keep coding.updated_at fresh on edits.
-- ----------------------------------------------------------------------------
create or replace function set_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at := now();
    return new;
end;
$$;

create trigger coding_set_updated_at
    before update on coding
    for each row
    execute function set_updated_at();
