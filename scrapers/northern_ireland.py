"""
Web scraper for Northern Irish universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Northern Ireland.
    
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
        
        # Find the paragraph that introduces the recognised bodies list
        target_phrase = "Current Northern Ireland recognised bodies are:"
        intro_paragraph = None
        for p in soup.find_all('p'):
            if target_phrase in p.get_text(strip=True):
                intro_paragraph = p
                break
        
        if intro_paragraph:
            # The list of recognised bodies follows this paragraph
            ul = intro_paragraph.find_next_sibling('ul')
            if ul:
                seen = set()
                for li in ul.find_all('li'):
                    link = li.find('a', href=True)
                    if not link:
                        continue
                    name = link.get_text(strip=True)
                    website = link.get('href', '').strip()
                    if not name or not website.startswith('http'):
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
        print(f"Error scraping Northern Ireland: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Northern Ireland: {str(e)}")
    
    return universities

if __name__ == "__main__":
    # Test scraper
    test_url = "https://www.economy-ni.gov.uk/articles/higher-education-policy"
    results = scrape_universities(test_url)
    
    print(f"Found {len(results)} universities:")
    for uni in results:
        print(f"  - {uni['name']}: {uni['website']}")
