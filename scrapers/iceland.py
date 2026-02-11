"""
Web scraper for Icelandic universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the provided URL for Iceland.
    
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
        
        # Find all table cells containing university data
        seen = set()
        for cell in soup.find_all('td', class_='wsite-multicol-col'):
            paragraph = cell.find('div', class_='paragraph')
            if not paragraph:
                continue
            
            # Get all strong tags
            strong_tags = paragraph.find_all('strong')
            
            i = 0
            while i < len(strong_tags):
                strong = strong_tags[i]
                text = strong.get_text(strip=True)
                
                # Check if this strong tag contains "/"
                if '/' in text:
                    # Extract name (after the "/" character)
                    name = text.split('/', 1)[-1].strip() if '/' in text else text
                    
                    # Clean up any embedded URLs or unicode chars
                    name = name.split('www.')[0].strip() if 'www.' in name else name
                    name = name.replace('​', '')
                    
                    # If name is empty, use next strong tag
                    if not name and i + 1 < len(strong_tags):
                        name = strong_tags[i + 1].get_text(strip=True).replace('​', '')
                        i += 1  # Skip the next one
                    elif not name:
                        i += 1
                        continue
                else:
                    i += 1
                    continue
                
                # Find the next link after this strong tag
                current = strong
                website = None
                for _ in range(10):
                    current = current.find_next('a', href=True) if current else None
                    if not current:
                        break
                    href = current.get('href', '')
                    link_text = current.get_text(strip=True)
                    if href.startswith('http') and link_text and len(link_text) > 2:
                        website = href
                        break
                
                if website:
                    key = (name, website)
                    if key not in seen:
                        seen.add(key)
                        universities.append({
                            'name': name,
                            'website': website
                        })
                
                i += 1
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Iceland: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Iceland: {str(e)}")
    
    return universities
