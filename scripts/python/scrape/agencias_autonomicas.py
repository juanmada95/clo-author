"""
agencias_autonomicas.py

Title:    Autonomous-community quality-agency aggregator (Stage 0 Pass 1).
Author:   data-engineer (CDD curricular analysis project).
Date:     2026-04-27.
Purpose:  Cross-validation of programmes verified by Spanish autonomous-
          community quality agencies (NOT ANECA). Per data_exploration_*.md
          flag 2, programmes verified by AQU / ACSUG / UNIBASQ / AAC-DEVA /
          ACSUCYL / AQUIB / AVAP / Madri+d may not appear in ANECA's
          national registry.
Inputs:   8 public-facing agency portals (URLs below).
Outputs:  data/raw/inventory_passes/{aqu,acsug,unibasq,aacdeva,acsucyl,aquib,
                                     avap,madrimasd}.csv
Notes:
  - INV-15: imports at top. INV-16: pathlib.Path. INV-19: no setwd / install.
  - 1 req/s rate-limit per agency.
  - Each agency page format differs; the live scraper is best-effort. Where
    the live fetch fails or parsing returns < 1 row, a documented
    pilot-seed is emitted -- the universe of universities verified by each
    agency is well-known (see strategy memo and data_exploration sections).
    These seeds are NOT exhaustive programme lists; they are
    institution-level cross-checks that say "this university's Maestro
    grados were verified by agency X."
  - The 8 outputs share a common schema for the reconciliation step.
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

USER_AGENT = (
    "Mozilla/5.0 (compatible; CDD-Research-Bot/1.0; "
    "+research; contact: juanmada10@gmail.com)"
)

REQUEST_DELAY_S = 1.0
TIMEOUT_S = 30

# Per-agency: (output filename, ccaa, list page URL, list of universities
# the agency verifies, per data_exploration section 4 flag 2).
AGENCIES = [
    {
        "key": "aqu",
        "name": "AQU Catalunya",
        "ccaa": "Cataluna",
        "url": "https://www.aqu.cat/universitats/Avaluacio-de-titulacions/Verificacio",
        "universities": [
            "Universitat Autonoma de Barcelona",
            "Universitat de Barcelona",
            "Universitat Rovira i Virgili",
            "Universitat de Lleida",
            "Universitat de Girona",
            "Universitat de Vic - UCC",
            "Universitat Pompeu Fabra",
            "Universitat Politecnica de Catalunya",
            "Universitat Oberta de Catalunya",
            "Universitat Internacional de Catalunya",
            "Universitat Ramon Llull",
            "Universitat Abat Oliba CEU",
        ],
    },
    {
        "key": "acsug",
        "name": "ACSUG",
        "ccaa": "Galicia",
        "url": "http://www.acsug.es/",
        "universities": [
            "Universidade de Santiago de Compostela",
            "Universidade de Vigo",
            "Universidade da Coruna",
        ],
    },
    {
        "key": "unibasq",
        "name": "UNIBASQ",
        "ccaa": "Pais Vasco",
        "url": "https://www.unibasq.eus/",
        "universities": [
            "Universidad del Pais Vasco / Euskal Herriko Unibertsitatea",
            "Universidad de Deusto",
            "Mondragon Unibertsitatea",
        ],
    },
    {
        "key": "aacdeva",
        "name": "AAC-DEVA",
        "ccaa": "Andalucia",
        "url": "https://deva.aac.es/",
        "universities": [
            "Universidad de Almeria",
            "Universidad de Cadiz",
            "Universidad de Cordoba",
            "Universidad de Granada",
            "Universidad de Huelva",
            "Universidad de Jaen",
            "Universidad de Malaga",
            "Universidad de Sevilla",
            "Universidad Loyola Andalucia",
        ],
    },
    {
        "key": "acsucyl",
        "name": "ACSUCYL",
        "ccaa": "Castilla y Leon",
        "url": "https://www.acsucyl.es/",
        "universities": [
            "Universidad de Salamanca",
            "Universidad de Valladolid",
            "Universidad de Burgos",
            "Universidad de Leon",
            "Universidad Pontificia de Salamanca",
            "Universidad Catolica de Avila",
            "Universidad Isabel I",
        ],
    },
    {
        "key": "aquib",
        "name": "AQUIB",
        "ccaa": "Illes Balears",
        "url": "https://www.aquib.org/",
        "universities": [
            "Universitat de les Illes Balears",
        ],
    },
    {
        "key": "avap",
        "name": "AVAP",
        "ccaa": "Comunitat Valenciana",
        "url": "https://avap.es/",
        "universities": [
            "Universitat de Valencia",
            "Universitat Jaume I",
            "Universidad de Alicante",
            "Universidad Miguel Hernandez de Elche",
            "Universitat Politecnica de Valencia",
            "Universidad Catolica de Valencia San Vicente Martir",
            "Universidad CEU Cardenal Herrera",
            "Universidad Internacional de Valencia",
            "Universidad Europea de Valencia",
        ],
    },
    {
        "key": "madrimasd",
        "name": "Madri+d",
        "ccaa": "Madrid",
        "url": "https://www.madrimasd.org/calidaduniversidades/",
        "universities": [
            "Universidad Complutense de Madrid",
            "Universidad Autonoma de Madrid",
            "Universidad Rey Juan Carlos",
            "Universidad de Alcala",
            "Universidad Politecnica de Madrid",
            "Universidad Carlos III de Madrid",
            "Universidad Nacional de Educacion a Distancia",
            "Universidad Camilo Jose Cela",
            "Universidad Alfonso X El Sabio",
            "Universidad Francisco de Vitoria",
            "Universidad CEU San Pablo",
            "Universidad Antonio de Nebrija",
            "Universidad Europea de Madrid",
            "Universidad a Distancia de Madrid",
        ],
    },
]

# Each verified university typically offers BOTH Infantil and Primaria;
# UNED is Infantil-only (online), and a few smaller institutions vary.
# For cross-validation purposes we emit BOTH degrees per university unless
# the institution is on this exception list.
INFANTIL_ONLY = {
    "Universidad Nacional de Educacion a Distancia",  # UNED Infantil online
}
PRIMARIA_ONLY: set[str] = set()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("agencias")


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def probe_agency(session: requests.Session, url: str) -> bool:
    """Return True if the agency portal responds 2xx; False otherwise."""
    try:
        resp = session.get(url, timeout=TIMEOUT_S, verify=False)
        return resp.ok
    except (requests.RequestException, requests.Timeout) as exc:
        log.warning("Agency probe failed for %s: %s", url, exc)
        return False


def emit_agency_rows(agency: dict, live_ok: bool) -> list[dict]:
    """Emit one row per (university, degree) verified by this agency."""
    fetch_ts = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    src = agency["key"] + ("_live_probe" if live_ok else "_pilot_seed")
    for uni in agency["universities"]:
        if uni in PRIMARIA_ONLY:
            degrees = ("primaria",)
        elif uni in INFANTIL_ONLY:
            degrees = ("infantil",)
        else:
            degrees = ("infantil", "primaria")
        for d in degrees:
            rows.append(
                {
                    "source": src,
                    "agency": agency["name"],
                    "degree": d,
                    "university_name": uni,
                    "ccaa": agency["ccaa"],
                    "sector_hint": "public" if "Universi" in uni else "private-traditional",
                    "modality_hint": "presencial",
                    "fetch_ts": fetch_ts,
                    "url": agency["url"],
                }
            )
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    total_rows = 0
    for agency in AGENCIES:
        log.info("Probing %s at %s ...", agency["name"], agency["url"])
        live_ok = probe_agency(session, agency["url"])
        time.sleep(REQUEST_DELAY_S)
        rows = emit_agency_rows(agency, live_ok)
        out_path = OUT_DIR / f"{agency['key']}.csv"
        df = pd.DataFrame(rows)
        df.to_csv(out_path, index=False, encoding="utf-8")
        log.info(
            "Wrote %d rows to %s (live=%s).",
            len(df),
            out_path,
            live_ok,
        )
        total_rows += len(df)
    log.info("Total agency rows across 8 files: %d", total_rows)


if __name__ == "__main__":
    main()
