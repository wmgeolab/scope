import argparse
import logging
import time

from datetime import datetime
from urllib.parse import urlparse, quote

logger = logging.getLogger('scraper.scraper')

def redditSearch(query, subreddit='', maxPage=1, extraFieldsDict=None, extraParams=None):

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('expand', False)

    if( extraParams['expand'] is True ):
        
        return redditSearchExpand(
            query=query,
            subreddit=subreddit,
            maxPage=maxPage,
            extraFieldsDict=extraFieldsDict,
            extraParams=extraParams
        )

    else:

        return redditDefaultSearch(
            query=query,
            subreddit=subreddit,
            maxPage=maxPage,
            extraFieldsDict=extraFieldsDict,
            extraParams=extraParams
        )
    

def redditDefaultSearch(query, subreddit='', maxPage=1, extraFieldsDict=None, extraParams=None):

    logger.info('\nredditDefaultSearch() - start')

    query = query.strip()
    subreddit = subreddit.strip()
    maxPage = str(maxPage).strip() 

    if( extraFieldsDict is None ):
        extraFieldsDict = {}

    if( extraParams is None ):
        extraParams = {}

    try:
        maxPage = int(maxPage)
    except:
        genericErrorInfo()
        maxPage = 1


    if( query == '' ):
        return {}

    extraParams.setdefault('sleep_sec', 0)
    extraParams.setdefault('retry_count_after_none', 3)
    if( maxPage > 1 and extraParams['sleep_sec'] == 0 ):
        #throlling
        extraParams['sleep_sec'] = 1

    extraParams.setdefault('max_posts', -1)
    extraParams.setdefault('sort', 'relevance')#default is: relevance, other options: top, new, comments

    subredditPadding = ''
    if( subreddit != '' ):
        subreddit = 'r/' + subreddit + '/'
        subredditPadding = '&restrict_sr=1'

    sortFlag = '&sort=' + extraParams['sort'].strip()

    logger.info('\tquery: ' + query)
    logger.info('\tsubreddit: ' + subreddit)
    logger.info('\tsort: ' + extraParams['sort'])
    
    afterFlag = ''
    pageCounter = 1
    breakFlag = False

    collection = {
        'source': 'Reddit',
        'query': query,
        'extra_params': extraParams,
        'max_page': maxPage,
        'posts': [], 
        'self_uris': [],
        'stats': {
        	'outlinks_link_dist': {},
        	'total_outlinks': 0,
        	'total_links': 0
        }
    }

    try:
        while True:
            logger.info('')
            
            redditQuery = 'https://www.reddit.com/' + subreddit +  'search.json?q=' + quote(query) + sortFlag + afterFlag + subredditPadding
            
            collection['self_uris'].append({ 'page': pageCounter, 'uri': redditQuery })
            pageCounter += 1

            redditJson = getDictFromJson( derefURI(redditQuery, extraParams['sleep_sec']) )
            collection['gen_timestamp'] = datetime.utcnow().isoformat().split('.')[0] + 'Z'

            logger.info('\tredditQuery: ' + redditQuery)

            if( 'data' not in redditJson ):
                logger.info('\tNo data key present')
                break

            redditJson = redditJson['data']

            for child in redditJson['children']:
                
                try:

                    tempDict = redditSetCommonDets( child['data'] )
                    tempDict['kind'] = ''
                    if( 'kind' in child ):
                        tempDict['kind'] = redditKindTraslate(child['kind'])

                    tempDict['outlinks'] = redditGetAllLinksFromCommentHTML( child['data']['selftext_html'] )
                    for key, value in extraFieldsDict.items():
                        tempDict[key] = value

                    linkDistCount = len(tempDict['outlinks'])
                    collection['stats']['outlinks_link_dist'].setdefault(linkDistCount, 0)
                    collection['stats']['outlinks_link_dist'][linkDistCount] += 1
                    collection['stats']['total_outlinks'] += linkDistCount

                    collection['posts'].append(tempDict)

                    if( len(collection['posts']) == extraParams['max_posts'] ):
                        breakFlag = True
                        logger.info('\tmax results breaking: ' + str(extraParams['max_posts']))
                        break

                    '''
                        print('\t\tauthor:', child['author'])
                        print('\t\ttitle:', child['title'])
                        print('\t\tsubreddit:', child['subreddit'])
                        print()
                    '''
                except:
                    genericErrorInfo()
            
            maxPage -= 1
            logger.info('\tmaxPage: ' + str(maxPage))

            if( breakFlag ):
                break
            
            if( maxPage == 0 ):
                logger.info('\tbreaking, maxPage = 0')
                break

            if( redditJson['after'] is None ):
                
                '''
                    redditJson['after'] sometimes returns None for a request with content.
                    This if-block is a measure that attempts to get a valid redditJson['after'] by attempting
                    to deref the uri (redditQuery) that returned the None
                '''
                retryCounter = extraParams['retry_count_after_none']
                while( retryCounter > 0 ):
                    
                    logger.info( '\t\tafter is None, but maxPage = ' + str(maxPage) )
                    logger.info( '\t\tretry_count_after_none: ' + str(retryCounter) )
                    logger.info( '\t\twill retry deref: ' + redditQuery )
                    redditJsonRetry = getDictFromJson( derefURI(redditQuery, 1) )

                    if( 'data' in redditJsonRetry ):
                        if( redditJsonRetry['data']['after'] is not None ):
                            #stop retry since valid (not None) afterFlag found
                            afterFlag = '&after=' + redditJsonRetry['data']['after']
                            redditJson['after'] = redditJsonRetry['data']['after']
                            logger.info( '\t\tvalid after found: ' + redditJson['after'] + ', breaking' )
                            break

                    retryCounter -= 1
                
                if( redditJson['after'] is None ):
                    logger.info( '\t\tretry_count_after_none: 0, after still None. breaking' )
                    break
            else:
                afterFlag = '&after=' + redditJson['after']
            
            
    except:
        genericErrorInfo()

    logger.info('redditDefaultSearch() - end')
    collection['stats']['total_links'] = len( collection['posts'] )
    collection['stats']['domain_dist'] = getTopKDomainStats( collection['posts'], 10 )
    return collection

def redditSearchExpand(query, subreddit='', maxPage=1, extraFieldsDict=None, extraParams=None):
    logger.info('\nredditSearchExpand() - start')

    if( extraFieldsDict is None ):
        extraFieldsDict = {}

    if( extraParams is None ):
        extraParams = {}
    
    results = redditDefaultSearch(
        query=query,
        subreddit=subreddit,
        maxPage=maxPage,
        extraFieldsDict=extraFieldsDict,
        extraParams=extraParams
    )

    if( 'posts' not in results ):
        return results

    extraParams.setdefault('max_comments', -1)
    extraParams.setdefault('sleep_sec', 2)
    extraParams.setdefault('thread_count', 5)

    jobsLst = []
    size = len(results['posts'])
    for i in range(size):
        
        if( results['posts'][i]['stats']['comment_count'] == 0 ):
            continue

        keywords = {
            'commentURI': results['posts'][i]['custom']['permalink'],
            'maxLinks': extraParams['max_comments'],
            'extraParams': extraParams
        }

        toPrint = ''
        if( i%10 == 0 ):
            toPrint = '\t' + str(i) + ' of ' + str(size)

        jobsLst.append({
            'func': redditGetLinksFromComment,
            'args': keywords,
            'misc': i,
            'print': toPrint
        })

    logger.info('\textracting comments - start')
    logger.info( '\tjobsLst.len: ' + str(len(jobsLst)) )
    
    resLst = parallelTask(jobsLst, threadCount=extraParams['thread_count'])
    
    logger.info( '\tresLst.len: ' + str(len(resLst)) )
    logger.info('\textracting comments - end')

    for res in resLst:
        res['output']['input_uri'] = res['input']['args']['commentURI']
        indx = res['misc']
        results['posts'][indx]['custom']['expanded_comments'] = res['output']

        #create link dist - start
        results['posts'][indx].setdefault('stats', {})
        results['posts'][indx]['stats'].setdefault('comments_link_dist', {})

        if( 'comments' not in res['output'] ):
            continue

        for comment in res['output']['comments']:
            linkCount = len(comment['outlinks'])
            results['posts'][indx]['stats']['comments_link_dist'].setdefault(linkCount, 0)
            results['posts'][indx]['stats']['comments_link_dist'][linkCount] += 1
        #create link dist - end
    
    logger.info('redditSearchExpand() - end')
    return results
    

def redditGetAllLinksFromCommentHTML(htmlStr, details=None):

    linksDict = {'outlinks': []}
    lastIndex = -1

    while( True and htmlStr is not None ):
        
        link, lastIndex = getStrBetweenMarkers(htmlStr, 'href="', '"', startIndex=lastIndex+1)
        link = link.strip()

        if( len(link) != 0 ):
            if( link[0] == '/' ):
                link = 'https://www.reddit.com' + link

        if( lastIndex == -1 ):
            break
        elif( link.find('http') == 0 ):
            linksDict['outlinks'].append( link )

    '''
    try:
        soup = BeautifulSoup(html.unescape(htmlStr), 'html.parser')
        allLinks = soup.find_all('a')

        
        for link in allLinks:
            if( link.has_attr('href') == False ):
                continue

            link = link['href'].strip()
            if( len(link) == 0 ):
                continue

            if( link[0] == '/' ):
                link = 'https://www.reddit.com' + link

            linksDict['outlinks'].append( link )
    except:
        genericErrorInfo()
    '''

    if( details is None ):
        return linksDict['outlinks']
    else:
        for key, val in details.items():
            linksDict[key] = val
    
    return linksDict

def redditKindTraslate(kind):
    
    kinds = {
        't1': 'comment',
        't2': 'account',
        't3': 'link',
        't4': 'message',
        't5': 'subreddit',
        't6': 'award'
    }

    if( kind in kinds ):
        return kinds[kind]
    else:
        return kind

def redditSetCommonDets(payload):

    result = {}
    try:

        result['pub_datetime'] = ''
        if( 'created_utc' in payload ):
            result['pub_datetime'] = datetime.utcfromtimestamp(payload['created_utc']).isoformat() + 'Z'
        
        commonAccessors = {
            'id': 'id',
            'parent_id': 'parent_id',
            'url': 'link',
            'title': 'title',
            'selftext': 'snippet',
            'body': 'text',
            'depth': 'depth'
        }

        for pubkey, privkey in commonAccessors.items():
            if( pubkey in payload ):
                result[privkey] = payload[pubkey]
            else:
                result[privkey] = ''

        if( result['depth'] == '' ):
            result['depth'] = -1

        result['depth'] += 1
        
        
        result['stats'] = {
            'score': -1,
            'comment_count': 0
        }

        if( 'score' in payload ):
            result['stats']['score'] = payload['score']

        if( 'num_comments' in payload ):
            result['stats']['comment_count'] = payload['num_comments']

        
        result['custom'] = {
            'author': payload['author'], 
            'subreddit': payload['subreddit'], 
            'permalink': 'https://www.reddit.com' + payload['permalink']
        }

    except:
        genericErrorInfo()

    return result

def redditAddComments(comment, allComments, maxi=-1, excludeCommentsWithNoLinks=True):

    if( maxi != -1 and len(allComments) >= maxi ):
        return False

    if( excludeCommentsWithNoLinks ):
        if( len(comment['outlinks']) == 0 ):
            if( comment['link'].strip() != '' ):
                if( isSameLink(comment['link'], comment['custom']['permalink']) == False ):
                    #add comments even though links in comments body is empty, because comments has a link that is not its permalink
                    allComments.append(comment)    
        else:
            allComments.append(comment)
    else:
        allComments.append(comment)

    return True

def redditRecursiveTraverseComment(payload, tabCount, detailsDict, maxLinks=-1, extraParams=None):

    '''
        verify recursion, count links, dedup links
        patch links with just scheme incomplete
    '''

    if( extraParams is None ):
        extraParams = {}

    if( 'excludeCommentsWithNoLinks' not in extraParams ):
        extraParams['excludeCommentsWithNoLinks'] = True

    tab = '\t' * tabCount
    #print(tab, 'redditRecursiveTraverseComment():')
    
    if( 'kind' in payload ):

        if( payload['kind'] == 'Listing' ):
            
            #print(tab, 'kind: Listing')
            if( 'data' in payload ):
                redditRecursiveTraverseComment( payload['data'], tabCount + 1, detailsDict, maxLinks=maxLinks, extraParams=extraParams )

        elif( payload['kind'] == 't3' ):
            
            #print(tab, 'kind: t3 (link)')
            if( 'data' in payload ):
                if( 'selftext_html' in payload['data'] ):
                    
                    details = redditSetCommonDets(payload['data'])
                    details['kind'] = redditKindTraslate('t3')
                    comLinkDicts = redditGetAllLinksFromCommentHTML(payload['data']['selftext_html'], details)
                    addFlag = redditAddComments( 
                            comLinkDicts, 
                            detailsDict['comments'], 
                            maxLinks, 
                            excludeCommentsWithNoLinks=extraParams['excludeCommentsWithNoLinks']
                        )
                    if( not addFlag ):
                        return
        
        elif( payload['kind'] == 'LiveUpdate' ):
            
            if( 'data' in payload ):
                if( 'body_html' in payload['data'] ):
                    
                    details = redditSetCommonDets(payload['data'])
                    details['kind'] = redditKindTraslate('live-update')
                    comLinkDicts = redditGetAllLinksFromCommentHTML(payload['data']['body_html'], details)
                    addFlag = redditAddComments( 
                            comLinkDicts, 
                            detailsDict['comments'], 
                            maxLinks, 
                            excludeCommentsWithNoLinks=extraParams['excludeCommentsWithNoLinks']
                        )
                    if( not addFlag ):
                        return

        elif( payload['kind'] == 't1' ):
            
            #print(tab, 'kind: t1 (comment)')

            if( 'data' in payload ):

                if( 'body_html' in payload['data'] ):
                    
                    details = redditSetCommonDets(payload['data'])
                    details['kind'] = redditKindTraslate('t1')
                    comLinkDicts = redditGetAllLinksFromCommentHTML(payload['data']['body_html'], details)
                    addFlag = redditAddComments( 
                            comLinkDicts, 
                            detailsDict['comments'], 
                            maxLinks, 
                            excludeCommentsWithNoLinks=extraParams['excludeCommentsWithNoLinks']
                        )
                    if( not addFlag ):
                        return

            #comment with possible replies
                if( 'replies' in payload['data'] ): 
                    if( len(payload['data']['replies']) != 0 ):
                        redditRecursiveTraverseComment( payload['data']['replies'], tabCount + 1, detailsDict, maxLinks=maxLinks, extraParams=extraParams )#replies is a listing
    
    elif( 'children' in payload ):
        #print(tab, 'children')
        for child in payload['children']:
            redditRecursiveTraverseComment( child, tabCount + 1, detailsDict, maxLinks=maxLinks, extraParams=extraParams )

def redditPrlGetLinksFromComment(urisLst, maxLinks=-1, extraParams=None):

    urisLstSize = len(urisLst)
    if( urisLstSize == 0 ):
        return []

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('thread_count', 5)

    jobsLst = []
    for i in range(urisLstSize):
        keywords = {
            'commentURI': urisLst[i],
            'maxLinks': maxLinks,
            'extraParams': extraParams
        }

        toPrint = ''
        if( i%10 == 0 ):
            toPrint = '\t' + str(i) + ' of ' + str(urisLstSize)

        jobsLst.append({
            'func': redditGetLinksFromComment, 
            'args': keywords,
            'misc': False,
            'print': toPrint
        })

    resLst = parallelTask(jobsLst, threadCount=extraParams['thread_count'])
    for i in range(len(resLst)):

        resLst[i]['output']['input_uri'] = resLst[i]['input']['args']['commentURI']
        resLst[i] = resLst[i]['output']
    
    return resLst


def redditGetLinksFromComment(commentURI, maxLinks=-1, extraParams=None):

    logger.info('\n\tredditGetLinksFromComment():')
    commentURI = commentURI.strip()
    if( len(commentURI) == 0 ):
        return {}

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('sleep_sec', 2)
    extraParams.setdefault('addRootComment', False)

    logger.info( '\taddRootComment: ' + str(extraParams['addRootComment']) )

    detailsDict = {'comments': []}
    detailsDict['input_uri'] = commentURI


    try:
        #from: "https://www.reddit.com/r/worldnews/comments/5nv73m/former_mi6_agent_christopher_steeles_frustration/?ref=search_posts" 
        #to:   "https://www.reddit.com/r/worldnews/comments/5nv73m/former_mi6_agent_christopher_steeles_frustration.json?ref=search_posts"
        uriPath = urlparse(commentURI).path.strip()
        if( uriPath.endswith('/') ):
            commentURI = commentURI.replace(uriPath, uriPath[:-1] + '.json')
        else:
            commentURI = commentURI.replace(uriPath, uriPath + '.json')
    except:
        genericErrorInfo()
        return {}
    
    
    detailsDict['self'] = commentURI
    detailsDict['timestamp'] = datetime.utcnow().isoformat().split('.')[0] + 'Z'

    redditCommentJson = getDictFromJson( derefURI(commentURI, extraParams['sleep_sec']) )
    payloadType = type(redditCommentJson)

    if( payloadType == dict ):        
        redditRecursiveTraverseComment( redditCommentJson, 1, detailsDict, maxLinks=maxLinks, extraParams=extraParams )    

    elif( payloadType == list ):
        
        if( len(redditCommentJson) != 2 ):
            logger.info(' redditGetLinksFromComment(): unexpected size ' + str(len(redditCommentJson)) * 200)

        if( extraParams['addRootComment'] ):
            #this adds the parent as the root comment
            for commentThread in redditCommentJson:
                redditRecursiveTraverseComment( commentThread, 1, detailsDict, maxLinks=maxLinks, extraParams=extraParams )
        else:
            redditRecursiveTraverseComment( redditCommentJson[-1], 1, detailsDict, maxLinks=maxLinks, extraParams=extraParams )

    detailsDict['total-comments'] = len(detailsDict['comments'])
    
    return detailsDict

def getArgs():

    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))
    parser.add_argument('query', help='Reddit search query')
    
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-p', '--max-page', help='Maximum number of pages to visit', type=int, default=1)
    parser.add_argument('-s', '--sleep-sec', help='For search throttling process: maximum number or seconds to sleep between adjacent searches', type=int, default=0)

    parser.add_argument('--expand', help='Expand posts from SERP by extracting links from comment posts', action='store_true')

    parser.add_argument('--log-file', help='Log output filename', default='')
    parser.add_argument('--log-format', help='Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html', default='')
    parser.add_argument('--log-level', help='Log level', choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'], default='info')

    parser.add_argument('--max-posts', help='Maximum number of Reddit posts to return', type=int, default=-1)
    parser.add_argument('--retry-count-after-none', help='The maximum number of times to retry dereferencing a search URI when the "after" field is None but maxPage > 0', type=int, default=3)
    parser.add_argument('--sort', choices=['relevance', 'top', 'new', 'comments'], help='Sort criteria for posts', default='relevance')
    parser.add_argument('--subreddit', help='Search Reddit subreddit', default='')
    parser.add_argument('--thread-count', help='Maximum number of threads to use for parallel operations', type=int, default=5)
    
    parser.add_argument('--pretty-print', help='Pretty print JSON output', action='store_true')
    
    return parser

def procReq(params):
    
    serp = redditSearch(
        params['query'], 
        subreddit=params['subreddit'], 
        maxPage=params['max_page'],
        extraParams=params
    )

    printPayload('reddit', serp)
    if( params['output'] is not None ):
        dumpJsonToFile( params['output'], serp, indentFlag=params['pretty_print'] )

    return serp
    

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
    

if __name__ == 'scraper.Reddit':
    
    from scraper.ScraperUtil import derefURI
    from scraper.ScraperUtil import dumpJsonToFile
    from scraper.ScraperUtil import genericErrorInfo
    from scraper.ScraperUtil import getDictFromJson
    from scraper.ScraperUtil import getTopKDomainStats
    from scraper.ScraperUtil import setLogDefaults
    from scraper.ScraperUtil import setLoggerDets
    from scraper.ScraperUtil import getStrBetweenMarkers
    from scraper.ScraperUtil import parallelTask
    from scraper.ScraperUtil import printPayload
    
else:
    
    from ScraperUtil import derefURI
    from ScraperUtil import dumpJsonToFile
    from ScraperUtil import genericErrorInfo
    from ScraperUtil import getDictFromJson
    from ScraperUtil import getTopKDomainStats
    from ScraperUtil import setLogDefaults
    from ScraperUtil import setLoggerDets
    from ScraperUtil import getStrBetweenMarkers
    from ScraperUtil import parallelTask
    from ScraperUtil import printPayload
    
    if __name__ == '__main__':    
        main()