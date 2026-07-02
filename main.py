import sqlite3
import logging
import schedule
import time
from config import DB_PATH, SCRAPE_INTERVAL_HOURS, BRANDS, CATEGORIES
from database import init_db, insert_rows, insert_brands
from scraper import scrape_all_pages

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect(DB_PATH)
init_db(conn)

insert_brands(conn, BRANDS)


def scrape_and_store():
    try:
        for category, base_url in CATEGORIES.items():
            rows = scrape_all_pages(category, base_url)
            new_count, updated_count = insert_rows(conn, rows)
            logger.info(f'Scrape run complete - {category}:{new_count} rows inserted')
            logger.info(f'Scrape run complete - {category}:{updated_count} rows updated')
    except Exception as e:
        logger.error(f'Scrape run failed: {e}')


scrape_and_store()

scrape_schedule = schedule.every(SCRAPE_INTERVAL_HOURS).hours.do(scrape_and_store)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    logger.info('Scheduler stopped by user')
    conn.close()
