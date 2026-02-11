"""
Web scraper for Norwegian universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin, urlparse

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Norway.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        List of dictionaries with 'name' and 'website' keys
    """
    universities = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')

        universities = []
        seen = set()
        for title in ['Universitet', 'Vitskaplege høgskular', 'Vitenskapelege høgskular']:
            section_links = _collect_section_links(soup, url, title)
            for item in section_links:
                key = (item['name'], item['website'])
                if key in seen:
                    continue
                seen.add(key)
                universities.append(item)
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Norway: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Norway: {str(e)}")
    
    return universities

def _collect_section_links(soup: BeautifulSoup, base_url: str, title: str) -> List[Dict[str, str]]:
    anchor_links = _collect_anchor_section_links(soup, base_url, title)
    if anchor_links:
        return anchor_links

    candidates = []
    for tag in soup.find_all(['h2', 'h3', 'h4', 'button', 'summary', 'span', 'p']):
        text = tag.get_text(" ", strip=True)
        if text.lower() == title.lower():
            candidates.append(tag)

    for tag in candidates:
        for attr in ['aria-controls', 'data-target', 'data-accordion-target', 'data-collapse-target']:
            target_id = tag.get(attr)
            if target_id:
                target = soup.find(id=target_id.lstrip('#'))
                if target:
                    links = _extract_links(target, base_url)
                    if links:
                        return _filter_links(links)

        details = tag.find_parent('details')
        if details:
            links = _extract_links(details, base_url)
            if links:
                return _filter_links(links)

        links = _extract_links_from_siblings(tag, base_url)
        if links:
            return _filter_links(links)

    for tag in candidates:
        parent = tag.find_parent(['section', 'div', 'article', 'li'])
        if parent:
            links = _extract_links(parent, base_url)
            if links:
                return _filter_links(links)

    return []

def _collect_anchor_section_links(soup: BeautifulSoup, base_url: str, title: str) -> List[Dict[str, str]]:
    for link in soup.find_all('a', href=True):
        text = link.get_text(" ", strip=True)
        href = link['href'].strip()
        if text.lower() == title.lower() and href.startswith('#'):
            target = soup.find(id=href.lstrip('#'))
            if target:
                links = _extract_links(target, base_url)
                return _filter_links(links)
    return []

def _extract_links_from_siblings(tag, base_url: str) -> List[Dict[str, str]]:
    stop_titles = {
        'universitet',
        'vitskaplege høgskular',
        'vitenskapelege høgskular',
        'høgskular med institusjonsakkreditering',
        'hogskular med institusjonsakkreditering',
        'høgskular med akkrediterte studietilbod',
        'hogskular med akkrediterte studietilbod',
    }
    links = []
    current = tag.find_next_sibling()
    while current:
        if current.name in ['h2', 'h3', 'h4', 'button', 'summary']:
            text = current.get_text(" ", strip=True).lower()
            if text in stop_titles:
                break
        links.extend(_extract_links(current, base_url))
        current = current.find_next_sibling()
    return links

def _extract_links(container, base_url: str) -> List[Dict[str, str]]:
    links = []
    for link in container.find_all('a', href=True):
        name = link.get_text(" ", strip=True)
        href = urljoin(base_url, link['href'].strip())
        if not name or not href.startswith('http'):
            continue
        if ' (' in name and name.endswith(')'):
            name = name.rsplit(' (', 1)[0].strip()
        links.append({'name': name, 'website': href})
    return links

def _filter_links(links: List[Dict[str, str]]) -> List[Dict[str, str]]:
    excluded_domains = {
        'nokut.no',
        'uustatus.no',
        'facebook.com',
        'linkedin.com',
        'gulesider.no',
    }
    seen = set()
    results = []

    for item in links:
        parsed = urlparse(item['website'])
        domain = parsed.netloc.lower()
        if not domain or any(domain.endswith(d) for d in excluded_domains):
            continue
        key = (item['name'], item['website'])
        if key in seen:
            continue
        seen.add(key)
        results.append(item)

    return results
