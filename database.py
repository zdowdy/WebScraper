import sqlite3
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

def init_db(conn):
    """
    Using SQL create 2 tables if it does not exist already named products and brand_focus

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        None. Creates products and and brand_focus tables if they dont already exist
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products 
                (
                id              INTEGER   PRIMARY KEY AUTOINCREMENT,
                title           TEXT,
                model           TEXT,
                brand           TEXT,
                price           REAL,
                price_change    REAL,
                rating          REAL,
                num_reviews     INTEGER,
                in_stock        INTEGER,
                url             TEXT      UNIQUE,
                scraped_at      TEXT
                )
                   """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brand_focus
                (
                id              INTEGER   PRIMARY KEY AUTOINCREMENT,
                brand_name      TEXT      UNIQUE,
                market_focus    TEXT
                )
                    """)


    conn.commit()

def insert_brands(conn, brands):
    """
    Inserts brand_name and market_focus values into the table brand_focus

    Args:
        conn: Active SQLite connection created in main.py
        brands: a list of dicts from config.py that holds brand_name and market_focus data

    Returns:
        None. Commits inserted rows into the database
    """
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO brand_focus
                        (brand_name, market_focus)
                        VALUES(?,?)""",
        [
        (
            brand['brand_name'],
            brand['market_focus']
        )
        for brand in brands
        ]
        )
    
    conn.commit()
    
def insert_rows(conn, rows):
    """
    Inserts id, title, model, brand, price, rating, num_reviews, in_stock, url, and scraped_at values into the table products

    Args:
        conn: Active SQLite connection created in main.py
        rows: a list of dicts from scraper.py that holds title, model, brand, price, rating, num_reviews, in_stock, url, and scraped_at data

    Returns:
        None. Commits inserted rows into the database
    """
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO products 
                       (title, model, brand, price, rating, num_reviews, in_stock, url, scraped_at) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        [
        (
            row['title'],
            row['model'],
            row['brand'],
            row['price'],
            row['rating'],
            row['num_reviews'],
            row['in_stock'],
            row['url'],
            row['scraped_at']
        )
        for row in rows
        ]
        )
    conn.commit()

def update_price_changes(conn):
    """
    Updates the table products with the SQL query for price_change which monitors the fluctuation in price from the first price scrape

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        None. Commits inserted rows into the database
    """
    cursor = conn.cursor()
    cursor.execute("""
                UPDATE products
                SET price_change = price - 
                    (
                    SELECT price FROM products as p2
                    WHERE p2.url = products.url
                    ORDER BY p2.scraped_at ASC
                    LIMIT 1
                    )
                """)
    conn.commit()

def add_column_days_tracked(conn):
    """
    Inserts a column named days_tracked using ALTER TABLE and checks if the column has already been added if it has output that the column already exists

    Args:
        conn: Active SQLite connection created in main.py
    Returns:
        None. Commits inserted column into the database
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        ALTER TABLE products
                        ADD COLUMN days_tracked INTEGER
                    """)
        conn.commit()
        logger.info("Added days_tracked column to products")
    except Exception as e:
        logger.info("days_tracked column already exists, skipping")

def update_days_tracked(conn):
    """
    Updates the table products with the SQL query for days_tracked which logs how many days the product has been in the DB for

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        None. Commits inserted rows into the database
    """
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE products 
                   SET days_tracked = 
                   (
                   SELECT COUNT(DISTINCT DATE(scraped_at))
                   FROM products as p3
                   WHERE p3.url = products.url
                   )
                """)
    conn.commit()

def get_all(conn):
    """
    Gets all data from the data base and sorts in descending order by the day and time it was scraped at

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        a list of tuples which contains all rows from products in descending order by date. Returns empty if the table is empty
    """
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM products
                       ORDER BY scraped_at DESC""")
    
    return cursor.fetchall()

def get_recent(conn,n_days):
    """
    Returns all products scraped within the last n_days

    Args:
        conn: Active SQLite connection created in main.py
        n_days: the number of days to look back from now
    
    Returns:
        a list of tuples containing the rows scraped after the cutoff timestamp. Returns [] if no rows fall in the cutoff window
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(days=n_days)).isoformat()
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM products
                       WHERE scraped_at > ?
                       ORDER BY scraped_at DESC""",
                       (cutoff,))
    return cursor.fetchall()
    
if __name__ == '__main__':
    from scraper import scrape_all_pages
    from config import DB_PATH

    conn = sqlite3.connect(DB_PATH)
    init_db (conn)
    rows = scrape_all_pages()
    insert_rows(conn, rows)

    recent = get_recent(conn, 1)
    print(f'Rows from last 1 day: {len(recent)}')
    results = get_all(conn)
    print(f'Rows in database: {len(results)}')
    print(results[0])

    conn.close()