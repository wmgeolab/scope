import argparse
import json
import logging
import os
import re
import time

from os.path import abspath
from bs4 import BeautifulSoup
from datetime import datetime
from os.path import dirname
from urllib.parse import parse_qs
from urllib.parse import quote
from random import randint
from urllib.parse import urlparse

logger = logging.getLogger('scraper.scraper')

#services for others - start
def getSubjectExpertQPDets(domain, query):

    domain = domain.strip()
    query = query.strip()

    params = {'directives': 'site:' + domain}
    serp = googleSearch(query=query, extraParams=params)

    if( 'extra_params' in serp ):
        if( 'page_dets' in serp['extra_params'] ):
            if( 'result_count' in serp['extra_params']['page_dets'] ):
                return serp['extra_params']['page_dets']['result_count']

    return 0

def second_try_find(link, title, serp_links):
    
    title = title.strip()
    title_set = set(title.split(' '))
    res = {
        'uri_key_found_indx': -1,
        'write_cache': False,
        'jaccard_sim': {'score': -1, 'dets': {}},
        'match_reason': {'description': '', 'uri': ''}
    }

    domain = getDomain(link)
    if( domain == 'twitter.com' ):
        return res

    for i in range( len(serp_links) ):

        cand_domain = getDomain( serp_links[i]['link'] )
        if( domain != cand_domain ):
            #print('\t\t\tdomain MISMATCH:', domain, 'vs', cand_domain, serp_links[i]['link'] )
            continue

        if( 'new_title' in serp_links[i] ):
            cand_title = serp_links[i]['new_title']
        else:
            html = derefURI( serp_links[i]['link'], 0 )
            
            serp_links[i]['new_title'] = extractPageTitleFromHTML(html)
            cand_title = serp_links[i]['new_title'].strip()
            res['write_cache'] = True
        
        #print('\t\t\t domain MATCH, check title vs cand_title')
        #print('\t\t\tcand_link:', serp_links[i]['link'])
        #print('\t\t\tcand_title:', cand_title)

        if( title == cand_title ):

            res['uri_key_found_indx'] = i
            res['match_reason']['description'] = 'exact title match'
            res['match_reason']['uri'] =  serp_links[i]['link']

            #print('\t\t\tHIT 0')
            #print()
            break
        
        cand_title_set = set(cand_title.split(' '))
        res['jaccard_sim']['score'] = jaccardFor2Sets(title_set, cand_title_set)
        res['jaccard_sim']['dets'] = {'uri': serp_links[i]['link'], 'title': cand_title}

        if( res['jaccard_sim']['score'] > 0.8 ):

            res['uri_key_found_indx'] = i
            res['match_reason']['description'] = 'jaccard_sim > 0.8'
            res['match_reason']['uri'] =  serp_links[i]['link']

            #print('\t\t\tHIT 1')
            #print()
            break

    return res

def get_query_set(uri, ngram_range=(2, 5), max_query_per_ngram=10):

    exp_uri = expandUrl(uri)
    html = derefURI( exp_uri, 0 )

    if( html == '' ):
        return {}

    pg_title = extractPageTitleFromHTML(html)
    if( pg_title == '' ):
        return {}


    queries = []
    ngram_stats = {}
    
    ngrams = DocVect.getNgram( [pg_title], ngramRange=ngram_range )
    queries.append({ 'query': pg_title, 'is_title': True, 'ngram': len(pg_title.split(' ')) })

    for ngram in ngrams:
        
        ngram = ngram.strip()
        if( ngram != '' ):
            
            n = len(ngram.split(' '))
            ngram_stats.setdefault(n, 0)
            ngram_stats[n] += 1
            
            if( ngram_stats[n] <= max_query_per_ngram ):
                queries.append({ 'query': ngram, 'ngram': n })
    
    if( exp_uri == uri ):
        exp_uri = None
    
    return {
        'uri': uri,
        'title': pg_title,
        'queries': queries,
        'expanded_uri': exp_uri
    }

def get_serp(query, max_page, find_uri_key, cache_outfile):

    extra_params = { 'find_uri_key': find_uri_key }
    
    if( os.path.exists(cache_outfile) == False ):
        serp = googleSearch(query=query, maxPage=max_page, extraParams=extra_params)
        write_cache = True
    else:
        serp = getDictFromJsonGZ(cache_outfile)
        write_cache = False

    return serp, write_cache

def get_uri_retrv(uri, max_query_per_ngram=10, min_ngram=2, max_ngram=5, max_page=2, no_second_try=False, stop_if_title_not_found=False, serp_cache_path=''):
    
    uri_query_set = get_query_set(uri, max_query_per_ngram=max_query_per_ngram, ngram_range=(min_ngram, max_ngram))
    
    if( 'queries' not in uri_query_set ):
        return {}

    query_size = len( uri_query_set['queries'] )
    uri_query_set.setdefault('scores', {'ret': 0, 'mrr': 0})
    uri_query_set['captcha_on'] = False

    if( serp_cache_path != '' ):
        os.makedirs( serp_cache_path, exist_ok=True )

    for j in range( query_size ):
        
        #init variables - start
        write_cache = False
        cache_outfile = ''
        uri_key_found_indx = -1
        
        query = uri_query_set['queries'][j]
        query['result_count'] = -1

        #uri_query_set['queries'][j]['result_count'] = -1
        #query = uri_query_set['queries'][j]['query'].strip()
        
        if( uri_query_set['expanded_uri'] is None ):
            find_uri_key = uri_query_set['uri']
        else:
            find_uri_key = uri_query_set['expanded_uri']
        #init variables - end


        if( serp_cache_path != '' ):
            cache_outfile = serp_cache_path + getStrHash( query['query'] + str(max_page) ) + '.json.gz'
            query['cache_outfile'] = cache_outfile

        serp, write_cache = get_serp( query['query'], max_page, find_uri_key, cache_outfile )
        if( 'extra_params' in serp ):
            uri_key_found_indx = serp['extra_params']['page_dets']['uri_key_found_indx']
            query['result_count'] = serp['extra_params']['page_dets']['result_count']


        logger.info('\tq: ' + str(j) + ' of ' + str(query_size) + ' q: ' +  query['query'])
        logger.info('\turi_key_found_indx: ' + str(uri_key_found_indx))
        
        if( uri_key_found_indx < 0 and no_second_try is False):
            
            logger.info('\tsecond try attempt to find uri')
            res = second_try_find( find_uri_key, uri_query_set['title'], serp['links'] )
            
            if( write_cache is False  ):
                #opportunity to write cache only if write_cache was OFF, it it was True
                write_cache = res['write_cache']

            uri_key_found_indx = res['uri_key_found_indx']
            query['jaccard_sim'] = res['jaccard_sim']
            
            if( res['match_reason']['uri'] != '' ):
                query['match_reason'] = res['match_reason']


        logger.info('')
        if( write_cache and cache_outfile != '' ):
            gzipTextFile(cache_outfile, json.dumps(serp, ensure_ascii=False))

        if( uri_key_found_indx < 0 ):
            #NOT FOUND, possibly even after second try
            query['found'] = {}
        else:
            #FOUND
            find = serp['links'][uri_key_found_indx]
            query['found'] = { 'page': find['page'], 'rank': find['rank'], 'rr': 1/find['rank']}
            uri_query_set['scores']['ret'] += 1
            uri_query_set['scores']['mrr'] += query['found']['rr']


        if( 'extra_params' in serp ):
            if( serp['extra_params']['page_dets']['captcha_on'] ):
                uri_query_set['captcha_on'] = True
                logger.info('\tCAPTCHA FLAG ON - BREAKING')
                break

        if( stop_if_title_not_found is True and 'is_title' in query and len(query['found']) == 0 ):
            logger.info('\tNOT CONTINUING RETRV BECAUSE TITLE QUERY NOT FOUND, BREAKING')
            break

    uri_query_set['query_count'] = query_size
    if( query_size == 0 ):
        uri_query_set['scores']['mrr'] = 0
        uri_query_set['scores']['rt'] = 0
    else:
        uri_query_set['scores']['mrr'] = uri_query_set['scores']['mrr']/query_size
        uri_query_set['scores']['rt'] = uri_query_set['scores']['ret']/query_size


    return uri_query_set
#services for others - end

def workingFolder():
    return dirname(abspath(__file__)) + '/'

def getQueryReciprocalRank(query, expectedLink, maxPage=3, seleniumFlag=False):
    
    logger.info('\ngetQueryReciprocalRank() - start')

    query = query.strip()
    expectedLink = expectedLink.strip()

    if( len(query) == 0 or len(expectedLink) == 0 ):
        return 0

    allLinksCount = 0
    try:
        for page in range(1, maxPage+1):
            logger.info('\tpage: ' + str(page) + ' of ' + str(maxPage))
            logger.info('\tquery: ' + query)
            logger.info('\texpectedLink: ' + expectedLink)
            
            googleHTMLPage = googleGetHTMLPage(searchString=query, page=page, seleniumFlag=seleniumFlag)
            soup = BeautifulSoup( googleHTMLPage['html'], 'html.parser' )
            linksDict = googleRetrieveLinksFromPage(soup)
            
            sortedKeys = sorted(linksDict, key=lambda x:linksDict[x]['rank'])
            for link in sortedKeys:
                
                allLinksCount += 1
                #print('\t\t', allLinksCount, link)
                
                if( link.find(expectedLink) == 0 ):
                    
                    RR = 1/allLinksCount
                    
                    logger.info('\tFound')
                    logger.info('\tallLinksCount: ' + str(allLinksCount))
                    logger.info('\tRR: ' +  RR)
                    return RR

            if( len(linksDict) == 0 ):
                logger.info('\tEmpty result, terminating')
                return 0
    except:
        genericErrorInfo()

    return 0
    logger.info('\ngetQueryReciprocalRank() - end')

def constructSearchURI(searchString, page, directives='', vertical=''):
    
    searchString = searchString.strip()
    directives = directives.strip()

    if( searchString == '' and directives == '' ):
        return payload

    if( searchString != '' and directives != '' ):
        directives = '%20' + directives
    
    searchQueryFragment = 'as_q=' + quote(searchString) + directives
    vrtMap = getVrtMap()
    vrtMap = {v: k for k, v in vrtMap.items()}

    if( page > 1 ):
        #to yield https://www.google.com/search?as_q=myQuery#q=myQuery&start=10 (for page 1)
        #anomaly - start
        #for reasons unknown, this block always got the first page
        #queryFragment = '#q=' + queryFragment
        #searchQueryFragment = searchQueryFragment + queryFragment + '&start=' + str((page-1) * 10)
        #anomaly - end

        searchQueryFragment = searchQueryFragment + '&start=' + str((page-1) * 10)
    
    if ( vertical in vrtMap ):
        vertical = '&tbm=' + vrtMap[vertical]

    if( vertical == 'all' ):
        vertical = ''

    searchQuery = 'https://www.google.com/search?' + searchQueryFragment + vertical

    return searchQuery

def googleGetHTMLPage(searchString, page, directives='', extraParams=None):

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('news', False)
    extraParams.setdefault('leave_browser_open', True)
    extraParams.setdefault('mimic_human_search', False)
    extraParams.setdefault('chromedriver_path', '')

    if( 'rand_sleep_range' in extraParams ):
        if( len(extraParams['rand_sleep_range']) == 2 ):
            extraParams['sleep_sec'] = randint( extraParams['rand_sleep_range'][0], extraParams['rand_sleep_range'][1] )


    extraParams.setdefault('sleep_sec', 1)
    payload = {'html': '', 'self': ''}
    
    if( extraParams['news'] is True ):
        searchQuery = constructSearchURI(searchString, page, directives=directives, vertical='news')
    else:
        searchQuery = constructSearchURI(searchString, page, directives=directives, vertical='')

    logger.info('\tsearchQuery: ' + searchQuery)
    
    payload['html'] = derefURI(searchQuery, sleepSec=extraParams['sleep_sec'], extraParams=extraParams)
    payload['self'] = searchQuery

    return payload

def getPayloadDetails(title, datetime, snippet, rank, page, custom=None):
    
    if( custom is None ):
        custom = {}

    return {
        'title': title, 
        'date': datetime, 
        'snippet': snippet, 
        'rank': rank,
        'page': page,
        'custom': custom
    }

def getLinkCustom(linkType='', dateAutoGen=False):
    return {'link_class': linkType, 'date_auto_gen': dateAutoGen, 'children': []}

def getSnptDate(resultInstance):
    
    returnObj = {'snippet': '', 'date': '', 'date_auto_gen': False}
    snippet = None

    #method1 - start
    for possibleTag in ['span', 'div']:
        for possibleClass in ['st', 'aCOpRe', 'hgKElc']:

            snippet = resultInstance.find(possibleTag, {'class': possibleClass})
            if( snippet is not None ):
                if( snippet.text.strip() != '' ):

                    returnObj['snippet'] = snippet.text.strip()
                    returnObj['snippet_class'] = possibleClass
                    break

        if( returnObj['snippet'] != '' ):
            break
    #method1 - end
    

    #method2 - start
    possibleSnippet = resultInstance.findAll('span')
    for p in possibleSnippet:
        
        #snippet likely has em tags and/or elipses
        if( p.find('em') is not None or p.text.find('...') > -1 ):
            
            #replace method1's snippet only if longer snippet found
            if( len(p.text.strip()) > len(returnObj['snippet']) ):
            
                snippet = p
                returnObj['snippet'] = snippet.text.strip()
                break
    #method2 - end
    
    
    if( snippet is None ):
        date = None
    else:
        date = snippet.find(class_='f')

    if( date is None ):
    
        #news serp, where date is NOT inside snippet
        d = resultInstance.find(class_='f')
        if( d is not None ):
            returnObj['date'] = d.text
        
    else:
        #general serp, where date is inside snippet
        returnObj['date'] = date.text

    returnObj['snippet'] = returnObj['snippet'].replace(returnObj['date'], '')
    returnObj['date'] = returnObj['date'].replace('-', '').strip()
    returnObj['date'], returnObj['date_auto_gen'] = formatDate( returnObj['date'] )

    return returnObj

def formatDate(dateStr):

    expectedDateFormat = '%b %d, %Y'
    try:
        datetime.strptime(dateStr, expectedDateFormat)
        return dateStr, False
    except:
        return datetime.now().strftime('%b %d, %Y'), True

def getTitleLink(resultInstance):

    payload = {'title': '', 'link': ''}
    explanation = ''
    
    h3 = resultInstance.find('h3')
    if( h3 is None ):
        #no need to attempt finding link in the absence of h3 tag
        return payload, 'No H3 tag'

    payload['title'] = h3.text
    
    link = resultInstance.find('a')
    if( link is None ):
        explanation = 'Parent has no Anchor tag'
    else:
    
        if( link.has_attr('data-href') ):
            payload['link'] = link['data-href'].strip()
        elif( link.has_attr('href') ):
            payload['link'] = link['href'].strip()
        else:
            explanation = "Anchor tag missing attrs 'data-href' or 'href'"


    if( payload['link'].startswith('/') or payload['link'] == '#' or payload['link'].startswith('https://www.google.com/search') ):
        explanation = "Google link: '" + payload['link'] + "'"
        payload['link'] = ''
        
    return payload, explanation

def addChildLinks(parentLink, elm, page, payload, allChildren):
    
    moreLinks = elm.findAll('a')
    for moreLink in moreLinks:

        link = ''
        if( moreLink.has_attr('data-href') ):
            link = moreLink['data-href'].strip()
        elif( moreLink.has_attr('href') ):
            link = moreLink['href'].strip()

        
        if( link == '' or link.startswith('/') ):
            continue
        
        if( link.find('googleusercontent.com') != -1 ):
            #skip request google links
            continue
        
        title = moreLink.text.strip()
        if( link == parentLink or title == '' or link.find('http') != 0 ):
            continue
    
        allChildren.add(link)
        linkDct = getPayloadDetails(
            title=title, 
            datetime=datetime.now().strftime('%b %d, %Y'),
            snippet='', 
            rank=-1,
            page=page,
            custom=getLinkCustom('main_blue_link_child', True)
        )
        linkDct['link'] = link
        payload.append(linkDct)

def getAllNonChildLinks(elm, page, parents, allChildren):

    linksLst = []
    dedupSet = set()
    explanation = ''
    links = elm.findAll('a')

    if( len(links) == 0 ):
        explanation = 'Parent has no Anchor tags'

    for i in range(len(links)):

        link = links[i]
        domain = ''
        title = link.text.strip()

        if( link.has_attr('data-href') ):
            link = link['data-href'].strip()
        elif( link.has_attr('href') ):
            link = link['href'].strip()
        else:
            link = ''
            explanation += '\n' + str(i) + ". Anchor tags missing attrs 'data-href' or 'href'"


        if( link == '' ):
            continue

        if( link.startswith('/') ):
            explanation += '\n' + str(i) + ". Google link: '" + link + "'"
            continue

        if( link.find('googleusercontent.com') != -1 ):
            explanation += '\n' + str(i) + ". googleusercontent.com link: '" + link + "'"
            continue

        if( title == '' ):
            explanation += '\n' + str(i) + ". Link without anchor text, link: '" + link + "'"
            continue

        if( link.find('://') == -1 ):
            explanation += '\n' + str(i) + ". Link has no scheme, link: '" + link + "'"
            continue

        if( link.startswith('https://www.google.com/search') ):
            explanation += '\n' + str(i) + ". www.google.com/search link: '" + link + "'"
            continue

        if( link in dedupSet ):
            continue

        #special case: where a link in child is also a parent - add link
        #standard case: where a link in child NOT a parent - don't add link
        if( link in allChildren and link not in parents ):
            continue
        
        
        #good link from here
        explanation = ''
        lnkDct = getPayloadDetails(
                title=title, 
                datetime=datetime.now().strftime('%b %d, %Y'), 
                snippet='', 
                rank=0,
                page=page,
                custom = getLinkCustom('extra', True)
            )
        lnkDct['link'] = link

        dedupSet.add(link)
        linksLst.append(lnkDct)
    
    if( explanation != '' ):
        explanation = explanation + '. Link count: ' + str(len(links))

    return linksLst, explanation

def getVrtMap():
    return {
        'nws': 'news',
        'isch': 'images',
        'vid': 'videos',
        'bks': 'books',
        'shop': 'shopping',
        'fin': 'finance'
    }

def sniffSerpPage(googleHTMLSoup):

    resultStats = getGoogleSrchResCount(googleHTMLSoup)
    
    if( resultStats['src_text'] == '' ):
        logger.warning('\nsniffSerpPage(): resultStats["src_text"] is blank, review getGoogleSrchResCount()\'s scraper')
        return -1
    '''
        Sample resultStats for Page 1 - about 53,900,000 results (0.58 seconds)
        Sample resultStats for Page 2 - Page 2 of about 53,900,000 results (0.49 seconds) 
    '''
    resultStats = resultStats['src_text'].lower()
    page = re.search('page(\s+)(\d+)', resultStats)

    if( page is None ):
        page = 1
    else:
        try:
            page = int( page.group(2) )
        except:
            logger.warning('\nsniffSerpPage(): error parsing int: ' + str(page))
            page = -1
    
    return page

def sniffSerpVertical(googleHTMLSoup):
    
    links = googleHTMLSoup.find_all('a')
    vrt = 'all'
    vrtMaps = getVrtMap()

    for link in links:

        if( link.has_attr('href') is False ):
            continue

        link = link['href'].strip()
        if( link.find('/search') == -1 ):
            continue

        if( link.find('start=') == -1 ):
            continue

        #first navigation link
        tbm = link.split('tbm=')
        if( len(tbm) > 1 ):
            vrt = tbm[1].split('&')[0]
        
        break

    if( vrt in vrtMaps ):
        return vrtMaps[vrt]
    else:
        return vrt

def sniffSerpQuery(googleHTMLSoup):

    inputs = googleHTMLSoup.find_all('input')
    firstChoice = ''
    secondChoice = ''
    for inp in inputs:
        
        if( inp.has_attr('type') is False or inp.has_attr('value') is False ):
            continue

        if( inp['type'] != 'text' ):
            continue

        if( inp.has_attr('name') is True ):
            if( inp['name'] == 'q' ):
                firstChoice = inp['value']
        
        secondChoice = inp['value']

    if( firstChoice == '' ):
        return secondChoice
    else:
        return firstChoice

def rankSensitiveGetLnksFrmPage(googleHTMLSoup, rankAdditiveFactor=0, page=1, extraParams=None):

    logger.debug('\nrankSensitiveGetLnksFrmPage()')
    '''
        References
        2020-08-25: https://web.archive.org/web/20200825002736/https://www.google.com/search?q=news
        2021-05-26: https://web.archive.org/web/20210526033303/https://www.google.com/search?q=news
    '''
    if( len(googleHTMLSoup) ==  0 ):
        return {}, {}

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('news', False)
    extraParams.setdefault('sniff_serp', False)
    sniffed_info = {}

    if( extraParams['sniff_serp'] is True ):
        
        sniffed_info['page'] = sniffSerpPage(googleHTMLSoup)
        sniffed_info['vertical'] = sniffSerpVertical(googleHTMLSoup)
        sniffed_info['query'] = sniffSerpQuery(googleHTMLSoup)

        if( sniffed_info['page'] > 0 ):
            page = sniffed_info['page']

        if( sniffed_info['vertical'] == 'news' ):
            extraParams['news'] = True


    #lnksDct format: {link, [datetime|nowDatetime]}
    lnksDct = {}
    results = []
    morePgDets = {
        'result_count': -1,
        'scraping_report': {},
        'sniffed_info': sniffed_info,
        'related_questions': getPeopleAlsoAsk(googleHTMLSoup),
        'related_queries': getRelatedQueries(googleHTMLSoup),
        'captcha_on': isCaptchaPage(googleHTMLSoup)
    }
    if( page == 1 ):
        morePgDets['result_count'] = getGoogleSrchResCount(googleHTMLSoup)['page']


    allChildren = set()

    for possibleClasses in ['med', 'srg', 'eqAnXb']:
        #possibleClasses these are the main divs that hold all the links in the SERP excluding the right panel
        results = googleHTMLSoup.findAll('div', {'class': possibleClasses})
        if( len(results) == 0 ):
            logger.debug(f'\tpossibleClasses: {possibleClasses} NOT found')
        else:
            #serp_marker 0
            morePgDets['scraping_report'] = {'tag': 'div', 'class': possibleClasses, 'children': [], 'count': len(results), 'misc': {}}
            break

    if( extraParams['news'] is True ):
        return googleNewsScraper(results, morePgDets, rankAdditiveFactor, page), morePgDets

    for result in results:
        #there are possibly empty result, indx 1 usually has the links

        liOrDiv = result.findAll('li', {'class': 'g'})
        
        if( len(liOrDiv) == 0 ):
            liOrDiv = result.findAll('div', {'class': 'g'})
            morePgDets['scraping_report']['children'].append({ 'tag': 'div', 'class': 'g', 'count': len(liOrDiv), 'children': [], 'messages': [] })
        else:
            morePgDets['scraping_report']['children'].append({ 'tag': 'li', 'class': 'g', 'count': len(liOrDiv), 'children': [], 'messages': [] })

        for resultInstance in liOrDiv:
            
            titleLink, explanation = getTitleLink(resultInstance)
            snippetDate = getSnptDate(resultInstance)
            explanation += '. Snippet: ' + snippetDate['snippet']
            
            link = titleLink['link'].strip()
            if( link == '' ):
                
                morePgDets['scraping_report']['children'][-1]['children'].append({ 
                    'status': 'getTitleLink() returned empty because: ' + explanation 
                })

            else:
                lnksDct[link] = getPayloadDetails(
                    title=titleLink['title'], 
                    datetime=snippetDate['date'], 
                    snippet=snippetDate['snippet'], 
                    rank=rankAdditiveFactor,#not actual rank
                    page=page,
                    custom = getLinkCustom('main_blue_link')
                )

                #attempt to get more links within block
                #addChildLinks extracts links without respecting structure of DOM, so parent link will be added, therefore avoid this
                addChildLinks(link, resultInstance, page, lnksDct[link]['custom']['children'], allChildren)

        #attempt to add even more links
        allNonChildLnks, explanation = getAllNonChildLinks(result, page, lnksDct, allChildren)
        
        if( len(allNonChildLnks) == 0 ):
            morePgDets['scraping_report']['children'][-1]['messages'].append('getAllNonChildLinks() returned empty because: ' + explanation)
        else:
            #use allNonChildLnks to determine ranks get extra details from lnksDct, 
            combineResults(allNonChildLnks, lnksDct)

    return lnksDct, morePgDets

def getPeopleAlsoAsk(pg):
    
    relatedQuestions = []
    for q in pg.find_all('div', {'class': 'related-question-pair'}):
        relatedQuestions.append( q.text.split('?')[0] + '?' )

    return relatedQuestions

def getRelatedQueries(pg):

    for opt in ['brs_col', 'AJLUJb']:
        brs_col = pg.findAll('div', {'class': opt})
        if( len(brs_col) != 0 ):
            break

    relatedQueries = []
    keyOpts = ['q', 'as_q']
    
    for col in brs_col:
        for link in col.findAll('a'):

            if( link.has_attr('href') == False ):
                continue

            queryComps = parse_qs( urlparse(link['href']).query )
            if( len(queryComps) == 0 ):
                continue

            for ky in keyOpts:
                if( ky in queryComps ):
                    relatedQueries += queryComps[ky]
                    break
                    
    return relatedQueries


def googleNewsScraper(results, morePgDets, rankAdditiveFactor=0, page=1):

    lnksDct = {}
    accessors = {
        'title': ['phYMDf', 'cJgcvb', 'JheGif', 'nDgy9d'],#phYMDf for card, cJgcvb for latest news
        'snippet': ['eYN3rb', 'Y3v8qd'],
        'date': 'hucR0d'
    }
    
    linkDets = {
        'title': '',
        'snippet': '',
        'date': ''
    }

    allChildren = set()
    for result in results:
        
        morePgDets['scraping_report']['children'].append({ 'tag': 'div', 'class': 'dbsr', 'count': len(result), 'children': [], 'misc': {} })
        tagsDct = {
            'div': {'class': 'dbsr'},
            'a': {'class': 'yQROm'}
        }

        for tag, classDct in tagsDct.items():
            for resultInstance in result.findAll(tag, classDct):

                if( tag == 'a' ):
                    link = resultInstance
                else:
                    link = resultInstance.find('a')


                if( link.has_attr('href') == False ):
                    morePgDets['scraping_report']['children'][-1]['children'].append({ 'status': "googleNewsScraper(): Anchor tag missing attr 'href'" })    
                    continue
                
                link = link['href'].strip()
                if( link == '' ):
                    morePgDets['scraping_report']['children'][-1]['children'].append({ 'status': "googleNewsScraper(): Anchor tag 'href' empty" })    
                    continue

                if( link.find('googleusercontent.com') != -1 ):
                    #skip request google links
                    morePgDets['scraping_report']['children'][-1]['children'].append({ 'status': "googleNewsScraper(): googleusercontent.com link: '" + link + "'" })
                    continue
                
                if( link.startswith('/') ):
                    morePgDets['scraping_report']['children'][-1]['children'].append({ 'status': "googleNewsScraper(): Google link: '" + link + "'" })    
                    continue

                for attr, clss in accessors.items():
                    
                    linkDets[attr] = resultInstance.find('div', {'class': clss})
                    if( linkDets[attr] is None ):
                        linkDets[attr] = ''
                    else:
                        linkDets[attr] = linkDets[attr].text

                linkDets['date'], dateAutoGen = formatDate( linkDets['date'] )
                lnksDct[link] = getPayloadDetails(
                    title=linkDets['title'], 
                    datetime=linkDets['date'], 
                    snippet=linkDets['snippet'], 
                    rank=rankAdditiveFactor,#not actual rank
                    page=page,
                    custom = getLinkCustom('main_blue_link', dateAutoGen=dateAutoGen)
                )

        allNonChildLnks, explanation = getAllNonChildLinks(result, page, lnksDct, allChildren)
        combineResults(allNonChildLnks, lnksDct)

    return lnksDct

def combineResults(allNonChildLnks, lnksDct):

    if( len(allNonChildLnks) == 0 or len(lnksDct) == 0 ):
        return

    for i in range(len(allNonChildLnks)):
        link = allNonChildLnks[i]['link']

        if( link not in lnksDct ):
            lnksDct[link] = allNonChildLnks[i]

        if( 'children' not in lnksDct[link]['custom'] ):
            continue
        
        if( 'children' not in lnksDct[link]['custom'] ):
            continue
            
        #previous rank is offset (rankAdditiveFactor)
        lnksDct[link]['rank'] = lnksDct[link]['rank'] + (i + 1)

        #flatten lnksDct by adding children to main list
        for j in range( len(lnksDct[link]['custom']['children']) ):
            
            child = lnksDct[link]['custom']['children'][j]

            child['rank'] = float( str(lnksDct[link]['rank']) + '.' + str((j+1)) )
            del child['custom']['children']

            if( child['link'] not in lnksDct ):
                lnksDct[ child['link'] ] = child

        #remove already added children
        del lnksDct[link]['custom']['children']

def markURIKey( pagePageLinksDict, mergedListOfLinks ):

    pagePageLinksDict['page_dets']['uri_key_found_indx'] = -1

    if( 'uri_key_found_indx' in pagePageLinksDict['page_dets'] ):

        if( pagePageLinksDict['page_dets']['uri_key_found_indx'] ):
            
            for i in range(len(mergedListOfLinks)):
                if( 'uri_key_flag' in mergedListOfLinks[i] ):
                    pagePageLinksDict['page_dets']['uri_key_found_indx'] = i
                    break
                    
                    
def googleSearch(query, maxPage=1, newsVertical=False, serps=None, extraParams=None):

    serp = {}
    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('files', False)
    extraParams.setdefault('max_file_depth', 1)

    if( extraParams['files'] is True ):
        
        serp['serps'] = []

        files = readTextFromFilesRecursive(query, addDetails=True, maxDepth=extraParams['max_file_depth'])
        querySerpClusters = clusterSerps(files)

        for queryKey, serps in querySerpClusters.items():
            
            singleSerp = googleSearchMain(
                serps['sniffed_info']['query'],
                maxPage=len( serps['pages'].keys() ),
                serps=serps, 
                extraParams=extraParams
            )

            singleSerp['sniffed_info'] = serps['sniffed_info']
            serp['serps'].append( singleSerp )
         
    else:
        
        if( isinstance(query, list) is True ):
            if( len(query) == 0 ):
                query = ''
            else:
                query = query[0]
        else:
            query = str(query)

        serp = googleSearchMain(
            query, 
            maxPage=maxPage, 
            newsVertical=newsVertical,
            extraParams=extraParams
        )

    return serp

def googleSearchMain(query, maxPage=1, newsVertical=False, serps=None, extraParams=None):

    logger.info('\ngoogleSearchMain():')

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('news', newsVertical)
    extraParams.setdefault('directives', '')
    extraParams.setdefault('no_interleave', False)
    extraParams.setdefault('find_uri_key', '')
    extraParams.setdefault('files', False)

    if( extraParams['no_interleave'] is False ):
        
        if( extraParams['directives'] != '' ):
        
            logger.info('\tdirectives ON, will switch on 1 interleave')
            extraParams['interleave_queries_params'] = {'count': 1}
        
        elif( maxPage > 2 ):
            
            logger.info('\tpagination > 2, will switch on 2 interleave')
            extraParams['interleave_queries_params'] = {'count': 2}
    
    if( serps is None ):
        pagePageLinksDict = googleGetSERPResults(
            query=query, 
            maxPage=maxPage, 
            directives=extraParams['directives'], 
            extraParams=extraParams
        )
    else:
        pagePageLinksDict = googleGetFileSERPResults(serps, extraParams=extraParams)
    
    if( 'links' not in pagePageLinksDict ):
        return {}
    
    '''
        ensure dictionary keys (pages) are in order before merging serp results, 
        internally, pagePageLinksDict['links'][page] have already been sorted by pagePageLinksDict['links'][page]
    '''
    sortedPages = sorted( pagePageLinksDict['links'] )
    mergedListOfLinks = []
    for page in sortedPages:
        mergedListOfLinks += pagePageLinksDict['links'][page]


    #mark location of key
    if( extraParams['find_uri_key'] != '' ):
        markURIKey( pagePageLinksDict, mergedListOfLinks )

    
    if( 'search_state' in extraParams ):
        del extraParams['search_state']

    self_uris = []
    if( 'self_uris' in pagePageLinksDict['page_dets'] ):
        self_uris = pagePageLinksDict['page_dets'].pop('self_uris')

    return {
        'source': 'Google',
        'query': query,
        'extra_params':{
            'raw_request_params': extraParams,
            'page_dets': pagePageLinksDict['page_dets']
        },
        'self_uris': self_uris,
        'max_page': maxPage,
        'gen_timestamp': datetime.utcnow().isoformat().split('.')[0] + 'Z',
        'links': mergedListOfLinks,
        'stats': {
            'total_links': len(mergedListOfLinks),
            'domain_dist': getTopKDomainStats(mergedListOfLinks, 10)
        }
    }

def getGoogleSrchResCount(googleHTMLSoup):

    divs = googleHTMLSoup.find_all('div')
    errorMsgs = []
    resultStats = ''
    for dv in divs:
        
        txt = dv.text.strip().lower()
        if( len(txt) < 100 and txt.find('result') != -1 ):

            resultStats = txt.split(' ')
            if( len(resultStats) > 1 ):

                resultStats = resultStats[1].replace(',', '').strip()
                try:
                    return {
                        'page': int(resultStats),
                        'src_text': dv.text
                    }
                except:
                    errorMsgs.append(resultStats)

    logger.error('\tgetGoogleSrchResCount(): error parsing int: ' + str(resultStats))
    return {
        'page': -1,
        'src_text': ''
    }

def isCaptchaPage(googleSoup):

    if( googleSoup.find(id='captcha-form') is None ):
        return False
    else:
        return True

def getRandQueries():

    randQueries = []
    src = workingFolder() + 'RandQueries.txt'
    try:
        infile = open(src, 'r')
        randQueries = infile.readlines()
        infile.close()
    except:
        genericErrorInfo('\tfilepath: ' + src)

    return randQueries

def randGoogleQuery(randQueries, extraParams):

    if( 'interleave_queries_params' not in extraParams ):
        logger.info('\trandGoogleQuery(): off')
        return

    extraParams['interleave_queries_params'].setdefault('count', 1)

    for i in range( extraParams['interleave_queries_params']['count'] ):
        if( len(randQueries) != 0 ):
            #dummy search
            randIndx = randint(0, len(randQueries) - 1)
            randQuery = randQueries[randIndx].strip()
            
            extraParams['interleave_queries_params']['news'] = False
            extraParams['interleave_queries_params']['leave_browser_open'] = False
            logger.info('\trandGoogleQuery(): ' + str(i) + '-' + randQuery)
            googleGetHTMLPage(randQuery, 1, extraParams=extraParams)

def isURIKeyPresent(key, links):

    key = key.strip()
    if( key == '' ):
        return False
    
    for i in range(len(links)):
        if( isSameLink(key, links[i]['link']) ):
            logger.info('\n\tisURIKeyPresent(): found key: ' + key)
            links[i]['uri_key_flag'] = True
            return True

    return False

def clusterSerps(files):
    
    '''
        querySerpClusters format:
        {
            key (query + vertical): {
                'sniffed_info': {},
                'pages': {
                    1: linksDict,...
                }
           },...
        }
    '''
    querySerpClusters = {}
    for potentialSerp in files:
        
        if( 'text' not in potentialSerp ):
            continue

        try:
            soup = BeautifulSoup( potentialSerp['text'], 'html.parser')
            linksDict, moreDets = rankSensitiveGetLnksFrmPage( soup, extraParams={'sniff_serp': True} )

            if( len(linksDict) == 0 ):
                continue

            query = moreDets['sniffed_info']['query'].strip()
            page = moreDets['sniffed_info']['page']
            vertical = moreDets['sniffed_info']['vertical']

            if( 'filename' in potentialSerp ):
                moreDets['sniffed_info']['filename'] = potentialSerp['filename']

            key = query + ', ' + vertical
            querySerpClusters.setdefault( key, {'sniffed_info': moreDets['sniffed_info'], 'pages': {}} )
            querySerpClusters[key]['pages'][page] = {'linksDict': linksDict, 'moreDets': moreDets}
        except:
            genericErrorInfo()

    return querySerpClusters

def googleGetFileSERPResults(serps, extraParams=None):
    '''
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetSERPResults(), synchronize both
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetSERPResults(), synchronize both
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetSERPResults(), synchronize both
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetSERPResults(), synchronize both
    '''
    logger.info('\ngoogleGetFileSERPResults() - start')

    if( extraParams is None ):
        extraParams = {}
    
    extraParams.setdefault('search_state', {})
    extraParams['search_state'].setdefault('proc_pg_count', 0)
    
    pageDets = {
        'result_count': -1,
        'search_state': extraParams['search_state'],
        'self_uris': []
    }

    pagePageLinksDict = {}
    prevLinksDictKeys = []
    rankAdditiveFactor = 0
    pages = sorted( list(serps['pages'].keys()) )

    for page in pages:
        
        pageDets['search_state']['proc_pg_count'] += 1
        
        linksDict = serps['pages'][page]['linksDict']
        moreDets = serps['pages'][page]['moreDets']
        sniffedSelf = constructSearchURI( searchString=serps['sniffed_info']['query'], page=page, vertical=serps['sniffed_info']['vertical'] )

        pageDets['captcha_on'] = moreDets['captcha_on']
        pageDets['self_uris'].append({ 'page': page, 'uri': sniffedSelf })

        logger.info('\tpage: ' + str(page) + ': ' + sniffedSelf)

        if( page == 1 ):
            for opt in moreDets:
                pageDets[opt] = moreDets[opt]
           

        if( prevLinksDictKeys == linksDict.keys() ):
            logger.info('\tDuplicate page: ' + str(page) + ' stopping')
            break

        for l, ldict in linksDict.items():
            ldict['rank'] += rankAdditiveFactor

        prevLinksDictKeys = linksDict.keys()
        pagePageLinksDict[page-1] = getListOfDict(linksDict)
        
        if( len(pagePageLinksDict[page-1]) != 0 ):    
            rankAdditiveFactor = str(pagePageLinksDict[page-1][-1]['rank'])
            #if the last rank is a child, the rank would be of form x.xx, so avoid this
            rankAdditiveFactor = int(rankAdditiveFactor.split('.')[0])


        #search for uri key if uri key supplied, if key found stop search
        if( extraParams['find_uri_key'] != '' ):
            
            pageDets['uri_key_found_indx'] = isURIKeyPresent( extraParams['find_uri_key'], pagePageLinksDict[page-1] )
            if( pageDets['uri_key_found_indx'] ):
                break

    
    logger.info('\ngoogleGetFileSERPResults() - end')
    return {
        'links': pagePageLinksDict,
        'page_dets': pageDets
    }

def googleGetSERPResults(query, maxPage=1, directives='', extraParams=None):
    '''
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetFileSERPResults(), synchronize both
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetFileSERPResults(), synchronize both
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetFileSERPResults(), synchronize both
        CAUTION FUNCTIONALITY IS DUPLICATED BY googleGetFileSERPResults(), synchronize both
    '''
    logger.info('\ngoogleGetSERPResults() - start')

    if( extraParams is None ):
        extraParams = {}

    if( maxPage < 1 ):
        return {}


    randQueries = []
    if( 'interleave_queries_params' in extraParams ):
        randQueries = getRandQueries()


    extraParams.setdefault('news', False)
    extraParams.setdefault('find_uri_key', '')
    extraParams.setdefault('search_state', {})
    extraParams['search_state'].setdefault('proc_pg_count', 0)
    slug = ''.join([ c if c.isalnum() else '_' for c in query ])

    newsSlug = ''
    if( extraParams['news'] is True ):
        newsSlug = '_news'

    
    '''
        pagePageLinksList format:
        { 
            page:
            [ 
                (link: datetime or nowDatetime),
                (link: datetime or nowDatetime),
                ...
            ],
            page:
            [
            ]
            ,...
        }
    '''
    pageDets = {
        'result_count': -1,
        'search_state': extraParams['search_state'],
        'self_uris': []
    }

    pagePageLinksDict = {}
    prevLinksDictKeys = []
    rankAdditiveFactor = 0
    for page in range(1, maxPage+1):
        
        logger.info('\tpage: ' + str(page))
        
        if( maxPage > 1 ):
            #default behavior (when closeBrowserFlag absent) ensure the same driver is used when other pages have to be explored,
            #so don't close browser
            if( 'leave_browser_open' not in extraParams ):
                extraParams['leave_browser_open'] = False
                if( page == maxPage ):
                    extraParams['leave_browser_open'] = True
        
        
        if( 'interleave_queries_params' in extraParams ):
            randGoogleQuery(randQueries, extraParams)
        
        googleHTMLPage = googleGetHTMLPage(query, page, directives=directives, extraParams=extraParams)
        pageDets['search_state']['proc_pg_count'] += 1

        if( googleHTMLPage['html'] == '' ):
            logger.info('\tEmpty html page: ' + str(page) + ' skipping')
            continue

        soup = BeautifulSoup( googleHTMLPage['html'], 'html.parser')
        if( 'html_out_path' in extraParams ):
            if( extraParams['html_out_path'] != '' ):

                if( extraParams['html_out_path'].endswith('/') == False ):
                    extraParams['html_out_path'] = extraParams['html_out_path'] + '/'

                if( 'html_out_slug' in extraParams ):
                    if( extraParams['html_out_slug'] != '' ):
                        slug = extraParams['html_out_slug']
                
                writeTextToFile( extraParams['html_out_path'] + slug + newsSlug + '_' + str(page) + '.html', googleHTMLPage['html'] )
        
        '''
            linksDict format:
            {
                'link': {'title': '', 'date': '', 'snippet': ''}
                ...
            }
        '''
        linksDict, moreDets = rankSensitiveGetLnksFrmPage( soup, rankAdditiveFactor=rankAdditiveFactor, page=page, extraParams=extraParams )
        pageDets['self_uris'].append({'page': page, 'uri': googleHTMLPage['self']})

        if( page == 1 ):
            #screening the following two lines pending removal
            #for opt in ['scraping_report', 'related_queries', 'result_count']:
            #if( opt in moreDets ):
            for opt in moreDets:
                pageDets[opt] = moreDets[opt]
        
        
        pageDets['captcha_on'] = moreDets['captcha_on']
        if( pageDets['captcha_on'] is True ):
            logger.info('\tCaptcha page, breaking')
            break
        

        if( prevLinksDictKeys == linksDict.keys() ):
            logger.info('\tDuplicate page: ' + str(page) + ' stopping')
            break


        prevLinksDictKeys = linksDict.keys()
        pagePageLinksDict[page-1] = getListOfDict(linksDict)
        if( len(pagePageLinksDict[page-1]) != 0 ):
            
            rankAdditiveFactor = str(pagePageLinksDict[page-1][-1]['rank'])
            #if the last rank is a child, the rank would be of form x.xx, so avoid this
            rankAdditiveFactor = int(rankAdditiveFactor.split('.')[0])
            


        #search for uri key if uri key supplied, if key found stop search
        if( extraParams['find_uri_key'] != '' ):
            
            pageDets['uri_key_found_indx'] = isURIKeyPresent( extraParams['find_uri_key'], pagePageLinksDict[page-1] )
            if( pageDets['uri_key_found_indx'] ):
                break

    
    logger.info('\ngoogleGetSERPResults() - end')
    return {
        'links': pagePageLinksDict,
        'page_dets': pageDets
    }

def getListOfDict(linksDict):

    '''
        linksDict format:
        {
            'link': {'title': '', 'date': ''}
            ...
        }
    '''
    sortedLinks = sorted( linksDict, key=lambda link:linksDict[link]['rank'] )
    listOfLinksDicts = []
    
    for link in sortedLinks:

        tempDict = {'link': link.strip()}
        for key, value in linksDict[link].items():
            
            if( isinstance(key, str) ):
                key = key.strip()

            if( isinstance(value, str) ):
                value = value.strip()
            
            tempDict[key] = value
        listOfLinksDicts.append(tempDict)

    return listOfLinksDicts

def getArgs():
   
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))
    parser.add_argument('query', nargs='+', help='Google search query or files (-f, --files)')
    
    parser.add_argument('-d', '--max-file-depth', help='When reading files recursively from directory stop at the specified path depth. 0 means no restriction', type=int, default=1)
    parser.add_argument('-f', '--files', help='Read Google SERPs from files instead of searching with query', action='store_true')#default false
    parser.add_argument('-n', '--news', help='Search Google News Vertical (default is False)', action='store_true')#default false
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-p', '--max-page', help='Maximum number of pages to visit', type=int, default=1)
    parser.add_argument('-s', '--sleep-sec', help='For search throttling process: maximum number or seconds to sleep between adjacent searches', type=int, default=1)
    
    parser.add_argument('--chromedriver-path', help='Path to selenium chromedriver to be used instead of curl', default='')
    parser.add_argument('--delay-sec', help='Delay by set value before extracting links', type=int, default=0)
    parser.add_argument('--headers', help='User-supplied headers delimited by <h>, e.g.,: "<h> user-agent: xyz <h> accept: xyz <h> connection: xyz"')
    parser.add_argument('--html-out-path', help='Path to save SERP', default='')
    parser.add_argument('--html-out-slug', help='Filename of SERP', default='')
    parser.add_argument('--directives', help='Directives to accompany search, e.g., "site:example.com")', default='')
    parser.add_argument('--find-uri-key', help='Search for uri', default='')

    parser.add_argument('--log-file', help='Log output filename', default='')
    parser.add_argument('--log-format', help='Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html', default='')
    parser.add_argument('--log-level', help='Log level', choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'], default='info')
    
    parser.add_argument('--no-interleave', help='Do not interleave search, override interleave logic', action='store_true')
    parser.add_argument('--pretty-print', help='Pretty print JSON output', action='store_true')
    
    return parser

def setCustomUserHeaders(params):

    if( 'headers' not in params ):
        return

    if( params['headers'] is None ):
        return
    
    '''
        example: 

        input:
        params['headers'] = <h>user-agent:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36<h>cache-control: max-age=0
        
        output:
        params['header-user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        params['header-cache-control'] = 'max-age=0'
    '''

    userHeaders = params['headers'].split('<h>')
    for i in range( len(userHeaders) ):
        
        head = userHeaders[i].strip()
        marker = head.find(':')

        if( marker == -1 ):
            continue

        params[ 'header-' + head[:marker].strip() ] = head[marker+1:].strip()

def procReq(params):
    
    setCustomUserHeaders(params)
    
    serps = googleSearch(
        params['query'], 
        maxPage=params['max_page'], 
        newsVertical=params['news'],
        extraParams=params
    )
    
    if( 'serps' in serps ):
        for singleSerp in serps['serps']:
            title = 'cluster for query: ' + singleSerp['query'] + ' (' + singleSerp['sniffed_info']['vertical'] + ') max page: ' + str(singleSerp['max_page']) 
            printPayload( 'google', singleSerp, title=title)
    else:
        printPayload('google', serps)
            
    if( params['output'] is not None ):
        dumpJsonToFile( params['output'], serps, indentFlag=params['pretty_print'] )

    return serps

def getDefaultArgs(parseKnown=''):
    parser = getArgs()
    
    if( parseKnown == '' ):
        return vars( parser.parse_args() )
    else:
        args, unknown = parser.parse_known_args()
        return vars( args )

def main():

    params = getDefaultArgs()
    
    setLogDefaults( params )
    setLoggerDets( logger, params['log_dets'] )
    procReq(params)

if __name__ == 'scraper.Google':
    
    from scraper.ScraperUtil import derefURI
    from scraper.ScraperUtil import DocVect
    from scraper.ScraperUtil import dumpJsonToFile
    from scraper.ScraperUtil import expandUrl
    from scraper.ScraperUtil import extractPageTitleFromHTML
    from scraper.ScraperUtil import getDictFromFile
    from scraper.ScraperUtil import getDictFromJsonGZ
    from scraper.ScraperUtil import getDomain
    from scraper.ScraperUtil import getStrHash
    from scraper.ScraperUtil import gzipTextFile
    from scraper.ScraperUtil import getTopKDomainStats
    from scraper.ScraperUtil import genericErrorInfo
    from scraper.ScraperUtil import isSameLink
    from scraper.ScraperUtil import jaccardFor2Sets
    from scraper.ScraperUtil import printPayload
    from scraper.ScraperUtil import readTextFromFilesRecursive
    from scraper.ScraperUtil import setLogDefaults
    from scraper.ScraperUtil import setLoggerDets
    from scraper.ScraperUtil import writeTextToFile
    
else:
    
    from ScraperUtil import derefURI
    from ScraperUtil import DocVect
    from ScraperUtil import dumpJsonToFile
    from ScraperUtil import expandUrl
    from ScraperUtil import extractPageTitleFromHTML
    from ScraperUtil import getDictFromFile
    from ScraperUtil import getDictFromJsonGZ
    from ScraperUtil import getDomain
    from ScraperUtil import getStrHash
    from ScraperUtil import gzipTextFile
    from ScraperUtil import getTopKDomainStats
    from ScraperUtil import genericErrorInfo
    from ScraperUtil import isSameLink
    from ScraperUtil import jaccardFor2Sets
    from ScraperUtil import printPayload
    from ScraperUtil import readTextFromFilesRecursive
    from ScraperUtil import setLogDefaults
    from ScraperUtil import setLoggerDets
    from ScraperUtil import writeTextToFile
    
    if __name__ == '__main__':    
        main()
