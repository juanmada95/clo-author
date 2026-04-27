"""
gradomania_aggregator.py

Title:    Gradomania.com 2024/2025 nota-de-corte aggregator (Stage 0 Pass 1).
Author:   data-engineer (CDD curricular analysis project).
Date:     2026-04-27.
Purpose:  Cross-validation source for the programme universe (Layer 0).
          Fetches the 2024/2025 nota-de-corte listings for both Grado en
          Educacion Primaria and Grado en Educacion Infantil, parses the
          per-CCAA university tables, and writes a normalised CSV.
Inputs:   Two public HTML pages on gradomania.com (URLs below).
Outputs:  data/raw/inventory_passes/gradomania.csv
          Columns: source, degree, university_name, ccaa, sector_hint,
                   modality_hint, fetch_ts, url
Notes:
  - INV-15: all imports at top.
  - INV-16: paths via pathlib.Path relative to the project root.
  - INV-17: rows pre-allocated as a list and converted to DataFrame in one shot.
  - INV-19: no setwd / os.chdir / install.
  - Courteous rate-limit (1 req/s) per data-discovery report.
  - If the live fetch fails, a pilot-evidence fallback is used (39 public
    Primaria universities documented in
    quality_reports/data_exploration_cdd_formacion_inicial.md Table 1.2).
    The fallback is logged to the output column `source` as
    `gradomania_pilot_fallback` so downstream reconciliation can flag it.
"""

from __future__ import annotations

import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = PROJECT_ROOT / "data" / "raw" / "inventory_passes"
OUT_PATH = OUT_DIR / "gradomania.csv"

URLS = {
    "primaria": (
        "https://www.gradomania.com/noticias_universitarias/"
        "notas-de-corte-para-el-grado-en-educacion-primaria-20242025-"
        "org-8125.html"
    ),
    "infantil": (
        "https://www.gradomania.com/noticias_universitarias/"
        "notas-de-corte-para-el-grado-en-educacion-infantil-20242025-"
        "org-8129.html"
    ),
}

USER_AGENT = (
    "Mozilla/5.0 (compatible; CDD-Research-Bot/1.0; "
    "+research; contact: juanmada10@gmail.com)"
)

REQUEST_DELAY_S = 1.0
TIMEOUT_S = 30

# 18 Spanish autonomous communities + Ceuta + Melilla (canonical Castilian
# spellings used as the reconciliation key).
CCAA_CANONICAL = {
    "andalucia": "Andalucia",
    "aragon": "Aragon",
    "asturias": "Asturias",
    "principado de asturias": "Asturias",
    "baleares": "Illes Balears",
    "illes balears": "Illes Balears",
    "islas baleares": "Illes Balears",
    "canarias": "Canarias",
    "cantabria": "Cantabria",
    "castilla y leon": "Castilla y Leon",
    "castilla-la mancha": "Castilla-La Mancha",
    "cataluna": "Cataluna",
    "catalunya": "Cataluna",
    "extremadura": "Extremadura",
    "galicia": "Galicia",
    "la rioja": "La Rioja",
    "rioja": "La Rioja",
    "madrid": "Madrid",
    "comunidad de madrid": "Madrid",
    "murcia": "Murcia",
    "region de murcia": "Murcia",
    "navarra": "Navarra",
    "comunidad foral de navarra": "Navarra",
    "pais vasco": "Pais Vasco",
    "euskadi": "Pais Vasco",
    "valencia": "Comunitat Valenciana",
    "comunitat valenciana": "Comunitat Valenciana",
    "comunidad valenciana": "Comunitat Valenciana",
    "ceuta": "Ceuta",
    "melilla": "Melilla",
}

# Pilot-evidence fallback: 39 public-uni Primaria programmes per
# data_exploration_cdd_formacion_inicial.md Table 1.2.
PILOT_FALLBACK_PRIMARIA = [
    # Andalucia (8)
    ("Universidad de Almeria", "Andalucia"),
    ("Universidad de Cadiz", "Andalucia"),
    ("Universidad de Cordoba", "Andalucia"),
    ("Universidad de Granada", "Andalucia"),
    ("Universidad de Huelva", "Andalucia"),
    ("Universidad de Jaen", "Andalucia"),
    ("Universidad de Malaga", "Andalucia"),
    ("Universidad de Sevilla", "Andalucia"),
    # Cataluna (6)
    ("Universitat Autonoma de Barcelona", "Cataluna"),
    ("Universitat de Barcelona", "Cataluna"),
    ("Universitat de Girona", "Cataluna"),
    ("Universitat de Lleida", "Cataluna"),
    ("Universitat Rovira i Virgili", "Cataluna"),
    ("Universitat de Vic - UCC", "Cataluna"),
    # Madrid (4)
    ("Universidad Autonoma de Madrid", "Madrid"),
    ("Universidad Complutense de Madrid", "Madrid"),
    ("Universidad de Alcala", "Madrid"),
    ("Universidad Rey Juan Carlos", "Madrid"),
    # Castilla y Leon (4)
    ("Universidad de Burgos", "Castilla y Leon"),
    ("Universidad de Leon", "Castilla y Leon"),
    ("Universidad de Salamanca", "Castilla y Leon"),
    ("Universidad de Valladolid", "Castilla y Leon"),
    # Comunitat Valenciana (3)
    ("Universitat de Valencia", "Comunitat Valenciana"),
    ("Universitat Jaume I", "Comunitat Valenciana"),
    ("Universidad de Alicante", "Comunitat Valenciana"),
    # Galicia (3)
    ("Universidade de Santiago de Compostela", "Galicia"),
    ("Universidade da Coruna", "Galicia"),
    ("Universidade de Vigo", "Galicia"),
    # Canarias (2)
    ("Universidad de La Laguna", "Canarias"),
    ("Universidad de Las Palmas de Gran Canaria", "Canarias"),
    # 1-each (9)
    ("Universidad de Zaragoza", "Aragon"),
    ("Universidad de Oviedo", "Asturias"),
    ("Universitat de les Illes Balears", "Illes Balears"),
    ("Universidad de Cantabria", "Cantabria"),
    ("Universidad de Castilla-La Mancha", "Castilla-La Mancha"),
    ("Universidad de Extremadura", "Extremadura"),
    ("Universidad de Murcia", "Murcia"),
    ("Universidad Publica de Navarra", "Navarra"),
    ("Universidad del Pais Vasco / Euskal Herriko Unibertsitatea", "Pais Vasco"),
]

PILOT_FALLBACK_INFANTIL = PILOT_FALLBACK_PRIMARIA[:]  # ~38 public unis, same set

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("gradomania")

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def normalise_ccaa(raw: str) -> str:
    """Map a raw CCAA string to its canonical Castilian form."""
    key = re.sub(r"[^a-zA-Z\s\-]", "", raw or "").strip().lower()
    key = re.sub(r"\s+", " ", key)
    return CCAA_CANONICAL.get(key, raw.strip() if raw else "Unknown")


def fetch_html(url: str, session: requests.Session) -> str | None:
    """Fetch the URL and return text on success, None on failure."""
    try:
        resp = session.get(url, timeout=TIMEOUT_S)
        resp.raise_for_status()
        return resp.text
    except (requests.RequestException, requests.Timeout) as exc:
        log.warning("Fetch failed for %s: %s", url, exc)
        return None


def parse_listing(html: str, degree: str, url: str) -> list[dict]:
    """Parse the gradomania nota-de-corte listing HTML.

    The page structure (per pilot inspection) interleaves CCAA headers (h3 or
    h2) with university names (table rows or list items). This parser is
    defensive: it scans every text-bearing element and assigns the most-recent
    CCAA header to each candidate university name.
    """
    soup = BeautifulSoup(html, "lxml")
    rows: list[dict] = []
    current_ccaa = "Unknown"
    fetch_ts = datetime.now(timezone.utc).isoformat()

    # Heuristic: walk h2/h3 (CCAA headers) and tr/li (universities).
    for el in soup.find_all(["h2", "h3", "tr", "li"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        # CCAA headers tend to be short and match a known CCAA name.
        if el.name in ("h2", "h3"):
            cand = normalise_ccaa(text)
            if cand in CCAA_CANONICAL.values():
                current_ccaa = cand
                continue
        # University rows: contain "Universidad" or "Universitat" or
        # "Universidade" and are inside tr/li elements.
        if el.name in ("tr", "li") and re.search(
            r"Universi(dad|tat|dade)", text, re.IGNORECASE
        ):
            # Take the first university-prefixed phrase up to a comma/dash.
            m = re.search(
                r"(Universi(?:dad|tat|dade)[^,\-\(]+)", text, re.IGNORECASE
            )
            if not m:
                continue
            uni = m.group(1).strip()
            rows.append(
                {
                    "source": "gradomania",
                    "degree": degree,
                    "university_name": uni,
                    "ccaa": current_ccaa,
                    "sector_hint": "public",  # gradomania lists nota-de-corte = public unis
                    "modality_hint": "presencial",
                    "fetch_ts": fetch_ts,
                    "url": url,
                }
            )
    return rows


def build_pilot_fallback() -> list[dict]:
    """Use the documented pilot evidence as a fallback inventory."""
    fetch_ts = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    for uni, ccaa in PILOT_FALLBACK_PRIMARIA:
        rows.append(
            {
                "source": "gradomania_pilot_fallback",
                "degree": "primaria",
                "university_name": uni,
                "ccaa": ccaa,
                "sector_hint": "public",
                "modality_hint": "presencial",
                "fetch_ts": fetch_ts,
                "url": URLS["primaria"],
            }
        )
    for uni, ccaa in PILOT_FALLBACK_INFANTIL:
        rows.append(
            {
                "source": "gradomania_pilot_fallback",
                "degree": "infantil",
                "university_name": uni,
                "ccaa": ccaa,
                "sector_hint": "public",
                "modality_hint": "presencial",
                "fetch_ts": fetch_ts,
                "url": URLS["infantil"],
            }
        )
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    all_rows: list[dict] = []
    live_success = False
    for degree, url in URLS.items():
        log.info("Fetching %s listing: %s", degree, url)
        html = fetch_html(url, session)
        time.sleep(REQUEST_DELAY_S)
        if html is None:
            log.warning("Live fetch failed for %s.", degree)
            continue
        parsed = parse_listing(html, degree, url)
        log.info("Parsed %d rows for %s.", len(parsed), degree)
        if len(parsed) >= 5:
            live_success = True
            all_rows.extend(parsed)
        else:
            log.warning(
                "Live parse returned only %d rows for %s; treating as parse "
                "failure (gradomania layout may have changed).",
                len(parsed),
                degree,
            )

    if not live_success or len(all_rows) < 30:
        log.warning(
            "Live aggregator unavailable or under-parsed (got %d rows); "
            "using documented pilot-evidence fallback. "
            "This is a logged substitution per plan section 7.",
            len(all_rows),
        )
        all_rows = build_pilot_fallback()

    df = pd.DataFrame(all_rows)
    df = df.drop_duplicates(subset=["degree", "university_name", "ccaa"])
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    log.info("Wrote %d rows to %s.", len(df), OUT_PATH)


if __name__ == "__main__":
    main()
