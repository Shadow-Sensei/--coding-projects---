# build the same webscraper out of memory but for books
# go for improvements 
import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import time 
from datetime import datetime
import random # this is for randomness in the amount of wait before a request is sent. 
from urllib.parse import urljoin # this is used to get the pagination link properly to be scraped 
from fake_useragent import UserAgent


log_filename = f"log_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format= '%(asctime)s-%(levelname)s-%(message)s'
)

Base_URL = "http://books.toscrape.com/"

def create_session():
    session = requests.Session()
    retry = Retry(
        total= 5,
        backoff_factor = 1,
        status_forcelist = [500, 502, 503, 504],
        raise_on_status = False
    )
    adapters = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter=adapters)
    session.mount("https://", adapter=adapters)
    return session



def book_scraper(session, page_url): 
    ua = UserAgent()
    headers = {
    "User-Agent" : ua.random
}
    response = session.get(page_url, headers=headers) # change to session here 
    if response.status_code != 200:
        logging.error(f"Failed to retrieve {page_url} - Status code: {response.status_code}")
        return []
    logging.debug(f"Sucessfully fetched {page_url}- Status:{response.status_code}")
    parse = BeautifulSoup(response.text, "lxml")
    return parse

def get_rating(rating_classes):
    return next((cls for cls in rating_classes if cls != 'star-rating'), 'Unknown')


def scrape_data(parsed_object, page_url):

     book_details = parsed_object.select(".product_pod")

     data = []
     for book in book_details:
        try:
            book_name = book.select_one('h3 a')['title']
            book_price_raw = book.select_one('.price_color').get_text(strip=True)
            book_price = float(book_price_raw.replace('Â£','').replace('£',''))
            availability = book.select_one('.instock.availability').get_text(strip=True)
            ratings = get_rating(book.select_one('p.star-rating')['class'])
            relative_url = book.select_one('h3 a')['href']
            product_url = urljoin(page_url, relative_url)
            data.append({"Book": book_name,
                "currency" : "GBP",
                "price":book_price,
                "Availability": availability,
                "rating/5" : ratings,
                "product-url": product_url

                })
        except Exception as e:
            logging.warning(f"failed to parse a book on {page_url}:{e}")
     return data 


def search_pages_books():
    session = create_session()
    current_url = Base_URL
    all_books = []

    while current_url:
        logging.info(f"scraping{current_url}")
        book = book_scraper(session=session, page_url=current_url)
        required_data = scrape_data(book, current_url)
        all_books.extend(required_data)

        try:
            next_button = book.select_one(".next")

            if next_button:
                next_page = next_button.find('a')['href']
                current_url = urljoin(current_url, next_page)
                time.sleep(random.uniform(1.0,2.5))
            else:
                logging.info("Reached the last page!")
                current_url = None
        except Exception as e:
            logging.error(f"Error processing {current_url} : {e}")
            current_url = None
    return all_books

if __name__ == "__main__":
    books = search_pages_books()
    dataframe = pd.DataFrame(books)
    columns = ["Book", "currency", "price", "Availability", "rating/5", "product-url"]
    dataframe.to_csv(f"books.csv", index=False,  columns=columns,encoding='utf-8')
    logging.info(f"\n  Books scraped = {len(books)}")
    print(f"\n Books scraped = {len(books)}")



