"""
Web scraper for Irish universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Ireland.
    
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
        
        # Collect from all three sections
        headings_to_collect = {
            'Publicly-funded universities',
            'Institutes of technology',
            'Other institutions that receive public funding'
        }
        seen = set()
        
        for heading in soup.find_all(['h2', 'h3']):
            heading_text = heading.get_text(strip=True)
            if heading_text not in headings_to_collect:
                continue
            
            for sibling in heading.find_next_siblings():
                if sibling.name in ['h2', 'h3']:
                    break
                
                for ul in sibling.find_all('ul'):
                    for li in ul.find_all('li'):
                        link = li.find('a', href=True)
                        if link:
                            name = link.get_text(strip=True)
                            website = link['href']
                            
                            if name and website and website.startswith('http'):
                                key = (name, website)
                                if key in seen:
                                    continue
                                seen.add(key)
                                universities.append({
                                    'name': name,
                                    'website': website
                                })
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Ireland: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Ireland: {str(e)}")
    
    return universities
