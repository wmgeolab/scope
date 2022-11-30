import json
from scraper.Google import googleSearch

if __name__ == '__main__':
    query = "midterm elections"
    extra_params = {}
    serp = googleSearch(query, maxPage=5, newsVertical=False,
                        extraParams=extra_params)

    with open('google_serp.json', 'w') as outfile:
        json.dump(serp, outfile, indent=4)
