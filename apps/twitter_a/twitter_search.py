import csv
import datetime
import os
import requests
import random
import re
import tweepy as tw

import pymysql

class SourceType3:
    def __init__(self, tweet, html):
        self.tweet = tweet # Status object
        self.source_api = str(tweet._api) # str api call reference
        self.source_type_code = "SCOPE_S_3"
        self.source_documentation = html # str repr of html
        self.source_json = str(tweet._json) # str
        self.source_url = "https://twitter.com/{}/status/{}".format(tweet.user.screen_name, tweet.id) # str
        self.source_id = str(tweet.id) # str
        self.source_text = tweet.extended_tweet["full_text"] if tweet.truncated else tweet.text # str
        self.source_created_at = tweet.created_at.strftime('%m/%d/%Y') # str
        self.source_in_reply_to_status_id = " __na__ " if not tweet.in_reply_to_status_id else str(tweet.in_reply_to_status_id) # str
        self.source_in_reply_to_user_id = " __na__ " if not tweet.in_reply_to_user_id else str(tweet.in_reply_to_user_id) # str
        self.source_in_reply_to_screen_name = " __na__ " if not tweet.in_reply_to_screen_name else tweet.in_reply_to_screen_name # str
        self.source_user_id = str(tweet.user.id) # str
        self.source_user_name = tweet.user.name # str
        self.source_user_screenname = tweet.user.screen_name # str
        self.source_user_location = " __na__ " if not tweet.user.location else tweet.user.location # str
        self.source_user_description = tweet.user.description # str
        self.source_user_url = tweet.user.url # str
        self.source_user_created_at = tweet.user.created_at.strftime('%m/%d/%Y') # str
        self.source_user_followers_count = tweet.user.followers_count # int
        self.source_user_friends_count = tweet.user.friends_count # int
        self.source_user_listed_count = tweet.user.listed_count # int
        self.source_user_favorites_count = tweet.user.favourites_count # int
        self.source_user_statuses_count = tweet.user.statuses_count # int
        # self.source_user_utc_offset = tweet.user.utc_offset # TODO
        # self.source_user_time_zone = tweet.user.time_zone # TODO
        try:
            self.source_user_geo_enabled = tweet.user.geo_enabled # bool
        except:
            self.source_user_geo_enabled = False
        self.source_user_verified = tweet.user.verified # bool
        try:
            self.source_user_lang = tweet.user.lang # str
        except:
            self.source_user_lang = " __na__ "
        try:
            self.source_user_contributors_enabled = tweet.user.contributors_enabled # bool
        except:
            self.source_user_contributors_enabled = False
        self.source_user_is_translator = tweet.user.is_translator # bool
        try:
            self.source_user_is_translation_enabled = tweet.user.user_is_translation_enabled # bool
        except:
            self.source_user_is_translation_enabled = False
        self.source_user_profile_background_color = tweet.user.profile_background_color # str
        self.source_user_profile_image_url_https = tweet.user.profile_image_url_https # str
        self.source_user_default_profile = tweet.user.default_profile # bool
        try:
            self.source_possibly_sensitive = tweet.possibly_sensitive # bool
        except:
            self.source_possibly_sensitive = False
        try:
            self.source_possibly_sensitive_appealable = tweet.possibly_sensitive_appealable # bool
        except:
            self.source_possibly_sensitive_appealable = False
        # try: TODO
        #   self.source_place = tweet.place
        # except:
        #   self.source_place = " __na__ "
        try: # str
            self.source_quoted_status_id = str(tweet.quoted_status_id)
        except:
            self.source_quoted_status_id = " __na__ "
        try: # int
            self.source_quote_count = tweet.quote_count
        except:
            self.source_quote_count = 0
        try: # int
            self.source_reply_count = tweet.reply_count
        except:
            self.source_reply_count = 0
        self.source_favorite_count = tweet.favorite_count # int
        self.source_retweet_count = tweet.retweet_count # int
        self.source_favorited = tweet.favorited # bool
        self.source_retweeted = tweet.retweeted # bool
        self.source_lang = tweet.lang # str
        self.source_hashtags = []
        self.source_hyperlinks = []
        self.source_relevance = 0
        self.source_search_id = self.source_id + "-" + datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")

        for i in self.source_text.split(' '):
            if len(i) > 1 and i[0] == "#":
                self.source_hashtags.append(i)
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, self.source_text)
        for j in url:
            self.source_hyperlinks.append(j[0])

def parse_date(d):
    # assert isinstance(d, str)
    w = d.strip()
    w = w.split(" ") # handles leading and trailing spaces
    ds = w[0].split("/")
    # if no time specified, defaults to midnight, first second of the day
    t = ["00", "00"] if len(w) == 1 else w[1].split(":")
    return "{}{}{}{}{}".format(ds[2], ds[0], ds[1], t[0], t[1])

def twitter_search(start_date, end_date, primary, secondary = [], tertiary = []):
    # assert isinstance(primary, list)
    # from the Twitter docs: "Limit your searches to 10 keywords and operators. Queries can be limited due to complexity."
    # assert((len(primary) + len(secondary)) < 11)
    # get dates into right format for api
    sd = parse_date(start_date)
    ed = parse_date(end_date)
    n = 100
    lines = []
    # api keys, change later after academic twitter dev request
    with open(os.path.join(os.getcwd(), 'apps/twitter_a/api.txt')) as f:
        lines = f.readlines()
    API_KEY = str(lines[1]).strip('\n')
    API_SECRET_KEY = str(lines[3]).strip('\n')
    ACCESS_TOKEN = str(lines[5]).strip('\n')
    ACCESS_TOKEN_SECRET = str(lines[7]).strip('\n')

    auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tw.API(auth)
    ret = []

    # twitter query system is quite flexible, in the future we could add more params for more targeted searches
    search_query = " ".join(primary) + " (" + " OR ".join(secondary) + ")"

    tweets = tw.Cursor(api.search_full_archive,
                label="dev", # might need to change later
                query=search_query,
                fromDate=sd,
                toDate=ed).items(n)

    for tweet in tweets:
        tweet_link = "https://twitter.com/{}/status/{}".format(tweet.user.screen_name, tweet.id)
        req = requests.get(tweet_link)
        html = req.text
        tmp = SourceType3(tweet, html)
        ret.append(tmp)
    for i in ret:
        for j in tertiary:
            if j in i.source_text:
                i.source_relevance += 1
    return ret

def sql_conn(tweet, create=False):
    host = "mysql.scopedata.org"
    user = "scopesql"
    pwd = "fY7Ukl52UI"
    db = "scopesourcedata"
    conn = pymysql.connect(host=host, user=user, password=pwd, db=db)
    curs = conn.cursor()
    if create:
        curs.execute("DROP TABLE IF EXISTS SourceType3")
        sql_create = """CREATE TABLE SourceType3 (source_search_id VARCHAR(255) PRIMARY KEY, source_id VARCHAR(25), source_type_code VARCHAR(10), source_json LONGTEXT, source_text LONGTEXT, source_documentation LONGTEXT, source_url TEXT,
            source_created_at TEXT, source_in_reply_to_status_id TEXT, source_in_reply_to_user_id TEXT, source_in_reply_to_screen_name TEXT, source_user_id TEXT, source_user_name TEXT, 
            source_user_screenname TEXT, source_user_location TEXT, source_user_description MEDIUMTEXT, source_user_url TEXT, source_user_created_at TEXT, source_user_followers_count INT,
            source_user_friends_count INT, source_user_listed_count INT, source_user_favorites_count INT, source_user_statuses_count INT, source_user_geo_enabled BIT, source_user_verified BIT, 
            source_user_lang TEXT, source_user_contributors_enabled BIT, source_user_is_translator BIT, source_user_is_translation_enabled BIT, source_user_profile_background_color TEXT, 
            source_user_profile_image_url_https TEXT, source_user_default_profile BIT, source_possibly_sensitive BIT, source_possibly_sensitive_appealable BIT, source_quoted_status_id TEXT, 
            source_quote_count INT, source_reply_count INT, source_favorite_count INT, source_retweet_count INT, source_favorited BIT, source_retweeted BIT, source_lang TEXT, source_relevance INT, 
            source_api TEXT);"""
        curs.execute(sql_create)
    sql = """INSERT INTO SourceType3 (source_search_id, source_id, source_type_code, source_json, source_text, source_documentation, source_url, source_created_at, source_in_reply_to_status_id, 
        source_in_reply_to_user_id, source_in_reply_to_screen_name, source_user_id, source_user_name, source_user_screenname, source_user_location, source_user_description, source_user_url, 
        source_user_created_at, source_user_followers_count, source_user_friends_count, source_user_listed_count, source_user_favorites_count, source_user_statuses_count, source_user_geo_enabled, 
        source_user_verified, source_user_lang, source_user_contributors_enabled, source_user_is_translator, source_user_is_translation_enabled, source_user_profile_background_color,
        source_user_profile_image_url_https, source_user_default_profile, source_possibly_sensitive, source_possibly_sensitive_appealable, source_quoted_status_id, source_quote_count,
        source_reply_count, source_favorite_count, source_retweet_count, source_favorited, source_retweeted, source_lang, source_relevance, source_api) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (tweet.source_search_id, tweet.source_id, tweet.source_type_code, tweet.source_json, tweet.source_text, tweet.source_documentation, tweet.source_url, tweet.source_created_at,  
        tweet.source_in_reply_to_status_id, tweet.source_in_reply_to_user_id, tweet.source_in_reply_to_screen_name, tweet.source_user_id, tweet.source_user_name, tweet.source_user_screenname, 
        tweet.source_user_location, tweet.source_user_description, tweet.source_user_url, tweet.source_user_created_at, tweet.source_user_followers_count, tweet.source_user_friends_count, 
        tweet.source_user_listed_count, tweet.source_user_favorites_count, tweet.source_user_statuses_count, tweet.source_user_geo_enabled, tweet.source_user_verified, tweet.source_user_lang, 
        tweet.source_user_contributors_enabled, tweet.source_user_is_translator, tweet.source_user_is_translation_enabled, tweet.source_user_profile_background_color, tweet.source_user_profile_image_url_https, 
        tweet.source_user_default_profile, tweet.source_possibly_sensitive, tweet.source_possibly_sensitive_appealable, tweet.source_quoted_status_id, tweet.source_quote_count, 
        tweet.source_reply_count, tweet.source_favorite_count, tweet.source_retweet_count, tweet.source_favorited, tweet.source_retweeted, tweet.source_lang, tweet.source_relevance, tweet.source_api)
    curs.execute(sql, val)
    conn.commit()
    output = curs.fetchall()
    conn.close()

if __name__ == '__main__':
    pass
