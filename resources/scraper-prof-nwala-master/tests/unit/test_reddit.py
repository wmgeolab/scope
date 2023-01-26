import unittest

from scraper.Reddit import redditSearch
from scraper.ScraperUtil import dumpJsonToFile

class TestGoogle(unittest.TestCase):

    def test_basic_search(self):
        query = 'politics'
        serp = redditSearch(query)

        self.assertTrue( 'posts' in serp, 'posts not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['posts']), 0, "serp['posts'].len = 0" )

    def test_pagination_max_page(self):
        query = 'politics'
        serp_page_1 = redditSearch(query, maxPage=1)
        serp_page_2 = redditSearch(query, maxPage=2)

        self.assertTrue( 'posts' in serp_page_1, 'posts not in serp_page_1, keys: ' + str(serp_page_1.keys()) )
        self.assertTrue( 'posts' in serp_page_2, 'posts not in serp_page_2, keys: ' + str(serp_page_2.keys()) )
        
        self.assertGreater( len(serp_page_1['posts']), 0, "serp_page_1.len = 0" )
        self.assertGreaterEqual( len(serp_page_2['posts']), len(serp_page_1['posts']), "serp_page_2.len < serp_page_1" )
    
    def test_subreddit_search(self):
        query = 'politics'
        serp = redditSearch(query, subreddit=query)

        self.assertTrue( 'posts' in serp, 'posts not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['posts']), 0, "serp['posts'].len = 0" )

    def test_sort(self):
        query = 'politics'
        extraParams = {'sort': 'comments'}
        serp = redditSearch(query, extraParams=extraParams)

        self.assertTrue( 'posts' in serp, 'posts not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['posts']), 0, "serp['posts'].len = 0" )

    
if __name__ == '__main__':
    unittest.main()