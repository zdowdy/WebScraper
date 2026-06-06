import matplotlib.pyplot as plt
from config import OUTPUT_DIR

def plot_price_trend(df):
    plt.figure(figsize=(10,5))
    plt.plot(df['date'], df['avg_price'])
    plt.title('Average Cost of Memory by Day from Newegg')
    plt.xlabel('Day')
    plt.ylabel('Average price of Memory')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(OUTPUT_DIR / 'price_trend.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_top_brands(df):
    plt.figure(figsize=(15,5))
    plt.bar(df['brand'], df['brand_count'])
    plt.title('Product Count by Brand from Newegg in Descending Order')
    plt.xlabel('Brand')
    plt.ylabel('Product Count')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(OUTPUT_DIR / 'top_brands.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_avg_price_by_brand(df):
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