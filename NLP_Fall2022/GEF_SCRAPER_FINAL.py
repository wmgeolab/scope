#Taylor Liegel 9/18/2022

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import requests

num_articles = 0

options = Options()
options.add_argument("headless")
options.add_argument("--log-level=3")
service = Service("chromedriver.exe")  ## THIS WILL NEED TO BE MODIFIED IF CHROMEDRIVER.EXE IN DIFFERENT LOCATION!.
OUTPUT_PATH = "pdf_links.txt" ## Change this to where you want the output file to go.

url = "https://www.thegef.org/projects-operations/database"
driver = webdriver.Chrome(service=service, options=options)
sting_url = "https://www.thegef.org/projects-operations/projects/"

## Change this as needed: What page of forums to start/end at.

url_info = {"url": sting_url, "start_index": 1, "end_index": 500}

current_index = url_info.get("start_index")
pdf_links = []

while current_index <= url_info.get("end_index"):

    cur_url = url_info.get("url") + str(current_index)
    driver.get(cur_url)

    all_links = driver.find_elements(By.TAG_NAME, "a")

    for links in all_links:
        href_link = links.get_attribute("href")
        if href_link is not None and "pdf" in href_link:
            pdf_links.append(href_link)

    current_index += 1
    num_articles += 1

    print("Current index is ", current_index, "out of ", url_info.get("end_index"))


with open(OUTPUT_PATH, 'w') as filehandle:  # if you want to append, change 'w' to 'a+'
    for link in list(pdf_links):
        filehandle.write("%s\n" % link)
