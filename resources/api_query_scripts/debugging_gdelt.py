import requests
# NOTE: This file uses the 'gdeltdoc' Python library
# more info about the library can be found at: https://pypi.org/project/gdeltdoc/
from gdeltdoc import GdeltDoc, Filters


if __name__ == '__main__':
    url = "https://api.gdeltproject.org/api/v2/doc/doc?format=html&mode=artlist&format=json&sort=hybridrel"

    # sample hardcoded args for debugging purposes
    gdelt_args = {
        "query": "Palestine",
        "startdatetime": "20210615000000",
        "enddatetime": "20240325000000",
        "maxrecords": "5"
    }

    params = ['query', 'startdatetime', 'enddatetime', 'maxrecords']

    for i in params:
        if i not in gdelt_args:
            continue

        if i == 'startdatetime' and 'enddatetime' not in gdelt_args:
            url += '&timespan=' + gdelt_args[i]
            continue

        url += '&' + i + '=' + gdelt_args[i]

    # URL WORKS FINE! I CAN SEE VALID JSON WHEN CLICKING ON THE BUILT URL
    
    # Trying out the new API:
    f = Filters(
        keyword = "palestine",
        start_date = "2020-05-10",
        end_date = "2024-03-20"
    )

    gd = GdeltDoc()

    articles = gd.article_search(f)

    print(articles.columns)