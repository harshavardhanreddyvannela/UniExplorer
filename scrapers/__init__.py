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
from .japan import scrape_universities as scrape_japan
from .singapore import scrape_universities as scrape_singapore
from .south_korea import scrape_universities as scrape_south_korea
from .taiwan import scrape_universities as scrape_taiwan
from .brunei import scrape_universities as scrape_brunei
from .estonia import scrape_universities as scrape_estonia
from .latvia import scrape_universities as scrape_latvia
from .lithuania import scrape_universities as scrape_lithuania
from .usa import scrape_universities as scrape_usa
from .poland import scrape_universities as scrape_poland
from .czechia import scrape_universities as scrape_czechia
from .slovakia import scrape_universities as scrape_slovakia
from .hungary import scrape_universities as scrape_hungary
from .slovenia import scrape_universities as scrape_slovenia
from .croatia import scrape_universities as scrape_croatia
from .spain import scrape_universities as scrape_spain
from .portugal import scrape_universities as scrape_portugal
from .italy import scrape_universities as scrape_italy
from .france import scrape_universities as scrape_france
from .germany import scrape_universities as scrape_germany
from .switzerland import scrape_universities as scrape_switzerland
from .austria import scrape_universities as scrape_austria
from .malta import scrape_universities as scrape_malta
from .belgium import scrape_universities as scrape_belgium
from .netherlands import scrape_universities as scrape_netherlands
from .monaco import scrape_universities as scrape_monaco
from .andorra import scrape_universities as scrape_andorra
from .liechtenstein import scrape_universities as scrape_liechtenstein
from .luxembourg import scrape_universities as scrape_luxembourg

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
    'scrape_japan',
    'scrape_singapore',
    'scrape_south_korea',
    'scrape_taiwan',
    'scrape_brunei',
    'scrape_estonia',
    'scrape_latvia',
    'scrape_lithuania',
    'scrape_usa',
    'scrape_poland',
    'scrape_czechia',
    'scrape_slovakia',
    'scrape_hungary',
    'scrape_slovenia',
    'scrape_croatia',
    'scrape_spain',
    'scrape_portugal',
    'scrape_italy',
    'scrape_france',
    'scrape_germany',
    'scrape_switzerland',
    'scrape_austria',
    'scrape_malta',
    'scrape_belgium',
    'scrape_netherlands',
    'scrape_monaco',
    'scrape_andorra',
    'scrape_liechtenstein',
    'scrape_luxembourg',
]
