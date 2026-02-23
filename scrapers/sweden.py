"""
Swedish higher education institutions scraper.
Source: UKÄ (Swedish Higher Education Authority)
URL: https://www.uka.se/.../lista-over-universitet-hogskolor-och-enskilda-utbildningsanordnare
"""

from typing import Dict, List

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.uka.se/sa-fungerar-hogskolan/universitet-och-hogskolor/lista-over-universitet-hogskolor-och-enskilda-utbildningsanordnare"

BLOCKED_DOMAINS = ("uka.se",)


def _extract_page_institutions(
    session: requests.Session, page_url: str
) -> List[Dict[str, str]]:
    response = session.get(page_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main = (
        soup.select_one("main")
        or soup.select_one('[role="main"]')
        or soup.select_one("article")
    )
    if not main:
        return []

    institutions: List[Dict[str, str]] = []
    seen = set()

    # Extract by section: h2 headings with institution links below
    current_section = None

    for elem in main.select("h2, a[href]"):
        if elem.name == "h2":
            heading = elem.get_text(" ", strip=True)
            if "webbplats" in heading.lower():
                current_section = heading
        elif elem.name == "a" and current_section:
            href = elem.get("href", "").strip()
            text = " ".join(elem.get_text(" ", strip=True).split())

            # Skip non-external links or short text
            if not text or not href.startswith("http"):
                continue
            if len(text) < 5 or "English version" in text:
                continue
            if any(domain in href.lower() for domain in BLOCKED_DOMAINS):
                continue

            # Extract institution name (remove URL part and domain abbreviations)
            name = text.split(",")[0].strip()
            if "(" in name:
                name = name.split("(")[0].strip()

            # Remove "webbplats" suffix and common suffixes
            name = name.replace(" webbplats", "").strip()
            if name.endswith("s"):
                name = name[:-1]  # Remove trailing 's' from genitive forms

            # Deduplicate by normalized name
            name_key = name.casefold()
            if name_key in seen:
                continue
            seen.add(name_key)

            institutions.append({"name": name, "website": href})

    return institutions


def scrape_universities() -> List[Dict[str, str]]:
    """
    Scrape Swedish higher education institutions from UKÄ.

    Returns:
        List[Dict[str, str]]: List of institutions with 'name' and 'website' keys.
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }
    )

    universities: List[Dict[str, str]] = []
    seen = set()

    for item in _extract_page_institutions(session, SOURCE_URL):
        key = item["name"].casefold()
        if key in seen:
            continue
        seen.add(key)
        universities.append(item)

    return universities
