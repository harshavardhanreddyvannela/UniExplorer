"""
Norwegian higher education institutions scraper.
Source: NOKUT (Norwegian Agency for Quality Assurance in Education)
URL: https://www.nokut.no/hogare-utdanning/akkrediterte-institusjonar/
"""

from typing import Dict, List

import requests
from bs4 import BeautifulSoup


def scrape_universities() -> List[Dict[str, str]]:
    """Scrape Norwegian universities and specialized universities from NOKUT."""
    url = "https://www.nokut.no/hogare-utdanning/akkrediterte-institusjonar/"

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    )

    response = session.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.select_one("main")
    if not main:
        return []

    universities = []
    seen = set()

    # Get first ul list which contains all sections
    first_ul = main.select_one("ul")
    if not first_ul:
        return []

    # Track which section we're in based on counting
    section_count = 0
    in_valid_section = False

    for li in first_ul.select("li"):
        a = li.select_one("a")
        if not a:
            continue

        text = a.get_text(strip=True)
        href = a.get("href", "").strip()

        # Detect section headers (non-http links, typically just anchors or no href)
        if not href or not href.startswith("http"):
            # This is a section header
            section_count += 1
            # Section 1: Universitet (Universities)
            # Section 2: Vitenskapelige høgskular (Specialized universities)
            # Section 3+: Other categories (skip these)
            in_valid_section = section_count <= 2
            continue

        # Only process if we're in sections 1 or 2
        if not in_valid_section:
            continue

        # Skip invalid or blocked links
        if not text:
            continue
        if "nokut.no" in href.lower():
            continue

        # Skip duplicates
        if text.lower() in seen:
            continue
        seen.add(text.lower())

        universities.append({"name": text, "website": href})

    return universities
