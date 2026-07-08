import matplotlib.pyplot as plt
from config import OUTPUT_DIR


def plot_price_trend(df, category):
    """
    Creates a line graph using matplotlib that graphs the date to the avg_price of products that day from products

    Args:
        df:pandas Dataframe with columns date and avg_price returned by avg_price_by_day()
        category: product category name, used in the title and filename (e.g. 'RAM', 'CPU', 'GPU')

    Returns:
        None. Saves chart to OUTPUT_DIR/price_trend.png.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['avg_price'])
    plt.title(f'Average Cost of {category} by Day from Newegg')
    plt.xlabel('Day')
    plt.ylabel(f'Average price of {category}')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(OUTPUT_DIR / f'{category}_price_trend.png', dpi=150, bbox_inches='tight')
    plt.close()


def plot_top_brands(df, category):
    """
    Creates a bar graph using matplotlib that graphs the brand to the brand_count in descending order from products

    Args:
        df:pandas DataFrame with columns brand and brand_count returned from top_brands()
        category: product category name, used in the title and filename (e.g. 'RAM', 'CPU', 'GPU')

    Returns:
        None. Saves chart to OUTPUT_DIR/top_brands.png.
    """
    plt.figure(figsize=(15, 5))
    plt.bar(df['brand'], df['brand_count'])
    plt.title(f'{category} Product Count by Brand from Newegg in Descending Order')
    plt.xlabel('Brand')
    plt.ylabel('Product Count')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(OUTPUT_DIR / f'{category}_top_brands.png', dpi=150, bbox_inches='tight')
    plt.close()


def plot_avg_price_by_brand(df, category):
    """
    Creates a horizontal bar graph using matplotlib that graphs brand to the avg_price of memory for that brand from products in descending order

    Args:
        df:pandas DataFrame with columns brand and avg_price returned from avg_price_by_brand
        category: product category name, used in the title and filename (e.g. 'RAM', 'CPU', 'GPU')

    Returns:
        None. Saves chart to OUTPUT_DIR/avg_price_by_brand.png.
    """
    plt.figure(figsize=(12, 15))
    plt.barh(df['brand'], df['avg_price'])
    plt.title(f'Average Cost of {category} by Brand from Newegg in Descending Order')
    plt.xlabel(f'Average Price of {category}')
    plt.ylabel('Brand')
    plt.savefig(OUTPUT_DIR / f'{category}_avg_price_by_brand.png', dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    import sqlite3
    from config import DB_PATH, CATEGORIES
    from analyzer import avg_price_by_day, top_brands, avg_price_by_brand

    conn = sqlite3.connect(DB_PATH)

    for category in CATEGORIES:
        plot_price_trend(avg_price_by_day(conn, category), category)
        plot_top_brands(top_brands(conn, category), category)
        plot_avg_price_by_brand(avg_price_by_brand(conn, category), category)

    conn.close()
    print("Charts saved to /output/")
