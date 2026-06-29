import pandas as pd


def avg_price_by_day(conn):
    """
    Calculate the avg_price per day from all scrape cycles

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        pandas DataFrame with columns date and avg_price in ascending order
    """

    sql = """
        SELECT DATE(scraped_at) as date, AVG(current_price) as avg_price
        FROM products
        GROUP BY date
        ORDER BY date ASC
    """
    df = pd.read_sql_query(sql, conn)
    return df


def top_brands(conn):
    """
    Calculate the brands with the most product count from all scrape cycles

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        pandas DataFrame with columns brand and brand_count in descending order
    """

    sql = """
        SELECT brand, COUNT(*) as brand_count
        FROM products
        GROUP BY brand
        ORDER BY brand_count DESC
    """
    df = pd.read_sql_query(sql, conn)
    return df


def avg_price_by_brand(conn):
    """
    Calculate the avg_price by brand from all scrape cycles

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        pandas DataFrame with columns brand and avg_price in descending order
    """

    sql = """
        SELECT brand, AVG(current_price) as avg_price
        FROM products
        GROUP BY brand
        ORDER BY avg_price DESC
    """
    df = pd.read_sql_query(sql, conn)
    return df


def products_by_market_focus(conn):
    """
    JOINS brand_focus and products by brand_name and brand

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        pandas DataFrame with columns market_focus, avg_price, and product_count in descending order
    """

    sql = """
        SELECT brand_focus.market_focus, AVG(products.current_price) as avg_price, COUNT(*) as product_count
        FROM products
        JOIN brand_focus ON products.brand = brand_focus.brand_name
        GROUP BY brand_focus.market_focus
        ORDER BY avg_price DESC
    """
    df = pd.read_sql_query(sql, conn)
    return df


def most_active_scrape_day(conn):
    """
    Calculate the count of products entered in to the database per day

    Args:
        conn: Active SQLite connection created in main.py

    Returns:
        pandas DataFrame with columns date and count
    """

    sql = """
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
    df = pd.read_sql_query(sql, conn)
    return df


def brands_with_significant_listings(conn, min_count):
    """
    Calculate the brands that have more than the min_count of products

    Args:
        conn: Active SQLite connection created in main.py
        min_count: the minimum count of products a brand can have in order to pass query

    Returns:
        pandas DataFrame with columns brand and product_count
    """

    sql = """
        SELECT brand,COUNT(*) as product_count
        FROM products
        GROUP BY brand
        HAVING product_count > ?
        """
    df = pd.read_sql_query(sql, conn, params=(min_count,))                                                        # Dont forget comma after min_count
    return df


if __name__ == "__main__":
    import sqlite3
    from config import DB_PATH

    conn = sqlite3.connect(DB_PATH)
    print(products_by_market_focus(conn))
    print(most_active_scrape_day(conn))
    print(brands_with_significant_listings(conn, 10))
    conn.close()
