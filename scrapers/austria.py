"""
Web scraper for Austria universities.
"""

import re
from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SOURCE_URLS = {
    "universities": "https://www.bmfwf.gv.at/wissenschaft/hochschulsystem/unis/unis-liste.html",
    "fachhochschulen": "https://www.bmfwf.gv.at/wissenschaft/hochschulsystem/fh/fh-liste.html",
    "private": "https://www.bmfwf.gv.at/wissenschaft/hochschulsystem/privatunis/privatunis-liste.html",
    "paedagogische": "https://www.bmfwf.gv.at/wissenschaft/hochschulsystem/paedagogische-hochschulen.html",
}

BLOCKED_DOMAINS = (
    "bmfwf.gv.at",
    "bmb.gv.at",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "youtube.com",
    "ris.bka.gv.at",
    "qsr.at",
    "lehramt-ost.at",
    "lehramt-so.at",
    "lehrerinnenbildung-west.at",
    "lehrerin-werden.at",
)

PATTERNS = {
    "universities": re.compile(
        r"(universität|university|akademie|mozarteum|montanuniversität|wirtschaftsuniversität)",
        re.IGNORECASE,
    ),
    "fachhochschulen": re.compile(
        r"(fachhochschule|hochschule für angewandte wissenschaften|\bfh\b|\bimc\b|\bmci\b|\bfhw\b|lauder business school|zentrum für gesundheitsberufe tirol|ferdinand porsche fernfachhochschule|fh gesundheitsberufe)",
        re.IGNORECASE,
    ),
    "private": re.compile(
        r"(privatunivers|privathochschule|private university|central european university|webster)",
        re.IGNORECASE,
    ),
    "paedagogische": re.compile(
        r"(pädagogische hochschule|paedagogische hochschule|hochschule für agrar- und umweltpädagogik|private pädagogische hochschule|kirchliche pädagogische hochschule)",
        re.IGNORECASE,
    ),
}


def _is_blocked(url: str) -> bool:
    lowered = url.lower()
    return any(domain in lowered for domain in BLOCKED_DOMAINS)


def _clean_name(name: str) -> str:
    return " ".join(name.replace("\xa0", " ").split())


def _extract_for_category(
    session: requests.Session, category: str, url: str
) -> List[Dict[str, str]]:
    response = session.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    pattern = PATTERNS[category]

    seen_names = set()
    results: List[Dict[str, str]] = []

    for anchor in soup.select("li a[href]"):
        name = _clean_name(anchor.get_text(" ", strip=True))
        href = urljoin(url, anchor["href"].strip())

        if not name or not href.startswith("http"):
            continue
        if _is_blocked(href):
            continue
        if not pattern.search(name):
            continue

        name_key = name.casefold()
        if name_key in seen_names:
            continue

        seen_names.add(name_key)
        results.append({"name": name, "website": href})

    return results


def scrape_universities() -> List[Dict[str, str]]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }
    )

    all_universities: List[Dict[str, str]] = []
    for category, url in SOURCE_URLS.items():
        all_universities.extend(_extract_for_category(session, category, url))

    return all_universities
