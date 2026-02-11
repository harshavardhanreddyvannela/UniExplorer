"""
Country-specific web scrapers for university data.
Each module should export a scrape_universities(url) function.
"""

from .scotland import scrape_universities as scrape_scotland
from .wales import scrape_universities as scrape_wales
from .northern_ireland import scrape_universities as scrape_northern_ireland
from .england import scrape_universities as scrape_england
from .ireland import scrape_universities as scrape_ireland
from .canada import scrape_universities as scrape_canada
from .australia import scrape_universities as scrape_australia
from .new_zealand import scrape_universities as scrape_new_zealand
from .greece import scrape_universities as scrape_greece
from .iceland import scrape_universities as scrape_iceland
from .denmark import scrape_universities as scrape_denmark
from .norway import scrape_universities as scrape_norway
from .sweden import scrape_universities as scrape_sweden
from .finland import scrape_universities as scrape_finland

__all__ = [
    'scrape_scotland',
    'scrape_wales',
    'scrape_northern_ireland',
    'scrape_england',
    'scrape_ireland',
    'scrape_canada',
    'scrape_australia',
    'scrape_new_zealand',
    'scrape_greece',
    'scrape_iceland',
    'scrape_denmark',
    'scrape_norway',
    'scrape_sweden',
    'scrape_finland',
]
