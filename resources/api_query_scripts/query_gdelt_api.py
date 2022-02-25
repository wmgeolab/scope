# This program takes in arugments as keywords, the length of time they want to
# query their data from, and how many articles they want returned (further expansion
# for parameters possible.) It then returns a json of all articles found.

# Here are some examples of the url based queries
# https://api.gdeltproject.org/api/v2/doc/doc?format=html&timespan=2Y&query=ecuador&mode=artlist&maxrecords=250&format=json&sort=hybridrel
# https://api.gdeltproject.org/api/v2/summary/summary?d=web&t=summary
# https://api.gdeltproject.org/api/v2/doc/doc?format=html&startdatetime=20170103000000&enddatetime=20181011235959&query=ecuador%20china&mode=artlist&maxrecords=75&format=json&sort=hybridrel

import requests
from bs4 import BeautifulSoup


# This function is called by the "GDELT API Query" model. Pass in an args dictionary with
# query = your keywords, startdatetime (and optional enddatatime) to specify query timeframe
# and maxrecords to limit the number of articles returned. This function returns a json of the articles
def query_gdelt(args):

    url = "https://api.gdeltproject.org/api/v2/doc/doc?format=html&mode=artlist&format=json&sort=hybridrel"

    parameter_list = ['query', 'startdatetime', 'enddatetime', 'maxrecords']
    for i in parameter_list:
        if i not in args:
            continue

        if i == 'startdatetime' and 'enddatetime' not in args:
            url += '&timespan=' + args[i]
            continue

        url += '&' + i + '=' + args[i]

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    req = requests.get(url, headers)
    return req.json()


# Use this to test specific arguments for querying. This is not run in the model call.
if __name__ == "__main__":
    args = {
        "query": "china ecuador",
        "startdatetime": "20170615000000",
        "enddatetime": "20170625000000",
        "maxrecords": "10"
    }
    #args['enddatetime'] = '20160620000000'

    print(query_gdelt(args))
