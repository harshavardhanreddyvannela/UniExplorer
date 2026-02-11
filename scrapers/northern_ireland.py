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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the recognised bodies paragraph
        target_phrase = "Current Northern Ireland recognised bodies are:"
        intro_paragraph = None
        for p in soup.find_all('p'):
            if target_phrase in p.get_text(strip=True):
                intro_paragraph = p
                break
        
        if intro_paragraph:
            # Get the list following the paragraph
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
        
        # Remove specific institutions after collecting all
        universities = [u for u in universities if u['name'] not in ['Open University', 'Presbyterian Theological Faculty, Ireland']]
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Northern Ireland: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Northern Ireland: {str(e)}")
    
    return universities
