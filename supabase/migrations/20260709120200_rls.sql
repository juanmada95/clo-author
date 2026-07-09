-- ============================================================================
-- Migration 003 — Row Level Security
-- Model:
--   * Reference/corpus data (areas, competences, programmes, segments) is
--     readable by any authenticated project member; writable only by a lead.
--   * A coder sees and edits only their OWN codings and assignments.
--   * A lead sees everything.
--   * anon (unauthenticated) sees nothing.
-- Identity is resolved via coder.auth_user_id = auth.uid().
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Identity helpers. security definer so they can read `coder` regardless of
-- the caller's RLS; search_path pinned to avoid hijacking.
-- ----------------------------------------------------------------------------
create or replace function current_coder_id()
returns smallint
language sql
stable
security definer
set search_path = public
as $$
    select coder_id from coder where auth_user_id = auth.uid() and active;
$$;

create or replace function is_lead()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1 from coder
        where auth_user_id = auth.uid() and role = 'lead' and active
    );
$$;

-- ----------------------------------------------------------------------------
-- Enable RLS everywhere.
-- ----------------------------------------------------------------------------
alter table mrcdd_area        enable row level security;
alter table mrcdd_competence  enable row level security;
alter table coder             enable row level security;
alter table programme         enable row level security;
alter table segment           enable row level security;
alter table coding_assignment enable row level security;
alter table coding            enable row level security;

-- ----------------------------------------------------------------------------
-- Reference framework: read for all authenticated, write for leads.
-- ----------------------------------------------------------------------------
create policy mrcdd_area_read   on mrcdd_area  for select to authenticated using (true);
create policy mrcdd_area_write  on mrcdd_area  for all    to authenticated using (is_lead()) with check (is_lead());

create policy mrcdd_comp_read   on mrcdd_competence for select to authenticated using (true);
create policy mrcdd_comp_write  on mrcdd_competence for all    to authenticated using (is_lead()) with check (is_lead());

-- ----------------------------------------------------------------------------
-- Coders: team is visible to authenticated members; only leads manage it.
-- ----------------------------------------------------------------------------
create policy coder_read  on coder for select to authenticated using (true);
create policy coder_write on coder for all    to authenticated using (is_lead()) with check (is_lead());

-- ----------------------------------------------------------------------------
-- Corpus (programmes, segments): read for all authenticated, write for leads.
-- ----------------------------------------------------------------------------
create policy programme_read  on programme for select to authenticated using (true);
create policy programme_write on programme for all    to authenticated using (is_lead()) with check (is_lead());

create policy segment_read  on segment for select to authenticated using (true);
create policy segment_write on segment for all    to authenticated using (is_lead()) with check (is_lead());

-- ----------------------------------------------------------------------------
-- Assignments: a coder sees their own; leads see and manage all.
-- ----------------------------------------------------------------------------
create policy assignment_read on coding_assignment for select to authenticated
    using (is_lead() or coder_id = current_coder_id());
create policy assignment_write on coding_assignment for all to authenticated
    using (is_lead()) with check (is_lead());

-- ----------------------------------------------------------------------------
-- Codings: a coder reads/writes only their own rows; leads read all and may
-- delete (e.g. to purge a withdrawn coder). Coders cannot forge another
-- coder_id (the WITH CHECK pins it to their own id).
-- ----------------------------------------------------------------------------
create policy coding_read on coding for select to authenticated
    using (is_lead() or coder_id = current_coder_id());
create policy coding_insert on coding for insert to authenticated
    with check (coder_id = current_coder_id());
create policy coding_update on coding for update to authenticated
    using (coder_id = current_coder_id())
    with check (coder_id = current_coder_id());
create policy coding_delete on coding for delete to authenticated
    using (is_lead() or coder_id = current_coder_id());

-- ----------------------------------------------------------------------------
-- Privileges. RLS gates rows; grants gate the operation. authenticated only —
-- anon gets nothing (no policies + no grants).
-- ----------------------------------------------------------------------------
grant usage on schema public to authenticated;
grant select, insert, update, delete on
    mrcdd_area, mrcdd_competence, coder, programme, segment,
    coding_assignment, coding
    to authenticated;
grant select on
    v_coding_full, v_programme_layer_area,
    v_coverage_by_degree_layer_area, v_double_coded_segment
    to authenticated;
grant execute on function current_coder_id(), is_lead() to authenticated;
