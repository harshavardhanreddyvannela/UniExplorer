"""
Web scraper for Flanders universities.
"""

from typing import Dict, List

import requests

SOURCE_URL = (
    "https://api.hogeronderwijsregister.be/api/institution?search=&page=0&size=0"
)

EXCLUDED_TYPES = {
    "Secundaire school",
    "Associatie",
    "Niet-ambtshalve geregistreerde instelling",
}


def scrape_universities() -> List[Dict[str, str]]:
    response = requests.get(
        SOURCE_URL,
        timeout=60,
        headers={
            "accept": "application/json, text/plain, */*",
            "origin": "https://www.hogeronderwijsregister.be",
            "referer": "https://www.hogeronderwijsregister.be/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "x-content-language": "nl",
        },
    )
    response.raise_for_status()

    payload = response.json()
    content = payload.get("content", []) if isinstance(payload, dict) else []

    universities: List[Dict[str, str]] = []
    seen_names = set()

    for item in content:
        if not isinstance(item, dict):
            continue

        institution_type = item.get("type")
        if institution_type in EXCLUDED_TYPES:
            continue

        name = (item.get("name") or "").strip()
        website = (item.get("url") or "").strip()

        if not name or not website:
            continue

        name_key = name.casefold()
        if name_key in seen_names:
            continue

        seen_names.add(name_key)
        universities.append({"name": name, "website": website})

    return universities
