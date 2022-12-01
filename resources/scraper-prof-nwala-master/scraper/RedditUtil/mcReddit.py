from datetime import datetime

def redditAuthorComp(a, b):
    if( a['custom']['author'] == b['custom']['author'] ):
        return True
    else:
        return False

def redditGetPstDets(pst, src, degree):

    if( len(pst) == 0 ):        
        return {}

    tmp = {}
    try:
        tmp['src'] = src
        tmp['id'] = pst['id']
        tmp['parent_id'] = pst['parent_id']
        tmp['author'] = pst['custom']['author']
        tmp['uri'] = pst['custom']['permalink']
        tmp['provenance'] = pst['provenance']
        tmp['thread_pos'] = pst['thread_pos']       

        tmp['creation_date'] = datetime.strptime(pst['pub_datetime'], '%Y-%m-%dT%H:%M:%SZ')
        tmp['creation_date'] = str( datetimeFromUtcToLocal(tmp['creation_date']) )
        
        tmp['substitute_text'] = pst['title'] + '\n' + pst['text']
        tmp['substitute_text'] = tmp['substitute_text'].strip()
        tmp['custom'] = {}
        if( 'custom' in pst['custom'] ):
            tmp['custom'] = pst['custom']['custom']

        if( len(pst['link']) == 0 ):
            uriType = 'comment'
        else:
            uriType = getGenericURIType( pst['link'], pst['custom']['permalink'], 'reddit.com', degree=degree )
        
            if( uriType == 'internal_self' ):
                uriType = 'self'
            elif( uriType == 'internal_degree_' + str(degree) ):
                uriType = 'permalink'
            else:
                #external
                indx = tmp['uri'].find('://redd.it/')
                if( indx == 4 or indx == 5 ):
                    uriType = 'external_shortlink'

        tmp['post_uri_type'] = uriType
    except:
        genericErrorInfo()

    return tmp

def redditAddLinksToSegCol(singleSegCol, links, pstDet, degree, dedupSet):

    for l in links:
        l = l.strip()

        if( len(l) == 0 ):
            continue

        uriKey = getDedupKeyForURI(l)
        if( uriKey in dedupSet ):
            continue

        dedupSet.add(uriKey)

        uriType = redditGetURIType(l, pstDet['uri'], 'reddit.com', degree=degree)
        uriDct = {
            'uri': l, 
            'post_details': pstDet,
            'domain': getDomain(l),
            'custom': {'uri_type': 'extra_link_' + uriType, 'is_short': naiveIsURIShort(l)}
        }
        singleSegCol['uris'].append( uriDct )

def redditGetURIType(uri, permalink, chkDomain, degree=1):
    uriType = getGenericURIType( uri, permalink, chkDomain, degree=degree )
    if( uriType == 'external' ):
        #external
        indx = uri.find('://redd.it/')
        if( indx == 4 or indx == 5 ):
            uriType = 'external-shortlink'
    return uriType

def redditAddRootCol(segCol, post, colSrc, singleSegIndx=-1, extraParams=None):

    if( extraParams == None ):
        extraParams = {}
    
    extraParams.setdefault('dedupSet', set())
    extraParams.setdefault('degree', 1)
    
    pstDet = redditGetPstDets(post, colSrc, degree=extraParams['degree'])
    uriType = redditGetURIType( post['link'], post['custom']['permalink'], 'reddit.com', degree=extraParams['degree'] )

    post['link'] = post['link'].strip()
    root = {
        'uri': post['link'], 
        'post_details': pstDet, 
        'custom': {'uri_type': uriType, 'is_short': naiveIsURIShort(post['link'])}
    }
    
    if( singleSegIndx != -1 and singleSegIndx < len(segCol) ):
        singleSegCol = segCol[singleSegIndx]
    else:
        singleSegCol = {}
    
    singleSegCol.setdefault('uris', [])
    singleSegCol.setdefault('stats', {})
    
    #uriType options: internal-self, internal-degree-1, external
    uriKey = getDedupKeyForURI( root['uri'] )
    if( uriType != 'internal-self' and uriKey not in extraParams['dedupSet'] ):

        extraParams['dedupSet'].add(uriKey)
        #don't add self link, but may add links embeded in the post
        if( len(root['uri']) != 0 ):
            #addition into segment also takes place in redditAddLinksToSegCol
            singleSegCol['uris'].append(root)


    redditAddLinksToSegCol(singleSegCol, post['outlinks'], pstDet, extraParams['degree'], extraParams['dedupSet'])
    if( len(singleSegCol['uris']) != 0 and singleSegIndx == -1 ):
        #case where root post is added for the first time, this case is false (singleSegIndx != -1)
        #when a uri from a comment is to be added to singleSegCol which is already in segCol
        singleSegIndx = len(segCol)
        segCol.append( singleSegCol )

    singleSegCol['stats']['uri_count'] = len(singleSegCol['uris'])

    return singleSegIndx

def redditSSColAdd(src, container, colSrc):
    
    colKind = 'ss'
    extraParams = {}
    extraParams['dedupSet'] = set()

    for post in src['posts']:

        post['provenance'] = { 'parent': {'uri': src['self_uris'][0]['uri']} }
        post['thread_pos'] = 0
        singleSegIndx = redditAddRootCol(
            container['segmented_cols'][colKind], 
            post,
            colSrc,
            extraParams=extraParams
        )

        #singleSegIndx indicates an addition of link(s) to a single segment
        if( singleSegIndx != -1 ):
            container['segmented_cols'][colKind][singleSegIndx]['stats']['total_posts'] = 1

def redditMSColAdd(src, container, colSrc):

    colKind = 'ms'
    extraParams = {}
    extraParams['dedupSet'] = set()
    
    for post in src['posts']:
        
        post['thread_pos'] = 0
        if( 'expanded_comments' not in post['custom'] ):
            continue

        if( 'reply_group' not in post['custom'] ):
            continue
        
        containerPrevSize = len(container['segmented_cols'][colKind])
        post['provenance'] = { 'parent': {'uri': src['self_uris'][0]['uri']} }
        singleSegIndx = redditAddRootCol(
            container['segmented_cols'][colKind], 
            post,
            colSrc,
            extraParams=extraParams
        )

        for i in range(len(post['custom']['reply_group'])):
            
            memb = post['custom']['reply_group'][i]
            indx = memb['pos']#this pos is position of member in reply-group list
            
            memb = post['custom']['expanded_comments']['comments'][indx]
            if( len(memb['outlinks']) == 0 ):
                continue
            
            if( memb['parent_id'] == '' ):
                memb['provenance'] = { 'parent': {'uri': src['self_uris'][0]['uri']} }
            else:
                memb['provenance'] = {
                    'parent': {
                        'uri': memb['custom']['permalink'].replace('/' + memb['id'] + '/', '/' + memb['parent_id'].split('_')[-1] + '/')
                    }
                }

            memb['thread_pos'] = i+1
            singleSegIndx = redditAddRootCol(
                container['segmented_cols'][colKind], 
                memb, 
                colSrc + '_comments',
                singleSegIndx=singleSegIndx
            )

        if( containerPrevSize != len(container['segmented_cols'][colKind]) ):
            #count addition of root post and maximum possible elements added to singleSegCol
            container['segmented_cols'][colKind][-1]['stats']['total_posts'] = 1 + len(post['custom']['reply_group'])

def redditMMColAdd(src, container, colSrc):

    colKind = 'mm'
    extraParams = {}
    extraParams['dedupSet'] = set()
    for post in src['posts']:
        
        post['thread_pos'] = 0
        if( 'expanded_comments' not in post['custom'] ):
            continue
        
        post['provenance'] = { 'parent': {'uri': src['self_uris'][0]['uri']} }
        containerPrevSize = len(container['segmented_cols'][colKind])
        singleSegIndx = redditAddRootCol(
            container['segmented_cols'][colKind], 
            post, 
            colSrc,
            extraParams=extraParams
        )


        for i in range(len(post['custom']['expanded_comments']['comments'])):

            com = post['custom']['expanded_comments']['comments'][i]
            com['thread_pos'] = i+1
            if( len(com['outlinks']) == 0 ):
                continue


            if( com['parent_id'] == '' ):
                com['provenance'] = { 'parent': {'uri': src['self_uris'][0]['uri']} }
            else:
                com['provenance'] = {
                    'parent': {
                        'uri': com['custom']['permalink'].replace('/' + com['id'] + '/', '/' + com['parent_id'].split('_')[-1] + '/')
                    }
                }

            singleSegIndx = redditAddRootCol(
                container['segmented_cols'][colKind], 
                com, 
                colSrc + '_comments',
                singleSegIndx=singleSegIndx
            )

        
        if( containerPrevSize != len(container['segmented_cols'][colKind]) ):
            #count addition of root post and maximum possible elements added to singleSegCol
            container['segmented_cols'][colKind][-1]['stats']['total_posts'] = 1 + len(post['custom']['expanded_comments']['comments'])

if __name__ == 'scraper.RedditUtil.mcReddit':

    from scraper.ScraperUtil import datetimeFromUtcToLocal
    from scraper.ScraperUtil import genericErrorInfo
    from scraper.ScraperUtil import getDedupKeyForURI
    from scraper.ScraperUtil import getDomain
    from scraper.ScraperUtil import getGenericURIType
    from scraper.ScraperUtil import naiveIsURIShort
    
else:
    
    from ScraperUtil import datetimeFromUtcToLocal
    from ScraperUtil import genericErrorInfo
    from ScraperUtil import getDedupKeyForURI
    from ScraperUtil import getDomain
    from ScraperUtil import getGenericURIType
    from ScraperUtil import naiveIsURIShort
        