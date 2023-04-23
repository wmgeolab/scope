import json
from scraper.Google import googleSearch
import time
import mysql.connector
import os

# this function is the main function for scraping google
# given a keyword


def main_query(args):
    # feed in a keyword, if there are multiple keywords, they will be combined with spaces
    keyword = args['primary'] + " " + args['secondary']
    serp = googleSearch(keyword, maxPage=1, newsVertical=False)

    print("\nSerp type: ", type(serp))
    print("\nSerp dict keys: ", serp.keys)
    # return just the sources, we don't need the other info
    return serp['links']


def store_in_db():
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
                    print("Length of results dict: ", len(results))
                    # print(results[0]['articles'])
                    #articles = results[0]['articles']
                    if len(results) > 0:
                        # goes through every subdict inside the bigger results dict
                        articles = results
                        for article in articles:
                            # cursor.execute(
                            #     "INSERT INTO scopeBackend_source(text, url, sourceType_id) VALUES (%s, %s, %s)", (article['title'], article['link'], 3, ))
                            cursor.execute("""INSERT INTO scopeBackend_source (text, url, sourceType_id)
                                SELECT * FROM (SELECT %s AS text, %s AS url, %s AS sourceType_id) AS temp
                                WHERE NOT EXISTS (
                                    SELECT url FROM scopeBackend_source WHERE url = %s
                                ) LIMIT 1;""", (article['title'], article['link'], 3, article['link'], ))
                            conn.commit()
                            cursor.execute(
                                "SELECT * FROM scopeBackend_source WHERE url=%s", (article['link'], ))
                            source = cursor.fetchall()
                            print("Source: ", source)
                            if len(source) > 0:
                                cursor.execute(
                                    "INSERT INTO scopeBackend_result (run_id, source_id) VALUES (%s, %s);", (current_run[0][0], source[0][0], ))
                                conn.commit()


if __name__ == '__main__':
    # FOR TESTING PURPOSES ONLY
    args = {
        "start_date": "20200915000000",
        "end_date": "20200917000000",
        "primary": "ukraine",
        "secondary": "bombings",
        "tertiary": "",
        "maxrecords": 5
    }
    result = main_query(args)
    for link in result:
        print(link)
    print(store_in_db())
