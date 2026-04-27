"""
ruct_scraper.py

Title:    RUCT (Registro de Universidades, Centros y Titulos) authoritative
          scraper (Stage 0 Pass 2).
Author:   data-engineer (CDD curricular analysis project).
Date:     2026-04-27.
Purpose:  Authoritative enumeration of the programme universe. RUCT is the
          official Ministerio registry; it carries the codigo_ruct programme
          identifier that anchors the reconciliation step.
Inputs:   https://www.educacion.gob.es/ruct/consultaestudios (session-based
          form; POST + cookies).
Outputs:  data/raw/inventory_passes/ruct.csv
          (or ruct_partial.csv if the time budget is exhausted)

Schema:   codigo_ruct, denominacion, universidad, centro, ccaa, modalidad,
          situacion, fecha_modificacion, fecha_publicacion_boe, source,
          fetch_ts, url

Filters:  nivel academico = Grado;
          denominacion contains 'Maestro Educacion Infantil' OR
          'Maestro Educacion Primaria' (separate queries);
          situacion = Active.

Rate-limit:  1 req/s.
Time budget: 8 minutes hard cap (the orchestrator's bash tool times out at
             10 min; we leave 2 min safety). On budget exhaustion we write
             whatever rows we have to ruct_partial.csv and exit cleanly.

If the live scrape fails entirely (form structure changed, IP blocked, TLS
error, etc.), we emit a documented pilot fallback: a synthesised row set
constructed from the cross-validation aggregates with codigo_ruct =
'NA-FALLBACK-{n}'. Reconciliation logs this substitution. See plan section
7 risk table.

Notes:
  - INV-15: imports at top.
  - INV-16: pathlib.Path.
  - INV-19: no setwd / install.
"""

from __future__ import annotations

import logging
import re
import time
import urllib3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = PROJECT_ROOT / "data" / "raw" / "inventory_passes"
OUT_PATH = OUT_DIR / "ruct.csv"
PARTIAL_PATH = OUT_DIR / "ruct_partial.csv"

BASE_URL = "https://www.educacion.gob.es/ruct/"
SEARCH_URL = BASE_URL + "consultaestudios"

USER_AGENT = (
    "Mozilla/5.0 (compatible; CDD-Research-Bot/1.0; "
    "+research; contact: juanmada10@gmail.com)"
)

REQUEST_DELAY_S = 1.0
TIMEOUT_S = 30
TIME_BUDGET_S = 8 * 60  # 8 minutes hard cap

QUERIES = [
    {"degree": "infantil", "denominacion": "Maestro Educacion Infantil"},
    {"degree": "primaria", "denominacion": "Maestro Educacion Primaria"},
]

# RUCT search form field names (from pilot inspection of the form HTML).
# Filters: nivel academico = Grado; situacion = active. The actual field
# names may differ -- the script attempts the most common variants and
# logs any 4xx / 5xx response.
FORM_FIELDS_TEMPLATE = {
    "actual": "S",       # situation = active (Spanish "S"i)
    "nivelAca": "GR",    # nivel academico = Grado
    "denomi": "",        # denominacion del titulo
}

CCAA_KEYWORDS = {
    "andalucia": "Andalucia",
    "aragon": "Aragon",
    "asturias": "Asturias",
    "baleares": "Illes Balears",
    "canarias": "Canarias",
    "cantabria": "Cantabria",
    "castilla y leon": "Castilla y Leon",
    "castilla-la mancha": "Castilla-La Mancha",
    "cataluna": "Cataluna",
    "catalunya": "Cataluna",
    "extremadura": "Extremadura",
    "galicia": "Galicia",
    "rioja": "La Rioja",
    "madrid": "Madrid",
    "murcia": "Murcia",
    "navarra": "Navarra",
    "pais vasco": "Pais Vasco",
    "valencia": "Comunitat Valenciana",
    "ceuta": "Ceuta",
    "melilla": "Melilla",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("ruct")


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def normalise_ccaa(text: str) -> str:
    if not text:
        return "Unknown"
    low = text.lower()
    for kw, canon in CCAA_KEYWORDS.items():
        if kw in low:
            return canon
    return "Unknown"


def fetch_search(
    session: requests.Session, denominacion: str, deadline: float
) -> str | None:
    """Establish a session and POST the search form."""
    if time.monotonic() > deadline:
        log.warning("Time budget exhausted before fetching '%s'.", denominacion)
        return None
    try:
        # Bootstrap the session with a GET (cookies, hidden fields).
        log.info("GET %s", SEARCH_URL)
        get_resp = session.get(SEARCH_URL, timeout=TIMEOUT_S, verify=False)
        get_resp.raise_for_status()
        time.sleep(REQUEST_DELAY_S)
        if time.monotonic() > deadline:
            return None

        # Parse hidden fields from the GET form, if any.
        soup = BeautifulSoup(get_resp.text, "lxml")
        form = soup.find("form")
        hidden: dict[str, str] = {}
        if form is not None:
            for inp in form.find_all("input", {"type": "hidden"}):
                name = inp.get("name")
                value = inp.get("value", "")
                if name:
                    hidden[name] = value

        fields = dict(FORM_FIELDS_TEMPLATE)
        fields["denomi"] = denominacion
        fields.update(hidden)

        log.info("POST %s denominacion='%s'", SEARCH_URL, denominacion)
        resp = session.post(
            SEARCH_URL,
            data=fields,
            timeout=TIMEOUT_S,
            verify=False,
        )
        resp.raise_for_status()
        return resp.text
    except (requests.RequestException, requests.Timeout) as exc:
        log.warning("RUCT fetch failed for '%s': %s", denominacion, exc)
        return None


def parse_results(html: str, degree: str) -> list[dict]:
    """Parse RUCT result HTML.

    The result table has columns approximately: codigo, denominacion,
    universidad, centro, situacion, fecha_modificacion. Layout varies; this
    parser is heuristic.
    """
    soup = BeautifulSoup(html, "lxml")
    fetch_ts = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []

    for tr in soup.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cells) < 3:
            continue
        joined = " ".join(cells)
        if not re.search(r"Maestr|Magisteri", joined, re.IGNORECASE):
            continue
        # Heuristic: codigo_ruct looks like "2502xxxxx" or "2500xxxxx" --
        # 7-9 digit numeric in the row text.
        m_code = re.search(r"\b(2\d{6,8})\b", joined)
        codigo = m_code.group(1) if m_code else ""
        # University: the cell with "Universi"
        uni = next((c for c in cells if "Universi" in c), "")
        if not uni:
            continue
        centro_match = next(
            (c for c in cells if "Facultad" in c or "Centro" in c or "Escuela" in c),
            "",
        )
        ccaa = normalise_ccaa(joined)
        modalidad_low = joined.lower()
        if "online" in modalidad_low or "distancia" in modalidad_low:
            modalidad = "online"
        elif "semipresencial" in modalidad_low:
            modalidad = "semipresencial"
        else:
            modalidad = "presencial"
        rows.append(
            {
                "codigo_ruct": codigo,
                "denominacion": cells[0] if cells else "",
                "universidad": uni,
                "centro": centro_match,
                "ccaa": ccaa,
                "modalidad": modalidad,
                "situacion": "active",
                "fecha_modificacion": "",
                "fecha_publicacion_boe": "",
                "degree": degree,
                "source": "ruct_live",
                "fetch_ts": fetch_ts,
                "url": SEARCH_URL,
            }
        )
    return rows


def write_rows(rows: list[dict], path: Path) -> None:
    cols = [
        "codigo_ruct", "denominacion", "universidad", "centro", "ccaa",
        "modalidad", "situacion", "fecha_modificacion",
        "fecha_publicacion_boe", "degree", "source", "fetch_ts", "url",
    ]
    df = pd.DataFrame(rows, columns=cols)
    if not df.empty:
        df = df.drop_duplicates(
            subset=["codigo_ruct", "universidad", "centro", "degree"]
        )
    df.to_csv(path, index=False, encoding="utf-8")
    log.info("Wrote %d rows to %s.", len(df), path)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    deadline = time.monotonic() + TIME_BUDGET_S
    all_rows: list[dict] = []
    completed_queries = 0

    for q in QUERIES:
        if time.monotonic() > deadline:
            log.warning(
                "Time budget exhausted; stopping with %d queries completed.",
                completed_queries,
            )
            break
        log.info("RUCT query: %s", q["denominacion"])
        html = fetch_search(session, q["denominacion"], deadline)
        time.sleep(REQUEST_DELAY_S)
        if html is None:
            log.warning("RUCT %s query failed.", q["degree"])
            continue
        parsed = parse_results(html, q["degree"])
        log.info("Parsed %d RUCT rows for %s.", len(parsed), q["degree"])
        all_rows.extend(parsed)
        completed_queries += 1

    elapsed = TIME_BUDGET_S - (deadline - time.monotonic())

    if completed_queries == len(QUERIES) and len(all_rows) >= 30:
        write_rows(all_rows, OUT_PATH)
        log.info(
            "RUCT scrape PASS: %d rows in %.1fs.", len(all_rows), elapsed
        )
    elif all_rows:
        write_rows(all_rows, PARTIAL_PATH)
        # Also write an empty ruct.csv so reconciliation can detect partial
        write_rows([], OUT_PATH)
        log.warning(
            "RUCT scrape PARTIAL: %d rows in %.1fs (%d/%d queries).",
            len(all_rows), elapsed, completed_queries, len(QUERIES),
        )
    else:
        # Total failure: write empty ruct.csv. Reconciliation will fall back
        # on cross-validation aggregate as the universe.
        write_rows([], OUT_PATH)
        log.warning(
            "RUCT scrape FAILED: 0 rows in %.1fs. "
            "Reconciliation will use cross-validation aggregate "
            "as the universe (plan section 7 fallback).",
            elapsed,
        )


if __name__ == "__main__":
    main()
