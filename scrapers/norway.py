"""
Norwegian higher education institutions scraper.
Source: NOKUT (Norwegian Agency for Quality Assurance in Education)
URL: https://www.nokut.no/hogare-utdanning/akkrediterte-institusjonar/
"""

from typing import Dict, List

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.nokut.no/hogare-utdanning/akkrediterte-institusjonar/"

BLOCKED_DOMAINS = ("nokut.no",)


def _extract_page_institutions(
    session: requests.Session, page_url: str
) -> List[Dict[str, str]]:
    response = session.get(page_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.select_one("main")
    if not main:
        return []

    institutions: List[Dict[str, str]] = []
    seen = set()

    # Get first ul list which contains all 4 sections
    first_ul = main.select_one("ul")
    if not first_ul:
        return []

    items = first_ul.select("li")

    # Find the index where the last section starts
    last_section_index = None
    for i, li in enumerate(items):
        a = li.select_one("a")
        if a:
            a_text = a.get_text(" ", strip=True)
            if a_text == "Høgskular med akkrediterte studietilbod":
                last_section_index = i
                break

    # Process items, skipping those at or after the last section
    for i, li in enumerate(items):
        if last_section_index is not None and i >= last_section_index:
            break

        a = li.select_one("a[href]")
        if not a:
            continue

        href = a.get("href", "").strip()
        text = " ".join(a.get_text(" ", strip=True).split())

        # Skip empty, non-http, or self-referential URLs
        if not text or not href:
            continue
        if not href.startswith("http"):
            continue
        if any(domain in href.lower() for domain in BLOCKED_DOMAINS):
            continue

        # Deduplicate by normalized name
        name_key = text.casefold()
        if name_key in seen:
            continue
        seen.add(name_key)

        institutions.append({"name": text, "website": href})

    return institutions


def scrape_universities() -> List[Dict[str, str]]:
    """
    Scrape Norwegian accredited higher education institutions from NOKUT.

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
