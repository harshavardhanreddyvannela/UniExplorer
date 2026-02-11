"""
Web scraper for Danish universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin, urlparse

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Denmark.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        List of dictionaries with 'name' and 'website' keys
    """
    universities = []
    seen = set()
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the two relevant section links from the overview page
        universities_url = None
        arts_url = None
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()
            text = link.get_text(strip=True)
            if 'universiteter' in href and text.lower() == 'universiteter':
                universities_url = urljoin(url, href)
            if 'kunstneriske-uddannelsesinstitutioner' in href:
                arts_url = urljoin(url, href)

        if not universities_url:
            universities_url = 'https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/universiteter/'
        if not arts_url:
            arts_url = 'https://ufsn.dk/uddannelse/de-videregaaende-uddannelsesinstitutioner/kunstneriske-uddannelsesinstitutioner/'

        for page_url, marker in [
            (universities_url, 'Danmark har otte universiteter:'),
            (arts_url, 'kunstneriske uddannelsesinstitutioner:'),
        ]:
            page_unis = _scrape_page_links(page_url, headers, marker)
            for uni in page_unis:
                key = (uni['name'], uni['website'])
                if key in seen:
                    continue
                seen.add(key)
                universities.append(uni)
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Denmark: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Denmark: {str(e)}")
    
    return universities

def _scrape_page_links(page_url: str, headers: Dict[str, str], marker: str) -> List[Dict[str, str]]:
    response = requests.get(page_url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the marker paragraph, then collect links in subsequent siblings
    marker_tag = None
    for tag in soup.find_all(['p', 'div']):
        if marker in tag.get_text(strip=True):
            marker_tag = tag
            break

    collected = []
    if marker_tag:
        current = marker_tag.find_next_sibling()
        while current and current.name not in ['h2', 'h3']:
            collected.extend(_extract_links(current, page_url))
            current = current.find_next_sibling()

    if not collected:
        main = soup.find('main') or soup
        collected = _extract_links(main, page_url)

    return _filter_links(collected)

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
        'ufsn.dk',
        'ufm.dk',
        'su.dk',
        'gribverden.dk',
        'forsk.dk',
        'linkedin.com',
        'cookiebot.com',
        'was.digst.dk',
    }
    seen = set()
    results = []

    for item in links:
        href = item['website']
        parsed = urlparse(href)
        domain = parsed.netloc.lower()
        if not domain or any(domain.endswith(d) for d in excluded_domains):
            continue
        key = (item['name'], item['website'])
        if key in seen:
            continue
        seen.add(key)
        results.append(item)

    return results
