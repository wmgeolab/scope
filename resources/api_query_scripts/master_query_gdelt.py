import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
from store_data import store
import os
import json

from query_gdelt_api import query_gdelt

# the master query itself


def main_query(args):
    # twitter_args = {
    #     "start_date": args["start_date"][0:len(args["start_date"]) - 2],
    #     "end_date": args["end_date"][0:len(args["end_date"]) - 2],
    #     "primary": args['primary'],
    #     "secondary": args['secondary'],
    #     "tertiary": args['tertiary']
    # }
    #tweets = get_tweets(twitter_args)

    gdelt_args = {
        "query": args['primary'],
        "startdatetime": args['start_date'],
        "enddatetime": args['end_date'],
        "maxrecords": str(args['maxrecords'])
    }
    gdelt_data = query_gdelt(gdelt_args)
    # WITH TWITTER USAGE:
    # lines_to_write = ["Query: " + args['primary'] + " From " +
    #                   args['start_date'] + " To " + args['end_date'] + "\n", tweets, gdelt_data]
    # store(lines_to_write)
    # return gdelt_data, tweets

    # WITHOUT TWITTER USAGE:
    lines_to_write = ["Query: " + args['primary'] + " From " +
                      args['start_date'] + " To " + args['end_date'] + "\n", gdelt_data]
    store(lines_to_write)
    return gdelt_data


def store_in_db():
    # with open(os.path.join(os.getcwd(), 'db.txt')) as f:
    #     lines = f.readlines()
    conn = mysql.connector.connect(
        user=os.environ.get("SCOPE_USER"),
        password=os.environ.get("SCOPE_PASSWORD"),
        host=os.environ.get("SCOPE_HOST"),
        db=os.environ.get("SCOPE_DB")
    )
    cursor = conn.cursor()

    # GETTING THE QUERIES:
    cursor.execute("SELECT * FROM scopeBackend_query;")
    queries = cursor.fetchall()
    # query[0] is the id for the query table
    # That id is a foreign key referring to the 'query_id' on the keywords table
    for query in queries:
        print(query[0])
        cursor.execute(
            "SELECT * FROM scopeBackend_keyword WHERE scopeBackend_keyword.query_id = %s;", (query[0], ))
        keywords = cursor.fetchall()
        print("Keywords: ", keywords)
        # INSERT ROW into run table to initiate a run:
        cur = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO scopeBackend_run (time, query_id) VALUES (%s, %s);", (cur, query[0], ))
        cursor.execute(
            "SELECT * FROM scopeBackend_run WHERE time=%s AND query_id=%s;", (cur, query[0]))
        current_run = cursor.fetchall()
        print("Current run: ", current_run)
        if (len(keywords) >= 0):
            for keyword in keywords:
                if (',' not in str(keyword[1])) and (len(str(keyword[1])) >= 4):
                    args = {
                        "start_date": "20200915000000",
                        "end_date": "20200917000000",
                        "primary": str(keyword[1]),
                        "secondary": str(keyword[1]),
                        "tertiary": str(keyword[1]),
                        "maxrecords": 5
                    }
                    results = main_query(args)
                    print(results)
                    print("Length of results dict: ", len(results))
                    # print(results[0]['articles'])
                    #articles = results[0]['articles']
                    if len(results) > 0:
                        articles = results['articles']
                        for article in articles:
                            # cursor.execute(
                            #     "INSERT INTO scopeBackend_source(text, url, sourceType_id) VALUES (%s, %s, %s)", (article['title'], article['url'], 1, ))
                            cursor.execute("""INSERT INTO scopeBackend_source (text, url, sourceType_id)
                                SELECT * FROM (SELECT %s AS text, %s AS url, %s AS sourceType_id) AS temp
                                WHERE NOT EXISTS (
                                    SELECT url FROM scopeBackend_source WHERE url = %s
                                ) LIMIT 1;""", (article['title'], article['url'], 1, article['url'], ))
                            conn.commit()
                            cursor.execute(
                                "SELECT * FROM scopeBackend_source WHERE url=%s", (article['url'], ))
                            source = cursor.fetchall()
                            print("Source: ", source)
                            if len(source) > 0:
                                cursor.execute(
                                    "INSERT INTO scopeBackend_result (run_id, source_id) VALUES (%s, %s);", (current_run[0][0], source[0][0], ))
                                conn.commit()
                        # FOLLOWING SECTION IS ONLY FOR TWEETS:
                        # tweets = results[1]['tweets']
                        # for tweet in tweets:
                        #     cursor.execute("""INSERT INTO scopeBackend_source (text, url, sourceType_id)
                        #         SELECT * FROM (SELECT %s AS text, %s AS url, %s AS sourceType_id) AS temp
                        #         WHERE NOT EXISTS (
                        #             SELECT url FROM scopeBackend_source WHERE url = %s
                        #         ) LIMIT 1;""", (tweet['text'], tweet['url'], 2, tweet['url'], ))
                        #     conn.commit()
                        #     cursor.execute(
                        #         "SELECT * FROM scopeBackend_source WHERE url=%s", (tweet['url'], ))
                        #     source = cursor.fetchall()
                        #     cursor.execute(
                        #         "INSERT INTO scopeBackend_result (run_id, source_id) VALUES (%s, %s);", (current_run[0][0], source[0][0], ))
                        #     conn.commit()


if __name__ == '__main__':
    print(store_in_db())
