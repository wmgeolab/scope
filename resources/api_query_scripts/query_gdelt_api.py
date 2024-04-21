# This program takes in arugments as keywords, the length of time they want to
# query their data from, and how many articles they want returned (further expansion
# for parameters possible.) It then returns a json of all articles found.

# Here are some examples of the url based queries
# https://api.gdeltproject.org/api/v2/doc/doc?format=html&timespan=2Y&query=ecuador&mode=artlist&maxrecords=250&format=json&sort=hybridrel
# https://api.gdeltproject.org/api/v2/summary/summary?d=web&t=summary
# https://api.gdeltproject.org/api/v2/doc/doc?format=html&startdatetime=20170103000000&enddatetime=20181011235959&query=ecuador%20china&mode=artlist&maxrecords=75&format=json&sort=hybridrel

import requests
from gdeltdoc import GdeltDoc, Filters


# This function is called by the "GDELT API Query" model. Pass in an args dictionary with
# query = your keywords, startdatetime (and optional enddatatime) to specify query timeframe
# and maxrecords to limit the number of articles returned. This function returns a json of the articles
def query_gdelt(args):
    
    # start and end datetime need to be parsed into a YYYY-MM-DD format for the API
    args["startdatetime"] = args["startdatetime"][0:4] + "-" + args["startdatetime"][4:6] + "-" + args["startdatetime"][6:8]
    print("Start dt: " + args["startdatetime"])

    args["enddatetime"] = args["enddatetime"][0:4] + "-" + args["enddatetime"][4:6] + "-" + args["enddatetime"][6:8]
    print("End dt: " + args["enddatetime"])

    # Put in the API code:
    f = Filters(
        keyword = args["query"],
        start_date = args["startdatetime"],
        end_date = args["enddatetime"]
    )

    gd = GdeltDoc()

    articles = gd.article_search(f)

    return articles


# Use this to test specific arguments for querying. This is not run in the model call.
if __name__ == "__main__":
    args = {
        "query": "palestine",
        "startdatetime": "20210615000000",
        "enddatetime": "20240325000000",
        "maxrecords": "10"
    }

    print(query_gdelt(args))
