"""
Web scraper for Australian universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the Study Australia website.
    
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
        
        # Find all h2 tags containing university links
        for h2 in soup.find_all('h2'):
            link = h2.find('a', href=True)
            if link:
                # Get name from full h2 text (not just link text)
                name = h2.get_text(strip=True)
                website = link['href']
                
                # Keep only valid university entries
                if name and website and '.edu.au' in website:
                    universities.append({
                        'name': name,
                        'website': website
                    })
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Australia: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Australia: {str(e)}")
    
    return universities


if __name__ == "__main__":
    # Test scraper
    test_url = "https://www.studyaustralia.gov.au/en/plan-your-studies/list-of-australian-universities"
    results = scrape_universities(test_url)
    
    print(f"Found {len(results)} universities:")
    for uni in results:
        print(f"  - {uni['name']}: {uni['website']}")
