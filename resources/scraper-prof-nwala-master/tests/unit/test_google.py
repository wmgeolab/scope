import unittest
from os.path import dirname, abspath, exists
from scraper.Google import googleSearch
from scraper.config import __installpath__

class TestGoogle(unittest.TestCase):
    
    global_serp = {}
    def test_basic_search(self):
        query = 'weather'
        serp = googleSearch(query)
        TestGoogle.global_serp = serp

        self.assertTrue( 'links' in serp, 'links not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['links']), 0, "serp['links'].len = 0" )

        self.assertTrue( 'extra_params' in serp, 'extra_params not in serp, keys: ' + str(serp.keys()) )
        self.assertTrue( 'page_dets' in serp['extra_params'], "page_dets not in serp['extra_params'], keys: " + str(serp['extra_params'].keys()) )
        self.assertTrue( 'result_count' in serp['extra_params']['page_dets'], "result_count not in serp['extra_params']['page_dets'], keys: " + str(serp['extra_params']['page_dets'].keys()) )
        self.assertGreater( serp['extra_params']['page_dets']['result_count'], -1, 'result_count = -1' )
    
    def test_related_questions_and_queries(self):
        query = 'president of the united states'
        serp = googleSearch(query)

        self.assertTrue( 'extra_params' in serp, 'extra_params not in serp, keys: ' + str(serp.keys()) )
        self.assertTrue( 'page_dets' in serp['extra_params'], "page_dets not in serp['extra_params'], keys: " + str(serp['extra_params'].keys()) )
        self.assertTrue( 'related_questions' in serp['extra_params']['page_dets'], "related_questions not in serp['extra_params']['page_dets'], keys: " + str(serp['extra_params']['page_dets'].keys()) )
    
        self.assertGreater( len(serp['extra_params']['page_dets']['related_questions']), 0, 'related_questions.len = 0' )
        self.assertGreater( len(serp['extra_params']['page_dets']['related_queries']), 0, 'related_queries.len = 0' )   

    def test_news_search(self):
        query = 'congress'
        serp = googleSearch(query, newsVertical=True)

        self.assertTrue( 'links' in serp, 'links not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['links']), 0, "serp['links'].len = 0" ) 

    def test_pagination_max_page(self):
        query = 'news'
        serp_page_1 = googleSearch(query, maxPage=1)
        serp_page_2 = googleSearch(query, maxPage=2)

        self.assertTrue( 'links' in serp_page_1, 'links not in serp_page_1, keys: ' + str(serp_page_1.keys()) )
        self.assertTrue( 'links' in serp_page_2, 'links not in serp_page_2, keys: ' + str(serp_page_2.keys()) )
        
        self.assertGreater( len(serp_page_1['links']), 0, "serp_page_1.len = 0" )
        self.assertGreaterEqual( len(serp_page_2['links']), len(serp_page_1['links']), "serp_page_2.len < serp_page_1" )
     
    def test_finding_uri(self):
        query = 'facebook'
        params = { 'find_uri_key': 'https://www.facebook.com/' }
        serp = googleSearch(query, extraParams=params)
        
        self.assertTrue( 'extra_params' in serp, 'extra_params not in serp, keys: ' + str(serp.keys()) )
        self.assertTrue( 'page_dets' in serp['extra_params'], "page_dets not in serp['extra_params'], keys: " + str(serp['extra_params'].keys()) )
        self.assertTrue( 'uri_key_found_indx' in serp['extra_params']['page_dets'], "uri_key_found_indx not in serp['extra_params']['page_dets'], keys: " + str(serp['extra_params']['page_dets'].keys()) )
        self.assertGreater( serp['extra_params']['page_dets']['uri_key_found_indx'], -1, 'uri key not found: ' + params['find_uri_key'] )
    
    def test_files_scraper(self):

        p = __installpath__ + 'GoogleSampleSerps/'
        queries = [
            [p + 'ebola_1.html'],
            [p + 'ebola_1.html', p + 'ebola_2.html'],
            [p],
        ]

        for query in queries:

            params = { 'files': True }
            serp = googleSearch(query, extraParams=params)

            self.assertTrue( 'serps' in serp, 'serps not in serp, keys: ' + str(serp.keys()) )
            self.assertGreater( len(serp['serps']), 0, "serp['serps'] = 0" )
            
            for i in range( len(serp['serps']) ):
                self.assertTrue( 'links' in serp['serps'][i], "links not in serp['serps'], keys: " + str(serp['serps'][i].keys()) )
                self.assertGreater( len(serp['serps'][i]['links']), 0, "serp['serps'][i]['links'].len = 0" )
    
    def test_directives(self):
        query = 'ebola'
        params = { 'directives': 'site:cdc.gov' }
        serp = googleSearch(query, extraParams=params)

        self.assertTrue( 'links' in serp, 'links not in serp, keys: ' + str(serp.keys()) )
        self.assertGreater( len(serp['links']), 0, "serp['links'].len = 0" )

if __name__ == '__main__':
    unittest.main()