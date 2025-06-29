import logging
from datetime import datetime
import requests 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd 
import time  # adding delays between requests 

import logging
from datetime import datetime

log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


Base_url = "http://quotes.toscrape.com/" # simple url

def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,                 # Retry 5 times
        backoff_factor=1,        # Wait 1s, 2s, 4s between tries
        status_forcelist=[500, 502, 503, 504],  # Retry on server errors
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# basic scraper to scrape the first page
def scrape_quotes(session, page_url):
    response = session.get(page_url)
    soup = BeautifulSoup(response.text, "lxml")
    quote_divs = soup.select(".quote")

    data = []
    for cite in quote_divs:
        quote = cite.select_one(".text").get_text(strip=True)
        author = cite.select_one(".author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in cite.select(".tag")]

        data.append({
            "Quote" :quote,
            "Author" : author, 
            "Tags" : ",".join(tags)
        })
    return data


# this is for pagination of the website 
def scrape_all_quotes():
    session = create_session()
    current_url = Base_url 
    all_quotes = []
# we use the scraper normally first 
    while current_url:
        logging.info(f"Scraping {current_url}")
        quotes = scrape_quotes(session, current_url)
        all_quotes.extend(quotes)
# then we try searching for the next button, to get more pages 
        try:
            response = session.get(current_url)
            soup = BeautifulSoup(response.text, "lxml")
            next_button = soup.select_one('.next')

            if next_button:
                next_page = next_button.find('a')['href']
                current_url = Base_url + next_page
                time.sleep(1)
            else:
                logging.info("Reached the last page!")
                current_url = None
        except Exception as e:
            logging.error(f"Error processing {current_url} : {e}")
            current_url = None

    return all_quotes

if __name__ == "__main__":
    quotes = scrape_all_quotes()
    df = pd.DataFrame(quotes)
    df.to_csv("quotes.csv", index=False)
    logging.info(f"\nThe number of quotes scraped:{len(quotes)}")
    print(f"\nThe number of quotes scraped:{len(quotes)}")
    for i, quote in enumerate(quotes[:5], 1):
        print(f"\nQuotes {i}: ")
        print(f"Text: {quote['Quote']}")
        print(f"Text: {quote['Author']}")
        print(f"Text: {quote['Tags']}")