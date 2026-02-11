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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all h2 tags containing university links
        for h2 in soup.find_all('h2'):
            link = h2.find('a', href=True)
            if link:
                # Get full h2 text for name
                name = h2.get_text(strip=True)
                website = link['href']
                
                # Keep only valid university entries
                if name and website and '.edu.au' in website:
                    universities.append({
                        'name': name,
                        'website': website
                    })
        
        # Remove specific institutions after collecting all
        universities = [u for u in universities if u['name'] not in ['Australian University of Theology', 'Torrens University Australia', 'University of Divinity']]
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Australia: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Australia: {str(e)}")
    
    return universities
