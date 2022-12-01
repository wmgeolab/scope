import argparse
import logging

logger = logging.getLogger('scraper.scraper')

class MicroCol(object):
    
    def __init__(self, posts, colName=''):
        
        self.posts = posts
        self.colName = colName
        self.postSrc = posts['source'].strip().lower()

        if( self.colName == '' and 'query' in self.posts ):
            self.colName = self.postSrc + ': ' + self.posts['query']

        if( 'col_creation_datetime' in posts ):
            gen_timestamp = posts['col_creation_datetime']
        else:
            gen_timestamp = getISO8601Timestamp()

        self.segmentedCols = {
            'name': self.colName,
            'gen_timestamp': gen_timestamp,
            'segmented_cols': {
                'ss': [],
                'sm': [],#NA
                'ms': [],
                'mm': [],
                'mc': [],
                'degree_1': {
                    'ss': [],
                    'sm': [],#NA
                    'ms': [],
                    'mm': []
                }
            }
        }

        if( self.postSrc == 'reddit' ):
            self.procReddit()
        elif( self.postSrc == 'twitter' ):
            self.procTwitter()

    def procReddit(self):
        genericAddReplyGroup(self.posts, 'posts', redditAuthorComp)
        redditSSColAdd(self.posts, self.segmentedCols, self.colName)
        redditMSColAdd(self.posts, self.segmentedCols, self.colName)
        redditMMColAdd(self.posts, self.segmentedCols, self.colName)

    def procTwitter(self):

        #see MicroCols.py to add degree 1 serp col
        tmp = { 
            'degree_1_twt_col': [{'name': self.colName, 'tweet_links': []}] 
        }

        twitterSSColAdd( self.posts, self.segmentedCols, self.colName, tmp['degree_1_twt_col'] )
        twitterMSColAdd( self.posts, self.segmentedCols, self.colName, tmp['degree_1_twt_col'] )
        twitterMMColAdd( self.posts, self.segmentedCols, self.colName, tmp['degree_1_twt_col'] )

def getArgs():
   
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))
    parser.add_argument('post_files', nargs='+', help='Files containing posts')
    
    parser.add_argument('-d', '--max-file-depth', help='When reading files recursively from directory stop at the specified path depth. 0 means no restriction', type=int, default=1)
    parser.add_argument('-f', '--format', choices=['post_class', 'vis'], help='Output format of file', default='post_class')
    parser.add_argument('-n', '--name', help='Collection name', default='untitled')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-q', '--query', help='Collection query', default='')

    parser.add_argument('--log-file', help='Log output filename', default='')
    parser.add_argument('--log-format', help='Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html', default='')
    parser.add_argument('--log-level', help='Log level', choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'], default='info')
    
    parser.add_argument('--pretty-print', help='Pretty print JSON output', action='store_true')
    
    return parser

def getDefaultArgs(parseKnown=''):
    parser = getArgs()
    
    if( parseKnown == '' ):
        return vars( parser.parse_args() )
    else:
        args, unknown = parser.parse_known_args()
        return vars( args )

def writeFormatedCol(cols, params):

    if( params['format'] == 'post_class' ):
        dumpJsonToFile( params['output'], cols, indentFlag=params['pretty_print'] )
        return

    if( 'segmented_cols' not in cols ):
        return

    allSegCols = {}
    for pc in ['ss', 'sm', 'ms', 'mm', 'mc']:

        allSegCols[pc] = {
            'name': params['name'] + '_' + pc,
            'query': params['query'],
            'uris': [],
            'summary': {},
            'reference_epicenter': {}
        }

        if( pc not in cols['segmented_cols'] ):
            continue

        for i in range ( len(cols['segmented_cols'][pc]) ):
            seg = cols['segmented_cols'][pc][i]

            for j in range( len(seg['uris']) ):
                seg['uris'][j]['post_class'] = pc

            allSegCols[pc]['uris'] += seg['uris']

        allSegCols[pc]['summary']['uri_count'] = len(allSegCols[pc]['uris'])
        allSegCols[pc]['summary']['col_creation_datetime'] = cols['gen_timestamp']

    if( len(allSegCols) == 0 ):
        return

    
    allSegCols['mc']['uris'] = []
    #mc (ms + mm) - start
    dedupSet = set()
    for u in allSegCols['ms']['uris'] + allSegCols['mm']['uris']:
        
        uriKey = getDedupKeyForURI(u['uri'])
        if( uriKey in dedupSet ):
            continue

        dedupSet.add(uriKey)
        allSegCols['mc']['uris'].append(u)
    #mc (ms + mm) - end

    allSegCols['mc']['summary']['uri_count'] = len(allSegCols['mc']['uris'])
    allSegCols['mc']['summary']['col_creation_datetime'] = cols['gen_timestamp']
    
    for pc in ['ss', 'ms', 'mm', 'mc']:
        dumpJsonToFile( params['output'] + '.' + pc, allSegCols[pc], indentFlag=params['pretty_print'] )


def procReq(params):

    cols = []
    posts = readTextFromFilesRecursive( params['post_files'], addDetails=True, maxDepth=params['max_file_depth'] )
    size = len(posts)
    for i in range(size):
        
        posts[i] = getDictFromJson( posts[i]['text'] )

        if( len(posts[i]) == 0 ):
            continue

        if( 'source' not in posts[i] ):
            logger.warning('"source" absent current posts, skipping')
            continue

        mc = MicroCol( posts[i], colName=params['name'])
        if( size == 1 ):
            cols = mc.segmentedCols
        else:
            cols.append( mc.segmentedCols )

    if( params['output'] is not None ):
        writeFormatedCol(cols, params)

def main():
    
    params = getDefaultArgs()
    
    setLogDefaults( params )
    setLoggerDets( logger, params['log_dets'] )
    procReq(params)

if __name__ == 'scraper.MicroCol':
    
    from scraper.RedditUtil.mcReddit import redditAuthorComp
    from scraper.RedditUtil.mcReddit import redditSSColAdd
    from scraper.RedditUtil.mcReddit import redditMSColAdd
    from scraper.RedditUtil.mcReddit import redditMMColAdd

    from scraper.TwitterUtil.mcTwitter import twitterSSColAdd
    from scraper.TwitterUtil.mcTwitter import twitterMSColAdd
    from scraper.TwitterUtil.mcTwitter import twitterMMColAdd
    
    from scraper.ScraperUtil import dumpJsonToFile
    from scraper.ScraperUtil import genericAddReplyGroup
    from scraper.ScraperUtil import getDictFromFile
    from scraper.ScraperUtil import getDictFromJson
    from scraper.ScraperUtil import getDedupKeyForURI
    from scraper.ScraperUtil import getISO8601Timestamp
    from scraper.ScraperUtil import getNowTime
    from scraper.ScraperUtil import readTextFromFilesRecursive
    from scraper.ScraperUtil import setLogDefaults
    from scraper.ScraperUtil import setLoggerDets

else:
    
    from RedditUtil.mcReddit import redditAuthorComp
    from RedditUtil.mcReddit import redditSSColAdd
    from RedditUtil.mcReddit import redditMSColAdd
    from RedditUtil.mcReddit import redditMMColAdd

    from TwitterUtil.mcTwitter import twitterSSColAdd
    from TwitterUtil.mcTwitter import twitterMSColAdd
    from TwitterUtil.mcTwitter import twitterMMColAdd
    
    from ScraperUtil import dumpJsonToFile
    from ScraperUtil import genericAddReplyGroup
    from ScraperUtil import getDictFromFile
    from ScraperUtil import getDictFromJson
    from ScraperUtil import getDedupKeyForURI
    from ScraperUtil import getISO8601Timestamp
    from ScraperUtil import getNowTime
    from ScraperUtil import readTextFromFilesRecursive
    from ScraperUtil import setLogDefaults
    from ScraperUtil import setLoggerDets

    if __name__ == "__main__":
        main()
