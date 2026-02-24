"""
Master orchestrator for web scraping universities across all countries.
Runs country-specific scrapers and uploads results to the database.
"""

from database import get_summary, get_total_count, initialize_db, insert_universities

# Import all country scrapers
from scrapers.australia import scrape_universities as scrape_australia
from scrapers.austria import scrape_universities as scrape_austria
from scrapers.belgium import scrape_universities as scrape_belgium
from scrapers.canada import scrape_universities as scrape_canada
from scrapers.czechia import scrape_universities as scrape_czechia
from scrapers.denmark import scrape_universities as scrape_denmark
from scrapers.france import scrape_universities as scrape_france
from scrapers.germany import scrape_universities as scrape_germany
from scrapers.ireland import scrape_universities as scrape_ireland
from scrapers.italy import scrape_universities as scrape_italy
from scrapers.japan import scrape_universities as scrape_japan
from scrapers.netherlands import scrape_universities as scrape_netherlands
from scrapers.new_zealand import scrape_universities as scrape_new_zealand
from scrapers.norway import scrape_universities as scrape_norway
from scrapers.poland import scrape_universities as scrape_poland
from scrapers.portugal import scrape_universities as scrape_portugal
from scrapers.singapore import scrape_universities as scrape_singapore
from scrapers.south_korea import scrape_universities as scrape_south_korea
from scrapers.spain import scrape_universities as scrape_spain
from scrapers.sweden import scrape_universities as scrape_sweden
from scrapers.switzerland import scrape_universities as scrape_switzerland
from scrapers.taiwan import scrape_universities as scrape_taiwan
from scrapers.united_kingdom import scrape_universities as scrape_united_kingdom
from scrapers.usa import scrape_universities as scrape_usa

# Mapping of country names to scraper functions
SCRAPERS = {
    "Australia": scrape_australia,
    "Austria": scrape_austria,
    "Canada": scrape_canada,
    "Czechia": scrape_czechia,
    "Denmark": scrape_denmark,
    "Belgium": scrape_belgium,
    "France": scrape_france,
    "Germany": scrape_germany,
    "Ireland": scrape_ireland,
    "Italy": scrape_italy,
    "Japan": scrape_japan,
    "Netherlands": scrape_netherlands,
    "New Zealand": scrape_new_zealand,
    "Norway": scrape_norway,
    "Poland": scrape_poland,
    "Portugal": scrape_portugal,
    "Singapore": scrape_singapore,
    "South Korea": scrape_south_korea,
    "Spain": scrape_spain,
    "Sweden": scrape_sweden,
    "Switzerland": scrape_switzerland,
    "Taiwan": scrape_taiwan,
    "United Kingdom": scrape_united_kingdom,
    "USA": scrape_usa,
}


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

    # Track results
    results = {}
    total_universities = 0

    # Run scrapers for each country
    print("=" * 60)
    print("  SCRAPING IN PROGRESS")
    print("=" * 60)
    print()

    for country, scraper_func in SCRAPERS.items():
        print(f"[{country}]")

        try:
            # Call the country-specific scraper
            universities = scraper_func()

            # Insert results into database
            if universities:
                insert_universities(country, universities)
                total_universities += len(universities)
                results[country] = len(universities)
                print(f"  ✓ Inserted {len(universities)} universities")
            else:
                results[country] = 0
                print("  ⚠ No universities scraped")

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
