"""
Country-specific web scrapers for university data.
Each module should export a scrape_universities(url) function.
"""

from .australia import scrape_universities as scrape_australia
from .austria import scrape_universities as scrape_austria
from .canada import scrape_universities as scrape_canada
from .czechia import scrape_universities as scrape_czechia
from .denmark import scrape_universities as scrape_denmark
from .england import scrape_universities as scrape_england
from .flanders import scrape_universities as scrape_flanders
from .france import scrape_universities as scrape_france
from .germany import scrape_universities as scrape_germany
from .ireland import scrape_universities as scrape_ireland
from .italy import scrape_universities as scrape_italy
from .japan import scrape_universities as scrape_japan
from .netherlands import scrape_universities as scrape_netherlands
from .new_zealand import scrape_universities as scrape_new_zealand
from .northern_ireland import scrape_universities as scrape_northern_ireland
from .norway import scrape_universities as scrape_norway
from .poland import scrape_universities as scrape_poland
from .portugal import scrape_universities as scrape_portugal
from .scotland import scrape_universities as scrape_scotland
from .singapore import scrape_universities as scrape_singapore
from .south_korea import scrape_universities as scrape_south_korea
from .spain import scrape_universities as scrape_spain
from .sweden import scrape_universities as scrape_sweden
from .switzerland import scrape_universities as scrape_switzerland
from .taiwan import scrape_universities as scrape_taiwan
from .usa import scrape_universities as scrape_usa
from .wales import scrape_universities as scrape_wales
from .wallonia import scrape_universities as scrape_wallonia

__all__ = [
    "scrape_australia",
    "scrape_austria",
    "scrape_canada",
    "scrape_czechia",
    "scrape_denmark",
    "scrape_england",
    "scrape_flanders",
    "scrape_france",
    "scrape_germany",
    "scrape_ireland",
    "scrape_italy",
    "scrape_japan",
    "scrape_netherlands",
    "scrape_new_zealand",
    "scrape_northern_ireland",
    "scrape_norway",
    "scrape_poland",
    "scrape_portugal",
    "scrape_scotland",
    "scrape_singapore",
    "scrape_south_korea",
    "scrape_spain",
    "scrape_sweden",
    "scrape_switzerland",
    "scrape_taiwan",
    "scrape_usa",
    "scrape_wales",
    "scrape_wallonia",
]
