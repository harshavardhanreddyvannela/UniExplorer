"""
Web scraper for Greek universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Greece.
    
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
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all h5 tags containing university links
        for h5 in soup.find_all('h5'):
            link = h5.find('a', href=True)
            if link:
                name = link.get_text(strip=True)
                website = link['href']
                
                if name and website and website.startswith('http'):
                    universities.append({
                        'name': name,
                        'website': website
                    })
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Greece: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Greece: {str(e)}")
    
    return universities

if __name__ == "__main__":
    # Test scraper
    test_url = "https://www.doatap.gr/enhmerosh/idrumata-ellados"
    results = scrape_universities(test_url)
    
    print(f"Found {len(results)} universities:")
    for uni in results:
        print(f"  - {uni['name']}: {uni['website']}")
