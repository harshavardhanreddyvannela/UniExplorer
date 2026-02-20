"""
Master orchestrator for web scraping universities across all countries.
Reads configuration, runs country-specific scrapers, and uploads results to the database.
"""

import csv
import sys
from typing import Dict, List
from database import initialize_db, insert_universities, get_summary, get_total_count

# Import all country scrapers
from scrapers.scotland import scrape_universities as scrape_scotland
from scrapers.wales import scrape_universities as scrape_wales
from scrapers.northern_ireland import scrape_universities as scrape_northern_ireland
from scrapers.england import scrape_universities as scrape_england
from scrapers.ireland import scrape_universities as scrape_ireland
from scrapers.canada import scrape_universities as scrape_canada
from scrapers.australia import scrape_universities as scrape_australia
from scrapers.new_zealand import scrape_universities as scrape_new_zealand
from scrapers.denmark import scrape_universities as scrape_denmark
from scrapers.norway import scrape_universities as scrape_norway
from scrapers.sweden import scrape_universities as scrape_sweden
from scrapers.japan import scrape_universities as scrape_japan
from scrapers.singapore import scrape_universities as scrape_singapore
from scrapers.south_korea import scrape_universities as scrape_south_korea
from scrapers.taiwan import scrape_universities as scrape_taiwan
from scrapers.usa import scrape_universities as scrape_usa
from scrapers.poland import scrape_universities as scrape_poland
from scrapers.czechia import scrape_universities as scrape_czechia
from scrapers.spain import scrape_universities as scrape_spain
from scrapers.portugal import scrape_universities as scrape_portugal
from scrapers.italy import scrape_universities as scrape_italy
from scrapers.france import scrape_universities as scrape_france
from scrapers.germany import scrape_universities as scrape_germany
from scrapers.switzerland import scrape_universities as scrape_switzerland
from scrapers.austria import scrape_universities as scrape_austria
from scrapers.belgium import scrape_universities as scrape_belgium
from scrapers.netherlands import scrape_universities as scrape_netherlands

# Mapping of country names to scraper functions
SCRAPERS = {
    'Scotland': scrape_scotland,
    'Wales': scrape_wales,
    'Northern Ireland': scrape_northern_ireland,
    'England': scrape_england,
    'Ireland': scrape_ireland,
    'Canada': scrape_canada,
    'Australia': scrape_australia,
    'New Zealand': scrape_new_zealand,
    'Denmark': scrape_denmark,
    'Norway': scrape_norway,
    'Sweden': scrape_sweden,
    'Japan': scrape_japan,
    'Singapore': scrape_singapore,
    'South Korea': scrape_south_korea,
    'Taiwan': scrape_taiwan,
    'USA': scrape_usa,
    'Poland': scrape_poland,
    'Czechia': scrape_czechia,
    'Spain': scrape_spain,
    'Portugal': scrape_portugal,
    'Italy': scrape_italy,
    'France': scrape_france,
    'Germany': scrape_germany,
    'Switzerland': scrape_switzerland,
    'Austria': scrape_austria,
    'Belgium': scrape_belgium,
    'Netherlands': scrape_netherlands,
}

def read_config(config_file: str = 'config.csv') -> Dict[str, str]:
    """
    Read configuration file and return country-to-URL mapping.
    
    Args:
        config_file: Path to the CSV configuration file
        
    Returns:
        Dictionary with country names as keys and URLs as values
    """
    config = {}
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                country = row['country'].strip()
                url = row['url'].strip()
                config[country] = url
        print(f"✓ Loaded {len(config)} countries from {config_file}\n")
    except FileNotFoundError:
        print(f"✗ Configuration file '{config_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error reading configuration: {str(e)}")
        sys.exit(1)
    
    return config

def main():
    """Main orchestrator function."""
    print("=" * 60)
    print("  UNIVERSITY WEB SCRAPER - Master Orchestrator")
    print("=" * 60)
    print()
    
    # Initialize database
    print("Initializing database...")
    initialize_db()
    print()
    
    # Read configuration
    config = read_config('config.csv')
    
    # Track results
    results = {}
    total_universities = 0
    
    # Run scrapers for each country
    print("=" * 60)
    print("  SCRAPING IN PROGRESS")
    print("=" * 60)
    print()
    
    for country in config:
        url = config[country]
        print(f"[{country}]")
        print(f"  URL: {url}")
        
        if country not in SCRAPERS:
            print(f"  ✗ No scraper found for {country}")
            results[country] = 0
            continue
        
        try:
            # Call the country-specific scraper
            scraper_func = SCRAPERS[country]
            universities = scraper_func(url)
            
            # Insert results into database
            if universities:
                insert_universities(country, universities)
                total_universities += len(universities)
                results[country] = len(universities)
                print(f"  ✓ Inserted {len(universities)} universities")
            else:
                results[country] = 0
                print(f"  ⚠ No universities scraped")
        
        except Exception as e:
            print(f"  ✗ Error scraping {country}: {str(e)}")
            results[country] = 0
        
        print()
    
    # Display summary
    print("=" * 60)
    print("  SCRAPING COMPLETE - SUMMARY")
    print("=" * 60)
    print()
    
    summary = get_summary()
    if summary:
        print("Universities by Country:")
        print("-" * 40)
        for country, count in summary:
            print(f"  {country:<25} {count:>5} universities")
        print("-" * 40)
        print(f"  {'TOTAL':<25} {get_total_count():>5} universities")
    else:
        print("  No data found in database")
    
    print()
    print(f"Total universities scraped: {total_universities}")
    print("=" * 60)

if __name__ == "__main__":
    main()
