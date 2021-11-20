import concurrent.futures
from time import time
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



MAX_THREADS = 30

data = {}
data['sources'] = []

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
driver = webdriver.Firefox(firefox_options=fireFoxOptions)
driver.set_page_load_timeout(3)

def download_url(url):


    try:
        resp = requests.get(url[1])
        title = ''.join(x for x in url if x.isalpha()) + "html"
        soup = BeautifulSoup(resp.content, 'html.parser')
        if get_only_text(soup.find_all("p")) == "":
            soup = scrape_with_selenium(url[1])
    except:
        soup = scrape_with_selenium(url[1])





    data['sources'].append({
        'relevant': url[0],
        'url': url[1],
        'text': get_only_text(soup.find_all("p"))
    })



    time.sleep(0.25)

def scrape_with_selenium(url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser')

def download_stories(story_urls):
    threads = min(MAX_THREADS, len(story_urls))

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threads)
    executor.map(download_url, story_urls)
    executor.shutdown(wait=True)


def main(story_urls):
    t0 = time()
    download_stories(story_urls)
    t1 = time()
    print(f"{t1-t0} seconds to download {len(story_urls)} stories.")

def get_only_text(p_array):
    output = ''
    for para in p_array:
        output += ' ' + para.get_text()

    return output

if __name__ == "__main__":
    file1 = open('small_sources.txt', 'r')
    story_urls = [x.strip().split() for x in file1.readlines()]

    main(story_urls)

    with open('small_sources.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)