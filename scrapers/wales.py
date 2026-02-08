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
        
        # TODO: Customize HTML parsing logic for Wales's specific website structure
        # Example:
        # uni_elements = soup.find_all('div', class_='university-item')
        # for elem in uni_elements:
        #     name = elem.find('h2').text.strip()
        #     website = elem.find('a', class_='uni-link')['href']
        #     universities.append({'name': name, 'website': website})
        
        print(f"Scraped {len(universities)} universities from Wales")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Wales: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Wales: {str(e)}")
    
    return universities

if __name__ == "__main__":
    # Test scraper
    test_url = "https://example.com/wales"
    results = scrape_universities(test_url)
    for uni in results:
        print(f"- {uni['name']}: {uni['website']}")
