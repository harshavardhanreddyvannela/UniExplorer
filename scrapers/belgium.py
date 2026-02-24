"""
Web scraper for Belgium universities.
"""

from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

FLANDERS_API_URL = (
    "https://api.hogeronderwijsregister.be/api/institution?search=&page=0&size=0"
)
WALLONIA_URL = "http://enseignement.be/index.php?page=28260&navi=4596"

BLOCKED_DOMAINS = (
    "enseignement.be",
    "cfwb.be",
    "federation-wallonie-bruxelles.be",
    "facebook.com",
    "faq.enseignement.be",
    "gallilex.cfwb.be",
    "mesetudes.be",
)


def _extract_flanders(session: requests.Session) -> List[Dict[str, str]]:
    """Extract universities from Flanders higher education register API."""
    response = session.get(
        FLANDERS_API_URL,
        timeout=60,
        headers={
            "accept": "application/json, text/plain, */*",
            "origin": "https://www.hogeronderwijsregister.be",
            "referer": "https://www.hogeronderwijsregister.be/",
        },
    )
    response.raise_for_status()

    data = response.json()
    institutions = data.get("content", [])

    universities = []
    for institution in institutions:
        if institution.get("type") != "Universiteit":
            continue

        name = institution.get("name", "").strip()
        website = institution.get("url", "").strip()

        if name and website:
            universities.append({"name": name, "website": website})

    return universities


def _extract_wallonia(session: requests.Session) -> List[Dict[str, str]]:
    """Extract universities from Wallonia education website."""
    response = session.get(WALLONIA_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    universities = []

    for heading in soup.find_all(["h2", "h3"]):
        heading_text = heading.get_text(strip=True).lower()

        if "universités" not in heading_text:
            continue

        next_element = heading.find_next_sibling()

        while next_element and next_element.name not in ["h2", "h3"]:
            for li in next_element.select("li"):
                link = li.find("a", href=True)
                if not link:
                    continue

                name = link.get_text(strip=True)
                website = urljoin(WALLONIA_URL, link["href"].strip())

                if not name or not website.startswith("http"):
                    continue

                if any(domain in website.lower() for domain in BLOCKED_DOMAINS):
                    continue

                universities.append({"name": name, "website": website})

            next_element = next_element.find_next_sibling()

    return universities


def scrape_universities() -> List[Dict[str, str]]:
    """Scrape universities from Belgium (Flanders and Wallonia)."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    )

    universities: List[Dict[str, str]] = []
    seen = set()

    # Extract from both Flanders and Wallonia
    for extractor in (_extract_flanders, _extract_wallonia):
        for item in extractor(session):
            key = item["name"].casefold()
            if key in seen:
                continue
            seen.add(key)
            universities.append(item)

    return universities
