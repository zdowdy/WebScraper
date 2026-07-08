import sqlite3
from database import init_db, insert_rows
from analyzer import avg_price_by_brand

def test_avg_price_by_brand():
    conn = sqlite3.connect(':memory:')
    init_db(conn)
    
    fake_rows = [
        {'category': 'RAM', 'title': 'RAM A', 'model': 'A1', 'brand': 'TestBrand',
         'price': 100.0, 'rating': 4.5, 'num_reviews': 10,
         'in_stock': 1, 'url': 'http://test.com/a',
         'scraped_at': '2026-01-01T00:00:00+00:00'},
        {'category': 'RAM', 'title': 'RAM B', 'model': 'B1', 'brand': 'TestBrand',
         'price': 200.0, 'rating': 4.0, 'num_reviews': 5,
         'in_stock': 1, 'url': 'http://test.com/b',
         'scraped_at': '2026-01-01T00:00:00+00:00'},
    ]
    insert_rows(conn, fake_rows)
    
    df = avg_price_by_brand(conn, 'RAM')
    
    assert df.iloc[0]['brand'] == 'TestBrand'
    assert df.iloc[0]['avg_price'] == 150.0
    
    conn.close()