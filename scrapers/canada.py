"""
Web scraper for Canadian universities.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the CICIC directory for Canada.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        List of dictionaries with 'name' and 'website' keys
    """
    universities = []
    seen_names = set()
    
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://www.cicic.ca/869/',
        }
        session.headers.update(headers)
        
        # Collect links from all pages
        all_detail_links = []
        
        # Page 1: Initial GET request
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        all_detail_links.extend(_extract_links_from_page(soup))
        
        # Navigate through remaining pages using POST with ViewState
        for page_num in range(2, 5):
            # Extract ViewState and other form data from current page
            viewstate = soup.find('input', {'name': '__VIEWSTATE'})
            viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})
            
            if not viewstate or not viewstate_gen:
                break
            
            # POST to get next page
            post_url = 'https://www.cicic.ca/869/results.canada?search=&s=2&t=1&sect=2,3&th=0&dist=0'
            form_data = {
                '__EVENTTARGET': 'ctl00$Main$EducationDirectory$gridresults$ctl00$ctl03$ctl01$ctl04',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate['value'],
                '__VIEWSTATEGENERATOR': viewstate_gen['value'],
            }
            
            if event_validation:
                form_data['__EVENTVALIDATION'] = event_validation['value']
            
            response = session.post(post_url, data=form_data, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_links = _extract_links_from_page(soup)
            all_detail_links.extend(page_links)
        
        # Visit each detail page to extract website
        for name, detail_url in all_detail_links:
            if name in seen_names:
                continue
            
            try:
                detail_response = session.get(detail_url, timeout=30)
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                
                # Strategy 1: Look for links in "REACH THE EDUCATIONAL INSTITUTION" section
                website = None
                for h3 in detail_soup.find_all(['h3', 'h4']):
                    if 'REACH' in h3.get_text().upper():
                        for link in h3.find_all_next('a', href=True, limit=10):
                            href = link['href']
                            if href.startswith('http') and 'cicic.ca' not in href:
                                if not any(skip in href.lower() for skip in ['gov.', 'government', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin']):
                                    if any(domain in href.lower() for domain in ['.ca', '.edu', 'university']):
                                        website = href
                                        break
                        if website:
                            break
                
                # Strategy 2: Fallback
                if not website:
                    for link in detail_soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith('http') and 'cicic.ca' not in href:
                            if not any(skip in href.lower() for skip in ['gov.', 'government', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin', 'google.com', 'cic.gc.ca']):
                                if any(domain in href.lower() for domain in ['.ca/', '.edu/', 'university']):
                                    if len(href) < 100:
                                        website = href
                                        break
                
                if website:
                    universities.append({
                        'name': name,
                        'website': website
                    })
                    seen_names.add(name)
                
            except Exception as e:
                continue
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Canada: {str(e)}")
    except Exception as e:
        print(f"Unexpected error scraping Canada: {str(e)}")
    
    return universities


def _extract_links_from_page(soup: BeautifulSoup) -> List[tuple]:
    """
    Extract university name and detail page URL from a results page.
    
    Args:
        soup: BeautifulSoup object of the page
        
    Returns:
        List of (name, detail_url) tuples
    """
    # Institutions to skip
    skip_institutions = {
        'Briercrest College and Seminary',
        'Campion College',
        'Gabriel Dumont Institute of Native Studies and Applied Research',
        'Grenfell Campus, Memorial University of Newfoundland',
        "King's University College",
        'La Cité universitaire francophone',
        'Labrador Campus, Memorial University of Newfoundland',
        'Luther College',
        'Marine Institute, Memorial University of Newfoundland',
        'Renison University College',
        'Royal Military College of Canada',
        'Saint Paul University',
        "St. Peter's College",
        'St. Thomas More College',
        'United College',
        'Victoria University'
    }
    
    links = []
    table = soup.find('table')
    if not table:
        return links
    
    rows = table.find_all('tr')[2:]  # Skip header rows
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            name_cell = cells[1]
            all_links = name_cell.find_all('a', href=True)
            if all_links:
                # If there are 2 links, take the second one; otherwise take the first
                link = all_links[1] if len(all_links) >= 2 else all_links[0]
                name = link.get_text(strip=True)
                
                # Skip institutions in the filter list
                if name in skip_institutions:
                    continue
                
                detail_url = 'https://www.cicic.ca' + link['href']
                links.append((name, detail_url))
    
    return links


if __name__ == "__main__":
    # Test scraper
    test_url = "https://www.cicic.ca/869/results.canada?search=&s=2&t=1&sect=2,3&th=0&dist=0"
    results = scrape_universities(test_url)
    
    print(f"Found {len(results)} universities:")
    for uni in results:
        print(f"  - {uni['name']}: {uni['website']}")
