import json
import logging
import requests
from config import TARGET_URL, REQUEST_HEADERS, REQUEST_TIMEOUT
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def _fetch(url:str) -> str|None:
    """
    Request the raw html data from the url as a string using request.get and handles HTTP errors, timeouts, and network failures

    Args:
        url:the TARGET_URL assigned in config + the incrementing page numbers
    
    Returns:
        the html string from each page of the website or None if there is a HTTP error, timeout, or network failure
    """                                      
    try: 
        response = requests.get(url,headers = REQUEST_HEADERS,timeout = REQUEST_TIMEOUT)
        response.raise_for_status()                                
        return response.text
    except requests.exceptions.Timeout:
        logger.error(f'Request timed out for URL: {url}')
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error {e.response.status_code} for URL: {url}')
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f'Requests failed: {e}')
        return None  

def _parse(html:str) -> list[dict]:           
    """
    Locates the embedded JSON inside of the html data then parses the product data

    Args:
        html:is the html string from the website pages

    Returns:
        A list of dicts that contains the keys: title, model, brand, price, rating, num_reviews, in_stock, url, scraped_at. Returns [] if it cannot locate or parse "__initialState__"
    """           

    #locate the __initialState__ assignment in the raw HTML 
    idx = html.find('__initialState__={')                                
    if idx == -1:
        idx = html.find('__initialState__ = {')
    if idx == -1:
        logger.error('Could not find __initialState__ assignment')
        return []
    
    #use a brace counter to find the true end of the JSON object
    start = html.find('{',idx)                                            
    depth = 0
    end = start
    for i, ch in enumerate(html[start:], start):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = i
                break

    #parse the extracted substring as JSON
    try:                                                                
        data = json.loads(html[start:end+1])
    except json.JSONDecodeError as e:
        logger.error(f'Failed to parse __initialState__ JSON: {e}')
        return []
    
    products_raw = data.get('Products', [])   
    scraped_at = datetime.now(timezone.utc).isoformat()
    results = []

    for product in products_raw:
        
        #skips combo deals and sponsored cards
        if product.get('IsCombo') or product.get('SponsoredMsg'):       
            continue

        cell = product.get('ItemCell', {})
        if not cell:
            continue
        
        #these fields are nested on level deeper inside ItemCell
        review = cell.get('Review') or {}
        manufacturer = cell.get('ItemManufactory') or {}
        description = cell.get('Description') or {}
        
        #these are flat string values pulled directly from their objects
        item_num = product.get('ProductNumber', '')
        brand = manufacturer.get('Manufactory') or None

        #build the final dict
        results.append({                                                
            'title': description.get('ProductName'),
            'model': cell.get('Model'),
            'brand': brand,
            'price': cell.get('FinalPrice') or cell.get('UnitCost'),
            'rating': review.get('RatingOneDecimal'),
            'num_reviews': review.get('HumanRating'),
            'in_stock' : cell.get('Instock'),
            'url' : f'https://www.newegg.com/p/{item_num}',
            'scraped_at' : scraped_at
        })
    
    logger.info(f'Parsed {len(results)} products')                    
    return results

#scrapes the website and returns data as a list of dicts ["->" is a return type hint]
def scrape(url:str = TARGET_URL) -> list[dict]:
    """
    Combines _fetch and _parse into one function that pulls the data as assigns it to a list of dicts

    Args:
        url: The full product listing from Newegg for one page and it defaults to TARGET_URL from config.py

    Returns:
        A list of dicts containg the keys: title, model, brand, price, rating, num_reviews, in_stock, url, scraped_at. If the request fails or no products are found it returns []
    """                           
    raw_html = _fetch(url)
    if raw_html is None:                                                
        return []
    return _parse(raw_html)

#this function was included to scrape all 20 pages on the product website
def scrape_all_pages() -> list[dict]:
    """
    Increments the page number on the website to scrape 20 pages of products.
     
    Returns:
        A list of dicts containg the keys: title, model, brand, price, rating, num_reviews, in_stock, url, scraped_at. Pages that fail return [] and are skipped, results may be less than expected.
    """
    
    results=[]
    
    for page_num in range(1,21):
        url = f'{TARGET_URL}&page={page_num}'
        results.extend(scrape(url))
        logger.info(f'Scraping page {page_num} of 20')

    return results

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)                           
    products = scrape_all_pages()
    print(f'Found {len(products)} products\n')
    for p in products[:3]:                                              #print the first 3 products to verify shape and content
        print(p)