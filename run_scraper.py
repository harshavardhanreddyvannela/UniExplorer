"""
Run a single country scraper directly.

Examples:
  python run_scraper.py --country austria
  python run_scraper.py --country "northern ireland" --limit 20
  python run_scraper.py --list
"""

import argparse
import json
import sys
from typing import Callable, Dict, List

from master import SCRAPERS


def _normalize_country(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _build_index(
    scrapers: Dict[str, Callable[[], List[Dict[str, str]]]],
) -> Dict[str, str]:
    index: Dict[str, str] = {}
    for country in scrapers:
        canonical = country
        normalized = _normalize_country(country)
        index[normalized] = canonical
        index[normalized.replace(" ", "_")] = canonical
        index[normalized.replace(" ", "-")] = canonical
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a single scraper by country name")
    parser.add_argument("--country", type=str, help="Country to scrape (e.g., austria)")
    parser.add_argument("--list", action="store_true", help="List available countries")
    parser.add_argument(
        "--limit", type=int, default=0, help="Limit printed rows (0 = all)"
    )
    parser.add_argument("--json", action="store_true", help="Print output as JSON")
    args = parser.parse_args()

    if args.list:
        for country in sorted(SCRAPERS.keys()):
            print(country)
        return

    if not args.country:
        parser.error("--country is required unless --list is used")

    index = _build_index(SCRAPERS)
    lookup = _normalize_country(args.country)
    canonical_country = index.get(lookup)

    if not canonical_country:
        print(f"Unknown country: {args.country}")
        print("Use --list to see available countries.")
        sys.exit(1)

    scraper = SCRAPERS[canonical_country]
    data = scraper()

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(f"{canonical_country}: {len(data)} institutions")

    rows = data if args.limit <= 0 else data[: args.limit]
    for item in rows:
        name = item.get("name", "")
        website = item.get("website", "")
        print(f"- {name} | {website}")


if __name__ == "__main__":
    main()
