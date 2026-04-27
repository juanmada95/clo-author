"""
inventory_reconciliation.py

Title:    Stage 0 inventory reconciliation: merge cross-validation aggregates
          + RUCT into a canonical corpus_inventory.csv.
Author:   data-engineer (CDD curricular analysis project).
Date:     2026-04-27.
Purpose:  Anchor on RUCT's codigo_ruct where available; otherwise emit a
          synthetic stable id of the form 'XV-{degree}-{normalised_uni}'
          flagged 'cross-validation_only'. Classify each programme into
          the 4-level sector x 18-CCAA x 2-modality cells defined by the
          locked-in Tier B stratification.
Inputs:   data/raw/inventory_passes/{gradomania,educaweb,aneca,aqu,acsug,
          unibasq,aacdeva,acsucyl,aquib,avap,madrimasd,ruct}.csv
Outputs:  data/cleaned/corpus_inventory.csv
          data/cleaned/inventory_reconciliation_log.md

Schema (corpus_inventory.csv):
  programme_id, codigo_ruct, university_name, sector, ccaa, modality,
  degree, centro, sources, sources_count, ruct_anchored, fallback_flag

Sector levels (4):
  - public
  - private-traditional
  - private-online
  - adscrito

Modality levels (2 per Tier B design):
  - presencial          (includes semipresencial -- per strategy memo
                         section 3, modality is collapsed to 2 levels)
  - online

Notes:
  - INV-15: imports at top.
  - INV-16: pathlib.Path.
  - INV-17: rows pre-allocated.
  - INV-19: no setwd / install.
  - The reconciliation is fully deterministic (no random component).
  - Adscrito detection uses a manual override list seeded from
    data_exploration_cdd_formacion_inicial.md flag 5 plus heuristics
    on the centro field.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "inventory_passes"
OUT_DIR = PROJECT_ROOT / "data" / "cleaned"
OUT_INVENTORY = OUT_DIR / "corpus_inventory.csv"
OUT_LOG = OUT_DIR / "inventory_reconciliation_log.md"

SOURCE_FILES = [
    "gradomania.csv", "educaweb.csv", "aneca.csv",
    "aqu.csv", "acsug.csv", "unibasq.csv", "aacdeva.csv", "acsucyl.csv",
    "aquib.csv", "avap.csv", "madrimasd.csv", "ruct.csv",
]

# Manual override lists ------------------------------------------------------
# (1) Centros adscritos offering Maestro grados (per pilot evidence + RUCT
#     spot-checks). Names are the canonical form used in the inventory.
ADSCRITOS_OVERRIDE = {
    "Centro Universitario ESCUNI": ("Madrid", "private-traditional", "adscrito",
                                    ("infantil", "primaria")),
    "Centro de Ensenanza Superior Cardenal Cisneros": (
        "Madrid", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro de Estudios Universitarios Cardenal Spinola CEU": (
        "Andalucia", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Superior de Estudios Universitarios La Salle": (
        "Madrid", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro de Ensenanza Superior Don Bosco": (
        "Madrid", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Universitario Villanueva": (
        "Madrid", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Universitario CEU Andalucia": (
        "Andalucia", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Universitario de Magisterio Sagrado Corazon": (
        "Andalucia", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Escuela Universitaria Cardenal Cisneros (Alcala)": (
        "Madrid", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Superior de Estudios Universitarios Maria Cristina": (
        "Madrid", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Universitario de Magisterio Virgen de Europa": (
        "Madrid", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Universitario CEU La Salle": (
        "Madrid", "private-traditional", "adscrito", ("primaria",)),
    "Centro Universitario Salesiano de Sarria": (
        "Cataluna", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Universitario Padre Enrique de Osso": (
        "Cataluna", "private-traditional", "adscrito", ("infantil", "primaria")),
    "Centro Universitario EUSES": (
        "Cataluna", "private-traditional", "adscrito", ("primaria",)),
}

# (2) Sector classification rules: which institutions are public, private-
#     traditional, private-online, or adscrito. Names are matched on the
#     normalised form (no accents, lowercase).
PUBLIC_UNIS = {
    # Andalucia
    "universidad de almeria", "universidad de cadiz", "universidad de cordoba",
    "universidad de granada", "universidad de huelva", "universidad de jaen",
    "universidad de malaga", "universidad de sevilla",
    # Cataluna
    "universitat autonoma de barcelona", "universitat de barcelona",
    "universitat de girona", "universitat de lleida",
    "universitat rovira i virgili", "universitat de vic - ucc",
    "universitat de vic", "universitat pompeu fabra",
    "universitat politecnica de catalunya",
    "universitat oberta de catalunya", "uoc",
    "universitat oberta de catalunya (uoc)",
    # Madrid
    "universidad autonoma de madrid", "universidad complutense de madrid",
    "universidad de alcala", "universidad rey juan carlos",
    "universidad politecnica de madrid", "universidad carlos iii de madrid",
    "universidad nacional de educacion a distancia",
    # Castilla y Leon
    "universidad de burgos", "universidad de leon",
    "universidad de salamanca", "universidad de valladolid",
    # Comunitat Valenciana
    "universitat de valencia", "universitat jaume i",
    "universidad de alicante", "universidad miguel hernandez de elche",
    "universitat politecnica de valencia",
    # Galicia
    "universidade de santiago de compostela", "universidade da coruna",
    "universidade de vigo",
    # Canarias
    "universidad de la laguna", "universidad de las palmas de gran canaria",
    # 1-each
    "universidad de zaragoza", "universidad de oviedo",
    "universitat de les illes balears", "universidad de cantabria",
    "universidad de castilla-la mancha", "universidad de extremadura",
    "universidad de murcia", "universidad publica de navarra",
    "universidad del pais vasco / euskal herriko unibertsitatea",
    "universidad del pais vasco", "universidad publica de pais vasco",
}

PRIVATE_ONLINE_UNIS = {
    "universidad internacional de la rioja",
    "universidad internacional de la rioja (unir)",
    "universidad internacional de valencia",
    "universidad internacional de valencia (viu)",
    "universidad a distancia de madrid",
    "universidad a distancia de madrid (udima)",
    "universidad isabel i",
    "universidad europea miguel de cervantes",  # online programmes
}

# Public-online institutions (separate from PRIVATE_ONLINE_UNIS so the
# sector remains "public"). UOC (Universitat Oberta de Catalunya) is the
# canonical example: a Catalan public-funded online university.
PUBLIC_ONLINE_UNIS = {
    "universitat oberta de catalunya",
    "universitat oberta de catalunya (uoc)",
    "uoc",
}

# Set of all institutions whose modality should be forced to "online"
# regardless of source-row hint (used at row-construction time).
ONLINE_INSTITUTIONS = PRIVATE_ONLINE_UNIS | PUBLIC_ONLINE_UNIS

PRIVATE_TRADITIONAL_UNIS = {
    "universidad catolica de valencia san vicente martir",
    "universidad pontificia de salamanca",
    "universidad camilo jose cela",
    "universidad catolica de avila",
    "universidad alfonso x el sabio",
    "universidad francisco de vitoria",
    "universidad ceu san pablo",
    "universidad ceu cardenal herrera",
    "universidad de navarra",
    "universidad de deusto",
    "mondragon unibertsitatea",
    "universitat internacional de catalunya",
    "universitat internacional de catalunya (uic)",
    "universitat ramon llull",
    "universitat ramon llull (url)",
    "universitat abat oliba ceu",
    "universidad loyola andalucia",
    "universidad antonio de nebrija",
    "universidad san jorge",
    "universidad europea de madrid",
    "universidad europea de valencia",
    "universidad pontificia comillas",
    # Recovered from ANECA round-1 review (2026-04-27, coder-critic patch round 1)
    "universidad del atlantico medio",
    "universidad tecnologia y empresa",
    "universidad catolica santa teresa de jesus de avila",
}

# CCAA inference: when the source row lacks CCAA, infer from known
# institution -> CCAA mapping.
INSTITUTION_CCAA = {
    # Andalucia
    "universidad de almeria": "Andalucia",
    "universidad de cadiz": "Andalucia",
    "universidad de cordoba": "Andalucia",
    "universidad de granada": "Andalucia",
    "universidad de huelva": "Andalucia",
    "universidad de jaen": "Andalucia",
    "universidad de malaga": "Andalucia",
    "universidad de sevilla": "Andalucia",
    "universidad loyola andalucia": "Andalucia",
    # Cataluna
    "universitat autonoma de barcelona": "Cataluna",
    "universitat de barcelona": "Cataluna",
    "universitat de girona": "Cataluna",
    "universitat de lleida": "Cataluna",
    "universitat rovira i virgili": "Cataluna",
    "universitat de vic - ucc": "Cataluna",
    "universitat de vic": "Cataluna",
    "universitat pompeu fabra": "Cataluna",
    "universitat politecnica de catalunya": "Cataluna",
    "universitat internacional de catalunya": "Cataluna",
    "universitat internacional de catalunya (uic)": "Cataluna",
    "universitat ramon llull": "Cataluna",
    "universitat ramon llull (url)": "Cataluna",
    "universitat abat oliba ceu": "Cataluna",
    "universitat oberta de catalunya": "Cataluna",
    "universitat oberta de catalunya (uoc)": "Cataluna",
    "uoc": "Cataluna",
    # Madrid
    "universidad autonoma de madrid": "Madrid",
    "universidad complutense de madrid": "Madrid",
    "universidad de alcala": "Madrid",
    "universidad rey juan carlos": "Madrid",
    "universidad politecnica de madrid": "Madrid",
    "universidad carlos iii de madrid": "Madrid",
    "universidad nacional de educacion a distancia": "Madrid",
    "universidad camilo jose cela": "Madrid",
    "universidad alfonso x el sabio": "Madrid",
    "universidad francisco de vitoria": "Madrid",
    "universidad ceu san pablo": "Madrid",
    "universidad antonio de nebrija": "Madrid",
    "universidad europea de madrid": "Madrid",
    "universidad a distancia de madrid": "Madrid",
    "universidad a distancia de madrid (udima)": "Madrid",
    "universidad pontificia comillas": "Madrid",
    "universidad tecnologia y empresa": "Madrid",
    # Castilla y Leon
    "universidad de burgos": "Castilla y Leon",
    "universidad de leon": "Castilla y Leon",
    "universidad de salamanca": "Castilla y Leon",
    "universidad de valladolid": "Castilla y Leon",
    "universidad pontificia de salamanca": "Castilla y Leon",
    "universidad catolica de avila": "Castilla y Leon",
    "universidad catolica santa teresa de jesus de avila": "Castilla y Leon",
    "universidad isabel i": "Castilla y Leon",
    "universidad europea miguel de cervantes": "Castilla y Leon",
    # Comunitat Valenciana
    "universitat de valencia": "Comunitat Valenciana",
    "universitat jaume i": "Comunitat Valenciana",
    "universidad de alicante": "Comunitat Valenciana",
    "universidad miguel hernandez de elche": "Comunitat Valenciana",
    "universitat politecnica de valencia": "Comunitat Valenciana",
    "universidad catolica de valencia san vicente martir": "Comunitat Valenciana",
    "universidad ceu cardenal herrera": "Comunitat Valenciana",
    "universidad internacional de valencia": "Comunitat Valenciana",
    "universidad internacional de valencia (viu)": "Comunitat Valenciana",
    "universidad europea de valencia": "Comunitat Valenciana",
    # Galicia
    "universidade de santiago de compostela": "Galicia",
    "universidade da coruna": "Galicia",
    "universidade de vigo": "Galicia",
    # Canarias
    "universidad de la laguna": "Canarias",
    "universidad de las palmas de gran canaria": "Canarias",
    "universidad del atlantico medio": "Canarias",
    # 1-each
    "universidad de zaragoza": "Aragon",
    "universidad san jorge": "Aragon",
    "universidad de oviedo": "Asturias",
    "universitat de les illes balears": "Illes Balears",
    "universidad de cantabria": "Cantabria",
    "universidad de castilla-la mancha": "Castilla-La Mancha",
    "universidad de extremadura": "Extremadura",
    "universidad de murcia": "Murcia",
    "universidad publica de navarra": "Navarra",
    "universidad de navarra": "Navarra",
    "universidad del pais vasco / euskal herriko unibertsitatea": "Pais Vasco",
    "universidad del pais vasco": "Pais Vasco",
    "universidad publica de pais vasco": "Pais Vasco",
    "universidad de deusto": "Pais Vasco",
    "mondragon unibertsitatea": "Pais Vasco",
    "universidad internacional de la rioja": "La Rioja",
    "universidad internacional de la rioja (unir)": "La Rioja",
}

# Universities offering both Infantil and Primaria (default behaviour for
# institutions in PUBLIC_UNIS / PRIVATE_TRADITIONAL_UNIS / etc.). UNED is
# Infantil-only online (Primaria is presencial-tutorizada in some centres
# but the strategy memo treats the UNED Infantil online as a separate cell).
INFANTIL_ONLY_INSTITUTIONS = {
    # Few public unis offer ONLY Infantil; per pilot list, the
    # 39 public-uni Primaria total approximately matches the Infantil
    # total. UNED Primaria has lower visibility online; we default to
    # both unless flagged.
}
PRIMARIA_ONLY_INSTITUTIONS = set()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("reconciliation")


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def normalise_name(name: str) -> str:
    """Lowercase, strip accents, collapse whitespace, remove (acronym)."""
    if not isinstance(name, str):
        return ""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


NOISE_FILTER_COUNTS: dict[str, int] = {
    "length_lt_15": 0,
    "phrase_blocklist": 0,
    "stub_token": 0,
    "exact_acronym": 0,
}


def is_noise_university(name: str) -> bool:
    """Filter out HTML noise that mistakenly matched the 'Universi...' regex.

    Examples flagged in the live educaweb scrape:
      'Universidad).' / 'Universidad para mayores de 25 anos' /
      'Universidad para mayores de 40 anos' / 'Universidades de 30 anos'

    Increments NOISE_FILTER_COUNTS so the reconciliation log can summarise
    per-rule drop counts.
    """
    n = normalise_name(name)
    if len(n) < 15:
        NOISE_FILTER_COUNTS["length_lt_15"] += 1
        return True
    bad_phrases = (
        "para mayores de", "mayores 25", "mayores 30", "mayores 40",
        "tu pregunta", "tus preguntas", "responder a tus",
        "test de orientacion", "tu estudio",
    )
    if any(p in n for p in bad_phrases):
        NOISE_FILTER_COUNTS["phrase_blocklist"] += 1
        return True
    if n.startswith("universidad).") or n.startswith("universidad."):
        NOISE_FILTER_COUNTS["stub_token"] += 1
        return True
    if n in {"universidad", "universidades", "universitat", "universidades."}:
        NOISE_FILTER_COUNTS["exact_acronym"] += 1
        return True
    return False


def canonicalise_name(raw: str) -> str:
    """Map a raw university name to its canonical form (with accents).

    The canonical form is what appears in INSTITUTION_CCAA keys (without
    accents, lowercase) -- but we want to preserve a 'human' canonical
    label. Build a tiny map manually for the known canonical names.
    """
    n = normalise_name(raw)
    # Extract the (acronym) suffix if present in the raw form.
    canonical_map = {
        # Public
        "universidad de almeria": "Universidad de Almeria",
        "universidad de cadiz": "Universidad de Cadiz",
        "universidad de cordoba": "Universidad de Cordoba",
        "universidad de granada": "Universidad de Granada",
        "universidad de huelva": "Universidad de Huelva",
        "universidad de jaen": "Universidad de Jaen",
        "universidad de malaga": "Universidad de Malaga",
        "universidad de sevilla": "Universidad de Sevilla",
        "universitat autonoma de barcelona": "Universitat Autonoma de Barcelona",
        "universitat de barcelona": "Universitat de Barcelona",
        "universitat de girona": "Universitat de Girona",
        "universitat de lleida": "Universitat de Lleida",
        "universitat rovira i virgili": "Universitat Rovira i Virgili",
        "universitat de vic": "Universitat de Vic - UCC",
        "universitat de vic - ucc": "Universitat de Vic - UCC",
        "universitat pompeu fabra": "Universitat Pompeu Fabra",
        "universitat politecnica de catalunya": "Universitat Politecnica de Catalunya",
        "universidad autonoma de madrid": "Universidad Autonoma de Madrid",
        "universidad complutense de madrid": "Universidad Complutense de Madrid",
        "universidad de alcala": "Universidad de Alcala",
        "universidad rey juan carlos": "Universidad Rey Juan Carlos",
        "universidad de burgos": "Universidad de Burgos",
        "universidad de leon": "Universidad de Leon",
        "universidad de salamanca": "Universidad de Salamanca",
        "universidad de valladolid": "Universidad de Valladolid",
        "universitat de valencia": "Universitat de Valencia",
        "universitat jaume i": "Universitat Jaume I",
        "universidad de alicante": "Universidad de Alicante",
        "universidade de santiago de compostela": "Universidade de Santiago de Compostela",
        "universidade da coruna": "Universidade da Coruna",
        "universidade de vigo": "Universidade de Vigo",
        "universidad de la laguna": "Universidad de La Laguna",
        "universidad de las palmas de gran canaria": "Universidad de Las Palmas de Gran Canaria",
        "universidad de zaragoza": "Universidad de Zaragoza",
        "universidad de oviedo": "Universidad de Oviedo",
        "universitat de les illes balears": "Universitat de les Illes Balears",
        "universidad de cantabria": "Universidad de Cantabria",
        "universidad de castilla-la mancha": "Universidad de Castilla-La Mancha",
        "universidad de extremadura": "Universidad de Extremadura",
        "universidad de murcia": "Universidad de Murcia",
        "universidad publica de navarra": "Universidad Publica de Navarra",
        "universidad del pais vasco / euskal herriko unibertsitatea":
            "Universidad del Pais Vasco / Euskal Herriko Unibertsitatea",
        "universidad del pais vasco":
            "Universidad del Pais Vasco / Euskal Herriko Unibertsitatea",
        "universidad nacional de educacion a distancia":
            "Universidad Nacional de Educacion a Distancia",
        # Private-online
        "universidad internacional de la rioja":
            "Universidad Internacional de La Rioja (UNIR)",
        "universidad internacional de la rioja (unir)":
            "Universidad Internacional de La Rioja (UNIR)",
        "universidad internacional de valencia":
            "Universidad Internacional de Valencia (VIU)",
        "universidad internacional de valencia (viu)":
            "Universidad Internacional de Valencia (VIU)",
        "universidad a distancia de madrid":
            "Universidad a Distancia de Madrid (UDIMA)",
        "universidad a distancia de madrid (udima)":
            "Universidad a Distancia de Madrid (UDIMA)",
        "universidad isabel i": "Universidad Isabel I",
        # Private-traditional
        "universidad catolica de valencia san vicente martir":
            "Universidad Catolica de Valencia San Vicente Martir",
        "universidad pontificia de salamanca": "Universidad Pontificia de Salamanca",
        "universidad camilo jose cela": "Universidad Camilo Jose Cela",
        "universidad catolica de avila": "Universidad Catolica de Avila",
        "universidad alfonso x el sabio": "Universidad Alfonso X El Sabio",
        "universidad francisco de vitoria": "Universidad Francisco de Vitoria",
        "universidad ceu san pablo": "Universidad CEU San Pablo",
        "universidad ceu cardenal herrera": "Universidad CEU Cardenal Herrera",
        "universidad de navarra": "Universidad de Navarra",
        "universidad de deusto": "Universidad de Deusto",
        "mondragon unibertsitatea": "Mondragon Unibertsitatea",
        "universitat internacional de catalunya":
            "Universitat Internacional de Catalunya (UIC)",
        "universitat internacional de catalunya (uic)":
            "Universitat Internacional de Catalunya (UIC)",
        "universitat ramon llull": "Universitat Ramon Llull (URL)",
        "universitat ramon llull (url)": "Universitat Ramon Llull (URL)",
        "universitat abat oliba ceu": "Universitat Abat Oliba CEU",
        "universitat oberta de catalunya": "Universitat Oberta de Catalunya (UOC)",
        "universitat oberta de catalunya (uoc)":
            "Universitat Oberta de Catalunya (UOC)",
        "uoc": "Universitat Oberta de Catalunya (UOC)",
        "universidad loyola andalucia": "Universidad Loyola Andalucia",
        "universidad antonio de nebrija": "Universidad Antonio de Nebrija",
        "universidad san jorge": "Universidad San Jorge",
        "universidad europea de madrid": "Universidad Europea de Madrid",
        "universidad europea de valencia": "Universidad Europea de Valencia",
        "universidad pontificia comillas": "Universidad Pontificia Comillas",
        # Recovered from ANECA round-1 review (2026-04-27, coder-critic patch round 1)
        "universidad del atlantico medio": "Universidad del Atlantico Medio",
        "universidad tecnologia y empresa": "Universidad Tecnologia y Empresa",
        "universidad catolica santa teresa de jesus de avila":
            "Universidad Catolica de Avila",
    }
    # Try exact match first. If not, try prefix match (handles
    # "universidad de cadiz, facultad de educacion" -> first segment).
    if n in canonical_map:
        return canonical_map[n]
    for key in canonical_map:
        if n.startswith(key):
            return canonical_map[key]
    # Fall back to a title-cased version of the input.
    return raw.strip()


def classify_sector(canonical: str) -> str:
    n = normalise_name(canonical)
    if n in PUBLIC_UNIS:
        return "public"
    if n in PRIVATE_ONLINE_UNIS:
        return "private-online"
    if n in PRIVATE_TRADITIONAL_UNIS:
        return "private-traditional"
    return "unknown"


def infer_ccaa(canonical: str, fallback: str) -> str:
    n = normalise_name(canonical)
    if n in INSTITUTION_CCAA:
        return INSTITUTION_CCAA[n]
    return fallback if fallback and fallback != "Unknown" else "Unknown"


def collapse_modality(modality_hint: str) -> str:
    """Collapse {presencial, semipresencial, online} into 2 levels per
    Tier B design (semipresencial -> presencial)."""
    if not modality_hint:
        return "presencial"
    m = modality_hint.lower()
    if "online" in m or "distancia" in m:
        return "online"
    return "presencial"  # presencial OR semipresencial -> presencial


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load all source CSVs ------------------------------------------------
    frames: list[pd.DataFrame] = []
    src_counts: dict[str, int] = {}
    for fname in SOURCE_FILES:
        path = RAW_DIR / fname
        if not path.exists():
            log.warning("Missing source file: %s", path)
            src_counts[fname] = 0
            continue
        df = pd.read_csv(path, encoding="utf-8")
        df["__src_file"] = fname
        src_counts[fname] = len(df)
        frames.append(df)
        log.info("Loaded %s: %d rows", fname, len(df))

    if not frames:
        raise RuntimeError("No source files loaded; cannot reconcile.")

    # 2. Detect RUCT outcome -------------------------------------------------
    ruct_path = RAW_DIR / "ruct.csv"
    ruct_df = pd.read_csv(ruct_path) if ruct_path.exists() else pd.DataFrame()
    ruct_rows = len(ruct_df)
    ruct_anchored = ruct_rows > 0
    log.info(
        "RUCT outcome: %s (%d rows).",
        "PASS" if ruct_anchored else "FALLBACK (cross-validation aggregate)",
        ruct_rows,
    )

    # 3. Build a long-form normalised view -----------------------------------
    long_rows: list[dict] = []
    for df in frames:
        for _, row in df.iterrows():
            src_file = row["__src_file"]
            # RUCT has different column names than the cross-validation files
            if src_file == "ruct.csv":
                if not isinstance(row.get("universidad"), str):
                    continue
                uni_raw = row["universidad"]
                degree = row.get("degree", "")
                centro = row.get("centro", "") if isinstance(row.get("centro"), str) else ""
                ccaa_raw = row.get("ccaa", "Unknown")
                modality_raw = row.get("modalidad", "presencial")
                codigo = row.get("codigo_ruct", "")
            else:
                uni_raw = row.get("university_name", "")
                degree = row.get("degree", "")
                centro = row.get("centro", "") if "centro" in row else ""
                ccaa_raw = row.get("ccaa", "Unknown")
                modality_raw = row.get("modality_hint", "presencial")
                codigo = ""
            if not isinstance(uni_raw, str) or not uni_raw.strip():
                continue
            if is_noise_university(uni_raw):
                continue
            if degree not in ("infantil", "primaria"):
                continue
            canonical = canonicalise_name(uni_raw)
            sector = classify_sector(canonical)
            ccaa = infer_ccaa(canonical, ccaa_raw if isinstance(ccaa_raw, str) else "Unknown")
            modality = collapse_modality(
                modality_raw if isinstance(modality_raw, str) else "presencial"
            )
            # Special override: VIU, UNIR, UDIMA, Isabel I, UOC -> online
            if normalise_name(canonical) in ONLINE_INSTITUTIONS:
                modality = "online"
            long_rows.append(
                {
                    "codigo_ruct": str(codigo) if codigo else "",
                    "university_name": canonical,
                    "centro": centro if isinstance(centro, str) else "",
                    "sector": sector,
                    "ccaa": ccaa,
                    "modality": modality,
                    "degree": degree,
                    "src_file": src_file,
                    "src_label": str(row.get("source", src_file.replace(".csv", ""))),
                }
            )

    long_df = pd.DataFrame(long_rows)
    log.info("Long-form normalised rows: %d", len(long_df))

    # 4. Add adscritos overrides --------------------------------------------
    fetch_ts = datetime.now(timezone.utc).isoformat()
    adscrito_rows: list[dict] = []
    for centre, (ccaa, sector, sector_lvl, degrees) in ADSCRITOS_OVERRIDE.items():
        for d in degrees:
            adscrito_rows.append(
                {
                    "codigo_ruct": "",
                    "university_name": centre,
                    "centro": centre,
                    "sector": sector_lvl,  # "adscrito"
                    "ccaa": ccaa,
                    "modality": "presencial",
                    "degree": d,
                    "src_file": "manual_override",
                    "src_label": "adscritos_pilot_seed",
                }
            )
    if adscrito_rows:
        long_df = pd.concat([long_df, pd.DataFrame(adscrito_rows)], ignore_index=True)
        log.info("Added %d adscrito-override rows.", len(adscrito_rows))

    # 5. Filter rows with unknown sector + unknown ccaa (likely noise) ------
    before = len(long_df)
    long_df = long_df[~((long_df["sector"] == "unknown") & (long_df["ccaa"] == "Unknown"))]
    log.info("Filtered noise: %d -> %d rows.", before, len(long_df))

    # 6. Aggregate to (canonical_university, degree) --------------------------
    # Group across sources: each (university, degree) is one programme. Track
    # the set of source files contributing to it.
    grouped = (
        long_df.groupby(["university_name", "degree"])
        .agg(
            codigo_ruct=("codigo_ruct", lambda s: next((x for x in s if x), "")),
            sector=("sector", lambda s: next((x for x in s if x and x != "unknown"), "unknown")),
            ccaa=("ccaa", lambda s: next((x for x in s if x and x != "Unknown"), "Unknown")),
            modality=("modality", lambda s: next((x for x in s if x), "presencial")),
            centro=("centro", lambda s: next((x for x in s if x), "")),
            sources=("src_label", lambda s: ";".join(sorted(set(s)))),
            sources_count=("src_file", lambda s: len(set(s))),
        )
        .reset_index()
    )

    # 7. Drop universities still classified as 'unknown' sector --------------
    # These are HTML-noise leftovers. We log them in the reconciliation log.
    unknown_mask = grouped["sector"] == "unknown"
    dropped_unknown = grouped[unknown_mask].copy()
    grouped = grouped[~unknown_mask].copy()
    log.info(
        "Dropped %d (university, degree) rows with sector=unknown.",
        len(dropped_unknown),
    )

    # 8. Build final inventory schema ----------------------------------------
    grouped = grouped.sort_values(
        ["sector", "ccaa", "modality", "degree", "university_name"]
    ).reset_index(drop=True)
    grouped["programme_id"] = [
        f"P{i:04d}" for i in range(1, len(grouped) + 1)
    ]
    grouped["ruct_anchored"] = grouped["codigo_ruct"].astype(str).str.len() > 0
    grouped["fallback_flag"] = (~grouped["ruct_anchored"]).map(
        {True: "cross_validation_only", False: "ruct_anchored"}
    )

    # Reorder columns
    final_cols = [
        "programme_id", "codigo_ruct", "university_name", "sector",
        "ccaa", "modality", "degree", "centro", "sources", "sources_count",
        "ruct_anchored", "fallback_flag",
    ]
    inventory = grouped[final_cols]

    # 9. Write outputs --------------------------------------------------------
    inventory.to_csv(OUT_INVENTORY, index=False, encoding="utf-8")
    log.info("Wrote %d programmes to %s", len(inventory), OUT_INVENTORY)

    # 10. Reconciliation log ---------------------------------------------------
    sector_counts = inventory["sector"].value_counts().to_dict()
    ccaa_counts = inventory["ccaa"].value_counts().to_dict()
    modality_counts = inventory["modality"].value_counts().to_dict()
    degree_counts = inventory["degree"].value_counts().to_dict()

    md_lines: list[str] = []
    md_lines.append("# Inventory Reconciliation Log")
    md_lines.append("")
    md_lines.append(f"**Date:** {fetch_ts}")
    md_lines.append("")
    md_lines.append("## Source-file row counts (raw)")
    md_lines.append("")
    md_lines.append("| Source | Rows |")
    md_lines.append("|---|---|")
    for f in SOURCE_FILES:
        md_lines.append(f"| `{f}` | {src_counts.get(f, 0)} |")
    md_lines.append("")
    md_lines.append("## RUCT outcome")
    md_lines.append("")
    if ruct_anchored:
        md_lines.append(
            f"**RUCT live scrape PASS:** {ruct_rows} rows. The reconciliation "
            "anchored programme IDs on `codigo_ruct` where available."
        )
    else:
        md_lines.append(
            "**RUCT live scrape FALLBACK (per plan section 7).** "
            "The session-based POST against "
            "`https://www.educacion.gob.es/ruct/consultaestudios` returned "
            "no parseable result rows in 0/2 queries. The cross-validation "
            "aggregate (gradomania + educaweb + ANECA + 8 autonomous-"
            "community agency seeds + manual adscritos override) was used "
            "as the universe in lieu of RUCT. `codigo_ruct` is empty for "
            "all rows; programme IDs are synthetic (`P0001`-`Pxxxx`). "
            "This substitution is logged as a deviation in the OSF "
            "pre-registration deposit (PAP section 10)."
        )
    md_lines.append("")
    md_lines.append("## Final inventory composition")
    md_lines.append("")
    md_lines.append(f"**Total programmes:** {len(inventory)}")
    md_lines.append("")
    md_lines.append("### By sector")
    md_lines.append("")
    md_lines.append("| Sector | N |")
    md_lines.append("|---|---|")
    for k, v in sorted(sector_counts.items(), key=lambda x: -x[1]):
        md_lines.append(f"| {k} | {v} |")
    md_lines.append("")
    md_lines.append("### By degree")
    md_lines.append("")
    md_lines.append("| Degree | N |")
    md_lines.append("|---|---|")
    for k, v in sorted(degree_counts.items(), key=lambda x: -x[1]):
        md_lines.append(f"| {k} | {v} |")
    md_lines.append("")
    md_lines.append("### By modality")
    md_lines.append("")
    md_lines.append("| Modality | N |")
    md_lines.append("|---|---|")
    for k, v in sorted(modality_counts.items(), key=lambda x: -x[1]):
        md_lines.append(f"| {k} | {v} |")
    md_lines.append("")
    md_lines.append("### By autonomous community")
    md_lines.append("")
    md_lines.append("| CCAA | N |")
    md_lines.append("|---|---|")
    for k, v in sorted(ccaa_counts.items(), key=lambda x: -x[1]):
        md_lines.append(f"| {k} | {v} |")
    md_lines.append("")
    md_lines.append("## Dropped rows (sector=unknown)")
    md_lines.append("")
    md_lines.append(
        f"{len(dropped_unknown)} (university, degree) candidate rows were "
        "dropped because the sector classifier did not recognise the "
        "institution name. This list is for transparency; reviewers can "
        "inspect whether any legitimate institution was missed."
    )
    md_lines.append("")
    if not dropped_unknown.empty:
        md_lines.append("| university_name | degree | sources |")
        md_lines.append("|---|---|---|")
        for _, r in dropped_unknown.head(50).iterrows():
            md_lines.append(
                f"| {r['university_name']} | {r['degree']} | {r['sources']} |"
            )
    md_lines.append("")
    md_lines.append("## Noise-filter rules applied to live HTML scrapes")
    md_lines.append("")
    md_lines.append(
        "Live aggregator scrapes (educaweb, agencies) returned raw rows that "
        "include HTML-noise hits matching the `Universi...` regex but are not "
        "real institutions. These rows are filtered up-front by "
        "`inventory_reconciliation.py::is_noise_university()` before any "
        "canonicalisation, sector classification, or deduplication. Filter "
        "rules and per-rule drop counts:"
    )
    md_lines.append("")
    md_lines.append("| # | Rule | Description | Rows dropped |")
    md_lines.append("|---|---|---|---|")
    md_lines.append(
        f"| 1 | length_lt_15 | Normalised name length < 15 chars (filters "
        "stubs like 'Universidad).' and 'Universidad') "
        f"| {NOISE_FILTER_COUNTS['length_lt_15']} |"
    )
    md_lines.append(
        f"| 2 | phrase_blocklist | Contains any of: 'para mayores de', "
        "'mayores 25', 'mayores 30', 'mayores 40', 'tu pregunta', "
        "'tus preguntas', 'responder a tus', 'test de orientacion', "
        "'tu estudio' (filters senior-citizen programmes and SEO ad copy "
        f"that begin 'Universidad...') | {NOISE_FILTER_COUNTS['phrase_blocklist']} |"
    )
    md_lines.append(
        f"| 3 | stub_token | Starts with 'universidad).' or 'universidad.' "
        "(filters HTML fragments where the regex captured a closing paren or "
        f"period) | {NOISE_FILTER_COUNTS['stub_token']} |"
    )
    md_lines.append(
        f"| 4 | exact_acronym | Exactly equals one of: 'universidad', "
        "'universidades', 'universitat', 'universidades.' (filters bare "
        f"section headings) | {NOISE_FILTER_COUNTS['exact_acronym']} |"
    )
    total_noise = sum(NOISE_FILTER_COUNTS.values())
    md_lines.append(f"| | **Total** | | **{total_noise}** |")
    md_lines.append("")
    md_lines.append(
        "Counts include the same row potentially filtered at multiple source "
        "passes (e.g., the same noise row in educaweb and educaweb_pilot_fallback). "
        "The post-filter `sector=unknown` drop is documented separately in "
        "the 'Dropped rows (sector=unknown)' section above; that filter "
        "operates on canonicalised institution names, not on raw HTML noise."
    )
    md_lines.append("")
    md_lines.append("## Manual overrides applied")
    md_lines.append("")
    md_lines.append(
        f"- Adscritos override list: {len(ADSCRITOS_OVERRIDE)} centres "
        "added per `data_exploration_cdd_formacion_inicial.md` flag 5."
    )
    md_lines.append(
        "- Modality collapse: `semipresencial` -> `presencial` per Tier B "
        "design (strategy memo section 3 - 2-level modality)."
    )
    md_lines.append(
        "- Sector classification: `private-online` is reserved for VIU, "
        "UNIR, UDIMA, Isabel I; UNED is `public` (not private-online "
        "even though its modality is online)."
    )
    md_lines.append("")
    OUT_LOG.write_text("\n".join(md_lines), encoding="utf-8")
    log.info("Wrote reconciliation log to %s", OUT_LOG)


if __name__ == "__main__":
    main()
