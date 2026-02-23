"""
Web scraper for Wallonia universities.
"""

from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "http://enseignement.be/index.php?page=28260&navi=4596"

TARGET_HEADINGS = {
    "universités",
    "hautes ecoles",
    "hautes écoles",
    "écoles supérieures des arts",
    "ecoles supérieures des arts",
}

BLOCKED_DOMAINS = (
    "enseignement.be",
    "cfwb.be",
    "federation-wallonie-bruxelles.be",
    "facebook.com",
    "faq.enseignement.be",
    "gallilex.cfwb.be",
    "mesetudes.be",
)


def _normalize(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").strip().lower().split())


def _extract_section_links(heading_tag) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    next_node = heading_tag.find_next_sibling()

    while next_node:
        if next_node.name in {"h2", "h3"}:
            break

        for li in next_node.select("li"):
            for anchor in li.select("a[href]"):
                name = " ".join(
                    anchor.get_text(" ", strip=True).replace("\xa0", " ").split()
                )
                href = urljoin(SOURCE_URL, anchor["href"].strip())
                lowered_href = href.lower()

                if not name or not href.startswith("http"):
                    continue
                if any(domain in lowered_href for domain in BLOCKED_DOMAINS):
                    continue

                items.append({"name": name, "website": href})
                break

        next_node = next_node.find_next_sibling()

    return items


def scrape_universities() -> List[Dict[str, str]]:
    response = requests.get(
        SOURCE_URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    universities: List[Dict[str, str]] = []
    seen = set()

    for heading in soup.find_all(["h2", "h3"]):
        heading_text = _normalize(heading.get_text(" ", strip=True))
        if heading_text not in TARGET_HEADINGS:
            continue

        for item in _extract_section_links(heading):
            key = item["name"].casefold()
            if key in seen:
                continue
            seen.add(key)
            universities.append(item)

    return universities
