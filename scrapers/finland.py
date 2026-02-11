"""
Web scraper for Finnish universities using opintopolku.fi API.
"""

import requests
from typing import List, Dict
from urllib.parse import urlparse

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the opintopolku.fi API.
    
    Args:
        url: Not used - kept for compatibility with existing interface
        
    Returns:
        List of dictionaries with 'name' and 'website' keys
    """
    universities = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        # Step 1: Get list of universities
        search_url = 'https://opintopolku.fi/konfo-backend/search/oppilaitokset'
        params = {
            'koulutustyyppi': 'yo',  # yo = yliopisto (university)
            'size': 50,
            'page': 1
        }
        
        response = requests.get(search_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'hits' not in data:
            print("No institutions found in API response")
            return []
        
        # Step 2: For each university, get detailed info including website
        for hit in data['hits']:
            nimi = hit.get('nimi', {})
            name = nimi.get('fi', nimi.get('en', nimi.get('sv', '')))
            oid = hit.get('oid')
            
            if not name or not oid:
                continue
            
            # Exclude National Defence University
            if _should_exclude(name):
                print(f"Excluding: {name}")
                continue
            
            # Get detailed information
            detail_url = f'https://opintopolku.fi/konfo-backend/oppilaitos/{oid}'
            detail_response = requests.get(detail_url, headers=headers, timeout=30)
            
            if detail_response.status_code != 200:
                print(f"Failed to get details for {name}")
                continue
            
            detail = detail_response.json()
            
            # Extract website from nested structure
            website = _extract_website(detail)
            
            if website:
                universities.append({
                    'name': name,
                    'website': website
                })
            else:
                print(f"No website found for {name}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Finland: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Finland: {str(e)}")
    
    return universities

def _extract_website(detail: dict) -> str:
    """Extract university website from API response."""
    try:
        # Navigate: oppilaitos -> metadata -> wwwSivu -> url -> fi
        oppilaitos = detail.get('oppilaitos', {})
        metadata = oppilaitos.get('metadata', {})
        www_sivu = metadata.get('wwwSivu', {})
        url_dict = www_sivu.get('url', {})
        
        # Try Finnish first, then English, then Swedish
        website = url_dict.get('fi') or url_dict.get('en') or url_dict.get('sv')
        
        if website:
            # Clean the URL - remove everything after the domain
            parsed = urlparse(website)
            return f"{parsed.scheme}://{parsed.netloc}"
        
    except (KeyError, AttributeError, TypeError):
        pass
    
    return None

def _should_exclude(name: str) -> bool:
    """Check if institution should be excluded."""
    lowered = name.lower()
    excluded_terms = [
        'maanpuolustuskorkeakoulu',
        'national defence university'
    ]
    return any(term in lowered for term in excluded_terms)
