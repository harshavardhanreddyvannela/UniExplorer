"""
Swiss higher education institutions scraper.
Source: SWISSUNIVERSITIES
URL: https://www.swissuniversities.ch/en/topics/studying/accredited-swiss-higher-education-institutions
"""

from typing import Dict, List

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.swissuniversities.ch/en/topics/studying/accredited-swiss-higher-education-institutions"

BLOCKED_DOMAINS = ("swissuniversities.ch",)


def _extract_applied_sciences(soup: BeautifulSoup, seen: set) -> List[Dict[str, str]]:
    """Extract Applied Sciences institutions from accordion.

    Handles both simple organizations (single link) and complex ones (multiple sections).
    """
    institutions: List[Dict[str, str]] = []

    accordion = soup.select_one("#accordion-28932")
    if not accordion:
        return institutions

    cards = accordion.find_all("div", class_="card")

    for card in cards:
        button = card.find("button")
        if not button:
            continue

        # Get the collapse section with links
        collapse = card.find("div", class_="collapse")
        if not collapse:
            continue

        bodytext = collapse.select_one(".ce-bodytext")
        if not bodytext:
            continue

        # Check if this organization has multi-section structure (multiple P tags)
        p_tags = list(bodytext.find_all("p", recursive=False))

        if len(p_tags) > 1:
            # Complex structure with sections (e.g., HES-SO)
            for p_tag in p_tags:
                p_links = p_tag.find_all("a", href=True)

                if p_links:
                    # P tag has a link: extract the heading link as one institution
                    for link in p_links:
                        href = link.get("href", "").strip()
                        text = link.get_text(strip=True)
                        if href.startswith("http") and not any(
                            domain in href.lower() for domain in BLOCKED_DOMAINS
                        ):
                            name_key = text.casefold()
                            if name_key not in seen:
                                seen.add(name_key)
                                institutions.append({"name": text, "website": href})
                            break
                else:
                    # P tag has no link: extract all links from following UL
                    next_ul = p_tag.find_next_sibling("ul")
                    if next_ul:
                        ul_links = next_ul.find_all("a", href=True)
                        for link in ul_links:
                            href = link.get("href", "").strip()
                            text = " ".join(link.get_text(" ", strip=True).split())
                            if (
                                text
                                and href.startswith("http")
                                and not any(
                                    domain in href.lower() for domain in BLOCKED_DOMAINS
                                )
                            ):
                                name_key = text.casefold()
                                if name_key not in seen:
                                    seen.add(name_key)
                                    institutions.append({"name": text, "website": href})
        else:
            # Simple structure: just extract first link from organization
            all_links = collapse.find_all("a", href=True)
            if all_links:
                for link in all_links:
                    href = link.get("href", "").strip()
                    if href.startswith("http") and not any(
                        domain in href.lower() for domain in BLOCKED_DOMAINS
                    ):
                        # Use organization name, not link text
                        org_name = button.get_text(strip=True)
                        name_key = org_name.casefold()
                        if name_key not in seen:
                            seen.add(name_key)
                            institutions.append({"name": org_name, "website": href})
                        break

    return institutions


def _extract_page_institutions(
    session: requests.Session, page_url: str
) -> List[Dict[str, str]]:
    response = session.get(page_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.select_one('[role="main"]')
    if not main:
        return []

    institutions: List[Dict[str, str]] = []
    seen = set()

    current_section = None

    # First, extract Applied Sciences from accordion
    institutions.extend(_extract_applied_sciences(soup, seen))

    # Then extract other sections from direct links
    for elem in main.select("h2, a[href]"):
        if elem.name == "h2":
            text = elem.get_text(" ", strip=True)
            valid_sections = [
                "Universities",
                "Universities of Teacher Education",
                "Other institutions of the higher education sector",
            ]
            if text in valid_sections:
                current_section = text
            else:
                current_section = None

        # Extract direct links from non-Applied Sciences sections
        elif current_section and elem.name == "a":
            href = elem.get("href", "").strip()
            text = " ".join(elem.get_text(" ", strip=True).split())

            # Skip empty, non-http, short text, or self-referential URLs
            if not text or not href.startswith("http"):
                continue
            if len(text) < 5:
                continue
            if any(domain in href.lower() for domain in BLOCKED_DOMAINS):
                continue
            # Skip legislation/policy links
            if (
                "fedlex" in href.lower()
                or "act" in text.lower()
                and "education" in text.lower()
            ):
                continue

            # Deduplicate by normalized name
            name_key = text.casefold()
            if name_key in seen:
                continue
            seen.add(name_key)

            institutions.append({"name": text, "website": href})

    return institutions


def scrape_universities() -> List[Dict[str, str]]:
    """
    Scrape Swiss accredited higher education institutions from SWISSUNIVERSITIES.

    Returns:
        List[Dict[str, str]]: List of institutions with 'name' and 'website' keys.
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }
    )

    universities: List[Dict[str, str]] = []
    seen = set()

    for item in _extract_page_institutions(session, SOURCE_URL):
        key = item["name"].casefold()
        if key in seen:
            continue
        seen.add(key)
        universities.append(item)

    return universities
