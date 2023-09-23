from datetime import datetime

def twitterGetDeg1Sub0(segCol, keyID, tweets, colSrc, dedupSet, provenance):

    verbose = False
    for tweet in tweets:
        if( len(tweet['tweet_links']) == 0 ):
            continue

        if( keyID == tweet['data_tweet_id'] ):

            prevSize = len(segCol)
            tweet['provenance'] = provenance
            tweet['thread_pos'] = 0
            twitterPopulateSeg(
                segCol, 
                None, 
                tweet, 
                colSrc,
                dedupSet
            )

            if( prevSize != len(segCol) and verbose):
                print('\t\t\tSuccess in adding deg link')
            
            return True

    return False

def twitterGetDeg1(segCol, uri, colKind, repo, colSrc, dedupSet):

    verbose = False
    uri = uri.strip()
    colKind = colKind.strip()
    uriDct = parseTweetURI(uri)

    if( len(uri) == 0 or len(colKind) == 0 or len(repo) == 0 or len(uriDct['id']) == 0 ):
        return False

    for rep in repo:
        for tweetCol in rep['tweet_links']:
            
            if( 'output' not in tweetCol ):
                continue

            if( len(tweetCol['output']) == 0 ):
                continue

            if( tweetCol['output']['self'] != uri ):
                continue

            provenance = {'parent': {'uri': tweetCol['parent']}}
            foundFlag = twitterGetDeg1Sub0( segCol, uriDct['id'], tweetCol['output']['tweets'], colSrc, dedupSet, provenance )
            if( foundFlag ):
                
                if( verbose ):
                    print('\t\tfound expanded deg 1 twt:', uri)

                return True
    
    return False

def twitterGetPstDets(pst, src):
    if( len(pst) == 0 ):
        return {}

    tmp = {}
    try:
        tmp['id'] = pst['data_tweet_id']
        tmp['parent_id'] = ''

        if( tmp['id'] != pst['data_conversation_id'] ):
            tmp['parent_id'] = pst['data_conversation_id']

        tmp['author'] = pst['data_screen_name']
        tmp['uri'] = getTweetLink(tmp['author'], tmp['id'])
        tmp['src'] = src
        tmp['creation_date'] = ''
        tmp['provenance'] = pst['provenance']

        tmp['substitute_text'] = pst['tweet_text'].strip()
        try:
            tmp['creation_date'] = pst['tweet_time']
            #new
            #tmp['creation_date'] = datetime.strptime(pst['tweet_time'], '%Y-%m-%dT%H:%M:%SZ')
            #tmp['creation_date'] = str( datetimeFromUtcToLocal(tmp['creation_date']) )
        except:
            genericErrorInfo( '\ttweet: ' + str(pst) )

    except:
        genericErrorInfo('\t\tError dets: ' + src + ', ' + pst['data_tweet_id'])

    return tmp

def twitterPopulateSeg(container, localDeg1Col, tweet, colSrc, dedupSet):
    
    pstDet = twitterGetPstDets(tweet, colSrc)
    pstDet['post_uri_type'] = 'tweet'

    for uriDets in tweet['tweet_links']:

        uri = uriDets['uri']
        uriKey = getDedupKeyForURI(uri)
        if( uriKey in dedupSet ):
            continue

        dedupSet.add(uriKey)
        #print('key ' * 4, pstDet.keys())
        uriType = getGenericURIType( uri, pstDet['uri'], 'twitter.com' )
        uriDct = {
            'uri': uri,
            'domain': getDomain(uri),
            'salams_policies': {},
            'quality_proxy_vectors': {},
            'post_details': pstDet, 
            'custom': {'uri_type': uriType, 'is_short': naiveIsURIShort(uri)}
        }

        if( 'quality_proxy_vectors' in uriDets ):
            uriDct['quality_proxy_vectors'] = uriDets['quality_proxy_vectors']
        
        #uriType options: internal_self, internal_degree_1, external
        if( uriType == 'internal_degree_1' ):
            if( localDeg1Col is not None ):
                localDeg1Col.append(uriDct)
        elif( uriType == 'external' ):
            #don't add self link, but may add links embeded in the post
            container.append(uriDct)

def twitterAddRootCol(segCol, post, deg1Container, colSrc, singleSegIndx=-1, extraParams=None):

    if( extraParams == None ):
        extraParams = {}

    if( 'deg1ColRepo' not in extraParams ):
        extraParams['deg1ColRepo'] = {}

    if( 'colKind' not in extraParams ):
        extraParams['colKind'] = ''

    if( 'dedupSet' not in extraParams ):
        extraParams['dedupSet'] = set()

    
    if( singleSegIndx != -1 and singleSegIndx < len(segCol) ):
        singleSegCol = segCol[singleSegIndx]
    else:
        singleSegCol = {}
    

    singleSegCol.setdefault('uris', [])
    singleSegCol.setdefault('stats', {})
    #addition into seg takes place in twitterPopulateSeg and twitterGetDeg1 for deg 1 links
    localDeg1Col = []
    twitterPopulateSeg(
        singleSegCol['uris'], 
        localDeg1Col, 
        post, 
        colSrc,
        extraParams['dedupSet']
    )

    #handle degree-1 col - start
    #crucial this block is here
    for deg1UriDct in localDeg1Col:

        deg1Container.append( deg1UriDct )
        found = twitterGetDeg1(singleSegCol['uris'], deg1UriDct['uri'], extraParams['colKind'], extraParams['deg1ColRepo'], colSrc, extraParams['dedupSet'])
        
        #if( found ):
        #   print('\tsucceed in extracting expanded deg1: consider not adding deg1UriDct into deg1Container when provenance implemented')
    #handle degree-1 col - end
    
    if( len(singleSegCol['uris']) != 0 and singleSegIndx == -1 ):
        #case where root post is added for the first time, this case is false (singleSegIndx != -1)
        #when a uri from a comment is to be added to singleSegCol which is already in segCol
        singleSegIndx = len(segCol)
        segCol.append( singleSegCol )


    singleSegCol['stats']['uri_count'] = len(singleSegCol['uris'])
    return singleSegIndx

def twitterSSColAdd(src, container, colSrc, deg1ColRepo):

    colKind = 'ss'

    extraParams = {}
    extraParams['colKind'] = colKind
    extraParams['deg1ColRepo'] = deg1ColRepo
    extraParams['dedupSet'] = set()
    
    for post in src['tweets']:
        
        if( len(post['tweet_links']) == 0 ):
            continue

        post['thread_pos'] = 0
        singleSegIndx = twitterAddRootCol(
            container['segmented_cols'][colKind], 
            post, 
            container['segmented_cols']['degree_1'][colKind], 
            colSrc,
            extraParams=extraParams
        )

        if( singleSegIndx != -1 ):
            container['segmented_cols'][colKind][singleSegIndx]['stats']['total_posts'] = 1


def msGetRootTweetDets(tweet, respType):

    if( len(tweet) == 0 ):
        return {}

    if( 'reply_group' in tweet['extra'] ):
        selfLink = 'https://twitter.com/' + tweet['data_screen_name'] + '/status/' + tweet['data_tweet_id']

        #label membership - start
        ids = set([ id['id'] for id in tweet['extra']['reply_group'] ])
        for i in range( len(tweet[respType]['tweets']) ):
            
            twt = tweet[respType]['tweets'][i]
            if( twt['data_tweet_id'] in ids ):
                twt['extra']['in_thread'] = True
            else:
                twt['extra']['in_thread'] = False
        #label membership - end

        return {
            'self': selfLink,
            'root': tweet,
            'replyGroup': tweet['extra']['reply_group'],
            'replyGroupTweets': tweet[respType],
            'addRefererTweet': False#Container is root so it'll be added
        }


    if( 'reply_group_loc' in tweet[respType] ):
        
        indx = tweet[respType]['reply_group_loc']
        if( indx < len(tweet[respType]['tweets']) ):

            rootTwt = tweet[respType]['tweets'][indx]

            if( 'reply_group' in rootTwt['extra'] ):

                selfLink = 'https://twitter.com/' + rootTwt['data_screen_name'] + '/status/' + rootTwt['data_tweet_id']
                addRefererTweet = False

                #label membership - start
                ids = set([ id['id'] for id in rootTwt['extra']['reply_group'] ])
                if( tweet['data_tweet_id'] in ids ):
                    addRefererTweet = True

                for i in range( len(tweet[respType]['tweets']) ):
                    
                    twt = tweet[respType]['tweets'][i]
                    if( twt['data_tweet_id'] in ids ):
                        twt['extra']['in_thread'] = True
                    else:
                        twt['extra']['in_thread'] = False
                #label membership - end
                
                return {
                    'self': selfLink,
                    'root': rootTwt,
                    'replyGroup': rootTwt['extra']['reply_group'],
                    'replyGroupTweets': tweet[respType],
                    'addRefererTweet': addRefererTweet
                }

    return {}



def twitterMSColAdd(src, container, colSrc, deg1ColRepo):
    

    '''
        structure of response  tweet 
        
        case 1: when tweet is the root node (data_tweet_id = data_conversation_id)
        tweet_x
        {   
            reply_group present if thread ms (multiple connected posts (connected comps with root node) from the same user present)
            tweet_replies
            {
            
            }
        }
        
        case 2: when tweet is not root node (data_tweet_id ≠ data_conversation_id). This can happen if a child tweet_y (e.g., https://twitter.com/WHO/status/1227661054492205056) from ms tweets is used to extract the tweets instead of the parent tweet (https://twitter.com/WHO/status/1227657276703428608).
        tweet_y
        {
            tweet_thread
            {
                reply_group: presence indicated by has_single_user_thread flag. tweet_y's id could be in the reply_group if it is a member of the ms chain
            }
        }
    '''
    colKind = 'ms'

    extraParams = {}
    extraParams['colKind'] = colKind
    extraParams['deg1ColRepo'] = deg1ColRepo
    extraParams['dedupSet'] = set()

    for i in range( len(src['tweets']) ):

        threadCol = src['tweets'][i]

        if( 'tweet_replies' in threadCol ):
            respType = 'tweet_replies'
        elif( 'tweet_thread' in threadCol ):
            respType = 'tweet_thread'
        else:
            respType = 'NONE'

        if( respType not in threadCol ):
            continue

        if( threadCol[respType]['stats']['total_links'] == 0 ):
            continue

    
        rootDets = msGetRootTweetDets(threadCol, respType)
        if( len(rootDets) == 0 ):
            continue
        
        containerPrevSize = len(container['segmented_cols'][colKind])
        
        singleSegIndx = twitterAddRootCol(
            container['segmented_cols'][colKind], 
            rootDets['root'], 
            container['segmented_cols']['degree_1'][colKind], 
            colSrc,
            extraParams=extraParams
        )

        for j in range( len(rootDets['replyGroupTweets']['tweets']) ):
            
            memb = rootDets['replyGroupTweets']['tweets'][j]

            if( memb['extra']['in_thread'] is False ):
                continue
            
            if( len(memb['tweet_links']) == 0 ):
                continue

            singleSegIndx = twitterAddRootCol(
                container['segmented_cols'][colKind], 
                memb, 
                container['segmented_cols']['degree_1'][colKind], 
                colSrc + '_thread',
                singleSegIndx=singleSegIndx,
                extraParams=extraParams
            )

        if( rootDets['addRefererTweet'] ):

            singleSegIndx = twitterAddRootCol(
                container['segmented_cols'][colKind], 
                threadCol, 
                container['segmented_cols']['degree_1'][colKind], 
                colSrc + '_thread',
                singleSegIndx=singleSegIndx,
                extraParams=extraParams
            )
        

        
        if( containerPrevSize != len(container['segmented_cols'][colKind]) and 'reply_group' in rootDets['root']['extra'] ):
            #note that tweet without links have been removed
            container['segmented_cols'][colKind][-1]['stats']['total_posts'] = len(rootDets['root']['extra']['reply_group'])
            
            if( rootDets['addRefererTweet'] ):
                container['segmented_cols'][colKind][-1]['stats']['total_posts'] += 1

def twitterMMColAdd(src, container, colSrc, deg1ColRepo):

    colKind = 'mm'
    #this function is essentially twitterMS without check for 
    #thread and if tweet is a member of explicit, implicit class

    extraParams = {}
    extraParams['colKind'] = colKind
    extraParams['deg1ColRepo'] = deg1ColRepo
    extraParams['dedupSet'] = set()

    for i in range( len(src['tweets']) ):
        
        threadCol = src['tweets'][i]
        
        if( 'tweet_replies' in threadCol ):
            respType = 'tweet_replies'
        elif( 'tweet_thread' in threadCol ):
            respType = 'tweet_thread'
        else:
            respType = 'NONE'

        if( respType not in threadCol ):
            continue

        if( threadCol[respType]['stats']['total_links'] == 0 ):
            continue

        containerPrevSize = len(container['segmented_cols'][colKind])
        singleSegIndx = twitterAddRootCol(
            container['segmented_cols'][colKind], 
            threadCol, 
            container['segmented_cols']['degree_1'][colKind], 
            colSrc,
            extraParams=extraParams
        )
        

        for j in range( len(threadCol[respType]['tweets']) ):
            
            memb = threadCol[respType]['tweets'][j]            
            if( len(memb['tweet_links']) == 0 ):
                continue

            singleSegIndx = twitterAddRootCol(
                container['segmented_cols'][colKind], 
                memb, 
                container['segmented_cols']['degree_1'][colKind], 
                colSrc + '_thread',
                singleSegIndx=singleSegIndx,
                extraParams=extraParams
            )

        if( containerPrevSize != len(container['segmented_cols'][colKind]) ):
            #count addition of root post and maximum possible elements added to singleSegCol
            #note that tweet without links have been removed so use total tweets
            container['segmented_cols'][colKind][-1]['stats']['total_posts'] = 1 + threadCol[respType]['stats']['total_tweets']

if __name__ == 'scraper.TwitterUtil.mcTwitter':
    
    from scraper.ScraperUtil import datetimeFromUtcToLocal
    from scraper.ScraperUtil import dumpJsonToFile
    from scraper.ScraperUtil import genericErrorInfo
    from scraper.ScraperUtil import getDedupKeyForURI
    from scraper.ScraperUtil import getDomain
    from scraper.ScraperUtil import getTweetLink
    from scraper.ScraperUtil import naiveIsURIShort
    from scraper.ScraperUtil import parseTweetURI
    from scraper.ScraperUtil import getGenericURIType

else:

    from ScraperUtil import datetimeFromUtcToLocal
    from ScraperUtil import dumpJsonToFile
    from ScraperUtil import genericErrorInfo
    from ScraperUtil import getDedupKeyForURI
    from ScraperUtil import getDomain
    from ScraperUtil import getTweetLink
    from ScraperUtil import naiveIsURIShort
    from ScraperUtil import parseTweetURI
    from ScraperUtil import getGenericURIType