"""
Swiss higher education institutions scraper.
Source: SWISSUNIVERSITIES
URL: https://www.swissuniversities.ch/en/topics/studying/accredited-swiss-higher-education-institutions
"""

from typing import Dict, List

import requests
from bs4 import BeautifulSoup


def scrape_universities() -> List[Dict[str, str]]:
    """Scrape Swiss universities from SWISSUNIVERSITIES."""
    url = "https://www.swissuniversities.ch/en/topics/studying/accredited-swiss-higher-education-institutions"

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    )

    response = session.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.select_one('[role="main"]')
    if not main:
        return []

    universities = []
    seen = set()
    in_universities_section = False

    # Extract only from "Universities" section
    for elem in main.select("h2, a[href]"):
        if elem.name == "h2":
            heading_text = elem.get_text(strip=True)
            # Only process the "Universities" section
            in_universities_section = heading_text == "Universities"

        elif elem.name == "a" and in_universities_section:
            href = elem.get("href", "").strip()
            text = elem.get_text(strip=True)

            # Skip invalid links
            if not text or not href.startswith("http"):
                continue
            if len(text) < 5:
                continue
            if "swissuniversities.ch" in href.lower():
                continue

            # Skip duplicates
            if text.lower() in seen:
                continue
            seen.add(text.lower())

            universities.append({"name": text, "website": href})

    return universities
