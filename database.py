import sqlite3
from datetime import datetime, timezone, timedelta

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products 
                (
                id          INTEGER   PRIMARY KEY AUTOINCREMENT,
                title       TEXT,
                model       TEXT,
                brand       TEXT,
                price       REAL,
                rating      REAL,
                num_reviews INTEGER,
                in_stock    INTEGER,
                url         TEXT      UNIQUE,
                scraped_at  TEXT
                )
                   """)
    conn.commit()

def insert_rows(conn, rows):
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

def get_all(conn):
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM products
                           ORDER BY scraped_at DESC""")
    
    return cursor.fetchall()

def get_recent(conn,n_days):
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
    init_db(conn)

    rows = scrape_all_pages()
    insert_rows(conn, rows)

    recent = get_recent(conn, 1)
    print(f'Rows from last 1 day: {len(recent)}')
    results = get_all(conn)
    print(f'Rows in database: {len(results)}')
    print(results[0])

    conn.close()