import json
from scraper.Google import googleSearch

# this function is the main function for scraping google
# given a keyword


def main_query(keyword):
    # feed in a keyword, if there are multiple keywords, they will be combined with spaces
    serp = googleSearch(keyword, maxPage=1, newsVertical=False)

    print("\nSerp type: ", type(serp))
    print("\nSerp dict keys: ", serp.keys)
    # return just the sources, we don't need the other info
    return serp['links']


if __name__ == '__main__':
    # FOR TESTING PURPOSES ONLY
    result = main_query('ukraine')
    for link in result:
        print(link)
