"""
Web scraper for Welsh universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Wales.
    
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
        
        content = soup.find('div', class_='gem-c-govspeak')
        if not content:
            content = soup.find('div', class_='govuk-govspeak')
        if not content:
            content = soup
        
        seen = set()
        for link in content.find_all('a', href=True):
            name = link.get_text(strip=True)
            website = link.get('href', '').strip()
            if not name or not website.startswith('http'):
                continue
            if 'gov.uk' in website:
                continue
            key = (name, website)
            if key in seen:
                continue
            seen.add(key)
            universities.append({
                'name': name,
                'website': website
            })
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Wales: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Wales: {str(e)}")
    
    return universities

if __name__ == "__main__":
    # Test scraper
    test_url = "https://www.gov.uk/check-university-award-degree/recognised-bodies-wales"
    results = scrape_universities(test_url)
    
    print(f"Found {len(results)} universities:")
    for uni in results:
        print(f"  - {uni['name']}: {uni['website']}")
