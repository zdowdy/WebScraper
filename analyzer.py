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

def products_by_market_focus(conn):
    sql="""
        SELECT brand_focus.market_focus, AVG(products.price) as avg_price, COUNT(*) as product_count
        FROM products
        JOIN brand_focus ON products.brand = brand_focus.brand_name
        GROUP BY brand_focus.market_focus
        ORDER BY avg_price DESC
    """
    df=pd.read_sql_query(sql,conn)
    return df

if __name__ == "__main__":
    import sqlite3
    from config import DB_PATH
    
    conn = sqlite3.connect(DB_PATH)
    df = products_by_market_focus(conn)
    print(df)
    conn.close()