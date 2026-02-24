"""
Web scraper for Belgium universities (Flanders + Wallonia).
"""

from typing import Dict, List

from scrapers.flanders import scrape_universities as scrape_flanders
from scrapers.wallonia import scrape_universities as scrape_wallonia


def scrape_universities() -> List[Dict[str, str]]:
    universities: List[Dict[str, str]] = []
    seen = set()

    for source in (scrape_flanders, scrape_wallonia):
        for item in source():
            name = (item.get("name") or "").strip()
            website = (item.get("website") or "").strip()

            if not name or not website:
                continue

            key = (name.casefold(), website.casefold())
            if key in seen:
                continue

            seen.add(key)
            universities.append({"name": name, "website": website})

    return universities
