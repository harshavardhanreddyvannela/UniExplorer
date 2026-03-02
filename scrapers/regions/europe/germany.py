from scrapers.template.scraper_template import BaseGeographyScraper


class GeographyScraper(BaseGeographyScraper):
    name = "europe.germany"

    def get_source_descriptors(self) -> list[dict]:
        return []

    def parse_source(self, source: dict, payload):
        return []
