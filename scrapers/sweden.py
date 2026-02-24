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


def scrape_universities() -> List[Dict[str, str]]:
    """Scrape Swedish universities from UKÄ (excluding högskolor and other institutions)."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    )

    response = session.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main = (
        soup.select_one("main")
        or soup.select_one('[role="main"]')
        or soup.select_one("article")
    )
    if not main:
        return []

    universities = []
    seen = set()
    in_university_section = False

    # Parse sections: only extract from sections with "universitet" in the heading
    for elem in main.select("h2, a[href]"):
        if elem.name == "h2":
            heading_text = elem.get_text(strip=True).lower()
            # Only include universities section, not högskolor or other sections
            if "universitet" in heading_text and "webbplats" in heading_text:
                in_university_section = True
            else:
                in_university_section = False

        elif elem.name == "a" and in_university_section:
            href = elem.get("href", "").strip()
            text = elem.get_text(strip=True)

            # Skip invalid links or short text
            if not text or not href.startswith("http"):
                continue
            if len(text) < 5 or "English version" in text:
                continue
            if any(domain in href.lower() for domain in BLOCKED_DOMAINS):
                continue

            # Clean institution name
            name = text.split(",")[0].strip()
            if "(" in name:
                name = name.split("(")[0].strip()

            # Remove "webbplats" suffix and genitive 's'
            name = name.replace(" webbplats", "").strip()
            if name.endswith("s"):
                name = name[:-1]

            # Skip duplicates
            if name.lower() in seen:
                continue
            seen.add(name.lower())

            universities.append({"name": name, "website": href})

    return universities
