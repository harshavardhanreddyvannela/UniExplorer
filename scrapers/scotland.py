"""
Web scraper for Scottish universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Scotland.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        List of dictionaries with 'name' and 'website' keys
    """
    universities = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the heading "Recognised bodies" (some pages include extra whitespace)
        recognised_heading = None
        for heading in soup.find_all(['h2', 'h3']):
            if heading.get_text(strip=True) == 'Recognised bodies':
                recognised_heading = heading
                break
        
        if recognised_heading:
            # Walk siblings until the next heading and collect links in lists
            current = recognised_heading.find_next_sibling()
            seen = set()
            
            while current and current.name not in ['h2', 'h3']:
                for link in current.find_all('a', href=True):
                    name = link.get_text(strip=True)
                    website = link.get('href', '').strip()
                    if not name or not website.startswith('http'):
                        continue
                    # Keep only likely Scottish university domains
                    if '.ac.uk' not in website:
                        continue
                    key = (name, website)
                    if key in seen:
                        continue
                    seen.add(key)
                    universities.append({
                        'name': name,
                        'website': website
                    })
                current = current.find_next_sibling()
        
        print(f"Scraped {len(universities)} universities from Scotland")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Scotland: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Scotland: {str(e)}")
    
    return universities

if __name__ == "__main__":
    # Test scraper
    test_url = "https://www.gov.scot/policies/universities/"
    results = scrape_universities(test_url)
    for uni in results:
        print(f"- {uni['name']}: {uni['website']}")
