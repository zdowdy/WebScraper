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

def most_active_scrape_day(conn):                                                                           #Subquery that finds the count of products entered into DB on specific days
    sql="""
        SELECT date, count 
        FROM 
            (SELECT DATE(scraped_at) as date, COUNT(*) as count
            FROM products
            GROUP BY date) 
        WHERE count = 
            (SELECT MAX(count) 
            FROM    
                (SELECT DATE(scraped_at) as date, COUNT(*) as count
                FROM products
                GROUP BY date))
        """
    df=pd.read_sql_query(sql,conn)
    return df

def brands_with_significant_listings(conn, min_count):
    sql="""
        SELECT brand,COUNT(*) as product_count
        FROM products
        GROUP BY brand
        HAVING product_count > ?
        """
    df=pd.read_sql_query(sql,conn,params=(min_count,))                                                      #Dont forget comma after min_count
    return df

if __name__ == "__main__":
    import sqlite3
    from config import DB_PATH
    
    conn = sqlite3.connect(DB_PATH)
    print(products_by_market_focus(conn))
    print(most_active_scrape_day(conn))
    print(brands_with_significant_listings(conn,10))
    conn.close()