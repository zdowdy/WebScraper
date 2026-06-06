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

#Scheduler
SCRAPE_INTERVAL_HOURS = 1                                             #How often the scraper gets ran

#Data Analysis
TOP_ITEMS = 10                                                  #The amount of top results to show in chart
RECENT_DAYS = 7                                                 #Lookback window for queries

#Output 
OUTPUT_DIR.mkdir(exist_ok=True)                                 #