# Newegg Memory Price Tracker

A few months ago, with the expansion of AI, the consumer memory market saw 
a massive jump in cost. One of the major producers of memory switched their 
priority to supporting AI data centers, causing major price increases for 
everyday consumers. I created this web scraper to visualize memory price 
averages and determine the best time to purchase PC memory.

## Sample Output
![Price Trend](outputs/price_trend.png)

## Features
- Scrapes all 20 pages of memory listings from Newegg
- Persists data in a SQLite database with duplicate prevention
- Schedules automated scrape runs on a configurable interval
- Analyzes accumulated data using SQL aggregate queries
- Generates three charts: price trends over time, top brands by 
  listing count, and average price by brand

## Project Structure
```
WebScraper/
├── config.py       # all settings and paths
├── scraper.py      # fetches and parses Newegg listings
├── database.py     # SQLite schema, insert, and query functions
├── main.py         # scheduler entry point
├── analyzer.py     # SQL aggregate queries via pandas
├── visualizer.py   # matplotlib chart generation
└── requirements.txt
```

## Setup
1. Clone the repository
2. Create and activate a virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
```
3. Install dependencies
```bash
   pip install -r requirements.txt
```
4. Run the scraper
```bash
   python main.py
```
5. Generate charts
```bash
   python visualizer.py
```

## Configuration
In `config.py`, change `SCRAPE_INTERVAL_HOURS` to set how often 
the scheduler runs.

## Skills Demonstrated
**Python:** `requests`, `json`, `re`, `schedule`, `logging`, 
`datetime`, `sqlite3`  
**SQL:** `CREATE TABLE`, `INSERT OR IGNORE`, `SELECT`, `WHERE`, 
`GROUP BY`, `ORDER BY`, `AVG()`, `COUNT()`, `DATE()`  
**Libraries:** pandas, matplotlib  
**Concepts:** JSON extraction from embedded JavaScript, parameterized 
queries, automated scheduling, data visualization

## Dependencies
requests==2.34.2
schedule==1.2.2
pandas==3.0.3
matplotlib==3.10.9

## Author
Zy Dowdy