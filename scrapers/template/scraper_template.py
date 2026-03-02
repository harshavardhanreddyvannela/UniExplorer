from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse
import time

import requests


@dataclass
class ScrapedUniversity:
    official_name: str
    english_name: str | None
    region: str
    country: str
    website: str


class BaseGeographyScraper:
    """
    Uniform scraper contract used across all geography-specific scrapers.

    Override extension points:
    - get_source_descriptors
    - parse_source
    - normalize_row (optional, if parse output already normalized)
    """

    name = "base"
    max_attempts = 3
    timeout_seconds = 20
    backoff_seconds = (1, 2, 4)

    def run(self) -> list[ScrapedUniversity]:
        print(f"[{self.name}] start")

        parsed_rows: list[dict[str, Any]] = []
        failures: list[str] = []

        for source in self.get_source_descriptors():
            try:
                payload = self.fetch_source(source)
                parsed_rows.extend(self.parse_source(source, payload))
            except Exception as exc:
                failures.append(f"source={source} error={exc}")
                print(f"[{self.name}] source failure: {exc}")

        normalized: list[ScrapedUniversity] = []
        for row in parsed_rows:
            try:
                normalized_row = self.normalize_row(row)
                if self.validate_row(normalized_row):
                    normalized.append(normalized_row)
            except Exception as exc:
                failures.append(f"row={row} error={exc}")

        deduped = self.deduplicate_by_domain(normalized)
        self.emit_records(deduped)
        self.print_summary(len(parsed_rows), len(deduped), failures)
        return deduped

    def get_source_descriptors(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def fetch_source(self, source: dict[str, Any]) -> Any:
        source_type = source.get("type")
        source_url = source.get("url")

        if source_type in {"html", "json"}:
            response = self._request_with_retry(source_url)
            if source_type == "json":
                return response.json()
            return response.text

        if source_type in {"xlsx", "csv"}:
            response = self._request_with_retry(source_url)
            return response.content

        raise ValueError(f"Unsupported source type: {source_type}")

    def parse_source(self, source: dict[str, Any], payload: Any) -> list[dict[str, Any]]:
        raise NotImplementedError

    def normalize_row(self, row: dict[str, Any]) -> ScrapedUniversity:
        official_name = str(row["official_name"]).strip()
        english_name = row.get("english_name")
        english_name = str(english_name).strip() if english_name else None
        region = str(row["region"]).strip()
        country = str(row["country"]).strip()
        website = self.normalize_website(str(row["website"]).strip())

        return ScrapedUniversity(
            official_name=official_name,
            english_name=english_name,
            region=region,
            country=country,
            website=website,
        )

    def validate_row(self, row: ScrapedUniversity) -> bool:
        if not row.official_name or not row.region or not row.country or not row.website:
            return False
        parsed = urlparse(row.website)
        return parsed.scheme in {"https", "http"} and bool(parsed.netloc)

    def deduplicate_by_domain(self, rows: list[ScrapedUniversity]) -> list[ScrapedUniversity]:
        seen: set[str] = set()
        deduped: list[ScrapedUniversity] = []

        for row in rows:
            domain = urlparse(row.website).netloc.lower()
            if domain in seen:
                continue
            seen.add(domain)
            deduped.append(row)

        return deduped

    def emit_records(self, rows: list[ScrapedUniversity]) -> None:
        print(f"[{self.name}] prepared {len(rows)} records for DB write")

    def print_summary(self, parsed_count: int, final_count: int, failures: list[str]) -> None:
        print(f"[{self.name}] parsed={parsed_count} final={final_count} failures={len(failures)}")
        for failure in failures:
            print(f"[{self.name}] failure: {failure}")

    def normalize_website(self, website: str) -> str:
        if website.startswith("http://"):
            website = "https://" + website.removeprefix("http://")
        elif not website.startswith("https://"):
            website = "https://" + website
        return website

    def _request_with_retry(self, url: str) -> requests.Response:
        last_error: Exception | None = None

        for attempt in range(self.max_attempts):
            try:
                response = requests.get(url, timeout=self.timeout_seconds)
                response.raise_for_status()
                return response
            except Exception as exc:
                last_error = exc
                if attempt < self.max_attempts - 1:
                    time.sleep(self.backoff_seconds[attempt])

        raise RuntimeError(f"request failed: {url}") from last_error
