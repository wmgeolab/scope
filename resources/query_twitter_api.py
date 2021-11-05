#import os

#os.system("pip3 install tweepy")

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
    """
    # assert isinstance(d, str)
    w = d.strip()
    w = w.split(" ") # handles leading and trailing spaces
    ds = w[0].split("/")
    # if no time specified, defaults to midnight, first second of the day
    t = ["00", "00"] if len(w) == 1 else w[1].split(":")
    return "{}{}{}{}{}".format(ds[2], ds[0], ds[1], t[0], t[1])
    """
    return d

def twitter_search(args):

    start_date = args['start_date']
    if 'end_date' in args:
      end_date = args['end_date']
    primary = args['primary']
    secondary = args['secondary']
    tertiary = args['tertiary']

    # assert isinstance(primary, list)
    # from the Twitter docs: "Limit your searches to 10 keywords and operators. Queries can be limited due to complexity."
    # assert((len(primary) + len(secondary)) < 11)
    # get dates into right format for api
    sd = parse_date(start_date)
    ed = parse_date(end_date)
    n = 100
    lines = []
    # api keys, change later after academic twitter dev request
    with open(os.path.join(os.getcwd(), 'api.txt')) as f:
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

if __name__ == '__main__':

    args = {}
    args['start_date'] = '202110010000'
    args['end_date'] = '202110180000'
    args['primary'] = 'russia'
    args['secondary'] = ['africa']
    args['tertiary'] = ['water']

    ret = twitter_search(args)
    for i in ret:
      print (i.source_text)


    pass
