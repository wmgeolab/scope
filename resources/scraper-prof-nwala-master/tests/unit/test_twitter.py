import os
import unittest

from os.path import dirname, abspath
from subprocess import check_output

from scraper.ScraperUtil import getChromedriver
from scraper.ScraperUtil import getDictFromJsonGZ

from scraper.Twitter import twitterSearch

#ChromedriverPath = '/usr/local/bin/chromedriver'
ChromedriverPath = None
CurPath = dirname(abspath(__file__)) + '/'
extraParams = {'driver': getChromedriver(ChromedriverPath), 'leave_browser_open': True}

class TestTwitter(unittest.TestCase):
    
    def test_basic_search(self):
        query = 'congress'
        serp = twitterSearch(
            chromedriverPath=ChromedriverPath, 
            query=query,
            maxTweetCount=20,
            extraParams=extraParams
        )

        self.assertTrue( 'tweets' in serp, 'tweets not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['tweets']), 0, "serp['tweets'].len = 0" )

    def test_latest_search(self):
        query = 'congress'
        serp = twitterSearch(
            chromedriverPath=ChromedriverPath, 
            query=query,
            maxTweetCount=20,
            latestVertical=True,
            extraParams=extraParams
        )

        self.assertTrue( 'tweets' in serp, 'tweets not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['tweets']), 0, "serp['tweets'].len = 0" )
    
    def test_extract_twts_frm_uri(self):
        query = 'https://twitter.com/storygraphbot/status/1079917816642457600'
        serp = twitterSearch(
            chromedriverPath=ChromedriverPath, 
            query=query,
            extraParams=extraParams
        )

        self.assertTrue( 'tweets' in serp, 'tweets not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['tweets']), 0, "serp['tweets'].len = 0" )
    
    def test_cache_write(self):
        query = 'https://twitter.com/storygraphbot/status/1079917816642457600'
        newParams = {
            'cache': {
                'cache_path': CurPath + 'TweetsCache/',
                'cache_write': True,
                'driver': extraParams['driver'],
                'leave_browser_open': True
            }
        }

        serp = twitterSearch(
            chromedriverPath=ChromedriverPath, 
            query=query,
            extraParams=newParams
        )

        self.assertTrue( 'tweets' in serp, 'tweets not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['tweets']), 0, "serp['tweets'].len = 0" )
        
        tweets = os.listdir( CurPath + 'TweetsCache/' )
        self.assertGreater( len(tweets), 0, "tweets.len = 0" )

    def test_search_with_uri(self):        
        #extract tweets with uri, NOT search for tweet with URI
        extraParams = {
            'search_uri_key': 'https://www.cnn.com/2020/01/08/politics/ruth-bader-ginsburg-civil-procedure/index.html'
        }
        serp = twitterSearch(
            chromedriverPath=ChromedriverPath, 
            maxTweetCount=30,
            extraParams=extraParams
        )

        self.assertTrue( 'tweets' in serp, 'tweets not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['tweets']), 0, "serp['tweets'].len = 0" )
    
if __name__ == '__main__':
    unittest.main()
    check_output(['rm', '-rf', CurPath + 'TweetsCache/'])