# Supabase database — MRCDD curricular-coding pipeline

Relational backend for the coding workflow described in
`quality_reports/strategy/cdd_formacion_inicial/pseudo_code.md` (Stages 0–5).
It holds the corpus, the MRCDD reference framework, and the per-coder codings,
with row-level security so each coder only touches their own work.

Remote project: `https://hxvixhuapkpsqbphyyxd.supabase.co`
(project ref `hxvixhuapkpsqbphyyxd`).

## Schema at a glance

```
mrcdd_area (6) ──1:N──▶ mrcdd_competence (23)
                              ▲ (competence_id, area_id)  ── composite FK ──┐
programme (174) ──1:N──▶ segment ──1:N──▶ coding ─────────────────────────┘
   in_tier_b (60)          layer:            (segment, coder, area) unique
                           memoria / guia    depth 0–3, is_uncertain flag
coder (lead / coder) ──▶ coding, coding_assignment
```

| Table | Rows seeded | Purpose |
|-------|-------------|---------|
| `mrcdd_area` | 6 | DigCompEdu/MRCDD areas (canonical ES/EN labels) |
| `mrcdd_competence` | 23 | MRCDD competences, nested in areas (Area 1 = 5, per BOE-A-2022-8042) |
| `programme` | 174 | `corpus_inventory.csv`; `in_tier_b` flags the n=60 sample |
| `coder` | 2 (placeholder) | Human coders; link `auth_user_id` after inviting users |
| `segment` | — | One codable text unit (Stage 1); memoria (no course) or guía |
| `coding_assignment` | — | Variant B assignment plan (double / single / escalation) |
| `coding` | — | One row per (segment, coder, area); `depth` 0–3, uncertainty flag |

### Views (Stages 4–5, SQL-tractable parts)

- `v_coding_full` — denormalised codings joined to programme/area/competence.
- `v_programme_layer_area` — presence/depth collapsed to (programme, layer, area), full 6-area grid.
- `v_coverage_by_degree_layer_area` — coverage and mean depth point estimates.
- `v_double_coded_segment` — segments with ≥2 coders (input to reliability in R).

Bootstrap CIs, Cohen's/weighted κ, and Krippendorff's α stay in R
(`scripts/R/…`); the views only produce their tidy inputs.

## Row-level security

RLS is on for every table. Identity resolves via `coder.auth_user_id = auth.uid()`.

- Reference + corpus tables: readable by any authenticated member; writable only by a **lead**.
- `coding` / `coding_assignment`: a coder reads and edits **only their own** rows; a lead reads all.
- `anon` (unauthenticated) sees nothing.

Helpers: `current_coder_id()`, `is_lead()`.

## Applying

With the [Supabase CLI](https://supabase.com/docs/guides/cli):

```bash
supabase link --project-ref hxvixhuapkpsqbphyyxd   # prompts for the DB password
supabase db push                                   # applies migrations/ in order
# seed.sql runs automatically on `supabase db reset` (local dev);
# to load the corpus into the remote, run seed.sql once via the SQL editor or psql.
```

Or paste each file in `migrations/` (then `seed.sql`) into the Supabase SQL editor, in filename order.

Migrations are ordered by timestamp:

1. `20260709120000_schema.sql` — enums, tables, indexes, constraints, trigger
2. `20260709120100_views.sql` — analysis views (`security_invoker`)
3. `20260709120200_rls.sql` — helper functions, policies, grants
4. `20260709120300_reference_seed.sql` — MRCDD areas + competences (canonical, idempotent)

## Regenerating the seed

`seed.sql` is generated — do not hand-edit. After the corpus CSVs change:

```bash
python scripts/python/db/generate_seed.py
```

## Caveats

- **After linking**, confirm `[db] major_version` in `config.toml` matches the remote Postgres version.
- **Coder identity**: seeded coders have no `auth_user_id`. Invite each coder as a Supabase auth user, then
  `update coder set auth_user_id = '<uuid>' where coder_id = …;` or RLS will grant them nothing.
- **Competence labels**: `name_es` in the reference seed follows the best available MRCDD transcription —
  verify verbatim against BOE-A-2022-8042 (pp. 7 ff.) before quoting in the manuscript.
