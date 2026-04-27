"""
educaweb_aggregator.py

Title:    Educaweb.com per-degree directory aggregator (Stage 0 Pass 1).
Author:   data-engineer (CDD curricular analysis project).
Date:     2026-04-27.
Purpose:  Cross-validation source for the programme universe (Layer 0).
          Captures private and online providers under-reported by gradomania.
          Reads the per-degree directory pages for Infantil and Primaria,
          extracts the (university, sector, modality) triples.
Inputs:   Two public HTML pages on educaweb.com.
Outputs:  data/raw/inventory_passes/educaweb.csv
          Columns: source, degree, university_name, ccaa, sector_hint,
                   modality_hint, fetch_ts, url
Notes:
  - INV-15: imports at top.
  - INV-16: pathlib.Path.
  - INV-19: no setwd / install.
  - 1 req/s rate-limit.
  - Pilot evidence: educaweb returned 17 universities for Infantil (8 public +
    9 private) with explicit modality tags. Pilot fallback list seeded from
    quality_reports/data_exploration_cdd_formacion_inicial.md.
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
OUT_PATH = OUT_DIR / "educaweb.csv"

URLS = {
    "infantil": "https://www.educaweb.com/estudio/titulacion-grado-educacion-infantil/",
    "primaria": "https://www.educaweb.com/estudio/titulacion-grado-educacion-primaria/",
}

USER_AGENT = (
    "Mozilla/5.0 (compatible; CDD-Research-Bot/1.0; "
    "+research; contact: juanmada10@gmail.com)"
)

REQUEST_DELAY_S = 1.0
TIMEOUT_S = 30

# Pilot-seed list of private and online providers + modality classification.
# Sources: data_exploration_cdd_formacion_inicial.md sections 1.1, 1.2, 4.1.
# (uni_name, ccaa, sector, modality, degrees)
PRIVATE_ONLINE_SEED = [
    ("Universidad Internacional de La Rioja (UNIR)", "La Rioja", "private-online", "online",
     ("infantil", "primaria")),
    ("Universidad Internacional de Valencia (VIU)", "Comunitat Valenciana",
     "private-online", "online", ("infantil", "primaria")),
    ("Universidad a Distancia de Madrid (UDIMA)", "Madrid",
     "private-online", "online", ("infantil", "primaria")),
    ("Universidad Nacional de Educacion a Distancia (UNED)", "Madrid",
     "public", "online", ("infantil",)),  # UNED Infantil online (public)
    ("Universidad Catolica de Valencia San Vicente Martir (UCV)",
     "Comunitat Valenciana", "private-traditional", "presencial",
     ("infantil", "primaria")),
    ("Universidad Pontificia de Salamanca (UPSA)", "Castilla y Leon",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad Camilo Jose Cela (UCJC)", "Madrid",
     "private-traditional", "semipresencial", ("infantil", "primaria")),
    ("Universidad Catolica de Avila (UCAV)", "Castilla y Leon",
     "private-traditional", "semipresencial", ("infantil", "primaria")),
    ("Universidad Alfonso X El Sabio (UAX)", "Madrid",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad Francisco de Vitoria (UFV)", "Madrid",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad CEU San Pablo", "Madrid",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad CEU Cardenal Herrera", "Comunitat Valenciana",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad de Navarra", "Navarra",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad de Deusto", "Pais Vasco",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Mondragon Unibertsitatea", "Pais Vasco",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universitat Internacional de Catalunya (UIC)", "Cataluna",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universitat Ramon Llull (URL)", "Cataluna",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universitat Abat Oliba CEU", "Cataluna",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad Loyola Andalucia", "Andalucia",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad Antonio de Nebrija", "Madrid",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad San Jorge", "Aragon",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad Europea de Madrid", "Madrid",
     "private-traditional", "presencial", ("infantil", "primaria")),
    ("Universidad Europea de Valencia", "Comunitat Valenciana",
     "private-traditional", "presencial", ("primaria",)),
    ("Universidad Isabel I", "Castilla y Leon",
     "private-online", "online", ("infantil", "primaria")),
]

CCAA_CANONICAL = {
    "andalucia": "Andalucia",
    "cataluna": "Cataluna",
    "madrid": "Madrid",
    "valencia": "Comunitat Valenciana",
    "castilla y leon": "Castilla y Leon",
    "navarra": "Navarra",
    "pais vasco": "Pais Vasco",
    "la rioja": "La Rioja",
    "aragon": "Aragon",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("educaweb")

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def fetch_html(url: str, session: requests.Session) -> str | None:
    try:
        resp = session.get(url, timeout=TIMEOUT_S)
        resp.raise_for_status()
        return resp.text
    except (requests.RequestException, requests.Timeout) as exc:
        log.warning("Fetch failed for %s: %s", url, exc)
        return None


def parse_listing(html: str, degree: str, url: str) -> list[dict]:
    """Parse the educaweb directory page.

    educaweb pages list each university in a card-like structure with
    sector/modality tags. The exact selector varies; use heuristics:
      - look for elements containing "Universi(dad|tat|dade)";
      - look for adjacent text nodes containing "presencial", "online",
        "semipresencial", "publica", "privada";
    """
    soup = BeautifulSoup(html, "lxml")
    fetch_ts = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    seen: set[str] = set()

    for el in soup.find_all(["a", "li", "div", "tr"]):
        text = el.get_text(" ", strip=True)
        if not text or len(text) > 600:
            continue
        m = re.search(r"(Universi(?:dad|tat|dade)[^,\-\(\n]{2,80})", text)
        if not m:
            continue
        uni = m.group(1).strip()
        if uni in seen:
            continue
        seen.add(uni)
        low = text.lower()
        if "online" in low or "a distancia" in low or "distancia" in low:
            modality = "online"
        elif "semipresencial" in low or "semi-presencial" in low:
            modality = "semipresencial"
        else:
            modality = "presencial"
        if "privada" in low:
            sector = "private-traditional"
        elif "publica" in low or "pública" in low:
            sector = "public"
        else:
            sector = "unknown"
        rows.append(
            {
                "source": "educaweb",
                "degree": degree,
                "university_name": uni,
                "ccaa": "Unknown",  # educaweb often lacks CCAA on directory
                "sector_hint": sector,
                "modality_hint": modality,
                "fetch_ts": fetch_ts,
                "url": url,
            }
        )
    return rows


def build_pilot_fallback() -> list[dict]:
    """Use the documented pilot-seed of private + online providers."""
    fetch_ts = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    for uni, ccaa, sector, modality, degrees in PRIVATE_ONLINE_SEED:
        for d in degrees:
            rows.append(
                {
                    "source": "educaweb_pilot_fallback",
                    "degree": d,
                    "university_name": uni,
                    "ccaa": ccaa,
                    "sector_hint": sector,
                    "modality_hint": modality,
                    "fetch_ts": fetch_ts,
                    "url": URLS[d],
                }
            )
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    all_rows: list[dict] = []
    live_total = 0
    for degree, url in URLS.items():
        log.info("Fetching %s listing: %s", degree, url)
        html = fetch_html(url, session)
        time.sleep(REQUEST_DELAY_S)
        if html is None:
            continue
        parsed = parse_listing(html, degree, url)
        log.info("Parsed %d rows for %s.", len(parsed), degree)
        live_total += len(parsed)
        all_rows.extend(parsed)

    # Always emit the pilot fallback rows on top of live (the pilot list
    # provides explicit sector/modality/CCAA tags that the live scrape often
    # cannot extract reliably from the card layout). Reconciliation handles
    # the dedup.
    fallback = build_pilot_fallback()
    log.info("Adding %d pilot-seeded private/online rows.", len(fallback))
    all_rows.extend(fallback)

    df = pd.DataFrame(all_rows)
    df = df.drop_duplicates(subset=["degree", "university_name"])
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    log.info(
        "Wrote %d rows to %s (live=%d, fallback included).",
        len(df),
        OUT_PATH,
        live_total,
    )


if __name__ == "__main__":
    main()
