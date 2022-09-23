from query_twitter_api import get_tweets

from query_gdelt_api import query_gdelt
from store_data import store

# Queries both gdelt and twitter with one set of arguments
# ARGUMENTS MUST BE IN THE FOLLOWING FORMAT:
# {
#         "start_date": "YYYYMMDDHHMMSS",
#         "end_date": "YYYYDDMMHHMMSS",
#         "primary": "russia",
#         "secondary": ["africa"],
#         "tertiary": ["education"],
#         "maxrecords": 10
#     }


def query(args):
    twitter_args = {
        "start_date": args["start_date"][0:len(args["start_date"]) - 2],
        "end_date": args["end_date"][0:len(args["end_date"]) - 2],
        "primary": args['primary'],
        "secondary": args['secondary'],
        "tertiary": args['tertiary']
    }
    tweets = get_tweets(twitter_args)
    gdelt_args = {
        "query": args['primary'],
        "startdatetime": args['start_date'],
        "enddatetime": args['end_date'],
        "maxrecords": str(args['maxrecords'])
    }
    gdelt_data = query_gdelt(gdelt_args)
    lines_to_write = ["Query: " + args['primary'] + " From " +
                      args['start_date'] + " To " + args['end_date'] + "\n", tweets, gdelt_data]
    print(lines_to_write)
    store(lines_to_write)
    return gdelt_data, tweets


if __name__ == '__main__':
    args = {
        "start_date": "20200915000000",
        "end_date": "20210918000000",
        "primary": "ukraine",
        "secondary": ["europe"],
        "tertiary": ["education"],
        "maxrecords": 10
    }

    print(query(args))
