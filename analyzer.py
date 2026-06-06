import pandas as pd

def avg_price_by_day(conn):
    sql="""
        SELECT DATE(scraped_at) as date, AVG(price) as avg_price
        FROM products
        GROUP BY date
        ORDER BY date ASC
    """
    df = pd.read_sql_query(sql, conn)
    return df

def top_brands(conn):
    sql="""
        SELECT brand, COUNT(*) as brand_count
        FROM products
        GROUP BY brand
        ORDER BY brand_count DESC
"""
    df = pd.read_sql_query(sql,conn)
    return df

def avg_price_by_brand(conn):
    sql="""
        SELECT brand, AVG(price) as avg_price
        FROM products
        GROUP BY brand
        ORDER BY avg_price DESC
"""
    df=pd.read_sql_query(sql, conn)
    return df