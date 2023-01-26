import argparse
import json
import logging
import os
import sys
import time
import networkx as nx
import tweepy

from bs4 import BeautifulSoup
from copy import deepcopy
from dateparser import parse as parseDateStr
from datetime import datetime
from urllib.parse import urlparse, quote, quote_plus
from os.path import dirname, abspath
from os import makedirs

from selenium import webdriver
from subprocess import check_output

logger = logging.getLogger('scraper.scraper')

def workingFolder():
    return dirname(abspath(__file__)) + '/'

def getTweetLink(screenName, tweetId):
    return 'https://twitter.com/' + screenName + '/status/' + tweetId

def getTweetLstName(tweetsCol):

    if( 'tweet_replies' in tweetsCol ):
        return 'tweet_replies'
    elif( 'tweet_thread' in tweetsCol ):
        return 'tweet_thread'
    else:
        return ''

def getHandle(candHandle):
    
    handle = ''
    candHandle = candHandle.strip().lower()
    for tok in candHandle:
        
        if( tok.isalnum() or tok == '_' ):
            handle += tok
        else:
            break

    if( handle in ['intent', 'share', 'tweet', 'search', 'hashtag'] ):
        return ''
    else:
        return handle

def getHandlesFrmLnks(links):

    handles = {'handles': [], 'provenance': {}}#provenance key is handle, value is link from which handle was extracted
    dedupSet = set()
    
    for link in links:

        try:
            link = link['href']
        except:
            continue

        if( link.find('twitter.com') == -1 ):
            continue

        tokens = link.split('twitter.com/')
        if( len(tokens) == 2 ):
            
            handle = getHandle( tokens[1] )
            if( handle != '' and handle not in dedupSet ):
                dedupSet.add(handle)
                
                handles['handles'].append(handle)
                handles['provenance'][handle] = link

    return handles

def isIsolatedTweet(twtDct):
    
    try:
        #first condition is for root tweet
        if( twtDct['data_conversation_id'] == twtDct['data_tweet_id'] and twtDct['tweet_stats']['reply'] == 0 ):
            return True
        else:
            return False
    except:
        genericErrorInfo()

    return None

#extract 863007411132649473 from 'https://twitter.com/realDonaldTrump/status/863007411132649473'
def getTweetIDFromStatusURI(tweetURI):

    if( tweetURI.startswith('https://twitter.com/') == False ):
        return ''

    tweetURI = tweetURI.strip()

    if( tweetURI[-1] == '/' ):
        tweetURI = tweetURI[:-1]

    if( tweetURI.find('status/') != -1 ):
        return tweetURI.split('status/')[1].strip()

    return ''

def parseTweetURI(tweetURI):

    twtDat = {'screenName': '', 'id': ''}
    if( tweetURI.startswith('https://twitter.com/') == False ):
        return twtDat


    tweetURI = tweetURI.strip()
    parts = urlparse(tweetURI)
    tweetURI = parts.scheme + '://' + parts.netloc + parts.path

    if( tweetURI[-1] == '/' ):
        tweetURI = tweetURI[:-1]

    if( tweetURI.find('status/') != -1 ):
        twtDat['id'] = tweetURI.split('status/')[1].strip()
        twtDat['id'] = twtDat['id'].split('?')[0].strip()
        twtDat['screenName'] = tweetURI.split('https://twitter.com/')[1].replace('/status/' + twtDat['id'], '')

    return twtDat

def getTweetLink(screenName, tweetId):
    return 'https://twitter.com/' + screenName + '/status/' + tweetId

    
def twitterSearch(chromedriverPath, query='', maxTweetCount=100, latestVertical=False, extraParams=None):

    query = query.strip()

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('query', query)
    extraParams.setdefault('expand', False)
    extraParams.setdefault('hydrate_files', False)

    if( extraParams['expand'] is True and extraParams['hydrate_files'] is False ):

        logger.info('\ntwitterSearch() calling searchExpand():')
        serp = searchExpand(
            chromedriverPath=chromedriverPath,
            query=query,
            maxTweetCount=maxTweetCount,
            latestVertical=latestVertical,
            searchTwts=None,
            extraParams=extraParams
        )

    else:
        
        logger.info('\ntwitterSearch() calling extractTweetsFromSearch():')
        serp = extractTweetsFromSearch(
            chromedriverPath=chromedriverPath,
            query=query,
            maxTweetCount=maxTweetCount,
            latestVertical=latestVertical,
            extraParams=extraParams
        )

    writeCache(serp, extraParams)
    #redact keys when no longer
    redactTweetKeys(extraParams)
    
    return serp

def writeCache(serp, params):

    if( 'tweets' not in serp ):
        return

    if( 'cache' not in params ):
        return

    if( 'cache_path' not in params['cache'] ):
        return

    if( params['cache']['cache_path'] == '' ):
        return

    if( 'cache_write' not in params['cache'] ):
        return

    if( params['cache']['cache_write'] is False ):
        return


    if( 'verbose' in params ):
        prevVerbose = params['verbose']
    else:
        prevVerbose = False

    #cache reading diff live: save conversation as group - start
    if('self' in serp ):
        
        id = parseTweetURI( serp['self'] )['id']
        if( id != '' ):
            
            writeTwtCache(
                cacheFolder=params['cache']['cache_path'],
                twtId=id,
                twtDct=serp
            )
            
            return
    #cache reading diff live: save conversation as group - end
    
    for i in range( len(serp['tweets']) ):
        
        twt = serp['tweets'][i]
        if( i % 50 == 0 ):
            params['verbose'] = True
        else:
            params['verbose'] = False

        writeTwtCache(
            cacheFolder=params['cache']['cache_path'],
            twtId=twt['data_tweet_id'],
            twtDct=twt
        )

    #restore state
    params['verbose'] = prevVerbose

def restructureThreadOrRelies(tweetsCol):
    logger.info('\nrestructureThreadOrRelies():')
    
    if( 'self' not in tweetsCol or 'tweets' not in tweetsCol ):
        return

    parentTwt = {}
    replies = {'tweets': []}
    requestID = parseTweetURI( tweetsCol['self'] )['id']

    for i in range( len(tweetsCol['tweets']) ):
        
        twt = tweetsCol['tweets'][i]
        if( twt['data_tweet_id'] == requestID ):
            parentTwt = twt
        else:
            replies['tweets'].append(twt)

    
    tweetListName = attachRepliesOrThreadsToTweet(parentTwt, replies)
    if( tweetListName != '' ):
        #here means a reply or thread was added to parentTwt, so remove relocated tweets
        newTweetsCol = ''
        for twt in tweetsCol['tweets']:
            if( 'tweet_thread' in twt or 'tweet_replies' in twt ):
                newTweetsCol = twt
                break
        
        if( newTweetsCol != '' ):
            
            #transfer properties from tweetsCol.keys() to newTweetsCol[tweetListName] - start
            for ky, val in tweetsCol.items():
                if( ky == 'tweets' ):
                    continue
                newTweetsCol[tweetListName][ky] = val
            #transfer properties from tweetsCol.keys() to newTweetsCol[tweetListName] - end

            tweetsCol['tweets'] = [newTweetsCol]
            logger.info('\nrestructureThreadOrRelies(): done')

def extractTweetsFromSearch(chromedriverPath, query='', maxTweetCount=100, latestVertical=False, extraParams=None):

    query = query.strip()

    if( extraParams is None ):
        extraParams = {}

    if( latestVertical ):
        latestVertical = 'f=live&'
    else:
        latestVertical = ''

    twitterURIPrefix = 'https://twitter.com/search?' + latestVertical + 'q='#top

    extraParams.setdefault('max_no_more_tweets_counter', 2)
    extraParams.setdefault('search_uri_key', '')
    extraParams.setdefault('hydrate_files', False)

    finalTweetsColDict = {}
    cachePathFlag = False

    if( 'cache' in extraParams ):
        if( 'cache_path' in extraParams['cache'] ):
            if( extraParams['cache']['cache_path'] != '' ):

                cachePathFlag = True
                if( 'cache_write' in extraParams['cache'] ):
                    try:
                        makedirs( extraParams['cache']['cache_path'], exist_ok=True )
                    except:
                        genericErrorInfo()
    

    if( query.startswith('https://twitter.com/') ):
        
        finalTweetsColDict = extractTweetsFromTweetURI(
            query, 
            maxTweetCount, 
            maxNoMoreTweetCounter=extraParams['max_no_more_tweets_counter'],
            chromedriverPath=chromedriverPath,
            extraParams=extraParams
        )

        #restructureThreadOrRelies(): this permits saving tweet with its replies as collection, not individuals
        restructureThreadOrRelies(finalTweetsColDict)

    elif( extraParams['search_uri_key'] != '' ):

        for urlPrefix in ['url:', '']:
            
            searchURI = twitterURIPrefix + quote_plus( urlPrefix + extraParams['search_uri_key'] ) + '&src=typd'
            finalTweetsColDict = extractTweetsFromTweetURI(
                searchURI, 
                maxTweetCount, 
                maxNoMoreTweetCounter=extraParams['max_no_more_tweets_counter'],
                chromedriverPath=chromedriverPath,
                extraParams=extraParams
            )

            if( 'tweets' in finalTweetsColDict ):
                if( len(finalTweetsColDict['tweets']) != 0 ):
                    break
                    
    elif( extraParams['hydrate_files'] is True and cachePathFlag ):

        finalTweetsColDict = hydrateExpandTweetsFromFiles(extraParams['cache']['cache_path'], extraParams=extraParams)

    else:

        searchURI = twitterURIPrefix + quote_plus(query) + '&src=typd'
        finalTweetsColDict = extractTweetsFromTweetURI(
            searchURI, 
            maxTweetCount, 
            maxNoMoreTweetCounter=extraParams['max_no_more_tweets_counter'],
            chromedriverPath=chromedriverPath,
            extraParams=extraParams
        )

    return finalTweetsColDict

def hydrateExpandTweetsFromFiles(cachePath, extraParams):

    logger.info('\nhydrateExpandTweetsFromFiles():')

    finalTweetsColDict = {'tweets': []}
    extraParams.setdefault('max_file_depth', 1)
    extraParams.setdefault('chromedriver_path', None)
    extraParams.setdefault('cache', {})
    extraParams.setdefault('max_tweets', -1)
    extraParams.setdefault('expand', False)
    extraParams['cache']['cache_write'] = True
    
    tweetScaffold = BeautifulSoup('<div></div', 'html.parser')
    tweetScaffold = twitterGetTweetIfExist(tweetScaffold, '', getTweetScaffold=True)

    twts = readTextFromFilesRecursive( cachePath, addDetails=True, maxDepth=extraParams['max_file_depth'] )
    for twt in twts:

        twt = getDictFromJson( twt['text'] )
        if( 'tweet_hydrated' in twt ):
            finalTweetsColDict['tweets'].append(twt)

        elif( 'data_tweet_id' in twt ):
            twtCopy = deepcopy(tweetScaffold)

            #transfer properties from twt['extra'] to twtCopy - start
            if( 'extraction_dets' in twt ):
                twtCopy['extra']['extraction_dets'] = twt['extraction_dets']
            #transfer properties from twt['extra'] to twtCopy - end
            
            twtCopy['data_tweet_id'] = twt['data_tweet_id']
            finalTweetsColDict['tweets'].append(twtCopy)
        else:
            logger.info('\t(tweet_hydrated not in twt) or data_tweet_id not in twt, skipping')

        if( len(finalTweetsColDict['tweets']) == extraParams['max_tweets'] ):
            break

    prepTwtsForRetrn(finalTweetsColDict, cachePath, extraParams=extraParams)
    if( extraParams['expand'] is True ):
        finalTweetsColDict = searchExpand(
            chromedriverPath=extraParams['chromedriver_path'],
            searchTwts=finalTweetsColDict,
            extraParams=extraParams
        )
    

    return finalTweetsColDict

def searchExpand(chromedriverPath, query='', maxTweetCount=100,  latestVertical=False, searchTwts=None, extraParams=None):

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('max_reply_count', 5)
    extraParams.setdefault('leave_browser_open', False)
    extraParams.setdefault('max_no_more_tweets_counter', 4)
    
    if( searchTwts is None ):
        searchTwts = extractTweetsFromSearch(
            chromedriverPath=chromedriverPath,
            query=query, 
            maxTweetCount=maxTweetCount,
            latestVertical=latestVertical,
            extraParams=deepcopy(extraParams)
        )

    del extraParams['leave_browser_open']
    extraParams['chromedriver_path'] = chromedriverPath

    searchTwtsWithReplies = searchExpandReplHelper(searchTwts, extraParams)
    return searchTwtsWithReplies

def attachRepliesOrThreadsToTweet(tweet, reply):
    
    #error checks - hydrated tweet usually has valid tweets fields
    if( 'data_tweet_id' not in tweet or 'data_conversation_id' not in tweet ):
        return ''

    if( tweet['data_tweet_id'] == tweet['data_conversation_id'] ):
        #actual root found
        tweetListName = 'tweet_replies'
    else:
        #unsure if payload is reply to tweet, tweet might be member of payload (thread), e.g., https://twitter.com/Gururizu612721/status/1227278699868721152
        tweetListName = 'tweet_thread'
    
    tweet[tweetListName] = reply
    tweet[tweetListName]['stats'] = {}
    tweet[tweetListName]['stats']['total_links'] = 0
    tweet[tweetListName]['stats']['total_tweets'] = 0

    if( 'tweets' in reply ):
        tweet[tweetListName]['stats']['total_links'] = countLinksInTweets( reply['tweets'] )
        tweet[tweetListName]['stats']['total_tweets'] = len( reply['tweets'] )    

    if( tweet['tweet_stats']['reply'] < tweet[tweetListName]['stats']['total_tweets'] ):
        tweet['tweet_stats']['reply'] = tweet[tweetListName]['stats']['total_tweets']

    return tweetListName

def searchExpandReplHelper(tweets, params):

    if( len(tweets) == 0 ):
        return tweets

    if( 'tweets' not in tweets ):
        return tweets
    

    threads = []
    threadLookupDict = {}
    params.setdefault('no_check_reply_count', False)
    logger.info( '\n\tsearchExpandReplHelper() len.tweets: ' + str(len(tweets['tweets'])) )

    for i in range( len(tweets['tweets']) ):

        if( params['no_check_reply_count'] is False ):
            if( tweets['tweets'][i]['tweet_stats']['reply'] == 0 ):
                continue

        tweetURI = getTweetLink( tweets['tweets'][i]['data_screen_name'], tweets['tweets'][i]['data_tweet_id'] )
        threads.append( tweetURI )
        threadLookupDict[tweetURI] = i

    if( len(threads) == 0 ):
        logger.info('\n\tsearchExpandReplHelper() threads 0 returning')
        return tweets

    
    params.setdefault('report_error', True)
    replies = retryParallelTwtsExt(
        threads,
        maxRetryCount=5,
        tweetConvMaxTweetCount=params['max_reply_count'],
        maxNoMoreTweetCounter=params['max_no_more_tweets_counter'],
        chromedriverPath=params['chromedriver_path'],
        extraParams=params
    )

    for reply in replies:

        #cache reading diff live: for handling when tweet collected from cache - start
        tweetListName = getTweetLstName(reply)
        if( tweetListName in reply ):
            reply = reply[tweetListName]
        #cache reading diff live: for handling when tweet collected from cache - end

        if( 'self' not in reply ):
            continue

        if( reply['self'] not in threadLookupDict ):
            continue
        
        i = threadLookupDict[ reply['self'] ]
        tweet = tweets['tweets'][i]
        
        #additional provenance - start
        for j in range( len(reply['tweets']) ):
            rp = reply['tweets'][j]
            rp['provenance']['parent']['parent'] = {'uri': tweet['provenance']['parent']['uri']}
        #additional provenance - end

        #reply['tweets'] possibly includes a clone of tweet, update - start
        
        #1. copy all properties from clone tweet
        cloneIndx = -1
        replyGroupInClone = False

        for j in range( len(reply['tweets']) ):
            
            clone = reply['tweets'][j]
            if( clone['data_tweet_id'] == tweet['data_tweet_id'] ):
                
                #2. clone found: set cloneIndx to allow removal of clone later
                cloneIndx = j

                #3. clone also has reply_group so transfer properties
                for key, val in clone['extra'].items():
                    #if( key not in tweet['extra'] ):
                    tweet['extra'][key] = val

                if( 'reply_group' in clone['extra'] ):
                    #3. add reply_group
                    replyGroupInClone = True

                break
        
        #4. remove clone from reply
        if( cloneIndx != -1 ):
            
            del reply['tweets'][cloneIndx]
            if( 'reply_group_loc' in reply and replyGroupInClone ):
                del reply['reply_group_loc']

        #reply['tweets'] possibly includes a clone of tweet, update - end
        attachRepliesOrThreadsToTweet(tweet, reply)

    return tweets


#maxRetryCount: -1 means unlimited
def retryParallelTwtsExt(urisLst, maxRetryCount=10, tweetConvMaxTweetCount=100, maxNoMoreTweetCounter=2, chromedriverPath='/usr/bin/chromedriver', extraParams=None):

    
    if( extraParams is None ):
        extraParams = {}

    result = []
    errorReqsDict = {}
    counter = 0
    extraParams['report_error'] = True


    while counter < maxRetryCount:

        tmpResult = parallelGetTwtsFrmURIs(
            urisLst,
            tweetConvMaxTweetCount=tweetConvMaxTweetCount,
            maxNoMoreTweetCounter=maxNoMoreTweetCounter,
            chromedriverPath=chromedriverPath,
            extraParams=extraParams
        )
        
        urisLst = []
        for res in tmpResult:
            if( 'error' in res and 'self' in res):
                urisLst.append( res['self'] )
                
                #save problematic request result payload, in case loop doesn't get chance to run again
                errorReqsDict[res['self']] = res
            else:
                result.append( res )

                if( 'self' in res ):
                    if( res['self'] in errorReqsDict ):
                        #remove this rectified request
                        del errorReqsDict[res['self']]

        logger.info('\nretryParallelTwtsExt, iter: ' + str(counter) + ' of ' + str(maxRetryCount) + ', queue: ' + str(len(urisLst)) )
        if( len(urisLst) == 0 ):
            logger.info('\n\tbreaking, queue empty')
            break
        
        counter += 1

    for uri, res in errorReqsDict.items():
        result.append(res)

    return result

def parallelGetTwtsFrmURIs(urisLst, tweetConvMaxTweetCount=100, maxNoMoreTweetCounter=2, chromedriverPath='/usr/bin/chromedriver', extraParams=None):
    
    logger.info('\nparallelGetTwts')

    if( len(urisLst) == 0 ):
        return []

    if( extraParams is None ):
        extraParams = {}

    offset = 0
    if( 'window_shift_offset' in extraParams ):
        offset = extraParams['window_shift_offset']
        logger.info( '\toffset: ' + str(offset) )

    jobsLst = []
    predefXYLocs = [
        (0 + offset, 0),
        (200 + offset, 0),
        (400 + offset, 0),
        (600 + offset, 0),
        (0 + offset, 0),
        (200 + offset, 0),
        (400 + offset, 0),
        (600 + offset, 0)
    ]

    indxer = 0
    length = len(urisLst)
    for i in range(length):
        
        locExtraParams = {}
        locExtraParams['window_x'], locExtraParams['window_y'] = predefXYLocs[indxer]
        indxer += 1
        indxer = indxer % len(predefXYLocs)

        #transfer props
        for key, val in extraParams.items():
            locExtraParams[key] = val

        locExtraParams.setdefault('leave_browser_open', False)
        keywords = {
            'tweetConvURI': urisLst[i],
            'tweetConvMaxTweetCount': tweetConvMaxTweetCount,
            'maxNoMoreTweetCounter': maxNoMoreTweetCounter,
            'chromedriverPath': chromedriverPath,
            'extraParams': locExtraParams
        }

        printMsg = '\t' + str(i) + ' of ' + str(length)
        jobsLst.append( {'func': extractTweetsFromTweetURI, 'args': keywords, 'misc': False, 'print': printMsg} )


    outLst = []
    resLst = parallelTask(jobsLst, threadCount=extraParams['thread_count'])
    
    for res in resLst:
        outLst.append( res['output'] )

    return outLst

def countLinksInTweets(tweets):
    
    totalLinks = 0
    for twt in tweets:
        totalLinks += len(twt['tweet_links'])

    return totalLinks

def getTwtFilename(cacheFolder, id, slug=''):
    
    cacheFolder = cacheFolder.strip()
    id = id.strip()

    if( cacheFolder == '' ):
        return ''

    if( cacheFolder.endswith('/') == False ):
        cacheFolder = cacheFolder + '/'

    return cacheFolder + id + slug + '.json.gz'

def readTwtCache(cacheFolder, tweetURI):
    
    twtDat = parseTweetURI(tweetURI)
    cacheFolder = cacheFolder.strip()

    if( cacheFolder != '' and twtDat['id'] != '' ):

        filename = getTwtFilename(cacheFolder, twtDat['id'])
        return getDictFromJsonGZ(filename)

    return {}

def writeTwtCache(cacheFolder, twtId, twtDct, twtFileName=''):
    
    if( twtFileName == '' ):
        twtFileName = getTwtFilename(cacheFolder, twtId)

    if( twtFileName == '' ):
        return

    gzipTextFile(twtFileName, json.dumps(twtDct, ensure_ascii=False))

def statusLookupReqRemain(api):
    try:
        return api.rate_limit_status()['resources']['statuses']['/statuses/lookup']['remaining']
    except:
        genericErrorInfo()
        return 0

def hydrateSingleTweet(twtClone, hydratedTweet, dontIncludeTweetJson=False):

    if( dontIncludeTweetJson is False ):
        twtClone['extra']['raw_json'] = hydratedTweet._json

    twtClone['tweet_hydrated'] = True
    if( hydratedTweet.in_reply_to_status_id_str is None ):
        twtClone['data_conversation_id'] = twtClone['data_tweet_id']
    else:
        twtClone['data_conversation_id'] = hydratedTweet.in_reply_to_status_id_str

    twtClone['data_name'] = hydratedTweet.user.name
    twtClone['data_screen_name'] = hydratedTweet.user.screen_name
    twtClone['user_verified'] = hydratedTweet.user.verified

    twtClone['tweet_stats']['retweet'] = hydratedTweet.retweet_count
    twtClone['tweet_stats']['favorite'] = hydratedTweet.favorite_count
    twtClone['tweet_text'] = hydratedTweet.full_text[ hydratedTweet.display_text_range[0]: hydratedTweet.display_text_range[1] ]
    twtClone['tweet_time'] = hydratedTweet.created_at.isoformat().split('.')[0] + 'Z'

    twtClone['data_mentions'] = []
    for mention in hydratedTweet.entities['user_mentions']:
        twtClone['data_mentions'].append({ 'data_screen_name': mention['screen_name'], 'data_name': mention['name'] })

    twtClone['hashtags'] = []
    for hashtag in hydratedTweet.entities['hashtags']:
        twtClone['hashtags'].append( hashtag['text'] )

    twtClone['tweet_links'] = []
    for url in hydratedTweet.entities['urls']:
        twtClone['tweet_links'].append({ 'uri': url['expanded_url'] })


def hydrateTweets(tweets, params):

    params.setdefault('consumer_key', '')
    params.setdefault('consumer_secret', '')
    params.setdefault('access_token', '')
    params.setdefault('access_token_secret', '')
    
    params.setdefault('hydrate_q_size', 100)
    params.setdefault('hydrate_sleep_sec', 1)

    params.setdefault('no_add_hydrated_tweet_json', False)
    params.setdefault('no_redact_keys', False)
    params.setdefault('no_hydrate_tweets', False)

    if( params['consumer_key'] == '' or params['consumer_secret'] == '' or params['access_token'] == '' or params['access_token_secret'] == '' ):
        logger.info( '\thydrateTweets(): some key (consumer_key, consumer_secret, access_token, or access_token_secret) or token is empty, returning, NOT HYDRATING' )
        return False

    if( params['no_hydrate_tweets'] is True ):
        logger.info( '\thydrateTweets(): USER SET --no-hydrate-tweets, NOT HYDRATING' )
        return False


    hydrateSleepSec = params['hydrate_sleep_sec']
    if( hydrateSleepSec > 0 and 'expand' in params and 'thread_count' in params ):
        if( params['expand'] is True and params['thread_count'] > 0 ):
            #since multiple threads are issued, instead of 1 request per second,
            #the api is now called params['thread_count'] request per second,
            #leading to the possibility of maxing out the request quota and hitting the rate limit
            #therefore remedy this by sleeping more when threads are active
            hydrateSleepSec = hydrateSleepSec + (params['thread_count'] - 1)


    auth = tweepy.OAuthHandler(params['consumer_key'], params['consumer_secret'])
    auth.set_access_token(params['access_token'], params['access_token_secret'])
    api = tweepy.API(auth)

    #if( statusLookupReqRemain(api) == 0 ):
    #    logger.info( '\thydrateTweets(): statusLookupReqRemain() = 0, returning' )
    #    return False

    tweetIDLocMap = {}
    hydrateQueue = [[]]
    for i in range( len(tweets) ):

        #100 because: 100 Tweets per request may be issued to GET statuses/lookup endpoint (https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-lookup)
        if( len(hydrateQueue[-1]) == params['hydrate_q_size'] ):
            hydrateQueue.append([])

        twt = tweets[i]
        hydrateCand = False

        if( 'tweet_hydrated' not in twt ):
            hydrateCand = True
        elif( twt['tweet_hydrated'] is False ):
            hydrateCand = True

        if( hydrateCand ):
            tweetIDLocMap[ twt['data_tweet_id'] ] = {'twtParentIdx': i, 'twtChildIdx': None}
            #add parent
            hydrateQueue[-1].append( twt['data_tweet_id'] )


        if( 'tweet_replies' in twt ):
            tweetListName = 'tweet_replies'
        elif( 'tweet_thread' in twt ):
            tweetListName = 'tweet_thread'
        else:
            tweetListName = 'NONE'
        
        if( tweetListName in twt ):
            if( 'tweets' in twt[tweetListName] ):
                for j in range( len(twt[tweetListName]['tweets']) ):

                    if( len(hydrateQueue[-1]) == params['hydrate_q_size'] ):
                        hydrateQueue.append([])

                    twtChild = twt[tweetListName]['tweets'][j]
                    if( twtChild['tweet_hydrated']  is False ):
                        tweetIDLocMap[ twtChild['data_tweet_id'] ] = {'twtParentIdx': i, 'twtChildIdx': j}
                        hydrateQueue[-1].append( twtChild['data_tweet_id'] )


    hydrateQSize = len(hydrateQueue)
    logger.info( '\thydrateTweets(): queue size: ' + str(hydrateQSize) )
    for ids in hydrateQueue:
        
        if( len(ids) == 0 ):
            continue

        hydratedTweets = []
        try:
            hydratedTweets = api.statuses_lookup(id_=ids, include_entities=True, tweet_mode='extended')
        except:
            genericErrorInfo( '\tids: ' + str(ids) )

        logger.info( '\thydrateTweets(): throttling, sleeping sec: ' + str(hydrateSleepSec) )
        time.sleep(hydrateSleepSec)

        for twt in hydratedTweets:

            if( twt.id_str not in tweetIDLocMap ):
                continue

            twtParentIdx = tweetIDLocMap[twt.id_str]['twtParentIdx']
            twtChildIdx = tweetIDLocMap[twt.id_str]['twtChildIdx']

            if( twtChildIdx is None ):
                twtClone = tweets[twtParentIdx]
            else:
                twtClone = tweets[twtParentIdx][twtChildIdx]

            hydrateSingleTweet(twtClone, twt, params['no_add_hydrated_tweet_json'])
    
    return True

def hydrateUsers(screenNames, params):

    if( len(screenNames) == 0 ):
        return {}

    params.setdefault('consumer_key', '')
    params.setdefault('consumer_secret', '')
    params.setdefault('access_token', '')
    params.setdefault('access_token_secret', '')

    params.setdefault('hydrate_q_size', 100)

    if( params['consumer_key'] == '' or params['consumer_secret'] == '' or params['access_token'] == '' or params['access_token_secret'] == '' ):
        logger.info( '\thydrateUsers(): some key or token is empty, returning' )
        logger.info( '\t\tconsumer_key:' + params['consumer_key'] )
        logger.info( '\t\tconsumer_secret:' + params['consumer_secret'] )
        logger.info( '\t\taccess_token:' + params['access_token'] )
        logger.info( '\t\taccess_token_secret:' + params['access_token_secret'] )
        return {}

    auth = tweepy.OAuthHandler(params['consumer_key'], params['consumer_secret'])
    auth.set_access_token(params['access_token'], params['access_token_secret'])
    api = tweepy.API(auth)

    usersProfiles = {}
    hydrateQueue = [[]]
    for user in screenNames:

        #100 because: 100 Tweets per request may be issued to GET users/lookup endpoint (https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup)
        if( len(hydrateQueue[-1]) == params['hydrate_q_size'] ):
            hydrateQueue.append([])
        
        #add parent
        hydrateQueue[-1].append(user)
    
    for screenNameGroup in hydrateQueue:
        
        hydratedUsers = []
        try:
            hydratedUsers = api.lookup_users(screen_names=screenNameGroup)
            logger.info( '\thydrateUsers(): throttling, sleeping for 1 sec' )
            time.sleep(1)
        except:
            genericErrorInfo( '\tscreenames: ' + str(screenNameGroup) )

        for hydUser in hydratedUsers:
            usersProfiles[hydUser.screen_name.lower()] = hydUser._json
    
    return usersProfiles

def prepTwtsForRetrn(finalTweetsColDict, uri, extraParams=None):

    if( extraParams is None ):
        extraParams = {}


    finalTweetsColDict['self'] = uri
    extraParams.setdefault('query', '')
    finalTweetsColDict['has_single_user_thread'] = False
    if( 'tweets' not in finalTweetsColDict ):
        return

    if( len(finalTweetsColDict['tweets']) == 0 ):
        return

    #attempt to find tweets from cache to avoid hydrating - start
    #read single tweets from cache
    if( 'cache' in extraParams ):
        if( 'cache_path' in extraParams['cache'] and 'cache_read' in extraParams['cache'] ):
            if( extraParams['cache']['cache_path'] != '' and extraParams['cache']['cache_read'] is True):
                
                for i in range( len(finalTweetsColDict['tweets']) ):
                    
                    twt = finalTweetsColDict['tweets'][i]
                    tmpTwt = readTwtCache(extraParams['cache']['cache_path'], getTweetLink(twt['data_screen_name'], twt['data_tweet_id']))
                    
                    if( 'tweet_hydrated' in tmpTwt ):
                        if( tmpTwt['tweet_hydrated'] is True ):
                            
                            logger.info('\ttweets_hydrated cache HIT: ' + twt['data_tweet_id'])
                            finalTweetsColDict['tweets'][i] = tmpTwt
    #attempt to find tweets from cache to avoid hydrating - start

    finalTweetsColDict['tweets_hydrated'] = hydrateTweets(finalTweetsColDict['tweets'], extraParams)
    for i in range( len(finalTweetsColDict['tweets']) ):
        finalTweetsColDict['tweets'][i]['pos'] = i
        finalTweetsColDict['tweets'][i]['provenance'] = {'parent': {'uri': uri}, 'query': extraParams['query']}
    
    #identifying threads - start
    uriDets = twitterGetURIDetails(uri)

    if( len(uriDets) == 2 ):
        markedDets = markThread( finalTweetsColDict['tweets'] )
        
        for key, val in markedDets.items():
            finalTweetsColDict[key] = val
    #identifying threads - end

def findRootTweetMain(driver, maxNoMoreTweetCounter, tweetConvURI, extraParams):
    
    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('sleep_sec', 2)

    if( maxNoMoreTweetCounter < 1 ):
        return

    prevLen = 0
    try:
        while( True ):
            if( maxNoMoreTweetCounter == 0 ):
                return
            
            scrollUp(driver)
            time.sleep( extraParams['sleep_sec'] )

            twitterHTMLPage = driver.page_source.encode('utf-8')
            tweets = twitterGetDescendants(twitterHTMLPage, uri=tweetConvURI, extraParams=extraParams)

            if( len(tweets) == prevLen ):
                maxNoMoreTweetCounter -= 1

            prevLen = len(tweets)
    except:
        genericErrorInfo()

def findRootTweet(driver, maxNoMoreTweetCounter, tweetConvURI, extraParams):

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('delay_sec', 0)

    if( extraParams['delay_sec'] > 0 ):
        logger.info( '\tdelay_sec, sleeping for: ' + str(extraParams['delay_sec']) )
        time.sleep(extraParams['delay_sec'])

    try:
        #reset before finding root tweet, also results in retrieving more tweets
        driver.get(tweetConvURI)
    except:
        genericErrorInfo()

    findRootTweetMain( driver, maxNoMoreTweetCounter, tweetConvURI, extraParams )


def isRootTweetPresent(finalTweetsColDict):

    if( 'tweets' not in finalTweetsColDict ):
        return False

    for twt in finalTweetsColDict['tweets']:
        if( twt['data_tweet_id'] == twt['data_conversation_id'] ):
            return True

    return False

def shouldUseCacheRead(twtsCol, expand, maxReplyCnt, referURI):

    if( expand is False or len(twtsCol) == 0 ):
        return twtsCol

    lstName = getTweetLstName(twtsCol)
    if( lstName == '' ):
        logger.info('\nshouldUseCacheRead() - Cache HIT burst Cache, tweet no reply')
        return {}

    elif( 'tweets' in twtsCol[lstName] ):
        #+1 because we count the parent tweet
        colSize = len(twtsCol[lstName]['tweets']) + 1
        replyCnt = twtsCol['tweet_stats']['reply']

        if( colSize > maxReplyCnt ):
            logger.info('\nshouldUseCacheRead() - Cache HIT burst Cache, more replies collected (' + str(colSize) + ') than requested ('+ str(maxReplyCnt) +'), so trimming')
            twtsCol[lstName]['tweets'] = twtsCol[lstName]['tweets'][:maxReplyCnt - 1]

        elif( colSize < maxReplyCnt and replyCnt >= maxReplyCnt ):
            logger.info('\nshouldUseCacheRead() - Cache HIT burst Cache, less replies collected (' + str(colSize) + ') but possible more ('+ str(replyCnt) +') tweets')
            return {}

    return twtsCol

def extractTweetsFromTweetURI(tweetConvURI, tweetConvMaxTweetCount=100, maxNoMoreTweetCounter=2, chromedriverPath='/usr/bin/chromedriver', extraParams=None):
    #patched use of Chrome with:https://archive.is/94Idt
    #set noMoreTweetCounter to -1 if no scroll required

    tweetConvURI = tweetConvURI.strip()
    finalTweetsColDict = {}
    cacheMiss = False
    if( tweetConvURI.find('https://twitter.com') != 0 ):
        return {}

    if( extraParams is None ):
        extraParams = {}
    
    extraParams.setdefault('cache', {})
    extraParams.setdefault('expand', False)
    extraParams.setdefault('max_reply_count', 5)

    extraParams['cache'].setdefault('cache_path', '')
    extraParams['cache'].setdefault('cache_read', False)

    logger.info('\nextractTweetsFromTweetURI():')
    logger.info('\turi: ' + tweetConvURI)


    #check if tweet in cache - start
    if( extraParams['cache']['cache_path'] != '' and extraParams['cache']['cache_read'] is True ):
        logger.info( '\tcache read: ' + tweetConvURI )
        finalTweetsColDict = readTwtCache(extraParams['cache']['cache_path'], tweetConvURI)
        #cache reading diff live - start
        finalTweetsColDict = shouldUseCacheRead( finalTweetsColDict, extraParams['expand'], extraParams['max_reply_count'], tweetConvURI )
        #cache reading diff live - end

    if( extraParams['cache']['cache_read'] and len(finalTweetsColDict) == 0 ):
        logger.info( '\tcache MISS: ' + tweetConvURI )
    
    elif( len(finalTweetsColDict) != 0 ):
        logger.info( '\tcache HIT: ' + tweetConvURI )
        return finalTweetsColDict
    #check if tweet in cache - end

    reportErrorFlag = False
    if( tweetConvMaxTweetCount < 1 ):
        tweetConvMaxTweetCount = 100

    
    extraParams.setdefault('window_width', 400)
    extraParams.setdefault('window_height', 1500)
    extraParams.setdefault('leave_browser_open', False)
    extraParams.setdefault('delay_sec', 5)
    extraParams.setdefault('delay_sec_after', 0)
    extraParams.setdefault('find_root_tweet', False)


    if( 'report_error' in extraParams ):
        reportErrorFlag = extraParams['report_error']

    driver = None
    if( 'driver' in extraParams ):
        driver = extraParams['driver']
        logger.info('\tusing user-supplied driver')
    
    if( driver is None ):
        driver = getChromedriver(chromedriverPath)
        if( driver is None ):
            logger.error('\nchromedriver is None, consider setting --chromedriver-path')
            return finalTweetsColDict
        else:
            driver.set_window_size(extraParams['window_width'], extraParams['window_height'])
            if( 'window_x' in extraParams and 'window_y' in extraParams ):
                driver.set_window_position(extraParams['window_x'], extraParams['window_y'] )


    try:
        #driver.maximize_window()
        driver.get(tweetConvURI)
    except:
        logger.info('\tsupplied chromedriverpath: ' + chromedriverPath)
        logger.info('\t\ttweetConvURI: ' + tweetConvURI)
        genericErrorInfo()
        if( reportErrorFlag ):
            return {
                'error': True,
                'self': tweetConvURI
            }    

        return {}

    if( extraParams['delay_sec'] > 0 ):
        logger.info( '\tdelay_sec, sleeping for: ' + str(extraParams['delay_sec']) )
        time.sleep(extraParams['delay_sec'])

    finalTweetsColDict = recursiveExtractTweetsMain(
        driver=driver, 
        tweetConvURI=tweetConvURI, 
        tweetConvMaxTweetCount=tweetConvMaxTweetCount, 
        maxNoMoreTweetCounter=maxNoMoreTweetCounter,
        extraParams=extraParams
    )

    #get proper count of tweets, since tweets sets retrieved in different sessions may have identical pos values
    #has to be called whenever after finalTweetsColDict is set
    prepTwtsForRetrn(finalTweetsColDict, tweetConvURI, extraParams=extraParams)

    if( extraParams['find_root_tweet'] is True ):#finding root tweet is active

        if( len(twitterGetURIDetails(tweetConvURI)) == 2 ):#conversation
            if( 'tweets' in finalTweetsColDict ):#tweet payload present
                if( len(finalTweetsColDict['tweets']) != 0 ):#tweet payload is non-empty
                    if( isRootTweetPresent(finalTweetsColDict) is False ):#root tweet NOT present
                        
                        logger.info( '\nFinding Root tweet' )
                        findRootTweet( driver, maxNoMoreTweetCounter, tweetConvURI, extraParams )
                        
                        finalTweetsColDict = recursiveExtractTweetsMain(
                            driver=driver, 
                            tweetConvURI=tweetConvURI, 
                            finalTweetsColDict=finalTweetsColDict,
                            tweetConvMaxTweetCount=tweetConvMaxTweetCount, 
                            maxNoMoreTweetCounter=maxNoMoreTweetCounter,
                            extraParams=extraParams
                        )
                        
                        #get proper count of tweets, since tweets sets retrieved in different sessions may have identical pos values
                        #has to be called whenever after finalTweetsColDict is set
                        prepTwtsForRetrn(finalTweetsColDict, tweetConvURI, extraParams=extraParams)

    if( extraParams['delay_sec_after'] > 0 ):
        logger.info( '\tdelay_sec_after, sleeping for: ' + str(extraParams['delay_sec_after']) )
        time.sleep(extraParams['delay_sec_after'])

    #anomaly: not closing browser only seems to work when the user supplies the driver
    if( extraParams['leave_browser_open'] is False ):
        driver.quit()

    return finalTweetsColDict

def redactTweetKeys(params):

    params.setdefault('no_redact_keys', False)

    if( params['no_redact_keys'] is False ):
        for ky in ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']:
            if( params[ky] != '' ):
                params[ky] = 'REDACTED'

def recursiveExtractTweetsMain(driver, tweetConvURI, finalTweetsColDict=None, tweetConvMaxTweetCount=100, maxNoMoreTweetCounter=2, extraParams=None):

    #set maxNoMoreTweetCounter to -1 if you don't want any scroll

    logger.info('\nrecursiveExtractTweetsMain()')
    logger.info('\turi: ' + tweetConvURI)

    tweetConvURI = tweetConvURI.strip()
    if( len(tweetConvURI) == 0 ):
        return {}

    if( extraParams is None ):
        extraParams = {}

    
    extraParams.setdefault('max_no_more_tweets_counter', maxNoMoreTweetCounter)
    extraParams.setdefault('stop_datetime', '')
    extraParams.setdefault('keep_dom_tweets', False)
    extraParams.setdefault('sleep_sec', 1)


    if( tweetConvMaxTweetCount < 1 ):
        tweetConvMaxTweetCount = 100

    if( finalTweetsColDict is None ):
        finalTweetsColDict = {'tweets': []}
        extraParams['dedup_set'] = set()


    finalTweetsColDictPrevLen = len(finalTweetsColDict['tweets'])

    logger.info( '\ttweet count: ' + str(finalTweetsColDictPrevLen) )
    logger.info( '\tmaxNoMoreTweetCounter: ' + str(maxNoMoreTweetCounter) )
    logger.info( '\ttweetConvMaxTweetCount: ' + str(tweetConvMaxTweetCount) )
    

    try:
        clickShowMore(driver)
        twitterHTMLPage = driver.page_source.encode('utf-8')
        tweets = twitterGetDescendants(twitterHTMLPage, uri=tweetConvURI, extraParams=extraParams)

        #transfer properties - start
        for key, val in tweets.items():
            if( key == 'tweets' or key in finalTweetsColDict ):
                continue
            finalTweetsColDict[key] = val
        #transfer properties - end

        idsToRm = []
        for twt in tweets['tweets']:
            if( twt['data_tweet_id'] in extraParams['dedup_set'] ):
                continue

            #check datetime limit - start
            #stop criteria here takes precedence over tweetConvMaxTweetCount
            if( extraParams['stop_datetime'] != '' ):
                if( isDateRestrict(twt['tweet_time'], extraParams['stop_datetime']) ):
                    continue
            #check datetime limit - end
            
            idsToRm.append( twt['data_tweet_id'] )
            extraParams['dedup_set'].add( twt['data_tweet_id'] )
            finalTweetsColDict['tweets'].append( twt )


        if( len(finalTweetsColDict['tweets']) > tweetConvMaxTweetCount ):
            logger.info('\tinput limit reached: ' + str(tweetConvMaxTweetCount) )
            
            finalTweetsColDict['tweets'] = finalTweetsColDict['tweets'][:tweetConvMaxTweetCount]
            return finalTweetsColDict


        if( finalTweetsColDictPrevLen == len(finalTweetsColDict['tweets']) ):
            maxNoMoreTweetCounter -= 1
        else:
            logger.info( '\tresetting maxNoMoreTweetCounter to: ' + str(maxNoMoreTweetCounter) )
            maxNoMoreTweetCounter = extraParams['max_no_more_tweets_counter']

        if( maxNoMoreTweetCounter < 1 ):
            logger.info( '\tno more tweets, breaking after tweets count: ' + str(len(finalTweetsColDict['tweets'])) )
            return finalTweetsColDict

        '''
        #abandoned after multiple measures to revove tweets (to speed up loading) interferred with
        #the loading of new tweets
        if( extraParams['keep_dom_tweets'] is False ):
            rmDomTweets(driver, extraParams['dedup_set'])
        '''
        
        scrollDown(driver)
        if( extraParams['sleep_sec'] > 0 ):
            logger.info( '\tthrottling, sleeping seconds: ' + str(extraParams['sleep_sec']) )#4 seconds - good, 2,3 - bad
            time.sleep( extraParams['sleep_sec'] )

        recursiveExtractTweetsMain(driver, tweetConvURI, finalTweetsColDict, tweetConvMaxTweetCount, maxNoMoreTweetCounter, extraParams)
    except:
        genericErrorInfo()

    return finalTweetsColDict

def isDateRestrict(tweetTime, limitDatetime):

    try:
        tweetTime = datetime.strptime( tweetTime, '%Y-%m-%dT%XZ' )
        tweetTime = datetimeFromUtcToLocal(tweetTime)
        tweetTime = str( tweetTime )

        if( tweetTime > limitDatetime ):
            return True
        else:
            return False

    except:
        genericErrorInfo()
        return False


#code modified due to DOM change (post 2020-01-27) - start    

def clickShowMore(driver):

    script = '''
        var showMore = document.querySelectorAll( '[aria-label="Timeline: Conversation"]' );
        if( showMore.length != 0 )
        {
            showMore = showMore[0];
            var buttons = showMore.querySelectorAll( '[role="button"]' );

            for(var i=0; i<buttons.length; i++)
            {
                if( buttons[i].innerText.trim().indexOf('more repl') != -1 )
                {
                    buttons[i].click();
                }
            }
        }
    '''
    driver.execute_script(script)

def scrollUp(driver):
    driver.execute_script("window.scrollTo( {'top': 0, 'left': 0, 'behavior': 'smooth'} );")

def scrollDown(driver):
    driver.execute_script("window.scrollTo( {'top': document.body.scrollHeight, 'left': 0, 'behavior': 'smooth'} );")
    #experiment with scrolls, knowing that scrolls affect loading of tweets: driver.execute_script("window.scrollTo( {'top': document.body.scrollHeight/"+ str(factor) +", 'left': 0, 'behavior': 'smooth'} );")
    
def twitterGetTweetIfExist(tweetDiv, uri, getTweetScaffold=False):

    #domGetBasicTweetComps gets data_tweet_id, data_name, data_screen_name, and tweet_time
    tweetDict = domGetBasicTweetComps(tweetDiv, uri)

    if( 'data_tweet_id' not in tweetDict ):
        #Support for old DOM - start
        for attr in ['data_tweet_id', 'data_name', 'data_screen_name']:
            
            if( tweetDiv.has_attr(attr.replace('_', '-')) ):
                tweetDict[attr] = tweetDiv[ attr.replace('_', '-') ]

            if( getTweetScaffold is True ):
                tweetDict[attr] = ''
        #Support for old DOM - end

    if( getTweetScaffold is False and 'data_tweet_id' not in tweetDict ):
        return {}

    tweetDict['tweet_hydrated'] = False
    tweetDict['tweet_text'] = ''
    tweetDict['data_conversation_id'] = ''
    tweetDict['user_verified'] = None
    tweetDict['tweet_stats'] = domGetTweetStats(tweetDiv)
    tweetDict['hashtags'] = []
    tweetDict['data_mentions'] = []

    tweetDict['tweet_links'] = []
    tweetDict['tweet_img_links'] = domGetLinks(tweetDiv)['images']

    tweetDict['extra'] = {}
    
    threadLink = domGetThreadLink(tweetDiv)
    if( threadLink != '' ):
        tweetDict['extra']['thread'] = threadLink
        
    return tweetDict

def twitterGetDescendants(twitterHTMLPage, uri='', extraParams=None):

    if( len(twitterHTMLPage) == 0 ):
        return {}
    
    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('query', '')
    extraParams.setdefault('max_tweets', 20)

    tweetsLst = []
    tweetCounter = 0
    isImplicitThreadPresent = False
    
    soup = BeautifulSoup(twitterHTMLPage, 'html.parser')
    tweets = soup.find_all('article')
    
    #Support for old DOM - start
    if( len(tweets) == 0 ):
        tweets = soup.find_all(class_='tweet')
    #Support for old DOM - end

    for i in range(len(tweets)):
        
        tweetHtml = tweets[i]
        tweets[i] = twitterGetTweetIfExist( tweets[i], uri )
        if( len(tweets[i]) != 0 ):
            tweetsLst.append( tweets[i] )
    
    return { 
        'source': 'Twitter',
        'query': extraParams['query'],
        'max_tweets': extraParams['max_tweets'],
        'tweets': tweetsLst,
        'gen_timestamp': datetime.utcnow().isoformat().split('.')[0] + 'Z'
    }

def markThread(tweetsLst):
    
    if( len(tweetsLst) < 2 ):
        return {}

    report = {}
    threadFlag = False
    nonRootInReplyGroup = False
    rootTweetPos = -1
    alternativeToRootPos = -1
    rootTwt = {}
    replyGroup = []
    replyGroupDedupSet = set()
    twitterIDIndxMap = {}
    
    #find root tweet - start
    for i in range(len(tweetsLst)):
        if( tweetsLst[i]['data_tweet_id'] == tweetsLst[i]['data_conversation_id']  ):

            rootTweetPos = i
            rootTwt = tweetsLst[i]
            break
    
    if( rootTweetPos == -1 ):
        #just in case root tweet is not found, use first tweet as reference to permit creating reply group
        #so reply group may be generated even though it would not be added to the real root tweet
        #if root of real thread not found for some reason, first tweet is likely created by the same author
        rootTwt = tweetsLst[0]
    #find root tweet - end


    #set alternativeToRootPos and twitterIDIndxMap - start
    for i in range(len(tweetsLst)):
        
        if( tweetsLst[i]['data_screen_name'] == rootTwt['data_screen_name'] and alternativeToRootPos == -1  ):
            alternativeToRootPos = i

        #reset states - start
        twitterIDIndxMap[ tweetsLst[i]['data_tweet_id'] ] = i
        if( 'reply_group' in tweetsLst[i]['extra'] ):
            
            for cand in tweetsLst[i]['extra']['reply_group']:                
                
                if( cand['id'] in replyGroupDedupSet ):
                    continue
                
                if( 'conv_root_tweet_id' in cand ):
                    del cand['conv_root_tweet_id']

                replyGroupDedupSet.add(cand['id'])
                replyGroup.append(cand)
            
            del tweetsLst[i]['extra']['reply_group']
        #reset states - end


    #set alternativeToRootPos and twitterIDIndxMap - end


    #create DiGraph with rootTwt as root node - start
    G = nx.DiGraph()
    for i in range(len(tweetsLst)):
        
        #add paths
        twt = tweetsLst[i]
        if( twt['data_screen_name'] == rootTwt['data_screen_name'] and twt['data_tweet_id'] != twt['data_conversation_id'] ):
            G.add_edge( twt['data_tweet_id'], twt['data_conversation_id'] )

    
    #find connected component (thread) in graph
    conComps = list(nx.weakly_connected_components(G))
    for cc in conComps:
        
        if( rootTwt['data_tweet_id'] not in cc ):
            continue

        #here means there exists a connected component of which the rootTwt is a member, aka, a thread might exist
        for twtId in list(cc):
            
            if( twtId not in twitterIDIndxMap ):#skip root node is second condition
                continue
            
            pos = twitterIDIndxMap[twtId]
            if( tweetsLst[pos]['data_screen_name'] != rootTwt['data_screen_name'] ):
                #can't be part of replyGroup thread if tweet from different author
                continue

            #add properties to thread membership
            if( twtId not in replyGroupDedupSet ):
                
                replyGroupDedupSet.add(twtId)
                replyGroup.append( {'id': twtId} )

                if( twtId == rootTwt['data_tweet_id'] ):
                    replyGroup[-1]['conv_root_tweet_id'] = True
                    #CAUTION: include root tweet in reply group: this comes in handy when --find-root-tweet and root changes
                else:
                    nonRootInReplyGroup = True
        break
    #create DiGraph with rootTwt as root node - end

    if( len(replyGroup) != 0 and nonRootInReplyGroup ):

        threadFlag = True
        if( rootTweetPos == -1 ):
            if( alternativeToRootPos != -1 ):
                #This happens when for some reason the root tweet was not in the sequence of tweets so place replyGroup inside first tweet that is not root but part of thread
                tweetsLst[alternativeToRootPos]['extra']['reply_group'] = replyGroup
                report['reply_group_loc'] = alternativeToRootPos
        else:
            tweetsLst[rootTweetPos]['extra']['reply_group'] = replyGroup
            report['reply_group_loc'] = rootTweetPos
    
    
    report['has_single_user_thread'] = threadFlag
    report['con_comp'] = []

    for cc in conComps:
        report['con_comp'].append(list(cc))

    if( 'data_tweet_id' in rootTwt ):
        report['conv_root_tweet_id'] = rootTwt['data_tweet_id']

    return report

#code modified due to DOM change (post 2020-01-27) - end


def rmDomTweets(driver, ids):
   
    ids = ','.join(ids)
    logger.info( 'to REMOVE tweets:' + str(ids) )

    script = '''
        let tweets = document.getElementsByClassName('tweet');
        let idsToRm = "''' + ids + '''";
        idsToRm = new Set( idsToRm.split(',') );
        
        let toRemoveSize = tweets.length - 200;
        for(let i=0; i<toRemoveSize; i++)
        {
            
            let twtId = tweets[i].getAttribute('data-tweet-id');
            //if( idsToRm.indexOf(twtId) != -1 )

            if( idsToRm.has(twtId) == true )
            {
                //method 1
                //tweets[i].parentNode.removeChild( tweets[i] );
                
                let content = tweets[i].getElementsByClassName('content');
                if( content.length != 0 )
                {
                    content = content[0];
                }
                //method 2
                //content.innerHTML = "";
                
                //method 3
                let divs = content.getElementsByTagName('div');
                for(let j=0; j<divs.length; j++)
                {
                    if( divs[j].className != 'stream-item-header' )
                    {
                       divs[j].innerHTML = "";
                    }
                }
            }
        }
    '''
    driver.execute_script(script)

def twitterGetURIDetails(uri):

    uriDets = {}
    uri = uri.split('/status/')

    if( len(uri) == 2 ):
    
        screenName = ''
        screenName = uri[0].split('https://twitter.com/')
        
        if( len(screenName) == 2 ):
            screenName = screenName[1]
        else:
            screenName = ''
        
        if( len(screenName) != 0 ):
            uriDets['screenName'] = screenName
            uriDets['id'] = uri[1]

    return uriDets


def domGetBasicTweetComps(tweetDiv, uri):
    
    '''
        Responsible for setting:
            data_tweet_id
            data_name
            data_screen_name
            tweet_time
    '''
    links = tweetDiv.find_all('a')
    nameCands = {'name': '', 'screenName': ''}
    tweetDict = {}

    for link in links:

        if( link.has_attr('href') is False ):
            continue

        datetime = link.find('time')
        if( datetime is None ):

            link['href'] = link['href'].replace('/', '').strip()
            linkText = link.text.strip()

            if( link['href'] != '' and linkText != '' and nameCands['name'] == '' ):
                #get first non-empty href and non-empty linkText
                nameCands['name'] = linkText.split('@')[0].strip()#conversations (status links) have name@screeName
                nameCands['screenName'] = link['href']
            continue

        if( datetime.has_attr('datetime') is False ):
            continue

        link['href'] = link['href'].strip()
        if( link['href'].startswith('/') ):
            link['href'] = 'https://twitter.com' + link['href']

        tweetComps = parseTweetURI( link['href'] )

        if( tweetComps['screenName'] != '' and tweetComps['id'] != '' and nameCands['screenName'].lower() == tweetComps['screenName'].strip().lower() ):
           
            tweetDict['data_tweet_id'] = tweetComps['id']
            tweetDict['data_name'] = nameCands['name']
            tweetDict['data_screen_name'] = tweetComps['screenName']
            tweetDict['tweet_time'] = datetime['datetime'].split('.')[0].strip() + 'Z'

            break

    if( len(tweetDict) == 0 and nameCands['name'] != '' and nameCands['screenName'] != '' ):
        #Here usually means time absent because the request tweet (supplied) is in focus
        tweetComps = parseTweetURI(uri)
        
        if( tweetComps['screenName'] != '' and tweetComps['id'] != '' and nameCands['screenName'].lower() == tweetComps['screenName'].strip().lower() ):
            tweetDict['data_tweet_id'] = tweetComps['id']
            tweetDict['data_name'] = nameCands['name']
            tweetDict['data_screen_name'] = tweetComps['screenName']
            tweetDict['tweet_time'] = domGetDatetimeForFocusTweet(tweetDiv)

    return tweetDict

def domGetDatetimeForFocusTweet(tweetDiv):

    spans = tweetDiv.find_all('span')
    date = ''
    for span in spans:

        spantext = span.text.strip().lower()
        if( spantext.find(' am') == -1 and spantext.find(' pm') == -1 ):
            continue

        try:
            date = parseDateStr(spantext)
            if( isinstance(date, datetime) ):
                
                date = datetimeFromLocalToUtc(date)    
                date = date.isoformat().split('.')[0] + 'Z'

                break
        except:
            genericErrorInfo()

    return date

def domGetTweetStats( tweetDiv ):

    divs = tweetDiv.find_all('div')
    statsStr = ''
    finalStats = {'reply': 0, 'retweet': 0, 'favorite': 0}

    for div in divs:
        if( div.has_attr('aria-label') and div.has_attr('role') ):
            if( div['role'].strip().lower() == 'group' ):
                
                statsStr = div['aria-label'].lower().strip()
                break

    statsStr = statsStr.split(', ')
    for stat in statsStr:
                
        stat = stat.split(' ')
        if( len(stat) == 2 ):

            stat[1] = stat[1].strip().lower()
            if( stat[0].isnumeric() is True ):

                stat[0] = int(stat[0])

                if( stat[1] == 'reply' or stat[1] == 'replies' ):
                    finalStats['reply'] = stat[0]
                
                elif( stat[1] == 'retweet' or stat[1] == 'retweets' ):
                    finalStats['retweet'] = stat[0]
                
                elif( stat[1] == 'like' or stat[1] == 'likes' ):
                    finalStats['favorite'] = stat[0]

    return finalStats

def domGetLinks(tweetDiv):

    links = tweetDiv.find_all('a')
    allLinks = {'links': [], 'images': []}
    dedupSet = set()

    #currently cannot retrieve embedded tweet link
    for link in links:
        
        if( link.has_attr('href') is False ):
            continue

        link['href'] = link['href'].strip()
        if( link['href'].startswith('https://t.co/') ):
            

            if( link.has_attr('title') ):
                extractedLink = link['title']
            else:
                extractedLink = link['href']

            if( extractedLink not in dedupSet ):
                allLinks['links'].append( {'uri': extractedLink} )
                dedupSet.add( extractedLink )

    
    imgs = tweetDiv.find_all('img')
    for img in imgs:

        if( img.has_attr('src') is False ):
            continue

        img['src'] = img['src'].strip()
        if( img['src'].startswith('https://pbs.twimg.com/media/') is False ):
            continue

        if( img['src'] not in dedupSet ):
            
            allLinks['images'].append( {'uri': img['src']} )
            dedupSet.add( img['src'] )

    return allLinks

def domGetThreadLink(tweetDiv):

    links = tweetDiv.find_all('a')
    
    for link in links:
        
        if( link.has_attr('href') is False ):
            continue

        if( link.text.strip().lower().find('show this thread') != -1 ):

            link['href'] = link['href'].strip()
            if( link['href'].startswith('/') ):
                link['href'] = 'https://twitter.com' + link['href']
            
            return link['href']

    return ''


def domGetTweetTxt(tweetDiv, screenName, name):

    #4th or 5th div containing spans with dir attribute is possibly contains tweet text
    divs = tweetDiv.find_all('div')
    tweetText = ''
    findCount = 0

    for i in range( len(divs) ):
        
        spanCount = len(divs[i].find_all('span'))
        text = divs[i].text.strip()
        
        if( text == '·' ):
            findCount += 1
            continue

        if( text.lower().startswith('replying to') ):
            findCount += 1
            continue

        if( divs[i].has_attr('dir') and spanCount > 0 ):

            if( text == '@' + screenName ):
                findCount += 1
            
            if( text == name ):
                findCount += 1

            if( findCount > 2 ):
                tweetText = text
                break

    return tweetText

def domIsVerifiedAccount(tweetDiv):

    svgs = tweetDiv.find_all('svg')
    
    for svg in svgs:
        if( svg.has_attr('aria-label') ):
            if( svg['aria-label'].lower().find('verified') != -1 ):
                return True

    return False

def domGetHashtags(tweetDiv):

    links = tweetDiv.find_all('a')
    hashtags = []

    for link in links:
        
        if( link.has_attr('href') is False ):
            continue

        if( link['href'].strip().lower().startswith('/hashtag/') is False ):
            continue

        hashtags.append( link.text.strip() )

    return hashtags

def domGetReplyTo(tweetDiv):

    divs = tweetDiv.find_all('div')

    for i in range(len(divs)-1, -1, -1):
        
        div = divs[i]

        if( div.text.strip().lower().find('replying to') != -1 ):
            return domGetTweetMentions(div.text)
            
    return []

def domIsConversation(tweetSoup):

    h2s = tweetSoup.find_all('h2')
    print('domIsConversation:', len(h2s))

    for h2 in h2s:
        
        print('COnv text:', h2.text.strip())

        if( h2.text.strip.lower() == 'thread' ):
            return True

    return False

def domGetTweetMentions(tweetText):
    
    mentions = []    
    
    for menCand in tweetText.split(' '):

        menCand = menCand.strip()
        if( menCand.startswith('@') ):
            mentions.append(menCand[1:])

    return mentions


def isTweetPresent(soup):
    
    logger.info('\t\tisTweetPresent()')
    tweets = soup.findAll('div', {'class': 'tweet'})
    if( len(tweets) == 0 ):
        return ''

    for tweet in tweets:
        if( tweet.has_attr('data-permalink-path') ):
            tweetPath = tweet['data-permalink-path'].strip()
            if( len(tweetPath) != 0 ):
                return tweetPath

    return ''

def optIsURIInTweet(link, maxSleep=3):

    logger.info('\noptIsURIInTweet()')

    urir = getURIRFromMemento(link)
    if( len(urir) != 0 ):
        logger.info('\t\turi-r extracted from memento link, to be checked in tweet index')
        link = urir

    tweetPath = ''

    for urlPrefix in ['url:', '']:
        
        logger.info('\t\turi prefix: ' + urlPrefix)

        uri = 'https://twitter.com/search?f=tweets&q=' + quote_plus(urlPrefix + link) + '&src=typd'
        htmlPage = derefURI(uri, maxSleep)
        soup = BeautifulSoup( htmlPage, 'html.parser' )
        tweetPath = isTweetPresent(soup)

        if( len(tweetPath) != 0 ):
            break

    return tweetPath

def isURIInTweet(link, driver=None, closeBrowserFlag=True, chromedriverPath='/usr/bin/chromedriver'):

    logger.info('\nisURIInTweet()')

    urir = getURIRFromMemento(link)
    if( len(urir) != 0 ):
        logger.info('\t\turi-r extracted from memento link, to be checked in tweet index')
        link = urir

    tweetPath = ''
    if( driver is None ):
        
        try:
            driver = getChromedriver(chromedriverPath)
        except:
            genericErrorInfo()
            return ''

    for urlPrefix in ['url:', '']:
        logger.info('\t\turi prefix: ' + urlPrefix)
        
        uri = 'https://twitter.com/search?f=tweets&q=' + quote_plus(urlPrefix + link) + '&src=typd'
        htmlPage = seleniumLoadWebpage(driver, uri, waitTimeInSeconds=1, closeBrowerFlag=False)
        soup = BeautifulSoup( htmlPage, 'html.parser' )
        tweetPath = isTweetPresent(soup)

        if( len(tweetPath) != 0 ):
            break

    if( closeBrowserFlag == True ):
        driver.quit()

    return tweetPath

def getArgs():

    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))
    parser.add_argument('query', help='Twitter search query or Twitter URL')
    
    parser.add_argument('-d', '--max-file-depth', help='When reading files recursively from directory stop at the specified path depth. 0 means no restriction', type=int, default=1)
    parser.add_argument('-l', '--latest', help='Search Twitter Latest vertical (default is False)', action='store_true')#default false
    parser.add_argument('-m', '--max-tweets', help='Maximum number of tweets to collect', type=int, default=20)
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-s', '--sleep-sec', help='For search throttling process: maximum number or seconds to sleep between adjacent searches', type=int, default=2)
    
    parser.add_argument('--cache-path', help='Path to save tweets (single and/or conversation)', default='')
    parser.add_argument('--cache-read', help='Switch on reading cache for conversations', action='store_true')
    parser.add_argument('--cache-write', help='Switch on writing cache', action='store_true')
    
    parser.add_argument('--chromedriver-path', help='Path to chromedriver')
    parser.add_argument('--delay-sec', help='Delay by set value before extracting tweets', type=int, default=5)
    parser.add_argument('--delay-sec-after', help='Delay by set value after extracting tweets', type=int, default=0)
    parser.add_argument('--expand', help='Expand tweets from SERP by extracting links from conversation tweets', action='store_true')
    parser.add_argument('--find-root-tweet', help='For threads (conversations): find root tweet when absent from list of collected tweets', action='store_true')
    parser.add_argument('--hydrate-files', help='Instead of searching, hydrate JSON files that have mininum of data_tweet_id', action='store_true')#default false
    parser.add_argument('--hydrate-q-size', help='Number of tweet hydrate requests to issue (per second) to statuses/lookup, see: https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-lookup', type=int, default=100)
    parser.add_argument('--hydrate-sleep-sec', help='Tweet hydrate throttling mechanism; sleep by set value', type=int, default=1)
    parser.add_argument('--no-hydrate-tweets', help='Do not hydrate tweets', action='store_true')
    parser.add_argument('--search-uri-key', help='Search with uri, NOT query. Extract tweets with uri', default='')
    parser.add_argument('--keep-dom-tweets', help='Do not remove tweets from DOM', action='store_true')

    parser.add_argument('--access-token', help='Twitter API info needed for hydrating tweets', default='')
    parser.add_argument('--access-token-secret', help='Twitter API info needed for hydrating tweets', default='')
    parser.add_argument('--consumer-key', help='Twitter API info needed for hydrating tweets', default='')
    parser.add_argument('--consumer-secret', help='Twitter API info needed for hydrating tweets', default='')

    parser.add_argument('--log-file', help='Log output filename', default='')
    parser.add_argument('--log-format', help='Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html', default='')
    parser.add_argument('--log-level', help='Log level', choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'], default='info')

    parser.add_argument('--max-no-more-tweets-counter', help='Maximum number of times to retry getting tweets before declaring: no more tweets', type=int, default=4)
    parser.add_argument('--max-reply-count', help='Maximum number of tweet replies to collect (for --expand)', type=int, default=5)
    parser.add_argument('--no-add-hydrated-tweet-json', help='Do not add raw tweet (hydrated tweet) JSON to extracted tweets', action='store_true')
    parser.add_argument('--no-check-reply-count', help='Do not check if tweets have replies before attempting to expand', action='store_true')
    parser.add_argument('--no-redact-keys', help='Do not redact consumer-key/secret access-token/secret', action='store_true')
    parser.add_argument('--pretty-print', help='Pretty print JSON output', action='store_true')
    parser.add_argument('--stop-datetime', help='Collect tweets with datetime < local stop-datetime (format: YYYY-MM-DD HH:MM:SS)', default='')
    parser.add_argument('--thread-count', help='Maximum number of threads to use for parallel operations', type=int, default=5)   
    
    parser.add_argument('--window-width', help='Browser window width', type=int, default=400)
    parser.add_argument('--window-height', help='Browser window height', type=int, default=1500)

    return parser

def procReq(params):
    
    serp = twitterSearch(
        chromedriverPath=params['chromedriver_path'], 
        query=params['query'], 
        maxTweetCount=params['max_tweets'],
        latestVertical=params['latest'],
        extraParams=params
    )

    if( 'dedup_set' in params ):
        del params['dedup_set']
        
    serp['extra_params'] = params

    printPayload('twitter', serp)
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

    params['cache'] = {
        'cache_path': params.pop('cache_path'),
        'cache_read': params.pop('cache_read'),
        'cache_write': params.pop('cache_write')
    }

    procReq(params)

if __name__ == 'scraper.Twitter':

    from scraper.ScraperUtil import datetimeFromLocalToUtc
    from scraper.ScraperUtil import datetimeFromUtcToLocal
    from scraper.ScraperUtil import derefURI
    from scraper.ScraperUtil import dumpJsonToFile
    from scraper.ScraperUtil import expandUrl
    from scraper.ScraperUtil import getChromedriver
    from scraper.ScraperUtil import genericErrorInfo
    from scraper.ScraperUtil import getDictFromFile
    from scraper.ScraperUtil import getDictFromJson
    from scraper.ScraperUtil import getDictFromJsonGZ
    from scraper.ScraperUtil import getURIRFromMemento
    from scraper.ScraperUtil import gzipTextFile
    from scraper.ScraperUtil import naiveIsURIShort
    from scraper.ScraperUtil import parallelTask
    from scraper.ScraperUtil import printPayload
    from scraper.ScraperUtil import readTextFromFilesRecursive
    from scraper.ScraperUtil import seleniumLoadWebpage
    from scraper.ScraperUtil import setLogDefaults
    from scraper.ScraperUtil import setLoggerDets
    from scraper.ScraperUtil import sortDctByKey
    from scraper.ScraperUtil import valueToFloat

else:

    from ScraperUtil import datetimeFromLocalToUtc
    from ScraperUtil import datetimeFromUtcToLocal
    from ScraperUtil import derefURI
    from ScraperUtil import dumpJsonToFile
    from ScraperUtil import expandUrl
    from ScraperUtil import getChromedriver
    from ScraperUtil import genericErrorInfo
    from ScraperUtil import getDictFromFile
    from ScraperUtil import getDictFromJson
    from ScraperUtil import getDictFromJsonGZ
    from ScraperUtil import getURIRFromMemento
    from ScraperUtil import gzipTextFile
    from ScraperUtil import naiveIsURIShort
    from ScraperUtil import parallelTask
    from ScraperUtil import printPayload
    from ScraperUtil import readTextFromFilesRecursive
    from ScraperUtil import seleniumLoadWebpage
    from ScraperUtil import setLogDefaults
    from ScraperUtil import setLoggerDets
    from ScraperUtil import sortDctByKey
    from ScraperUtil import valueToFloat
       
    if __name__ == '__main__':    
        main()
