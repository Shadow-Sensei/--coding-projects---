from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time
from random import uniform
import logging
from datetime import datetime
import pandas as pd 

log_filename = f"log_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s-%(levelname)s-%(message)s'
)

def open_browser(path, headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver_path = Service(executable_path=path)
    driver = webdriver.Firefox(service=driver_path,options=options)
    return driver

def retry_logic(browser,url,retries=5,delay=2):
    for attempt in range(retries):
        try:
            browser.get(url)
            if "404 Not Found" in browser.page_source:
                logging.critical(f'Page not found! : {url}')
                return False
            elif "403 Forbidden" in browser.page_source:
                logging.critical(f"Access denied : {url}")
                return False
            elif "429 Too Many Requests" in browser.page_source:
                logging.critical(f"Rate limit Hit:{url}")
                return False
            return True
        except WebDriverException as e:
            logging.warning(f"Atemtpt:{attempt+1}/{retries} failed to load {url}:{e}")
            time.sleep(delay + attempt * 2)
    logging.error(f"Failed to load {url} after {retries} retries")
    return False

def basic_scraper(browser_beginner):
    quotes = browser_beginner.find_elements(By.CLASS_NAME,"quote")
    data = []
    for quote in quotes:
        quote_text = quote.find_element(By.CLASS_NAME,"text").text
        quote_author = quote.find_element(By.CLASS_NAME,"author").text
        quote_tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME,"tag")]

        data.append({
            "Quote" : quote_text,
            "Author": quote_author,
            "Tags" : quote_tags})
    return data

def next_button_clicker(browser_beginner):
    try:
        next_button = browser_beginner.find_element(By.CLASS_NAME,"next")
        next_link = next_button.find_element(By.TAG_NAME,"a")
        next_link.click()
        time.sleep(uniform(1.0,2.0))
        return True
    except NoSuchElementException:
        return False

def website_login(browser_beginner):
    User_name = browser_beginner.find_element(By.ID,"username")
    User_name.send_keys("Sufi")
    PassWord = browser_beginner.find_element(By.ID,"password")
    PassWord.send_keys("Sufi")
    Submit_button = browser_beginner.find_element(By.XPATH,"/html/body/div/form/input[2]")
    Submit_button.click()

    return browser_beginner

def main():
    all_data = []
    path = "/usr/bin/geckodriver"
    gateway = open_browser(path=path,headless=True)
    scrape_da_website = "https://quotes.toscrape.com/login"
    logging.info(f"\nAttempting to scrape page :{scrape_da_website}")
    if not retry_logic(browser=gateway,url=scrape_da_website):
        logging.error(f"Couldn't load start page.")
        return []
    login_details = website_login(browser_beginner=gateway)
    while True:
        logging.info(f"Scraping:{gateway.current_url}")
        data = basic_scraper(browser_beginner=gateway)
        all_data.extend(data)

        if not next_button_clicker(browser_beginner=gateway):
            logging.info("Reached the last page.")
            break
    return all_data

result = main()
dataframe = pd.DataFrame(result)
columns = ["Quote","Author","Tags"]
dataframe.to_csv(f"quotes.csv",index=False,columns=columns,encoding='utf-8')
logging.info(f"\n Quotes scraped = {len(result)}")
print(f"\n Quotes scraped = {len(result)}")

        
