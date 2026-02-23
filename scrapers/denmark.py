"""
Web scraper for Denmark universities.
"""

import re
from typing import Dict, List
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

SOURCE_URLS = [
    "https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/universiteter/",
    "https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/kunstneriske-uddannelsesinstitutioner/",
    "https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/professionshoejskoler/",
    "https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/erhvervsakademier/",
    "https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/maritime-uddannelsesinstitutioner/",
]

BLOCKED_DOMAINS = ("ufsn.dk",)


def _clean_name(name: str) -> str:
    cleaned = " ".join(name.replace("\xa0", " ").split())
    cleaned = re.sub(r"\s*\([^)]*\)", "", cleaned)
    return " ".join(cleaned.split())


def _clean_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _extract_page_institutions(
    session: requests.Session, page_url: str
) -> List[Dict[str, str]]:
    response = session.get(page_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.select_one("#content") or soup.select_one("main") or soup

    institutions: List[Dict[str, str]] = []
    for li in article.select("li"):
        for anchor in li.select("a[href]"):
            name = _clean_name(anchor.get_text(" ", strip=True))
            href = _clean_url(urljoin(page_url, anchor["href"].strip()))

            if not name or not href.startswith("http"):
                continue
            if any(domain in href.lower() for domain in BLOCKED_DOMAINS):
                continue

            institutions.append({"name": name, "website": href})
            break

    return institutions


def scrape_universities() -> List[Dict[str, str]]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }
    )

    universities: List[Dict[str, str]] = []
    seen = set()

    for page_url in SOURCE_URLS:
        for item in _extract_page_institutions(session, page_url):
            key = item["name"].casefold()
            if key in seen:
                continue
            seen.add(key)
            universities.append(item)

    return universities
