"""
Web scraper for Poland universities.
"""

from typing import Dict, List
from urllib.parse import urlparse

import requests

SOURCE_URL = "https://radon.nauka.gov.pl/opendata/polon/institutions"
RESULTS_PER_PAGE = 100
INSTITUTION_KINDS = ["1", "10", "13"]
INSTITUTION_TYPES = ["1"]  # 1 = academic, 2 = vocational
STATUS_CODES = ["1"]


def _normalize_website(url: str) -> str:
    website = (url or "").strip()
    if not website:
        return ""

    parsed = urlparse(website)
    if parsed.scheme:
        return website

    return f"https://{website}"


def _build_base_params() -> List[tuple[str, str]]:
    params: List[tuple[str, str]] = [("resultNumbers", str(RESULTS_PER_PAGE))]
    params.extend(("iKindCd", kind) for kind in INSTITUTION_KINDS)
    params.extend(("uTypeCd", utype) for utype in INSTITUTION_TYPES)
    params.extend(("statusCode", status) for status in STATUS_CODES)
    return params


def scrape_universities() -> List[Dict[str, str]]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
    )

    universities: List[Dict[str, str]] = []
    seen = set()
    token: str | None = None

    while True:
        params = _build_base_params()
        if token:
            params.append(("token", token))

        response = session.get(SOURCE_URL, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()

        batch = payload.get("results", [])
        for item in batch:
            name = (item.get("name") or "").strip()
            website = _normalize_website(item.get("www") or "")
            institution_kind = (item.get("iKindCd") or "").strip()

            if not name:
                continue

            key = (name.casefold(), website.casefold())
            if key in seen:
                continue

            seen.add(key)
            universities.append(
                {"name": name, "website": website, "institution_kind": institution_kind}
            )

        next_token = ((payload.get("pagination") or {}).get("token") or "").strip()
        if not batch or not next_token or next_token == token:
            break

        token = next_token

    filtered_universities: List[Dict[str, str]] = []
    for university in universities:
        if university["institution_kind"] == "1" and not university["website"]:
            continue

        filtered_universities.append(
            {
                "name": university["name"],
                "website": university["website"],
            }
        )

    return filtered_universities
