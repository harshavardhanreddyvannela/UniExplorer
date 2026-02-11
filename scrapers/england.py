"""
Web scraper for English universities.
"""

import io
import requests
import openpyxl
from typing import List, Dict

def scrape_universities(url: str) -> List[Dict[str, str]]:
    """
    Scrape universities from the England.xlsx spreadsheet.
    
    Args:
        url: Path to the Excel file (or will read from local England.xlsx)
        
    Returns:
        List of dictionaries with 'name' and 'website' keys
    """
    universities = []
    
    try:
        # Download the Excel file
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Load it into openpyxl
        workbook = openpyxl.load_workbook(io.BytesIO(response.content))
        sheet = workbook.active
        
        # Delete the first two rows
        sheet.delete_rows(1, 2)
        
        rows = list(sheet.iter_rows(min_row=2, values_only=True))
        
        legal_name_idx = 0       # Column 1: Provider's legal name
        trading_name_idx = 2     # Column 3: Provider's trading name(s)
        website_idx = 6          # Column 7: Provider's website
        degree_powers_idx = 13   # Column N (14): Highest level of degree awarding powers held
        
        def should_include(row):
            # Only include if degree awarding powers is "Research"
            if degree_powers_idx < len(row):
                powers = str(row[degree_powers_idx]).strip()
                if powers != "Research":
                    return False
            return True
        
        for row in rows:
            if not row or len(row) < max(trading_name_idx, website_idx) + 1:
                continue
            
            if not should_include(row):
                continue
            
            # Get trading name and take only the first line if there are multiple
            trading_name = row[trading_name_idx]
            trading_name_full = str(trading_name).strip() if trading_name else ""
            
            if trading_name:
                trading_name = str(trading_name).strip()
                if '\n' in trading_name:
                    trading_name = trading_name.split('\n')[0].strip()
            else:
                trading_name = ""
            
            # If trading name contains "Hospital", use legal name instead
            if trading_name_full and 'Hospital' in trading_name_full:
                legal_name = row[legal_name_idx]
                trading_name = str(legal_name).strip() if legal_name else ""
            
            # If no trading name, trading name is "Not applicable", or trading name is all caps (abbreviation), use legal name
            if not trading_name or trading_name.lower() == "not applicable":
                legal_name = row[legal_name_idx]
                trading_name = str(legal_name).strip() if legal_name else ""
            else:
                # Check if trading name is just an abbreviation (all uppercase letters)
                letters_only = ''.join(c for c in trading_name if c.isalpha())
                if letters_only and letters_only.isupper():
                    legal_name = row[legal_name_idx]
                    trading_name = str(legal_name).strip() if legal_name else ""
            
            # Get website
            website = row[website_idx]
            website = str(website).strip() if website else ""
            
            if not trading_name:
                continue
            
            universities.append({
                'name': trading_name,
                'website': website
            })
        
        # Remove "The Open University" after collecting all
        universities = [u for u in universities if u['name'] != 'The Open University']
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading England spreadsheet: {str(e)}")
    except Exception as e:
        print(f"Error scraping England: {str(e)}")
    
    return universities
