"""
Web scraper for Denmark universities.
"""

import re
from typing import Dict, List
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup


def scrape_universities() -> List[Dict[str, str]]:
    """Scrape universities from Denmark's education website."""
    url = "https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/universiteter/"

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    )

    response = session.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.select_one("#content") or soup.select_one("main") or soup

    universities = []
    seen = set()

    for li in content.select("li"):
        # Get first link in each list item
        link = li.find("a", href=True)
        if not link:
            continue

        # Clean name: remove parenthetical content and extra whitespace
        name = link.get_text(strip=True)
        name = re.sub(r"\s*\([^)]*\)", "", name)
        name = " ".join(name.split())

        # Clean URL: remove query parameters and fragments
        href = urljoin(url, link["href"].strip())
        parts = urlsplit(href)
        website = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

        # Skip invalid or blocked links
        if not name or not website.startswith("http"):
            continue

        if "ufsn.dk" in website.lower():
            continue

        # Skip duplicates
        if name.lower() in seen:
            continue

        seen.add(name.lower())
        universities.append({"name": name, "website": website})

    return universities
