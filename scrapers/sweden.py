"""
Web scraper for Swedish universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urlparse

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Sweden.
    
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
        
        section_titles = {
            'Universitetens webbplatser',
            'Högskolornas webbplatser',
            'De konstnärliga högskolornas webbplatser',
        }
        seen = set()
        for heading in soup.find_all('h2'):
            if heading.get_text(strip=True) not in section_titles:
                continue
            for sibling in heading.find_next_siblings():
                if sibling.name == 'h2':
                    break
                for link in sibling.find_all('a', href=True):
                    name = link.get_text(" ", strip=True)
                    website = link['href'].strip()
                    if not name or not website.startswith('http'):
                        continue
                    if ' webbplats' in name:
                        name = name.split(' webbplats', 1)[0].strip().rstrip(',')
                    key = (name, website)
                    if key in seen:
                        continue
                    seen.add(key)
                    universities.append({'name': name, 'website': website})

        universities = _filter_links(universities)
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Sweden: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Sweden: {str(e)}")
    
    return universities

def _filter_links(links: List[Dict[str, str]]) -> List[Dict[str, str]]:
    excluded_domains = {
        'uka.se',
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
