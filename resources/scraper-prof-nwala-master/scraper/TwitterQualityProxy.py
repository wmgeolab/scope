import argparse
import googlemaps
import json
import logging
import os
import sys


from bs4 import BeautifulSoup
from subprocess import check_output
from copy import deepcopy
from os import makedirs
from fake_useragent import UserAgent

logger = logging.getLogger('scraper.scraper')

def expandOrMarkShortURIs(tweets, extraParams):

    if( 'tweets' not in tweets ):
        return

    extraParams.setdefault('no_expand_short_uri', False)
    extraParams.setdefault('thread_count', 5)

    logger.info('\nexpandOrMarkShortURIs()')
    jobLst = []
    for i in range( len(tweets['tweets']) ):

        tweet = tweets['tweets'][i]
        for j in range( len(tweet['tweet_links']) ):
            
            if( 'short_uri' in tweet['tweet_links'][j] ):
                continue

            link = tweet['tweet_links'][j]['uri']

            if( naiveIsURIShort(link) ):
                if( extraParams['no_expand_short_uri'] is False ):
                    logger.info('\tgenPopMatInpFrmTwts(): expanding short URI: ' + link)
                    
                    keywords = {
                        'url': link
                    }
                    jobLst.append( {'func': expandUrl, 'args': keywords, 'misc': {'i': i, 'j': j, 'link': link} } )

                    if( 'is_short_uri' in tweet['tweet_links'][j] ):
                        del tweet['tweet_links'][j]['is_short_uri']
                else:
                    tweet['tweet_links'][j]['is_short_uri'] = True

    if( len(jobLst) != 0 ):
    
        resLst = parallelTask(jobLst, threadCount=extraParams['thread_count'])
        for rs in resLst:
            
            i = rs['misc']['i']
            j = rs['misc']['j']
            tweets['tweets'][i]['tweet_links'][j]['uri'] = rs['output']
            tweets['tweets'][i]['tweet_links'][j]['short_uri'] = rs['misc']['link']

    
    #mark tweets with twitter links exclusively - start
    for i in range( len(tweets['tweets']) ):
        
        tweet = tweets['tweets'][i]
        #find non-twitter link        
        exclusivelyTwitterLinksFlag = True
        size = len(tweet['tweet_links'])
        for j in range(size):

            uri = tweet['tweet_links'][j]['uri']

            if( getDomain(uri, includeSubdomain=False) not in ['twimg.com', 'twitter.com'] ):
                exclusivelyTwitterLinksFlag = False
                break

        if( exclusivelyTwitterLinksFlag and size != 0 ):
            tweet['extra']['twitter_links_exclusively'] = True
    #mark tweets with twitter links exclusively - end

def getChildrenTweets(tweets):

    childTweets = {'tweets': []}
    
    if( 'tweets' not in tweets ):
        return childTweets
    
    for i in range( len(tweets['tweets']) ):
        
        tweet = tweets['tweets'][i]
        lstName = getTweetLstName( tweet )
        if( lstName == '' ):
            continue

        if( 'tweets' not in tweet[lstName] ):
            continue
            
        for chd in tweet[lstName]['tweets']:
            
            if( 'tweet_hydrated' not in chd ):
                continue

            if( chd['tweet_hydrated'] is False ):
                continue

            childTweets['tweets'].append(chd)

    return childTweets

def getTwitterAuthorDets(tweet):

    if( len(tweet) == 0 ):
        return {}

    authorDet = {
        'handle': tweet['data_screen_name'],
        'tweets': tweet['extra']['raw_json']['user']['statuses_count'],
        'followers': tweet['extra']['raw_json']['user']['followers_count'],
        'following': tweet['extra']['raw_json']['user']['friends_count'],
        'favorites': tweet['extra']['raw_json']['user']['favourites_count'],
        'location': tweet['extra']['raw_json']['user']['location'],
        'website': {'uri': ''},
        'bio': tweet['extra']['raw_json']['user']['description']
    }

    if( tweet['extra']['raw_json']['user']['url'] is not None ):
        if( len(tweet['extra']['raw_json']['user']['entities']['url']['urls']) != 0 ):
            authorDet['website']['uri'] = tweet['extra']['raw_json']['user']['entities']['url']['urls'][0]['expanded_url']

    return authorDet

def getTwitterHandlesFrmPage(link, searchGoogle=True, maxSleepInSeconds=0):

    link = link.strip()
    handles = {'handles': [], 'provenance': {}}
    if( len(link) == 0 ):
        return handles

    html = derefURI(link, maxSleepInSeconds)
    if( len(html) == 0 ):
        return handles

    links = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
    except:
        genericErrorInfo()


    if( len(links) != 0 ):
        handles = getHandlesFrmLnks(links)
        

    if( len(handles['handles']) == 0 and searchGoogle is True ):
        
        serp = googleSearch(link + ' twitter handle')
        if( 'links' in serp ):
            for i in range( len(serp['links']) ):
                serp['links'][i]['href'] = serp['links'][i]['link']

            handles = getHandlesFrmLnks( serp['links'] )
            for handle, src in handles['provenance'].items():
                handles['provenance'][handle] = 'google => ' + src
    

    return handles

def accumulateDomain(excludeDomains, tweets):
    
    logger.info('\naccumulateDomain()')

    domainsDct = {}

    for twt in tweets:

        if( len(twt['tweet_links']) == 0 ):
            continue

        if( 'twitter_links_exclusively' in twt['extra'] ):
            if( twt['extra']['twitter_links_exclusively'] ):
                continue

        for i in range( len(twt['tweet_links']) ):
            
            link = twt['tweet_links'][i]['uri']

            if( getDomain(link, includeSubdomain=False) in excludeDomains ):
                logger.info('\tgenPopMatInpFrmTwts(): skipping excluded domain, URI: ' + link)
                continue

            if( 'is_short_uri' in twt['tweet_links'][i] ):
                logger.info('\tgenPopMatInpFrmTwts(): skipping short URI: ' + link)
                continue
            
            domain = getDomain(link, includeSubdomain=False)
            domainsDct.setdefault(domain, 
            {
                'domain_handle': '',
                'domain_handle_location': '',
                'link': link
            })

    return domainsDct

def extractTwitterHandlesFrmWebsite(tweets, domainsDct, extraParams=None):

    logger.info('\nextractTwitterHandlesFrmWebsite()')

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('cache_path', '')
    extraParams.setdefault('no_google_twitter_handle', False)
    extraParams.setdefault('thread_count', 5)

    extraParams.setdefault('consumer_key', '')
    extraParams.setdefault('consumer_secret', '')
    extraParams.setdefault('access_token', '')
    extraParams.setdefault('access_token_secret', '')
    
    tweets.setdefault('website_handles', {})
    websiteHandlesForHydration = []
    hydratedUsers = {}

    if( extraParams['no_google_twitter_handle'] is False ):
        searchGoogle = True
    else:
        searchGoogle = False

    '''
        Steps summary: (needs update)
        step 1: attempt to read website_handles from cache
        step 2: attempt getting all twitter handles found on homepage of website
        step 3: attempt getting twitter author profile details for handles found from the websites in step 2
        step 4: set followers following counts from the author profiles extracted in step 3
    '''

    if( extraParams['cache_path'] != '' ):
        
        #step 1
        #attempt to read website_handles from cache - start


        for domain in domainsDct:
            
            domFilename = extraParams['cache_path'] + 'WebsiteHandles/' + domain + '.json.gz'
            if( os.path.exists(domFilename) ):
                tweets['website_handles'][domain] = getDictFromJsonGZ(domFilename)

        #attempt to read website_handles from cache - end


    #step 2
    #attempt getting all twitter handles found on homepage of website - start
    jobLst = []
    for domain, domDct in domainsDct.items():
        
        if( domain == '' ):
            continue

        if( domain in tweets['website_handles'] ):
            continue

        homepage = domDct['link'].split(domain)[0] + domain + '/'
        toPrint = '\tgetTwitterHandlesFrmPage - domain: ' + domain + ', \n\thomepage: ' + homepage + ', ' + str(len(jobLst)) + ' of max: ' + str(len(domainsDct))

        keywords = {
            'link': homepage,
            'searchGoogle': searchGoogle,
            'maxSleepInSeconds': 0
        }
        
        jobLst.append( {'func': getTwitterHandlesFrmPage, 'args': keywords, 'misc': domain, 'print': toPrint} )
    #attempt getting all twitter handles found on homepage of website - end


    #step 3
    #attempt getting twitter author details for handles found - start

    jobLstSize = len(jobLst)
    if( jobLstSize != 0 ):

        resLst = parallelTask(jobLst, threadCount=extraParams['thread_count'])
        jobLst = [] 
        for rs in resLst:
            
            domain = rs['misc']
            websiteTwitterHandles = rs['output']['handles']
            websiteTwitterHandleProv = rs['output']['provenance']

            if( len(websiteTwitterHandles) == 0 ):
                continue

            if( 'website_handles' in tweets ):
                if( domain in tweets['website_handles'] ):
                    continue

            websiteTwitterHandles =  [handle.lower() for handle in websiteTwitterHandles]
            websiteHandlesForHydration += websiteTwitterHandles
            domainsDct[domain]['domain_handle'] = websiteTwitterHandles
            domainsDct[domain]['domain_handle_provenance'] = websiteTwitterHandleProv
    
    if( len(websiteHandlesForHydration) != 0 ):
        hydratedUsers = hydrateUsers(websiteHandlesForHydration, params=extraParams)
    #attempt getting twitter author details for handles found - end
    

    #step 4
    #set followers following counts from the author profiles extracted - start

    for domain, domDct in domainsDct.items():
        
        websiteTwitterHandles = domainsDct[domain]['domain_handle']
        firstValidWebsiteHandleProfile = {}

        for websiteHandle in websiteTwitterHandles:
            
            if( websiteHandle not in hydratedUsers ):
                continue

            if( len(hydratedUsers[websiteHandle]) == 0 ):
                continue


            firstValidWebsiteHandleProfile = hydratedUsers[websiteHandle]
            #validate bidirectional link: does twitter handle profile point to website domain?
            isValidBil = isValidBiLink( firstValidWebsiteHandleProfile, domain )

            if( isValidBil is True ):

                tweets['website_handles'][domain] = firstValidWebsiteHandleProfile
                tweets['website_handles'][domain]['qp_cache'] = {}

                tweets['website_handles'][domain]['domain'] = domain
                tweets['website_handles'][domain]['domain_handle_cands'] = websiteTwitterHandles
                
                #valid profile has been found, no need to proceed to check other profiles
                break
            else:
                tweets['website_handles'][domain] = {}
                tweets['website_handles'][domain]['domain'] = domain
                tweets['website_handles'][domain]['domain_handle_cands'] = websiteTwitterHandles

                tweets['website_handles'][domain].setdefault('invalid_profile', [])
                tweets['website_handles'][domain]['invalid_profile'].append(firstValidWebsiteHandleProfile)

            

    #copy existing from cache within tweets
    if( 'website_handles' in tweets ):
        
        makedirs( extraParams['cache_path'] + 'WebsiteHandles/' , exist_ok=True )

        for domain, websiteTwitProfile in tweets['website_handles'].items():

            #attempt to write website_handles into cache - start
            domFilename = extraParams['cache_path'] + 'WebsiteHandles/' + domain + '.json.gz'
            if( os.path.exists(domFilename) == False ):
                gzipTextFile(domFilename, json.dumps(websiteTwitProfile, ensure_ascii=False))
            #attempt to write website_handles into cache - end

    #set followers following counts from the author profiles extracted - end
   

def isValidBiLink(websiteTwitterProfileDets, domain):

    try:
       
        profileURL = websiteTwitterProfileDets['entities']['url']['urls']
        if( len(profileURL) != 0 ):
            
            profileURL = profileURL[0]['expanded_url']
            if( getDomain(profileURL, includeSubdomain=False).strip().lower() != domain.strip().lower() ):
                #no bidirectional link
                return False

    except:
        genericErrorInfo()
        return False

    return True

def normalizeLoc(loc, googlemapsKey):

    loc = loc.strip()
    googlemapsKey = googlemapsKey.strip()
    normalizedLocation = {'location_name': loc, 'coordinates': {}}

    if( loc == '' or googlemapsKey == '' ):
        return normalizedLocation

    places = []
    try:
        gmaps = googlemaps.Client(key=googlemapsKey)
        places = gmaps.places(loc)
    except:
        genericErrorInfo()

    if( len(places) == 0 ):
        return normalizedLocation

    if( 'results' in places ):
        if( len(places['results']) == 1 ):

            try:
                normalizedLocation['location_name'] = places['results'][0]['formatted_address']
                normalizedLocation['coordinates'] = places['results'][0]['geometry']['location']
            except:
                genericErrorInfo()

    return normalizedLocation

def addSingleLocation(tweet, normalizedLocations, googlemapsKey, msg):

    if( len(tweet['tweet_links']) == 0 ):
        return

    if( 'twitter_links_exclusively' in tweet['extra'] ):
        if( tweet['extra']['twitter_links_exclusively'] ):
            return

    if( 'raw_json' not in tweet['extra'] ):
        return
    
    if( tweet['extra']['raw_json']['user']['location'] == '' ):
        return

    if( 'normalized' in tweet['extra']['raw_json']['user']['location'] ):
        return
    
    userLocation = tweet['extra']['raw_json']['user']['location']
    screenName = tweet['data_screen_name'].lower()
    if( screenName in normalizedLocations ):
        tweet['extra']['raw_json']['user']['location'] = normalizedLocations[screenName]
        #print('cache hit:', screenName, normalizedLocations[screenName])
        return

    tmp = {'location_name': userLocation}
    tmp['normalized'] = normalizeLoc( userLocation, googlemapsKey )
    
    logger.info(msg + ', userLocation: ' + userLocation)
    logger.info('\t\tresult: ' + str(tmp['normalized']) + '\n')
    
    tweet['extra']['raw_json']['user']['location'] = tmp
    normalizedLocations[screenName] = tmp

def addLocations(tweets, domainsDct, googlemapsKey='', extraParams=None):

    logger.info('\nnormalizing locations:')

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('cache_path', '')
    
    normalizedLocations = {}
    size = len(tweets['tweets'])
    sizeStr = str(size)

    for i in range(size):

        tweet = tweets['tweets'][i]
        msg = '\tuser: ' + str(i) + ' of ' + sizeStr + '\n\t' + tweet['data_screen_name'] + '-' + tweet['data_tweet_id']
        addSingleLocation(tweet, normalizedLocations, googlemapsKey, msg)

        if( 'tweet_replies' in tweet ):
            listName = 'tweet_replies'
        elif( 'tweet_thread' in tweet ):
            listName = 'tweet_thread'
        else:
            continue

        for j in range( len(tweet[listName]['tweets']) ):
            
            tweetChild = tweet[listName]['tweets'][j]
            if( tweetChild['extra']['raw_json']['user']['location'] != '' and len(tweetChild['tweet_links']) != 0 ):
                addSingleLocation(tweetChild, normalizedLocations, googlemapsKey, msg)



    count = 0
    size = str(len(domainsDct))
    normalizedLocations = {}
    for domain, domDct in domainsDct.items():

        count += 1

        if( domain in tweets['website_handles'] ):
            if( 'location' in tweets['website_handles'][domain] ):
                if( tweets['website_handles'][domain]['location'] != '' ):

                    if( 'normalized' in tweets['website_handles'][domain]['location'] ):
                        domDct['domain_handle_location'] = tweets['website_handles'][domain]['location']
                        continue

                    tmp = { 'location_name': tweets['website_handles'][domain]['location'] }
                    if( domain in normalizedLocations ):
                        userLocationNorm = normalizedLocations[domain]
                    else:
                        userLocationNorm = normalizeLoc( tmp['location_name'], googlemapsKey )
                    
                    logger.info('domain: ' + domain)
                    logger.info('\tdomainLocation: ' + tmp['location_name'] + ': ' + str(count) + ' of ' + size)
                    logger.info('\t\tresult: ' + str(userLocationNorm))
                    
                    tmp['normalized'] = userLocationNorm
                    normalizedLocations[domain] = userLocationNorm

                    tweets['website_handles'][domain]['location'] = tmp
                    domDct['domain_handle_location'] = tmp

                    #update domain cache since it's accrued more information - start
                    domFilename = extraParams['cache_path'] + 'WebsiteHandles/' + domain + '.json.gz'
                    gzipTextFile(domFilename, json.dumps(tweets['website_handles'][domain], ensure_ascii=False))
                    #update domain cache since it's accrued more information - end

#reputation qp - start
def repGenStats(payload):
    
    if( len(payload) == 0 ):
        return {}

    
    if( isinstance(payload[0], str) ):

        domainStats = {}
        for uri in payload:
            
            domain = getDomain(uri)
            domainStats.setdefault(domain, 0)
            domainStats[domain] += 1

        return domainStats

    elif( isinstance(payload[0], dict) ):

        domainStats = {'total': 0, 'domains': {} }
        binaryDomStats = {'total': 0, 'domains': {} }

        for gold in payload:

            binaryDomStats['total'] += 1
            for dom, domCount in gold['stats'].items():

                domainStats['domains'].setdefault(dom, 0)
                binaryDomStats['domains'].setdefault(dom, 0)

                domainStats['domains'][dom] += domCount
                binaryDomStats['domains'][dom] += 1

                domainStats['total'] += domCount

        
        for lst in [binaryDomStats, domainStats]:
            
            lst['domains_sorted'] = sorted( lst['domains'].items(), key=lambda x: x[1], reverse=True )
            for j in range( len(lst['domains_sorted']) ):
                
                tmp = lst['domains_sorted'][j]
                lst['domains_sorted'][j] = {'domain': tmp[0], 'freq': tmp[1], 'rate': tmp[1]/lst['total']}

        return {
            'binary': binaryDomStats,
            'non_binary': domainStats
        }

    return {}

def repGetExtrnRef(page, gold):

    dedubSet = set()
    try:
        reqURI = 'https://en.wikipedia.org/w/api.php?action=parse&page=' + page + '&format=json'
        wiki = getDictFromJson( derefURI(reqURI) )

        logger.info( '\turi: ' + gold['uri'] )
        logger.info( '\tpage: ' + page )
        logger.info( '\treqURI: ' + reqURI )
        if( 'parse' not in wiki ):
            logger.info('\tEMPTY')
        logger.info('')

        for link in wiki['parse']['externallinks']:
            
            link = link.strip()
            if( link == '' ):
                continue

            if( link.startswith('//') ):
                link = 'http:' + link

            urir = getURIRFromMemento(link)
            if( urir != '' ):
                link = urir

            if( link in dedubSet ):
                continue

            dedubSet.add(link)
            gold['external_refs'].append(link)
    except:
        genericErrorInfo()

def genReputationStore(goldFile):

    goldFile = goldFile.strip()
    if( goldFile == '' ):
        return {}

    updateGold = False
    reputationStore = getDictFromFile(goldFile)

    if( 'topics' not in reputationStore ):
        return {}
    
    for topic, topicDct in reputationStore['topics'].items():

        if( 'gold' not in topicDct ):
            continue

        logger.info('\ngenReputationStore(), topic: ' + topic)

        for i in range( len(topicDct['gold']) ):
            
            g = topicDct['gold'][i]
            if( 'external_refs' in g ):
                g['stats'] = repGenStats( g['external_refs'] )

                if( len(g['stats']) != 0 ):
                    continue
            
            updateGold = True
            g['external_refs'] = []
            page = g['uri'].replace('https://en.wikipedia.org/wiki/', '')
            
            repGetExtrnRef(page, g)
            g['stats'] = repGenStats( g['external_refs'] )
            
        topicDct['stats'] = repGenStats( topicDct['gold'] )

    if( updateGold ):
        logger.info('\ngenReputationStore(), updating gold')
        dumpJsonToFile(goldFile, reputationStore)

    return reputationStore

def getReputationQPDets(reputationStore, query, topic, uri):

    topic = topic.strip()
    uri = uri.strip()
    query = query.strip()

    if( len(reputationStore) == 0 or query == '' or topic == '' or uri == '' ):
        logger.info('\ngetReputationQPDets(): Not calculating reputation')
        return {}

    domain = getDomain(uri)

    try:
        reput = {}
        for opt in ['binary', 'non_binary']:
        
            reput[opt] = {
                'total': reputationStore['topics'][topic]['stats'][opt]['total'],
                'count': reputationStore['topics'][topic]['stats'][opt]['domains'][domain]
            }
    except:
        pass


    #calculate story-level-reputation - start
    #only references the stats in narrow_reputation_refs
    
    allStats = {}
    totalDomainFreq = 0
    try:
        
        uriRef = reputationStore['topics'][topic]['narrow_reputation_refs']['queries'][query]

        for uri in uriRef:
            for g in reputationStore['topics'][topic]['gold']:
                
                if( uri['uri'] != g['uri'] ):
                    continue

                
                for dom, domFreq in g['stats'].items():

                    allStats.setdefault(dom, 0)
                    allStats[dom] += domFreq
                    totalDomainFreq += domFreq
    except:
        pass

    if( domain in allStats ):
        reput['story'] = {
            'total': totalDomainFreq,
            'count': allStats[domain]
        }
    #calculate story-level-reputation - end

    return reput
#reputation qp - end

def qpPopularity(seed, twt, domain, websiteHandles):
    
    #set post popularity
    seed['quality_proxy_vectors']['popularity'] = {'details': {}}
    if( 'tweet_stats' in twt ):
        seed['quality_proxy_vectors']['popularity']['reply'] = twt['tweet_stats']['reply']
        seed['quality_proxy_vectors']['popularity']['share'] = twt['tweet_stats']['retweet']
        seed['quality_proxy_vectors']['popularity']['like'] = twt['tweet_stats']['favorite']
    else:
        seed['quality_proxy_vectors']['popularity']['reply'] = None
        seed['quality_proxy_vectors']['popularity']['share'] = None
        seed['quality_proxy_vectors']['popularity']['like'] = None

    #set author popularity
    seed['quality_proxy_vectors']['popularity']['author_popularity'] = None
    seed['quality_proxy_vectors']['popularity']['details']['author_popularity'] = {'in_degree': None, 'out_degree': None}

    if( 'extra' in twt ):
        if( 'raw_json' in twt['extra'] ):
            seed['quality_proxy_vectors']['popularity']['author_popularity'] = twt['extra']['raw_json']['user']['followers_count'] - twt['extra']['raw_json']['user']['friends_count']
            seed['quality_proxy_vectors']['popularity']['details']['author_popularity'] = {
                'in_degree': twt['extra']['raw_json']['user']['followers_count'],
                'out_degree': twt['extra']['raw_json']['user']['friends_count']
            }

    #set domain popularity and domain geo proximity
    seed['quality_proxy_vectors']['popularity']['domain_popularity'] = None
    seed['quality_proxy_vectors']['popularity']['details']['domain_popularity'] = {}

    if( isUserOwnerOfDomain(domain) and domain in websiteHandles ):
        if( 'followers_count' in websiteHandles[domain] ):

            seed['quality_proxy_vectors']['popularity']['details']['domain_popularity']['in_degree'] = websiteHandles[domain]['followers_count']
            seed['quality_proxy_vectors']['popularity']['details']['domain_popularity']['out_degree'] = websiteHandles[domain]['friends_count']
            seed['quality_proxy_vectors']['popularity']['details']['domain_popularity']['domain_account'] = websiteHandles[domain]['screen_name']

            seed['quality_proxy_vectors']['popularity']['domain_popularity'] = websiteHandles[domain]['followers_count'] - websiteHandles[domain]['friends_count']

def qpGeo(seed, location, domain, websiteHandles):

    #set author geo proximity
    seed['quality_proxy_vectors']['geo'] = {'author': {}, 'domain': {}}

    if( isUserOwnerOfDomain(domain) and domain in websiteHandles ):
        if( 'followers_count' in websiteHandles[domain] and websiteHandles[domain]['location'] != '' ):
            seed['quality_proxy_vectors']['geo']['domain'] = websiteHandles[domain]['location']

    if( location != '' ):
        seed['quality_proxy_vectors']['geo']['author'] = location

def qpSubjectExpertHit(seed, query, cachePath, domain, websiteHandles):

    #set subject expert
    if( domain not in websiteHandles ):
        return
    if( 'qp_cache' not in websiteHandles[domain] ):
        return


    doSu = True
    if( 'subject_expert' in websiteHandles[domain]['qp_cache'] ):
        if( query in websiteHandles[domain]['qp_cache']['subject_expert'] ):
            
            hit_count = websiteHandles[domain]['qp_cache']['subject_expert'][query]['details']['hit_count']
            if( hit_count > -1 ):
                
                doSu = False
                seed['quality_proxy_vectors'].setdefault('subject_expert', {
                    'details': {'hit_count': -1, 'webpage_count': -1}
                })
                seed['quality_proxy_vectors']['subject_expert']['details']['hit_count'] = hit_count
                logger.info( '\tsu-cache (hit, query:' + query + ') for ' + domain + ': ' + str(hit_count) )

    if( doSu ):
        
        su = getSubjectExpertQPDets(domain, query)
        logger.info('\tsu (hit, query:' + query + ') for ' + domain + ': ' + str(su))
        
        websiteHandles[domain]['qp_cache'].setdefault('subject_expert', {})
        websiteHandles[domain]['qp_cache']['subject_expert'].setdefault(query, {
            'details': {'hit_count': -1, 'webpage_count': -1}
        })

        seed['quality_proxy_vectors'].setdefault('subject_expert', {
            'details': {'hit_count': -1, 'webpage_count': -1}
        })

        #placed subject_expert in qp_cache because other links might share common subject_expert
        websiteHandles[domain]['qp_cache']['subject_expert'][query]['details']['hit_count'] = su
        seed['quality_proxy_vectors']['subject_expert']['details']['hit_count'] = su

        
        #attempt to write website_handles into cache - start
        if( cachePath != '' ):
            domFilename = cachePath + 'WebsiteHandles/' + domain + '.json.gz'
            gzipTextFile(domFilename, json.dumps(websiteHandles[domain], ensure_ascii=False))
        #attempt to write website_handles into cache - end

    if( seed['quality_proxy_vectors']['subject_expert']['details']['webpage_count'] == 0 ):
        seed['quality_proxy_vectors']['subject_expert']['subject_expert_score'] = 0
    else:
        seed['quality_proxy_vectors']['subject_expert']['subject_expert_score'] = seed['quality_proxy_vectors']['subject_expert']['details']['hit_count']/seed['quality_proxy_vectors']['subject_expert']['details']['webpage_count']

def qpSubjectExpertSize(seed, query, cachePath, domain, websiteHandles):

    if( domain not in websiteHandles ):
        return
    if( 'qp_cache' not in websiteHandles[domain] ):
        return

    
    doSu = True
    if( 'subject_expert' in websiteHandles[domain]['qp_cache'] ):
        if( query in websiteHandles[domain]['qp_cache']['subject_expert'] ):
            
            webpage_count = websiteHandles[domain]['qp_cache']['subject_expert'][query]['details']['webpage_count']
            if( webpage_count > -1 ):

                doSu = False
                seed['quality_proxy_vectors'].setdefault('subject_expert', {
                    'details': {'hit_count': -1, 'webpage_count': -1}
                })
                seed['quality_proxy_vectors']['subject_expert']['details']['webpage_count'] = webpage_count
                logger.info( '\tsu-cache (website size) for ' + domain + ': ' + str(webpage_count) )

    if( doSu ):
        
        su = getSubjectExpertQPDets(domain, '')
        logger.info('\tsu (website size) for ' + domain + ': ' + str(su))
        
        websiteHandles[domain]['qp_cache'].setdefault('subject_expert', {})
        websiteHandles[domain]['qp_cache']['subject_expert'].setdefault(query, {
            'details': {'hit_count': -1, 'webpage_count': -1}
        })

        seed['quality_proxy_vectors'].setdefault('subject_expert', {
            'details': {'hit_count': -1, 'webpage_count': -1}
        })

        #placed subject_expert in qp_cache because other links might share common subject_expert
        websiteHandles[domain]['qp_cache']['subject_expert'][query]['details']['webpage_count'] = su
        seed['quality_proxy_vectors']['subject_expert']['details']['webpage_count'] = su

        
        #attempt to write website_handles into cache - start
        if( cachePath != '' ):
            domFilename = cachePath + 'WebsiteHandles/' + domain + '.json.gz'
            gzipTextFile(domFilename, json.dumps(websiteHandles[domain], ensure_ascii=False))
        #attempt to write website_handles into cache - end

    if( seed['quality_proxy_vectors']['subject_expert']['details']['webpage_count'] == 0 ):
        seed['quality_proxy_vectors']['subject_expert']['subject_expert_score'] = 0
    else:
        seed['quality_proxy_vectors']['subject_expert']['subject_expert_score'] = seed['quality_proxy_vectors']['subject_expert']['details']['hit_count']/seed['quality_proxy_vectors']['subject_expert']['details']['webpage_count']


def qpReputation(seed, query, topic, reputationStore, cachePath, domain, websiteHandles):

    if( query == '' or topic == '' or len(reputationStore) == 0 ):
        logger.info('\nqpReputation(): Not calculating reputation, blanks query or topic or reputationStore')
        return

    #set reputation quality proxy
    if( domain in websiteHandles ):
        if( 'qp_cache' in websiteHandles[domain] ):

            doReput = True
            #consider not using cache in case gold is updated
            '''
            if( 'reput' in websiteHandles[domain]['qp_cache'] ):
                if( topic in websiteHandles[domain]['qp_cache']['reput'] ):
                    
                    doReput = False
                    seed['quality_proxy_vectors']['reput'] = websiteHandles[domain]['qp_cache']['reput'][topic]
            '''

            if( doReput ):
                
                reput = getReputationQPDets(reputationStore, query, topic, seed['uri'])
                websiteHandles[domain]['qp_cache'].setdefault('reput', {})

                #placed reput in qp_cache because other links might share common reput
                websiteHandles[domain]['qp_cache']['reput'][topic] = reput
                seed['quality_proxy_vectors']['reput'] = reput
                
                #attempt to write website_handles into cache - start
                if( cachePath != '' ):
                    domFilename = cachePath + 'WebsiteHandles/' + domain + '.json.gz'
                    gzipTextFile(domFilename, json.dumps(websiteHandles[domain], ensure_ascii=False))
                #attempt to write website_handles into cache - end


def qpRetrv(seed, extraParams):

    #set retrievability score

    if( extraParams['cache_path'] == '' ):
        serp_cache_path = ''
    else:
        serp_cache_path = extraParams['cache_path'] + 'SERPs/'

    if( extraParams['rt_no_stop_if_title_not_found'] is False ):
        stop_if_title_not_found = True
    else:
        stop_if_title_not_found = False

    retrv = get_uri_retrv(
        uri=seed['uri'], 
        max_query_per_ngram=extraParams['rt_max_query_per_ngram'],
        min_ngram=extraParams['rt_min_ngram'],
        max_ngram=extraParams['rt_max_ngram'],
        max_page=extraParams['rt_max_page'],
        no_second_try=extraParams['rt_no_second_try'],
        stop_if_title_not_found=stop_if_title_not_found,
        serp_cache_path=serp_cache_path
    )

    seed['quality_proxy_vectors']['retrv'] = retrv
    if( 'captcha_on' in retrv ):
        return retrv['captcha_on']

    return False

def qpGoogleRetrv(seed, gserp):

    if( 'links' not in gserp ):
        logger.info("\nqpGoogleRetrv(): rt_google_serp_file 'links' not in gserp, returning")
        logger.info( '\ngserp keys: ' + str(gserp.keys()) )
        return

    seed['quality_proxy_vectors']['retrv'] = { 'scores': {'rr': 0} }
    size = len(gserp['links'])
    
    for i in range(size):
        if( isSameLink(gserp['links'][i]['link'], seed['uri']) ):

            #print( 'FOUND:', seed['uri'] )
            seed['quality_proxy_vectors']['retrv']['scores']['rr'] = 1/(i+1)
            return

    return

def qpAudience(seed, twtCount, params):
    
    seed['quality_proxy_vectors']['audience'] = {'reply': 0, 'share': 0, 'like': 0, 'count': 0, 'details': []}
    
    chromedriverPath = None
    latestVertical = False
    params.setdefault('audience_twitter_request_counter', 0)
    params.setdefault('audience_ua_cursor', 0)


    '''
        --cache-path: consider caching tweets at cache-path if need to read process the same tweets arisis
    '''
    params['leave_browser_open'] = True
    params['search_uri_key'] = seed['uri']

    params.setdefault('driver', None)
    params.setdefault('chromedriver_path', None)
    params.setdefault('no_hydrate_tweets', True)#No need to hydrate since tweet_stats can be extracted from scraping

    if( params['audience_twitter_request_counter'] % 10 == 0 ):
        
        ua = getUserAgentLst()
        if( params['audience_ua_cursor'] >= len(ua) ):
            params['audience_ua_cursor'] = 0
        
        ua = ua[ params['audience_ua_cursor'] ]
        params['audience_ua_cursor'] += 1

        logger.info( '\nqpAudience new driver for req: ' + str(params['audience_twitter_request_counter']) )
        logger.info( '\tuser-agent: ' + ua )
        if( params['driver'] is not None ):
            params['driver'].quit()

        params['driver'] = getChromedriver( params['chromedriver_path'], userAgent=ua )

    if( 'latest' in params ):
        latestVertical = params['latest']

    params['audience_twitter_request_counter'] += 1
    logger.info( '\nqpAudience req: ' + str(params['audience_twitter_request_counter']) )

    serp = twitterSearch(
        chromedriverPath=params['chromedriver_path'], 
        query='', 
        maxTweetCount=twtCount,
        latestVertical=latestVertical,
        extraParams=params
    )

    if( 'tweets'  in serp ):
        for twt in serp['tweets']:
            
            seed['quality_proxy_vectors']['audience']['count'] += 1
            seed['quality_proxy_vectors']['audience']['reply'] += twt['tweet_stats']['reply']
            seed['quality_proxy_vectors']['audience']['share'] += twt['tweet_stats']['retweet']
            seed['quality_proxy_vectors']['audience']['like'] += twt['tweet_stats']['favorite']
            
            twtDets = {
                'data_tweet_id': twt['data_tweet_id'],
                'data_screen_name': twt['data_screen_name'],
                'data_name': twt['data_name'],
                'tweet_stats': twt['tweet_stats']
            }

            seed['quality_proxy_vectors']['audience']['details'].append(twtDets)
        

def measurePrec(gold, testCol, cachePath):
    
    if( len(testCol['uris']) == 0 ):
        return {}

    logger.info('\nmeasurePrec(): ' + cachePath)
    res = precisionEval( gold, testCol, cachePath)
    if( 'test_col' in res ):
        return res['test_col']
    
    #print('measurePrec res:', res)

def addSingleTweetQPVector(twt, websiteHandles, rtrvGoogleSerp, precGold, captchaOn, label, extraParams=None):
    
    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('cache_path', '')
    extraParams.setdefault( 'prec_eval_cache_path', extraParams['cache_path'] )

    extraParams.setdefault('re_topic', '')
    extraParams.setdefault('reput_qp_gold', {})

    extraParams.setdefault('rt_max_query_per_ngram', 2)
    extraParams.setdefault('rt_min_ngram', 2)
    extraParams.setdefault('rt_max_ngram', 5)
    extraParams.setdefault('rt_max_page', 2)
    extraParams.setdefault('rt_no_second_try', False)
    extraParams.setdefault('rt_no_stop_if_title_not_found', False)
    
    extraParams.setdefault('no_geo_qp', False)
    extraParams.setdefault('no_popularity_qp', False)
    extraParams.setdefault('no_reput_qp', False)
    extraParams.setdefault('no_retrv_qp', False)
    extraParams.setdefault('no_audience_qp', False)

    extraParams.setdefault('audience_tweet_count', 20)

    extraParams.setdefault('query', '')
    
    totalLinks = str( len(twt['tweet_links'])-1 )
    precEvalInput = {'uris': []}
    for i in range( len(twt['tweet_links']) ):
        
        seed = twt['tweet_links'][i]
        if( seed['uri'].startswith('https://twitter.com') ):
            continue

        logger.info(label)
        logger.info('\t\ttweet link: ' + str(i) + ' of ' + totalLinks )
        seed.setdefault('quality_proxy_vectors', {})
        domain = getDomain(seed['uri'], includeSubdomain=False)

        if( extraParams['no_popularity_qp'] is False ):
            qpPopularity(seed, twt, domain, websiteHandles)            

        if( extraParams['no_geo_qp'] is False ):
            userLoc = ''
            if( 'raw_json' in twt['extra'] ):
                userLoc = twt['extra']['raw_json']['user']['location']
            qpGeo(seed, userLoc, domain, websiteHandles)
        
      
        if( extraParams['no_reput_qp'] is False ):
            qpReputation(seed, extraParams['query'], extraParams['re_topic'], extraParams['reput_qp_gold'], extraParams['cache_path'], domain, websiteHandles)

        if( captchaOn is True ):
            logger.info('\tCAPTCHA ON NOT CHECKING RETRV for victim: ' + seed['uri'])

        if( extraParams['no_retrv_qp'] is False ):
            #qpRetrv too expensive, so I substituted it with qpGoogleRetrv
            #captchaOn = qpRetrv(seed, extraParams)
            qpGoogleRetrv(seed, rtrvGoogleSerp)

        if( extraParams['no_prec_eval'] is False and 'relevance' not in seed['quality_proxy_vectors'] ):
            precEvalInput['uris'].append({ 'uri': seed['uri'], 'indx': i})

        if( extraParams['no_audience_qp'] is False and 'audience' not in seed['quality_proxy_vectors'] ):
            qpAudience(seed, extraParams['audience_tweet_count'], extraParams)
        
        #if( extraParams['no_audience_qp'] is False ):
        #    qpAudience(seed, extraParams['audience_tweet_count'], extraParams)

        '''
            #su switched OFF because Google result count stat is not always reliable.
            if( extraParams['no_subject_expert_hit_qp'] is False ):
                qpSubjectExpertHit(seed, extraParams['query'], extraParams['cache_path'], domain, websiteHandles)
            
            if( extraParams['no_subject_expert_size_qp'] is False ):
                qpSubjectExpertSize(seed, extraParams['query'], extraParams['cache_path'], domain, websiteHandles)
        '''
    
    if( len(precGold) != 0 ):
        precRes = measurePrec( precGold, precEvalInput, extraParams['prec_eval_cache_path'] )
        if( 'uris' in precRes ):

            for u in precRes['uris']:
                
                i = u['indx']
                twt['tweet_links'][i]['quality_proxy_vectors']['relevance'] = {
                    'sim': u['sim'],
                    'text_len': u['text_len'],
                    'title': u['title']
                }

    return captchaOn

def enrichPrecGold(precGold, extraParams):

    if( 'query' not in precGold or 'uris' not in precGold ):
        return

    slug = slugifyStr(precGold['query'])
    extraParams.setdefault('gold_file', '')

    aFrag = extraParams['gold_file'].replace('.json', '')

    if( aFrag.find(slug) == -1 ):
        enrichedFile = aFrag + '_' + slug + '_enriched.json'
    else:
        enrichedFile = aFrag + '_enriched.json'


    if( os.path.exists(enrichedFile) ):
        logger.info('\nenrichPrecGold(), enrichedFile exists, returning, enrichedFile: ' + enrichedFile )
        return

    
    logger.info('\nenrichPrecGold(): enrichedFile: ' + enrichedFile )

    #one vs rest gold
    size = len(precGold['uris'])
    precGold['prec_summary'] = {'sim': {'avg': 0, 'median': []}}
    for i in range( size ):
        
        gu = precGold['uris'][i]
        gu['prec_dets'] = {}

        locGold = set([ u['uri'] for u in precGold['uris'] ])
        locGold.remove( gu['uri'] )

        locGold = [{'uri': u} for u in locGold]
        locGold = {'uris': locGold}

        precEvalInput = {}
        precEvalInput['uris'] = [{ 'uri': gu['uri'] }]


        extraParams['prec_sim_cache_lookup'] = False#reevaluate precision because if an entry exists in cache it might mean that gold uri and collection uri coincide, and collection was evaluated with a different gold than would we would want to evaluate gold now.
        res = precisionEval(locGold, precEvalInput, extraParams['prec_eval_cache_path'], extraParams=extraParams)
        
        logger.info( '\tenrichPrecGold(): ' + str(i) + ' of ' + str(size) )
        if( 'test_col' in res ):
            if( 'uris' in res['test_col'] ):
                if( len(res['test_col']['uris']) == 1 ):
                    
                    gu['prec_dets'] = res['test_col']['uris'][0]

                    if( gu['prec_dets']['sim'] > -1 ):
                        precGold['prec_summary']['sim']['avg'] += gu['prec_dets']['sim']
                        precGold['prec_summary']['sim']['median'].append( gu['prec_dets']['sim'] )

    
    precGold['prec_summary']['sim']['count'] = len(precGold['prec_summary']['sim']['median'])
    if( precGold['prec_summary']['sim']['count'] != 0 ):
        precGold['prec_summary']['sim']['avg'] = precGold['prec_summary']['sim']['avg']/precGold['prec_summary']['sim']['count']

    precGold['prec_summary']['sim']['median'] = median( precGold['prec_summary']['sim']['median'] )
    dumpJsonToFile(enrichedFile, precGold)
                

def getPrecGoldFrmReputGold(gold, query):

    if( 'precision_refs' not in gold or 'gold' not in gold ):
        logger.info('\ngetPrecGoldFrmReputGold(): gold.precision_refs or gold absent, returning')
        return {}
    
    if( 'queries' not in gold['precision_refs'] ):
        logger.info('\ngetPrecGoldFrmReputGold(): queries absent from gold.precision_refs, returning')
        return {}

    if( query not in gold['precision_refs']['queries'] ):
        logger.info('\ngetPrecGoldFrmReputGold(): '+ query +' absent from gold.precision_refs.queries, returning')
        return {}

    goldURIs = gold['precision_refs']['queries'][query]
    allExternalRefs = {'uris': [], 'query': query }
    
    for gURI in goldURIs:
        for g in gold['gold']:

            if( gURI['uri'] == g['uri'] ):
                allExternalRefs['uris'] += g['external_refs']
                break

    allExternalRefs['uris'] = [{'uri': u} for u in allExternalRefs['uris']]
    return allExternalRefs

def burstSingleTwt(twt, burstOpts):
    
    if( 'tweet_links' not in twt or len(burstOpts) == 0 ):
        return


    for i in range( len(twt['tweet_links']) ):        
        
        seed = twt['tweet_links'][i]
        if( 'quality_proxy_vectors' not in seed ):
            continue

        if( 'relevance' in burstOpts and 'relevance' in seed['quality_proxy_vectors'] ):
            del seed['quality_proxy_vectors']['relevance']

def burstQPCache(tweets, burstOpts, cachePath):

    logger.info('\nburstQPCache(): ' + str(burstOpts))   

    for i in range( len(tweets['tweets']) ):
        
        twt = tweets['tweets'][i]
        burstSingleTwt(twt, burstOpts)
        lstName = getTweetLstName(twt)

        if( lstName != '' ):
            if( 'tweets' in twt[lstName] ):
            
                for j in range( len(twt[lstName]['tweets']) ):
                    twtChd = twt[lstName]['tweets'][j]
                    burstSingleTwt(twtChd, burstOpts)

    '''
    if( 'relevance' in burstOpts and cachePath != '' ):
        logger.info('\tremoving CosineSim, HTML and Plaintext from: ' + cachePath)
        
        for loc in ['CosineSim/', 'HTML/', 'Plaintext/']:
            try:
                if( os.path.exists(cachePath + loc) ):
                    check_output(['rm', '-rf', cachePath + loc])
            except:
                genericErrorInfo('\terror path: ' + cachePath + loc)
    '''

def addTweetQPVector(tweets, extraParams=None):

    if( 'tweets' not in tweets or 'website_handles' not in tweets ):
        return

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('cache_path', '')
    extraParams.setdefault('re_topic', '')
    extraParams.setdefault('reput_qp_gold', {})
    extraParams.setdefault('rt_google_serp_file', '')
    extraParams.setdefault('query', '')
    extraParams.setdefault('gold_file', '')

    precGold = {}
    gserp = extraParams['rt_google_serp_file'].strip()
    if( gserp == '' ):
        gserp = {}
    else:
        gserp = getDictFromFile(gserp)

    if( 'topics' in extraParams['reput_qp_gold'] ):
        if( extraParams['re_topic'] in extraParams['reput_qp_gold']['topics'] ):
            
            precGold = extraParams['reput_qp_gold']['topics'][ extraParams['re_topic'] ]
            precGold = getPrecGoldFrmReputGold( precGold, extraParams['query'] )
            enrichPrecGold( precGold, extraParams )

    totalTweets = str( len(tweets['tweets'])-1 )
    captchaOn = False
    for i in range( len(tweets['tweets']) ):
        
        label = 'addTweetQPVector() - tweet: ' + str(i) + ' of ' + totalTweets
        twt = tweets['tweets'][i]
        captchaOn = addSingleTweetQPVector( twt, tweets['website_handles'], gserp, precGold, captchaOn, label, extraParams )
        procReplies = True

        if( 'tweet_replies' in twt ):
            listName = 'tweet_replies'
        elif( 'tweet_thread' in twt ):
            listName = 'tweet_thread'
        else:
            procReplies = False

        if( procReplies ):

            totalChildTweets = str( len(twt[listName]['tweets'])-1 )
            for j in range( len(twt[listName]['tweets']) ):
                
                label = 'addTweetQPVector() - tweet: ' + str(i) + ' of ' + totalTweets + '\n\ttweet child: ' + str(j) + ' of ' + totalChildTweets
                tweetChild = twt[listName]['tweets'][j]
                captchaOn = addSingleTweetQPVector( tweetChild, tweets['website_handles'], gserp, precGold, captchaOn, label, extraParams )

        #update tweet cache since tweets might accrued additional data - start
        if( extraParams['cache_path'] != '' ):
            writeTwtCache( extraParams['cache_path'], twt['data_tweet_id'], twt )
        #update tweet cache since tweets might accrued additional data - end
        
        logger.info('')

def isUserOwnerOfDomain(domain):

    blacklistDomains = {
        'twitter.com',
        'facebook.com',
        'youtube.com',
        'instagram.com'
    }
    
    if( domain.strip().lower() in blacklistDomains ):
        return False

    return True

def genQualityProxies(tweets, extraParams=None):
    
    '''
        see explanation: https://ws-dl.cs.odu.edu/wiki/images/1/1d/Seed-hosts-auth-study.png
        Sample ranking quality_proxy of domains based on popularity: https://www.cs.odu.edu/~anwala/files/transient-cols/ebola-virus-outbreak-pop-rank.json
        Sample geo-locality ranking of seed hosts: https://www.cs.odu.edu/~anwala/files/transient-cols/ebola-virus-outbreak-geoloc-rank.json

        pending work: addLocations()

        - reacess website handles caching
        - mapping short uris to their long uri counterparts in website handles
    '''

    if( len(tweets) == 0 ):
        return {}

    if( 'tweets' not in tweets ):
        logger.info('\ngenQualityProxies(): "tweets" key not found in input, returning')
        return {}

    newTweetsCol = []
    #get only hydratedTweets - start
    for twt in tweets['tweets']:
        
        if( 'tweet_hydrated' not in twt ):
            continue

        if( twt['tweet_hydrated'] is False ):
            continue

        newTweetsCol.append( twt )
    tweets['tweets'] = newTweetsCol
    #get only hydratedTweets - end

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('cache_path', '')
    extraParams.setdefault('googlemaps_key', '')

    extraParams.setdefault('no_geo_qp', False)
    extraParams.setdefault('no_popularity_qp', False)
    extraParams.setdefault('no_reput_qp', False)
    extraParams.setdefault('no_retrv_qp', False)
    extraParams.setdefault('no_audience_qp', False)

    extraParams.setdefault('exclude_domains', ['twimg.com', 'twitter.com'])
    extraParams.setdefault('re_topic', '')
    extraParams.setdefault('gold_file', '')
    extraParams.setdefault('burst_qp_cache', [])
    extraParams.setdefault('chromedriver_path', None)
    extraParams.setdefault('no_redact_keys', True)

    if( extraParams['cache_path'] != '' and extraParams['cache_path'].endswith('/') == False ):
        extraParams['cache_path'] = extraParams['cache_path'] + '/'

    extraParams.setdefault( 'prec_eval_cache_path', extraParams['cache_path'] )
    
    if( extraParams['no_reput_qp'] is True ):
        extraParams['reput_qp_gold'] = {}
    else:
        extraParams['reput_qp_gold'] = genReputationStore( extraParams['gold_file'] )
        
    '''
        expandOrMarkShortURIs(): 
            since the URIs will be used to build the quality_proxy matrix expand short URIs first

        accumulateDomain(): 
            responsible for initializing domainsDct with domains from tweets

        extractTwitterHandlesFrmWebsite(): 
            accumulateDomain() accumulates counts (followers and following) for domains from the reference point of the tweets that embed the links, extractTwitterHandlesFrmWebsite does a similar operation, but exclusively using information extracted from the websites

            isValidBiLink():
                For websites with twitter handles are extracted from Google, there is a chance that the wrong handle is assigned to a website, so avoid this by checking if the twitter handle's website and the website have the same domain

        addTweetPopularityVector(): 
            Responsible for the actual creation of the popularity quality_proxy vector for tweet
    '''
    
    expandOrMarkShortURIs(tweets, extraParams)
    childTweets = getChildrenTweets(tweets)
    expandOrMarkShortURIs(childTweets, extraParams)

    domainsDct = accumulateDomain(extraParams['exclude_domains'], tweets['tweets'] + childTweets['tweets'])
    extractTwitterHandlesFrmWebsite(tweets, domainsDct, extraParams=extraParams)

    addLocations(tweets, domainsDct, googlemapsKey=extraParams['googlemaps_key'], extraParams=extraParams)
    burstQPCache(tweets, extraParams['burst_qp_cache'], extraParams['prec_eval_cache_path'])
    addTweetQPVector(tweets, extraParams=extraParams)

    del extraParams['reput_qp_gold']
    extraParams['no_redact_keys'] = False
    redactTweetKeys(extraParams)
    
    logger.info('\ngenQualityProxies(): disregarding ' + str(len(tweets['tweets']) - len(newTweetsCol)) + ' unhydrated tweets')

    tweets['source'] = 'Twitter'
    tweets['col_creation_datetime'] = getISO8601Timestamp()
    
    allTweetTimes = [ t['tweet_time'] for t in tweets['tweets'] ]
    allTweetTimes.sort()
    if( len(allTweetTimes) != 0 and tweets['col_creation_datetime'] > allTweetTimes[0] ):
        tweets['col_creation_datetime'] = allTweetTimes[0]

    if( len(tweets['tweets']) == 1 ):
        if( 'human_generated' in tweets['tweets'][0]['extra'] ):
            tweets['col_creation_datetime'] = tweets['tweets'][0]['tweet_time']
    
    try:
        if( 'driver' in extraParams ):
            if( extraParams['driver'] is not None ):
                extraParams['driver'].quit()
    except:
        genericErrorInfo()

    return tweets

def getArgs():
   
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))
    parser.add_argument('tweetspath', nargs='+', help='Path to tweet(s)')
    
    parser.add_argument('--cache-path', help='Path to save tweets post quality proxy processing, default is the input location of tweets file', default='tweetspath')
    parser.add_argument('--prec-eval-cache-path', help='Path for writing/reading HTML/Plaintext/CosineSim used for precision evaluation', default='')
    parser.add_argument('--chromedriver-path', help='Path to chromedriver')#, default='/usr/local/bin/chromedriver'
    parser.add_argument('--max-read-file-depth', help='Maximum depth to read tweet files. 0 means no depth restriction when reading file', type=int, default=1)
    
    parser.add_argument('--access-token', help='Twitter API info needed for hydrating tweets', default='')
    parser.add_argument('--access-token-secret', help='Twitter API info needed for hydrating tweets', default='')
    parser.add_argument('--consumer-key', help='Twitter API info needed for hydrating tweets', default='')
    parser.add_argument('--consumer-secret', help='Twitter API info needed for hydrating tweets', default='')

    parser.add_argument('-b', '--burst-qp-cache', action='append', default=[], choices=['relevance'], help='Re-extract qp metric')
    parser.add_argument('--googlemaps-key', help='Google maps API needed for normalizing locations', default='')

    parser.add_argument('--audience-tweet-count', help='Audience quality proxy: maximum number of audience tweets to extract', type=int, default=5)
    parser.add_argument('--re-topic', help='Reputation quality proxy: topic', default='')
    parser.add_argument('--gold-file', help='Reputation quality proxy: gold standard file path', default='')
    parser.add_argument('-o', '--output', help='Output file')

    parser.add_argument('--rt-max-query-per-ngram', help='Retrievability quality proxy: maximum number of queries to generate per ngram class', type=int, default=2)
    parser.add_argument('--rt-min-ngram', help='Retrievability quality proxy: minimum ngram query ngram length', type=int, default=2)
    parser.add_argument('--rt-max-ngram', help='Retrievability quality proxy: maximum ngram query ngram length', type=int, default=5)
    parser.add_argument('--rt-max-page', help='Retrievability quality proxy: maximum SERP page to search for query URI', type=int, default=2)
    parser.add_argument('--rt-no-second-try', help='Retrievability quality proxy: do not attempt to search for URI again (with title) if not found initially', action='store_true')
    parser.add_argument('--rt-no-stop-if-title-not-found', help='Retrievability quality proxy: continue searching for URI with other ngrams even if title not found', action='store_true')
    parser.add_argument('--rt-google-serp-file', help='Retrievability quality proxy: Google SERP file to use as reference for calculating retrievability', default='')

    parser.add_argument('--thread-count', help='Maximum number of threads to use for parallel operations', type=int, default=5)
    parser.add_argument('--no-expand-short-uri', help='Do not expand short uris', action='store_true')
    parser.add_argument('--no-google-twitter-handle', help='Do not Google search for twitter handles', action='store_true')

    parser.add_argument('--no-audience-qp', help='Do not insert replies/share/like/ quality proxy measures', action='store_true')
    parser.add_argument('--no-geo-qp', help='Do not insert geographical quality proxy measures', action='store_true')
    parser.add_argument('--no-popularity-qp', help='Do not insert popularity quality proxy measures', action='store_true')
    parser.add_argument('--no-prec-eval', help='Do not measure precision for uris', action='store_true')
    parser.add_argument('--no-reput-qp', help='Do not insert reputation quality proxy measures', action='store_true')
    parser.add_argument('--no-retrv-qp', help='Do not insert retrievability quality proxy measures', action='store_true')
    

    parser.add_argument('--log-file', help='Log output filename', default='')
    parser.add_argument('--log-format', help='Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html', default='')
    parser.add_argument('--log-level', help='Log level', choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'], default='info')
    
    parser.add_argument('--pretty-print', help='Pretty print JSON output', action='store_true')
    parser.add_argument('-q', '--query', help='Query used to generate quality proxy', default='')
    
    return parser

def getTweets(files, maxDepth):
    
    allTweets = {'tweets': []}
    tweets = readTextFromFilesRecursive(files, maxDepth=maxDepth)
    
    for i in range( len(tweets) ):
        
        twt = getDictFromJson( tweets[i]['text'] )
        if( 'data_screen_name' in twt ):
            allTweets['tweets'].append(twt)

    return allTweets

def procReq(params):
    
    tweets = getTweets( params['tweetspath'], maxDepth=params['max_read_file_depth'] )
    
    if( params['cache_path'] == 'tweetspath' ):
        params['cache_path'] = params['tweetspath'][0]

    tweets = genQualityProxies(tweets=tweets, extraParams=params)
            
    if( params['output'] is not None ):
        dumpJsonToFile( params['output'], tweets, indentFlag=params['pretty_print'] )

    return tweets

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

if __name__ == 'scraper.TwitterQualityProxy':
    from scraper.ScraperUtil import derefURI
    from scraper.ScraperUtil import dumpJsonToFile
    from scraper.ScraperUtil import expandUrl
    from scraper.ScraperUtil import genericErrorInfo
    from scraper.ScraperUtil import getChromedriver
    from scraper.ScraperUtil import getDomain
    from scraper.ScraperUtil import getDictFromFile
    from scraper.ScraperUtil import getDictFromJson
    from scraper.ScraperUtil import getDictFromJsonGZ
    from scraper.ScraperUtil import getISO8601Timestamp
    from scraper.ScraperUtil import getURIRFromMemento
    from scraper.ScraperUtil import getUserAgentLst
    from scraper.ScraperUtil import gzipTextFile
    from scraper.ScraperUtil import isSameLink
    from scraper.ScraperUtil import median
    from scraper.ScraperUtil import naiveIsURIShort
    from scraper.ScraperUtil import parallelTask
    from scraper.ScraperUtil import precisionEval
    from scraper.ScraperUtil import readTextFromFilesRecursive
    from scraper.ScraperUtil import setLogDefaults
    from scraper.ScraperUtil import setLoggerDets
    from scraper.ScraperUtil import slugifyStr
    
    from scraper.Twitter import getHandlesFrmLnks
    from scraper.Twitter import getTweetLstName
    from scraper.Twitter import getTweetLink
    from scraper.Twitter import hydrateUsers
    from scraper.Twitter import redactTweetKeys
    from scraper.Twitter import twitterSearch
    from scraper.Twitter import writeTwtCache

    #from scraper.Google import getSubjectExpertQPDets
    #from scraper.Google import get_uri_retrv
    from scraper.Google import googleSearch
else:
    from ScraperUtil import derefURI
    from ScraperUtil import dumpJsonToFile
    from ScraperUtil import expandUrl
    from ScraperUtil import genericErrorInfo
    from ScraperUtil import getChromedriver
    from ScraperUtil import getDomain
    from ScraperUtil import getDictFromFile
    from ScraperUtil import getDictFromJson
    from ScraperUtil import getDictFromJsonGZ
    from ScraperUtil import getISO8601Timestamp
    from ScraperUtil import getURIRFromMemento
    from ScraperUtil import getUserAgentLst
    from ScraperUtil import gzipTextFile
    from ScraperUtil import isSameLink
    from ScraperUtil import median
    from ScraperUtil import naiveIsURIShort
    from ScraperUtil import parallelTask
    from ScraperUtil import precisionEval
    from ScraperUtil import readTextFromFilesRecursive
    from ScraperUtil import setLogDefaults
    from ScraperUtil import setLoggerDets
    from ScraperUtil import slugifyStr
    
    from Twitter import getHandlesFrmLnks
    from Twitter import getTweetLstName
    from Twitter import getTweetLink
    from Twitter import hydrateUsers
    from Twitter import redactTweetKeys
    from Twitter import twitterSearch
    from Twitter import writeTwtCache

    #from Google import getSubjectExpertQPDets
    #from Google import get_uri_retrv
    from Google import googleSearch

    if __name__ == '__main__':    
        main()
