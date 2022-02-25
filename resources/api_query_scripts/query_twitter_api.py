import tweepy as tw
import re
import random
import requests
import datetime
import csv
import os

os.system("pip3 install tweepy")

#import pymysql

data = {}  # data will be returned to the model after scraping
data['tweets'] = []

# This class takes in a tweet object and html string, then gets relevant data from it (only some of this data
# is returned in the model, but expansion is possible by accessing other variables)


class SourceType3:
    def __init__(self, tweet, html):
        self.tweet = tweet  # Status object
        self.source_api = str(tweet._api)  # str api call reference
        self.source_type_code = "SCOPE_S_3"
        self.source_documentation = html  # str repr of html
        self.source_json = str(tweet._json)  # str
        self.source_url = "https://twitter.com/{}/status/{}".format(
            tweet.user.screen_name, tweet.id)  # str
        self.source_id = str(tweet.id)  # str
        # str
        self.source_text = tweet.extended_tweet["full_text"] if tweet.truncated else tweet.text
        self.source_created_at = tweet.created_at.strftime('%m/%d/%Y')  # str
        self.source_in_reply_to_status_id = " __na__ " if not tweet.in_reply_to_status_id else str(
            tweet.in_reply_to_status_id)  # str
        self.source_in_reply_to_user_id = " __na__ " if not tweet.in_reply_to_user_id else str(
            tweet.in_reply_to_user_id)  # str
        self.source_in_reply_to_screen_name = " __na__ " if not tweet.in_reply_to_screen_name else tweet.in_reply_to_screen_name  # str
        self.source_user_id = str(tweet.user.id)  # str
        self.source_user_name = tweet.user.name  # str
        self.source_user_screenname = tweet.user.screen_name  # str
        self.source_user_location = " __na__ " if not tweet.user.location else tweet.user.location  # str
        self.source_user_description = tweet.user.description  # str
        self.source_user_url = tweet.user.url  # str
        self.source_user_created_at = tweet.user.created_at.strftime(
            '%m/%d/%Y')  # str
        self.source_user_followers_count = tweet.user.followers_count  # int
        self.source_user_friends_count = tweet.user.friends_count  # int
        self.source_user_listed_count = tweet.user.listed_count  # int
        self.source_user_favorites_count = tweet.user.favourites_count  # int
        self.source_user_statuses_count = tweet.user.statuses_count  # int
        # self.source_user_utc_offset = tweet.user.utc_offset # TODO
        # self.source_user_time_zone = tweet.user.time_zone # TODO
        try:
            self.source_user_geo_enabled = tweet.user.geo_enabled  # bool
        except:
            self.source_user_geo_enabled = False
        self.source_user_verified = tweet.user.verified  # bool
        try:
            self.source_user_lang = tweet.user.lang  # str
        except:
            self.source_user_lang = " __na__ "
        try:
            self.source_user_contributors_enabled = tweet.user.contributors_enabled  # bool
        except:
            self.source_user_contributors_enabled = False
        self.source_user_is_translator = tweet.user.is_translator  # bool
        try:
            self.source_user_is_translation_enabled = tweet.user.user_is_translation_enabled  # bool
        except:
            self.source_user_is_translation_enabled = False
        self.source_user_profile_background_color = tweet.user.profile_background_color  # str
        self.source_user_profile_image_url_https = tweet.user.profile_image_url_https  # str
        self.source_user_default_profile = tweet.user.default_profile  # bool
        try:
            self.source_possibly_sensitive = tweet.possibly_sensitive  # bool
        except:
            self.source_possibly_sensitive = False
        try:
            self.source_possibly_sensitive_appealable = tweet.possibly_sensitive_appealable  # bool
        except:
            self.source_possibly_sensitive_appealable = False
        # try: TODO
        #   self.source_place = tweet.place
        # except:
        #   self.source_place = " __na__ "
        try:  # str
            self.source_quoted_status_id = str(tweet.quoted_status_id)
        except:
            self.source_quoted_status_id = " __na__ "
        try:  # int
            self.source_quote_count = tweet.quote_count
        except:
            self.source_quote_count = 0
        try:  # int
            self.source_reply_count = tweet.reply_count
        except:
            self.source_reply_count = 0
        self.source_favorite_count = tweet.favorite_count  # int
        self.source_retweet_count = tweet.retweet_count  # int
        self.source_favorited = tweet.favorited  # bool
        self.source_retweeted = tweet.retweeted  # bool
        self.source_lang = tweet.lang  # str
        self.source_hashtags = []
        self.source_hyperlinks = []
        self.source_relevance = 0
        self.source_search_id = self.source_id + "-" + \
            datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")

        for i in self.source_text.split(' '):
            if len(i) > 1 and i[0] == "#":
                self.source_hashtags.append(i)
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, self.source_text)
        for j in url:
            self.source_hyperlinks.append(j[0])


# Using the arguments provided, this function querys the tweepy API and returns a list of tweet variables
def twitter_search(args):

    sd = args['start_date']
    if 'end_date' in args:
        ed = args['end_date']
    primary = args['primary']
    secondary = args['secondary']

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

    # twitter query system is quite flexible, in the future we could add more params for more targeted searches
    search_query = " ".join(primary) + " (" + " OR ".join(secondary) + ")"

    tweets = tw.Cursor(api.search_full_archive,
                       label="dev",  # might need to change later
                       query=search_query,
                       fromDate=sd,
                       toDate=ed).items(n)

    return tweets


# The function called by the cdsw model, takes in arguments to search for tweets and returns a json
# with the urls, text content, and relevancy based on tertiary words
def get_tweets(args):

    tertiary = args['tertiary']

    tweets = twitter_search(args)

    # ret = []

    for tweet in tweets:
        tweet_link = "https://twitter.com/{}/status/{}".format(
            tweet.user.screen_name, tweet.id)
        req = requests.get(tweet_link)
        html = req.text
        tmp = SourceType3(tweet, html)

        for j in tertiary:  # Increases relevancy based on the appearance of tertiary words
            if j.lower() in tmp.source_text.lower():
                tmp.source_relevance += 1

        data['tweets'].append({  # Add the scraped data as a dictionary to be converted to json
            'relevance': tmp.source_relevance,
            'url': tmp.source_url,
            'text': tmp.source_text
        })

    temp_data = data.copy()
    data['tweets'] = []

    return temp_data


# Use the main method to test argument input. This is not run during model calls
if __name__ == '__main__':

    args = {
        "start_date": "202109150000",
        "end_date": "202109180000",
        "primary": "russia",
        "secondary": ["africa"],
        "tertiary": ["education"]

    }

    print(get_tweets(args))

    pass
