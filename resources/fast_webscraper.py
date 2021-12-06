# This program scrapes the urls inside the "all_sources.txt" file and puts the output
# in the "all_sources.json" file

# This program functions correctly, but is only included in this repository for
# readability, the actual version of this code is running on CDSW and will be
# called somewhere else in the code.

import concurrent.futures
from time import time
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


MAX_THREADS = 30

data = {} # data will be written to the "all_sources.json" file after running
data['sources'] = []

# set up selenium web driver
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
driver = webdriver.Firefox(firefox_options=fireFoxOptions)
driver.set_page_load_timeout(3)

# This function is run by every thread, and scrapes the passed url
def download_url(url):

    try: # First try scraping with the faster BeautifulSoup scraper
        resp = requests.get(url[1])
        title = ''.join(x for x in url if x.isalpha()) + "html"
        soup = BeautifulSoup(resp.content, 'html.parser')
        if get_only_text(soup.find_all("p")) == "":
            soup = scrape_with_selenium(url[1])
    except: # If BeautifulSoup cannot scrape the website, try scraping with the slower, more reliable selenium
        soup = scrape_with_selenium(url[1])

    data['sources'].append({ # Add the scraped data as a dictionary to be converted to json
        'relevant': url[0],
        'url': url[1],
        'text': get_only_text(soup.find_all("p"))
    })

    time.sleep(0.25)


# Scrapes the given url using selenium
def scrape_with_selenium(url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser')


# Creates the worker threads that each scrape through the url inputs
def download_stories(story_urls):
    threads = min(MAX_THREADS, len(story_urls))

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threads)
    executor.map(download_url, story_urls)
    executor.shutdown(wait=True)

# Breaks the scraped html down into just the text, ignoring html like <p> or <a>
def get_only_text(p_array):
    print(p_array)
    output = ''
    for para in p_array:
        output += ' ' + para.get_text()
    print(output)
    return output

def main(story_urls):
    t0 = time()
    download_stories(story_urls)
    t1 = time()
    print(f"{t1-t0} seconds to download {len(story_urls)} stories.")

if __name__ == "__main__":
    file1 = open('small_sources.txt', 'r')
    story_urls = [x.strip().split() for x in file1.readlines()]

    main(story_urls)

    with open('small_sources.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)