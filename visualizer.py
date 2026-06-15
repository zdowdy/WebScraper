import matplotlib.pyplot as plt
from config import OUTPUT_DIR

def plot_price_trend(df):
    """
    Creates a line graph using matplotlib that graphs the date to the avg_price of products that day from products

    Args:
        df:pandas Dataframe with columns date and avg_price returned by avg_price_by_day()
    
    Returns:
        None. Saves chart to OUTPUT_DIR/price_trend.png.
    """
    plt.figure(figsize=(10,5))
    plt.plot(df['date'], df['avg_price'])
    plt.title('Average Cost of Memory by Day from Newegg')
    plt.xlabel('Day')
    plt.ylabel('Average price of Memory')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(OUTPUT_DIR / 'price_trend.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_top_brands(df):
    """
    Creates a bar graph using matplotlib that graphs the brand to the brand_count in descending order from products 

    Args:
        df:pandas DataFrame with columns brand and brand_count returned from top_brands()
    
    Returns:
        None. Saves chart to OUTPUT_DIR/top_brands.png.
    """
    plt.figure(figsize=(15,5))
    plt.bar(df['brand'], df['brand_count'])
    plt.title('Product Count by Brand from Newegg in Descending Order')
    plt.xlabel('Brand')
    plt.ylabel('Product Count')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(OUTPUT_DIR / 'top_brands.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_avg_price_by_brand(df):
    """
    Creates a horizontal bar graph using matplotlib that graphs brand to the avg_price of memory for that brand from products in descending order

    Args:
        df:pandas DataFrame with columns brand and avg_price returned from avg_price_by_brand

    Returns:
        None. Saves chart to OUTPUT_DIR/avg_price_by_brand.png.
    """
    plt.figure(figsize=(12,15))
    plt.barh(df['brand'], df['avg_price'])
    plt.title('Average Cost of Memory by Brand from Newegg in Descending Order')
    plt.xlabel('Average Price of Memory')
    plt.ylabel('Brand')
    plt.savefig(OUTPUT_DIR / 'avg_price_by_brand.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    import sqlite3
    from config import DB_PATH
    from analyzer import avg_price_by_day, top_brands, avg_price_by_brand

    conn = sqlite3.connect(DB_PATH)

    plot_price_trend(avg_price_by_day(conn))
    plot_top_brands(top_brands(conn))
    plot_avg_price_by_brand(avg_price_by_brand(conn))

    conn.close()
    print("Charts saved to /outputs/")