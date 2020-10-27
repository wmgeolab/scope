import pandas as pd
import sqlite3
import urllib.request
import zipfile

def iter_gdelt_sources(file_url):

    # read the mentions csv file
    mentions = pd.read_csv(file_url)
    # store only the language code
    mentions['MentionDocTranslationInfo'] = mentions['MentionDocTranslationInfo'].str[6:9]

    # loop through rows and yield the columns:
    # file_url
    # MentionType
    # MentionSourceName
    # MentionIdentifier
    # MentionDocTranslationInfo (only the language code)
    ment_dict = dict.fromkeys(['url', 'MentionType', 'MentionSourceName', 'MentionIdentifier', 'MentionDocTranslationInfo'])

    ment_dict['url'] = file_url

    for column in ['MentionType', 'MentionSourceName', 'MentionIdentifier', 'MentionDocTranslationInfo']:
        data = mentions[column]
        ment_dict[column] = data

    yield ment_dict

def scrape_gdelt_sources():

    # connect to scope database
    conn = pymysql.connect(host="mysql.scopedata.org", user="scopesql",
                         password="fY7Ukl52UI", db="scopesourcedata")

    curs = conn.cursor()


    # read master file list
    masterfileurl = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"


    masterfilelist = urllib.request.urlopen(masterfileurl)

    for line in masterfilelist:
        if 'mentions' in line:
            # extract url from masterfilelist
            index = line.find('http:')
            url = line[index:]

            # loop through csv with iter_gdelt_sources
            zf = zipfile.ZipFile(url)
            iter_gdelt_sources(zf.open(url[:-4]))
            # slice is to drop the .zip extension from the url

            # "If row key 'MentionIdentifier' does not already exist in the database:
                # Add to database"

            # ^^not entirely sure how to do this
