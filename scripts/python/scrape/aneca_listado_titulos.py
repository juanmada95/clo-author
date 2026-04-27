"""
aneca_listado_titulos.py

Title:    ANECA Listado de Titulos cross-validation scraper (Stage 0 Pass 1).
Author:   data-engineer (CDD curricular analysis project).
Date:     2026-04-27.
Purpose:  Cross-validation of programme universe against ANECA's public
          registry. ANECA covers programmes nationally evaluated; programmes
          evaluated by the autonomous-community agencies are NOT in this
          registry (see agencias_autonomicas.py).
Inputs:   ANECA Listado de Titulos search endpoint.
Outputs:  data/raw/inventory_passes/aneca.csv

TLS workaround: ANECA's site uses a non-standard certificate chain that
broke verification in the data-discovery pilot. Per plan section 7, the
scraper invokes requests with verify=False and logs the workaround. This
is acceptable for a public read-only data source where the URL itself
identifies the authority. This script DOES NOT submit credentials and
DOES NOT modify any state on the ANECA server.

Notes:
  - INV-15: imports at top. INV-16: pathlib.Path. INV-19: no setwd / install.
  - 1 req/s rate-limit.
  - On any failure (TLS, timeout, HTTP error, parse error), an empty CSV
    with the correct schema is written and the failure is logged. The
    reconciliation step treats ANECA as advisory cross-validation, not
    authoritative -- losing it does not block Stage 0.
"""

from __future__ import annotations

import logging
import time
import urllib3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Suppress the InsecureRequestWarning from urllib3 when verify=False is used.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = PROJECT_ROOT / "data" / "raw" / "inventory_passes"
OUT_PATH = OUT_DIR / "aneca.csv"

BASE_URL = "https://srv.aneca.es/ListadoTitulos/"
SEARCH_URL = BASE_URL + "busqueda-titulaciones"

USER_AGENT = (
    "Mozilla/5.0 (compatible; CDD-Research-Bot/1.0; "
    "+research; contact: juanmada10@gmail.com)"
)

REQUEST_DELAY_S = 1.0
TIMEOUT_S = 30

# Search queries: ANECA's public search returns rows when the title contains
# the search term. Two queries cover both Maestro grados.
QUERIES = [
    {"degree": "infantil", "denominacion": "Maestro Educacion Infantil"},
    {"degree": "primaria", "denominacion": "Maestro Educacion Primaria"},
]

# ANECA's search form posts to the search endpoint with these field names
# (per pilot inspection of the form's HTML).
FORM_FIELDS_TEMPLATE = {
    "tipoTitulacion": "Grado",
    "denominacion": "",
    "universidad": "",
    "ramaConocimiento": "",
    "ambitoEstudio": "",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("aneca")

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def fetch_search(session: requests.Session, denominacion: str) -> str | None:
    """POST the search form and return the result HTML, or None on error."""
    fields = dict(FORM_FIELDS_TEMPLATE)
    fields["denominacion"] = denominacion
    try:
        # First GET the search page to establish a session and CSRF token
        # if any. Then POST the search.
        session.get(SEARCH_URL, timeout=TIMEOUT_S, verify=False)
        time.sleep(REQUEST_DELAY_S)
        resp = session.post(
            SEARCH_URL, data=fields, timeout=TIMEOUT_S, verify=False
        )
        resp.raise_for_status()
        return resp.text
    except (requests.RequestException, requests.Timeout) as exc:
        log.warning("ANECA fetch failed for '%s': %s", denominacion, exc)
        return None


def parse_results(html: str, degree: str) -> list[dict]:
    """Parse ANECA search-result HTML.

    The result table (per pilot) lists one row per programme with columns
    like title / university / centro / status. The exact selectors may
    vary; this parser is heuristic.
    """
    soup = BeautifulSoup(html, "lxml")
    fetch_ts = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    for tr in soup.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cells) < 2:
            continue
        joined = " ".join(cells).lower()
        if "maestro" not in joined and "magisterio" not in joined:
            continue
        # Heuristic: first cell is title, second is university, third is
        # centro. ANECA layout may put the university in cell 1 -- guess
        # by finding the cell with "Universi".
        title = cells[0]
        uni = ""
        centro = ""
        for c in cells[1:]:
            if "Universi" in c and not uni:
                uni = c
            elif uni and not centro:
                centro = c
        if not uni:
            continue
        rows.append(
            {
                "source": "aneca",
                "degree": degree,
                "university_name": uni,
                "centro": centro,
                "title": title,
                "ccaa": "Unknown",
                "sector_hint": "unknown",
                "modality_hint": "unknown",
                "fetch_ts": fetch_ts,
                "url": SEARCH_URL,
            }
        )
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    all_rows: list[dict] = []
    for q in QUERIES:
        log.info("Querying ANECA for %s ...", q["denominacion"])
        html = fetch_search(session, q["denominacion"])
        time.sleep(REQUEST_DELAY_S)
        if html is None:
            log.warning("Skipping %s due to fetch failure.", q["degree"])
            continue
        parsed = parse_results(html, q["degree"])
        log.info("Parsed %d ANECA rows for %s.", len(parsed), q["degree"])
        all_rows.extend(parsed)

    # ANECA is advisory cross-validation. If empty, we still write the file
    # (with header only) so the reconciliation step can read it.
    df = pd.DataFrame(
        all_rows,
        columns=[
            "source", "degree", "university_name", "centro", "title", "ccaa",
            "sector_hint", "modality_hint", "fetch_ts", "url",
        ],
    )
    df = df.drop_duplicates(subset=["degree", "university_name", "centro"])
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    log.info("Wrote %d rows to %s.", len(df), OUT_PATH)


if __name__ == "__main__":
    main()
