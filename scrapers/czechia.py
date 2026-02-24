"""
Web scraper for Czechia universities.
"""

import re
from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SOURCE_URLS = [
    "https://msmt.gov.cz/areas-of-work/tertiary-education/public-higher-education-institutions-websites",
    "https://msmt.gov.cz/areas-of-work/tertiary-education/overview-of-private-higher-education-institutions",
]

BLOCKED_DOMAINS = (
    "msmt.gov.cz",
    "termsfeed.com",
    "qcm.eu",
)

BLOCKED_TEXTS = {"up", "jump to content", "jump to navigation", "home"}


def _clean_text(value: str) -> str:
    cleaned = " ".join(value.replace("\xa0", " ").split())
    cleaned = cleaned.replace("U niversity", "University")
    cleaned = re.sub(r"\s*\([^)]*\)", "", cleaned)
    return " ".join(cleaned.split())


def _extract_page_institutions(
    session: requests.Session, page_url: str
) -> List[Dict[str, str]]:
    response = session.get(page_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.select_one("#article") or soup.select_one("#content") or soup

    institutions: List[Dict[str, str]] = []
    list_items = article.select("li")

    if list_items:
        for li in list_items:
            li_text = _clean_text(li.get_text(" ", strip=True))

            for anchor in li.select("a[href]"):
                href = urljoin(page_url, anchor["href"].strip())
                anchor_text = _clean_text(anchor.get_text(" ", strip=True))

                name = li_text or anchor_text

                if not name or not href.startswith("http"):
                    continue
                if "#" in href:
                    continue
                if any(domain in href.lower() for domain in BLOCKED_DOMAINS):
                    continue
                if name.casefold() in BLOCKED_TEXTS:
                    continue

                institutions.append({"name": name, "website": href})
                break
    else:
        for anchor in article.select("a[href]"):
            name = _clean_text(anchor.get_text(" ", strip=True))
            href = urljoin(page_url, anchor["href"].strip())

            if not name or not href.startswith("http"):
                continue
            if "#" in href:
                continue
            if any(domain in href.lower() for domain in BLOCKED_DOMAINS):
                continue
            if name.casefold() in BLOCKED_TEXTS:
                continue

            institutions.append({"name": name, "website": href})

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
