import os
from pathlib import Path

#Paths
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR/'data.db'
OUTPUT_DIR = BASE_DIR/'output'
LOG_FILE = BASE_DIR/'scrapper.log'

#Scraper
TARGET_URL = 'https://www.newegg.com/p/pl?N=100006650'
REQUEST_TIMEOUT = 15                                                    #the amount of times in sec before gibing up on a url request
REQUEST_HEADERS = {                                                     #very important will get a 403 or bot-detection error without realistic header
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}
BRANDS = [
    {'brand_name': 'Corsair',   'market_focus':'both'},
    {'brand_name': 'G.SKILL',   'market_focus':'consumer'},
    {'brand_name': 'Kingston Technology Corp.',   'market_focus':'both'},
    {'brand_name': 'Crucial',   'market_focus':'enterprise'},
    {'brand_name': 'Black Diamond Memory',   'market_focus':'both'},
    {'brand_name': 'Team Group',   'market_focus':'both'},
    {'brand_name': 'A-Tech',   'market_focus':'both'},
    {'brand_name': 'SAMSUNG',   'market_focus':'enterprise'},
    {'brand_name': 'NEMIX RAM',   'market_focus':'both'},
    {'brand_name': 'V-color',   'market_focus':'both'},
    {'brand_name': 'Patriot Memory',   'market_focus':'both'},
    {'brand_name': 'Timetec',   'market_focus':'consumer'},
    {'brand_name': 'SK hynix',   'market_focus':'enterprise'},
    {'brand_name': 'RIMLANCE',   'market_focus':'enterprise'},
    {'brand_name': 'OWC',   'market_focus':'both'},
    {'brand_name': 'Silicon Power',   'market_focus':'both'},
    {'brand_name': 'DELL',   'market_focus':'both'},
    {'brand_name': 'XPG',   'market_focus':'both'},
    {'brand_name': 'PNY Technologies, INC.',   'market_focus':'both'},
    {'brand_name': 'Micron Technologies, INC.',   'market_focus':'enterprise'},
    {'brand_name': 'KLEVV',   'market_focus':'consumer'},
    {'brand_name': 'KINGBANK',   'market_focus':'consumer'},
    {'brand_name': 'DATO',   'market_focus':'consumer'},
    {'brand_name': 'ADATA',   'market_focus':'both'},
    {'brand_name': 'HP',   'market_focus':'both'},
    {'brand_name': 'Gigastone Corporation',   'market_focus':'consumer'},
    {'brand_name': 'Brute Networks',   'market_focus':'enterprise'},
    {'brand_name': 'Micron',   'market_focus':'enterprise'},
    {'brand_name': 'KingSpec',   'market_focus':'consumer'},
    {'brand_name': 'KINGSMAN GAMING',   'market_focus':'consumer'},
    {'brand_name': 'Ballistix',   'market_focus':'consumer'}
]

#Scheduler
SCRAPE_INTERVAL_HOURS = 1                                             #How often the scraper gets ran

#Data Analysis
TOP_ITEMS = 10                                                  #The amount of top results to show in chart
RECENT_DAYS = 7                                                 #Lookback window for queries

#Output 
OUTPUT_DIR.mkdir(exist_ok=True)                                 #