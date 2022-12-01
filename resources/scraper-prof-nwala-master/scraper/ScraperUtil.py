import gzip
import hashlib
import json
import justext
import os
import re
import logging
import requests
import sys
import tarfile
import time


from bs4 import BeautifulSoup
from datetime import datetime
from copy import deepcopy
from boilerpy3 import extractors
from tldextract import extract
from multiprocessing import Pool

import numpy as np
from selenium import webdriver

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize


from subprocess import check_output
from urllib.parse import urlparse

logger = logging.getLogger('scraper.scraper')

def printPayload(src, serp, title=''):

    print('\nprintPayload(), src:', src)
    if( title != '' ):
        print(title)

    if( src == 'google' or src == 'reddit' ):
        printGoogleReddit(serp)
    
    elif( src == 'twitter' ):
        printTwitter(serp)

def printGoogleReddit(serp):
    
    if( len(serp) == 0 ):
        return
    
    if( 'links' in serp ):
        src = 'links'
    elif( 'posts' in serp ):
        src = 'posts'
    else:
        return

    for i in range( len(serp[src]) ):
        print( i+1, serp[src][i]['link'] )

def printTwitter(serp):
    
    if( len(serp) == 0 ):
        return

    if( 'tweets' not in serp ):
        return

    counter = 1
    for i in range( len(serp['tweets']) ):

        if( 'tweet_links' not in serp['tweets'][i] ):
            continue

        for link in serp['tweets'][i]['tweet_links']:
            
            print(counter, link['uri'])
            counter += 1



#http://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime
# From 2015-07-12 18:45:11datetime_from_utc_to_local
def datetimeFromUtcToLocal(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
    return utc + offset

def datetimeFromLocalToUtc(local):
    UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
    return local + UTC_OFFSET_TIMEDELTA

def getNowTime():

    now = str(datetime.now()).split('.')[0]
    return now

def getISO8601Timestamp():
    return datetime.utcnow().isoformat().split('.')[0] + 'Z'

def setLoggerDets(logger, loggerDets):

    if( len(loggerDets) == 0 ):
        return

    consoleHandler = logging.StreamHandler()

    if( 'level' in loggerDets ):
        logger.setLevel( loggerDets['level'] )
    else:
        logger.setLevel( logging.INFO )

    if( 'file' in loggerDets ):
        loggerDets['file'] = loggerDets['file'].strip()
        
        if( loggerDets['file'] != '' ):
            fileHandler = logging.FileHandler( loggerDets['file'] )
            procLogHandler(fileHandler, loggerDets)

    procLogHandler(consoleHandler, loggerDets)

def setLogDefaults(params):
    
    params['log_dets'] = {}

    if( params['log_level'] == '' ):
        params['log_dets']['level'] = logging.INFO
    else:
        
        logLevels = {
            'CRITICAL': 50,
            'ERROR': 40,
            'WARNING': 30,
            'INFO': 20,
            'DEBUG': 10,
            'NOTSET': 0
        }

        params['log_level'] = params['log_level'].strip().upper()

        if( params['log_level'] in logLevels ):
            params['log_dets']['level'] = logLevels[ params['log_level'] ]
        else:
            params['log_dets']['level'] = logging.INFO
    
    params['log_format'] = params['log_format'].strip()
    params['log_file'] = params['log_file'].strip()

    if( params['log_format'] != '' ):
        params['log_dets']['format'] = params['log_format']

    if( params['log_file'] != '' ):
        params['log_dets']['file'] = params['log_file']

def procLogHandler(handler, loggerDets):
    
    if( handler is None ):
        return
        
    if( 'level' in loggerDets ):
        handler.setLevel( loggerDets['level'] )    
        
        if( loggerDets['level'] == logging.ERROR ):
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s :\n%(message)s')
            handler.setFormatter(formatter)

    if( 'format' in loggerDets ):
        
        loggerDets['format'] = loggerDets['format'].strip()
        if( loggerDets['format'] != '' ):
            formatter = logging.Formatter( loggerDets['format'] )
            handler.setFormatter(formatter)

    logger.addHandler(handler)


def parallelProxy(job):
    
    output = job['func'](**job['args'])

    if( 'print' in job ):
        if( len(job['print']) != 0 ):
            logger.info( job['print'] )

    return {'input': job, 'output': output, 'misc': job['misc']}

'''
    jobsLst: {
                'func': function,
                'args': {functionArgName0: val0,... functionArgNamen: valn}
                'misc': ''
             }
    
    usage example:
    jobsLst = []
    keywords = {'uri': 'http://www.odu.edu'}
    jobsLst.append( {'func': getDedupKeyForURI, 'args': keywords} )

    keywords = {'uri': 'http://www.cnn.com'}
    jobsLst.append( {'func': getDedupKeyForURI, 'args': keywords} )

    keywords = {'uri': 'http://www.arsenal.com'}
    jobsLst.append( {'func': getDedupKeyForURI, 'args': keywords} )

    print( parallelTask(jobsLst) )
'''
def parallelTask(jobsLst, threadCount=5):

    if( len(jobsLst) == 0 ):
        return []

    if( threadCount < 2 ):
        threadCount = 2

    try:
        workers = Pool(threadCount)
        resLst = workers.map(parallelProxy, jobsLst)
        
        workers.close()
        workers.join()
    except:
        genericErrorInfo( '\terror func: ' + str(jobsLst[0]['func']) )
        return []

    return resLst


def genericErrorInfo(slug=''):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    
    errMsg = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
    logger.error(errMsg + slug)

    return errMsg

def getDictFromJsonGZ(path):

    json = getTextFromGZ(path)
    if( len(json) == 0 ):
        return {}
    return getDictFromJson(json)

def gzipTextFile(path, txt):
    
    try:
        with gzip.open(path, 'wb') as f:
            f.write(txt.encode())
    except:
        genericErrorInfo()


def getTextFromGZ(path):
    
    try:
        with gzip.open(path, 'rb') as f:
            return f.read().decode('utf-8')
    except:
        genericErrorInfo()

    return ''

def readTextFromTar(filename, addDetails=True):

    payload = []
    try:
        tar = tarfile.open(filename, 'r:*')

        for tarinfo in tar.getmembers():
            if tarinfo.isreg():

                try:
                    f = tar.extractfile(tarinfo)
                    text = f.read()
                    
                    if( tarinfo.name.endswith('.gz') ):
                        text = gzip.decompress(text)
                    
                    text = text.decode('utf-8')
                    if( text != '' ):
                        if( addDetails is True ):
                            extra = {'src': filename}
                            text = getTextDetails( filename=os.path.basename(tarinfo.name), text=text, extra=extra )
                        
                        payload.append(text)

                except UnicodeDecodeError as e:
                    logger.error('\nreadTextFromTar(), UnicodeDecodeError file: ' + tarinfo.name)
                except:
                    genericErrorInfo('\n\treadTextFromTar(), Error reading file: ' + tarinfo.name)

        tar.close()
    except:
        genericErrorInfo()

    return payload

def readTextFromFile(infilename):

    try:
        with open(infilename, 'r') as infile:
            return infile.read()
    except:
        genericErrorInfo( '\n\treadTextFromFile(), error filename: ' + infilename )

    return ''

def readTextFromFilesRecursive(files, addDetails=True, curDepth=0, maxDepth=0):

    if( isinstance(files, str) ):
        files = [files]

    if( isinstance(files, list) is False ):
        return []

    if( maxDepth != 0 and curDepth > maxDepth ):
        return []

    result = []
    for f in files:

        f = f.strip()
        
        if( f.endswith('.tar') or f.endswith('.tar.gz') ):
            result += readTextFromTar(f, addDetails=addDetails)

        elif( f.endswith('.gz') ):
            
            text = getTextFromGZ(f)
            if( text != '' ):
                if( addDetails is True ):
                    extra = {'depth': curDepth}
                    text = getTextDetails(filename=f, text=text, extra=extra)
                
                result.append(text)

        elif( os.path.isfile(f) ):

            text = readTextFromFile(f)
            if( text != '' ):
                if( addDetails is True ):
                    extra = {'depth': curDepth}
                    text = getTextDetails(filename=f, text=text, extra=extra)
                
                result.append(text)
        
        elif( os.path.isdir(f) ):
    
            if( f.endswith('/') is False ):
                f = f + '/'
            
            secondLevelFiles = os.listdir(f)
            secondLevelFiles = [f + f2 for f2 in secondLevelFiles]
            result += readTextFromFilesRecursive(secondLevelFiles, addDetails=addDetails, curDepth=curDepth+1, maxDepth=maxDepth)

    return result

def getTextDetails(filename, text, extra=None):
    
    if( extra is None ):
        extra = {}

    payload = {'filename': filename, 'text': text}

    for key, val in extra.items():
        payload[key] = val

    return payload

def writeTextToFile(outfilename, text, extraParams=None):
    
    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('verbose', True)

    try:
        with open(outfilename, 'w') as outfile:
            outfile.write(text)
        
        if( extraParams['verbose'] ):
            logger.info('\twriteTextToFile(), wrote: ' + outfilename)
    except:
        genericErrorInfo()

def sortDctByKey(dct, key, reverse=True):

    key = key.strip()
    if( len(dct) == 0 or len(key) == 0 ):
        return []

    return sorted(dct.items(), key=lambda x: x[1][key], reverse=reverse)

def getDictFromFile(filename):

    filename = filename.strip()
    if( filename == '' ):
        return {}

    try:

        if( os.path.exists(filename) == False ):
            return {}

        return getDictFromJson( readTextFromFile(filename) )
    except:
        genericErrorInfo('\n\tgetDictFromFile(): error filename: ' + filename)

    return {}

def getDictFromJson(jsonStr):

    try:
        return json.loads(jsonStr)
    except:
        genericErrorInfo('\tjsonStr prefix: ' + jsonStr[:100])

    return {}

def dumpJsonToFile(outfilename, dictToWrite, indentFlag=True, extraParams=None):

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('verbose', True)

    try:
        outfile = open(outfilename, 'w')
        
        if( indentFlag ):
            json.dump(dictToWrite, outfile, ensure_ascii=False, indent=4)#by default, ensure_ascii=True, and this will cause  all non-ASCII characters in the output are escaped with \uXXXX sequences, and the result is a str instance consisting of ASCII characters only. Since in python 3 all strings are unicode by default, forcing ascii is unecessary
        else:
            json.dump(dictToWrite, outfile, ensure_ascii=False)

        outfile.close()

        if( extraParams['verbose'] ):
            logger.info('\tdumpJsonToFile(), wrote: ' + outfilename)
    except:
        genericErrorInfo('\n\terror: outfilename: ' + outfilename)

def getUserAgentLst():
    return [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3955.4 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3948.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3958.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    ]

def getCustomHeaderDict():

    '''
        Reviewing situation where captcha was seen, considering whether variation of user-agent could fix the problem
    '''
    userAgents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
    ]
    headers = {
        'User-Agent': userAgents[0],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connnection': 'keep-alive',
        'Cache-Control':'max-age=0' 
        }

    return headers

def isSizeLimitExceed(responseHeaders, sizeRestrict):

    if( 'Content-Length' in responseHeaders ):
        if( int(responseHeaders['Content-Length']) > sizeRestrict ):
            return True

    return False

def downloadSave(response, outfile):
    
    try:
        with open(outfile, 'wb') as dfile:
            for chunk in response.iter_content(chunk_size=1024): 
                # writing one chunk at a time to pdf file 
                if(chunk):
                    dfile.write(chunk) 
    except:
        genericErrorInfo()

def seleniumLoadWebpage(driver, uri, waitTimeInSeconds=10, closeBrowserFlag=True, extraParams=None):
    
    logger.info( '\nseleniumLoadWebpage():' )

    uri = uri.strip()
    if( len(uri) == 0 ):
        return ''
    html = ''

    if( extraParams is None ):
        extraParams = {}

    #directive: consider phantom js but set header
    try:
        logger.info('\tgetting: ' + uri)

        driver.get(uri)
        '''
            this statement
            driver.maximize_window()
            unknown error: cannot get automation extension\nfrom unknown error
        '''

        if( waitTimeInSeconds > 0 ):
            logger.info('\tsleep seconds: ' +  str(waitTimeInSeconds))
            time.sleep(waitTimeInSeconds)

        if( 'script' in extraParams ):
            driver.execute_script( extraParams['script'] )

        html = driver.page_source.encode('utf-8')
        if( closeBrowserFlag ):
            driver.quit()
    except:
        genericErrorInfo()
        return ''

    return html

def mimicBrowser(uri, getRequestFlag=True, timeout=10, sizeRestrict=-1, saveFilePath=None, headers={}):
    
    uri = uri.strip()
    payload = {'self': uri, 'text': ''}

    if( uri == '' ):
        return payload

    tmpHeader = getCustomHeaderDict()
    for h, hVal in tmpHeader.items():
        if( h not in headers ):
            headers[h] = hVal

    try:
        response = ''
        reponseText = ''
        if( getRequestFlag is True ):

            if( saveFilePath is None ):
                response = requests.get(uri, headers=headers, timeout=timeout)
            else:
                response = requests.get(uri, headers=headers, timeout=timeout, stream=True)
                
            
            if( sizeRestrict != -1 ):
                if( isSizeLimitExceed(response.headers, sizeRestrict) ):
                    payload['text'] = 'Error: Exceeded size restriction: ' + str(sizeRestrict)
                    return payload

            
            if( saveFilePath is None ):
                reponseText = response.text
            else:
                downloadSave(response, saveFilePath)
                
            
            payload['response_header'] = response.headers 
            payload['text'] = reponseText
        else:
            response = requests.head(uri, headers=headers, timeout=timeout)
            response.headers['status_code'] = response.status_code
            payload['response_header'] = response.headers
    except:
        genericErrorInfo('\n\tmimicBrowser(), error uri: ' + uri)
    
    return payload

def naiveIsURIShort(uri):

    specialCases = ['tinyurl.com']

    try:
        scheme, netloc, path, params, query, fragment = urlparse( uri )
        if( netloc in specialCases ):
            return True

        path = path.strip()
        if( len(path) != 0 ):
            if( path[0] == '/' ):
                path = path[1:]

        path = path.split('/')
        if( len(path) > 1 ):
            #path length exceeding 1 is not considered short
            return False

        tld = extract(uri).suffix
        tld = tld.split('.')
        if( len(tld) == 1 ):
            #e.g., tld = 'com', 'ly'
            #short: http://t.co (1 dot) not news.sina.cn (2 dots)
            if( len(tld[0]) == 2 and netloc.count('.') == 1 ):
                return True
        else:
            #e.g., tld = 'co.uk'
            return False
    except:
        genericErrorInfo()

    return False

def slugifyStr(txt):
    return ''.join([ c if c.isalnum() else '_' for c in txt ])

def getStrHash(txt):
    txt = txt.strip()
    hash_object = hashlib.md5(txt.encode())
    return hash_object.hexdigest()

def expanUrlSecondTry(url, curIter=0, maxIter=100):

    '''
    Attempt to get first good location. For defunct urls with previous past
    '''

    url = url.strip()
    if( len(url) == 0 ):
        return ''

    if( maxIter % 10 == 0 ):
        logger.info('\n' + str(maxIter) + ' expanUrlSecondTry(): url - ' + url)

    if( curIter>maxIter ):
        return url


    try:

        # when using find, use outputLowercase
        # when indexing, use output
        
        output = check_output(['curl', '-s', '-I', '-m', '10', url])
        output = output.decode('utf-8')
        
        outputLowercase = output.lower()
        indexOfLocation = outputLowercase.rfind('\nlocation:')

        if( indexOfLocation != -1 ):
            # indexOfLocation + 1: skip initial newline preceding location:
            indexOfNewLineAfterLocation = outputLowercase.find('\n', indexOfLocation + 1)
            redirectUrl = output[indexOfLocation:indexOfNewLineAfterLocation]
            redirectUrl = redirectUrl.split(' ')[1]

            return expanUrlSecondTry(redirectUrl, curIter+1, maxIter)
        else:
            return url

    except:
        genericErrorInfo( '\n\texpanUrlSecondTry(), error url: ' + url )
    

    return url

def getURIRFromMemento(memento):
    
    memento = memento.strip()
    if( len(memento) == 0 ):
        return ''

    colonSlashSlash = memento.rfind('://')
    if( colonSlashSlash == -1 ):
        return ''
    else:
        indxScheme = memento[:colonSlashSlash].rfind('/')
        
        if( indxScheme == -1 ):
            return ''

        return memento[indxScheme + 1:]

def expandUrl(url, secondTryFlag=True, timeoutInSeconds='10'):

    #http://tmblr.co/ZPYSkm1jl_mGt, http://bit.ly/1OLMlIF
    timeoutInSeconds = str(timeoutInSeconds)
    '''
    Part A: Attempts to unshorten the uri until the last response returns a 200 or 
    Part B: returns the lasts good url if the last response is not a 200.
    '''
    url = url.strip()
    if( len(url) == 0 ):
        return ''
    
    try:
        #Part A: Attempts to unshorten the uri until the last response returns a 200 or 
        output = check_output(['curl', '-s', '-I', '-L', '-m', '10', '-c', 'cookie.txt', url])
        output = output.decode('utf-8')
        output = output.splitlines()
        
        longUrl = ''
        path = ''
        locations = []

        for line in output:
            line = line.strip()
            if( len(line) == 0 ):
                continue

            indexOfLocation = line.lower().find('location:')
            if( indexOfLocation != -1 ):
                #location: is 9
                locations.append(line[indexOfLocation + 9:].strip())

        if( len(locations) != 0 ):
            #traverse location in reverse: account for redirects to path
            #locations example: ['http://www.arsenal.com']
            #locations example: ['http://www.arsenal.com', '/home#splash']
            for url in locations[::-1]:
                
                if( url.strip().lower().find('/') == 0 and len(path) == 0 ):
                    #find path
                    path = url

                if( url.strip().lower().find('http') == 0 and len(longUrl) == 0 ):
                    #find url
                    
                    #ensure url doesn't end with / - start
                    #if( url[-1] == '/' ):
                    #   url = url[:-1]
                    #ensure url doesn't end with / - end

                    #ensure path begins with / - start
                    if( len(path) != 0 ):
                        if( path[0] != '/' ):
                            path = '/' + path
                    #ensure path begins with / - end

                    longUrl = url + path

                    #break since we are looking for the last long unshortened uri with/without a path redirect
                    break
        else:
            longUrl = url



        return longUrl
    except Exception as e:
        #Part B: returns the lasts good url if the last response is not a 200.
        genericErrorInfo( '\n\terror url: ' + url + ', e: ' + str(e) )

        
        
        if( secondTryFlag ):
            logger.info('\nexpandUrl(): second try')
            return expanUrlSecondTry(url)
        else:
            return url

def isSameLink(left, right):
    return getDedupKeyForURI(left) == getDedupKeyForURI(right)

def getStrBetweenMarkers(inputStr, beginMarker, endMarker, startIndex=0):

    begIndex = inputStr.find(beginMarker, startIndex)
    
    if( begIndex != -1 ):
        begIndex += len(beginMarker)
        endIndex = inputStr.find(endMarker, begIndex)
        if( endIndex != -1 ):
            return inputStr[begIndex:endIndex].strip(), endIndex

    return '', -1

def getDedupKeyForURI(uri):

    uri = uri.strip()
    if( len(uri) == 0 ):
        return ''

    exceptionDomains = ['www.youtube.com']

    try:
        scheme, netloc, path, params, query, fragment = urlparse( uri )
        
        netloc = netloc.strip()
        path = path.strip()
        optionalQuery = ''

        if( len(path) != 0 ):
            if( path[-1] != '/' ):
                path = path + '/'

        if( netloc in exceptionDomains ):
            optionalQuery = query.strip()

        netloc = netloc.replace(':80', '')
        return netloc + path + optionalQuery
    except:
        genericErrorInfo( '\n\tgetDedupKeyForURI(), Error uri: ' + uri )

    return ''

def getChromedriver(chromedriverPath, userAgent=''):

    driver = None
    try:
        if( chromedriverPath is None ):
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--headless")
            chromeOptions.add_argument("--window-size=500x1500")#1920x1080
            chromeOptions.add_argument("--disable-dev-shm-usage")
            chromeOptions.add_argument("--no-sandbox")
            if( userAgent != '' ):
                chromeOptions.add_argument('--user-agent="' + userAgent + '"')
        
            driver = webdriver.Chrome(options=chromeOptions)
        else:
            driver = webdriver.Chrome(executable_path=chromedriverPath)
    except:
        genericErrorInfo()

    if( driver is None ):
        try:
            driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        except:
            genericErrorInfo()
    
    return driver

def extractPageTitleFromHTML(html):

    title = ''
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')

        if( title is None ):
            title = ''
        else:
            title = title.text.strip()
    except:
        genericErrorInfo()

    return title

def clean_html(html, method='python-boilerpipe'):
    
    if( html == '' ):
        return ''

    method = method.strip().lower()
    #experience problem of parallelizing, maybe due to: https://stackoverflow.com/questions/8804830/python-multiprocessing-pickling-error
    if( method == 'python-boilerpipe' ):
        try:
            extractor = extractors.ArticleExtractor()
            return extractor.get_content(html)
        except:
            genericErrorInfo()

    elif( method == 'justext' ):
        try:
            
            plaintext = ''
            paragraphs = justext.justext(html, justext.get_stoplist("English"))
            
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    plaintext = plaintext + paragraph.text + '\n'

            return plaintext
        except:
            genericErrorInfo()

    elif( method == 'nltk' ):
        """
        Copied from NLTK package.
        Remove HTML markup from the given string.

        :param html: the HTML string to be cleaned
        :type html: str
        :rtype: str
        """

        # First we remove inline JavaScript/CSS:
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)

        #my addition to remove blank lines
        cleaned = re.sub("\n\s*\n*", "\n", cleaned)

        return cleaned.strip()

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

def derefURI(uri, sleepSec=0, timeout=10, sizeRestrict=4000000, headers={}, extraParams=None):
    
    uri = uri.strip()
    if( uri == '' ):
        return ''

    if( extraParams is None ):
        extraParams = {}

    htmlPage = ''
    extraParams.setdefault('chromedriver_path', '')
    extraParams.setdefault('chromedriver', None)
    extraParams.setdefault('leave_browser_open', False)
    extraParams.setdefault('delay_sec', 0)
    extraParams.setdefault('html_cache_file', '')

    #check for custom headers - start
    for ky, val in extraParams.items():
        if( ky.startswith('header-') is False ):
            continue
        #custom header example: header-user-agent, header-cache-control
        custHeader = ky.split('-')[1:]

        custHeader = [h.capitalize() for h in custHeader]
        custHeader = '-'.join(custHeader)
        headers[custHeader] = val
    #check for custom headers - end

    try:

        if( extraParams['html_cache_file'] != '' ):
            htmlPage = getTextFromGZ( extraParams['html_cache_file'] )

            if( htmlPage != '' ):
                logger.info( '\tderefURI(), cache hit' )
                return htmlPage


        if( sleepSec > 0 ):
            logger.info( '\tderefURI(), sleep: ' + str(sleepSec) )
            time.sleep(sleepSec)


        driver = None
        if( extraParams['chromedriver'] is not None ):
            driver = extraParams['chromedriver']
        
        elif( extraParams['chromedriver_path'] != '' ):
            driver = getChromedriver( extraParams['chromedriver_path'] )
        

        if( driver is not None ):

            driver.get(uri)
            if( extraParams['delay_sec'] > 0 ):
                logger.info( '\tderefURI(), delay sleep: ' + str(extraParams['delay_sec']) )
                time.sleep( extraParams['delay_sec'] )
                #extraParams['delay_sec'] = -1 * extraParams['delay_sec']

            htmlPage = driver.page_source.encode('utf-8')
            if( extraParams['leave_browser_open'] is False ):
                driver.quit()

        if( htmlPage == '' ):
            htmlPage = mimicBrowser(uri, sizeRestrict=sizeRestrict, headers=headers, timeout=timeout)
            htmlPage = htmlPage['text']

        if( extraParams['html_cache_file'] != '' ):
            gzipTextFile( extraParams['html_cache_file'], htmlPage )
    except:
        genericErrorInfo()
    
    return htmlPage

def getDomain(url, includeSubdomain=False, excludeWWW=True):

    url = url.strip()
    if( len(url) == 0 ):
        return ''

    if( url.find('http') == -1  ):
        url = 'http://' + url

    domain = ''
    
    try:
        ext = extract(url)
        
        domain = ext.domain.strip()
        subdomain = ext.subdomain.strip()
        suffix = ext.suffix.strip()

        if( len(suffix) != 0 ):
            suffix = '.' + suffix 

        if( len(domain) != 0 ):
            domain = domain + suffix
        
        if( excludeWWW ):
            if( subdomain.find('www') == 0 ):
                if( len(subdomain) > 3 ):
                    subdomain = subdomain[4:]
                else:
                    subdomain = subdomain[3:]


        if( len(subdomain) != 0 ):
            subdomain = subdomain + '.'

        if( includeSubdomain ):
            domain = subdomain + domain
    except:
        genericErrorInfo()
        return ''

    return domain

def getTopKDomainStats(links, k):

    linkCount = len(links)
    if( linkCount == 0 or k == 0 ):
        return {}

    domainDict = {}
    for link in links:

        if( isinstance(link, dict) ):
            for key in ['uri', 'link']:
                if( key in link ):
                    link = link[key]
                    break

        domain = getDomain(link)

        domain = domain.strip()
        if( domain == '' ):
            continue

        domainDict.setdefault(domain, 0)
        domainDict[domain] += 1

    sortedTopKDomains = sorted( domainDict.items(), key=lambda x: x[1], reverse=True )
    sortedTopKDomains = sortedTopKDomains[:k]

    topKDomLinkCount = 0
    for i in range(len(sortedTopKDomains)):
        domain, domainCount = sortedTopKDomains[i]
        topKDomLinkCount += domainCount

    return {
        'top_k_domain_link_count': topKDomLinkCount,
        'col_frac': topKDomLinkCount/linkCount,
        'top_k_domains': sortedTopKDomains,
        'k': k
    }

def overlapFor2Sets(firstSet, secondSet):

    intersection = float(len(firstSet & secondSet))
    minimum = min(len(firstSet), len(secondSet))

    if( minimum != 0 ):
        return  round(intersection/minimum, 4)
    else:
        return 0

def jaccardFor2Sets(firstSet, secondSet):

    intersection = float(len(firstSet & secondSet))
    union = len(firstSet | secondSet)

    if( union != 0 ):
        return  round(intersection/union, 4)
    else:
        return 0

def valueToFloat(num):
    
    if type(num) == float or type(num) == int:
        return num

    num = num.replace(',', '')
    multiplier = {
        'K': 1000.0,
        'M': 1000000.0,
        'B': 1000000000.0
    }
    
    for mult, multi in multiplier.items():
        if mult in num:
            if len(num) > 1:
                
                try:
                    return float(num.replace(mult, '')) * multi
                except:
                    pass

            return multi

    try:
        return float(num)
    except:
        return 0.0

#credit to: https://github.com/mapado/haversine/blob/master/haversine/__init__.py
def haversine(point1, point2, miles=True):
    from math import radians, cos, sin, asin, sqrt
    """ Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance bewteen the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
    AVG_EARTH_RADIUS = 6371  # in km

    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
    if miles:
        return h * 0.621371  # in miles
    else:
        return h  # in kilometers

def median(dataPoints, sortedFlag=True):

    #credit: https://github.com/Mashimo/datascience/blob/master/datascience/stats.py
    if not dataPoints:
        raise ValueError('no data points passed')

    if( sortedFlag is True ):
        dataPoints = sorted(dataPoints)

    mid = len(dataPoints) // 2  #floor division for int
    median = 0
    if (len(dataPoints) % 2 == 0):
        median = (dataPoints[mid-1] + dataPoints[mid]) / 2.0
    else:
        median = dataPoints[mid]

    return median

#micro cols - start
def getGenericURIType(uri, permalink, chkDomain, degree=1):

    uri = uri.strip()
    if( len(uri) == 0 ):
        return ''

    uriType = ''
    if( getDomain(uri, includeSubdomain=False) == chkDomain ):
        if( isSameLink(permalink, uri) ):
            uriType = 'internal_self'
        else:
            uriType = 'internal_degree_' + str(degree)
    else:
        uriType = 'external'

    return uriType

def genericAddReplyGroup(src, srckey, authorCompFunc):

    if( srckey not in src ):
        return

    for i in range( len(src[srckey]) ):
        
        seg = src[srckey][i]
        if( 'expanded_comments' not in seg['custom'] ):
            continue            

        comments = seg['custom']['expanded_comments']['comments']
        if( len(comments) == 0 ):
            continue

        if( authorCompFunc(seg, comments[0]) == False ):
            continue


        seg['custom']['reply_group'] = []
        for j in range(len(comments)):
            
            if( authorCompFunc(seg, comments[j]) == False ):
                break
            tmp = {
                'id': comments[j]['id'],
                'pos': j
            }
            seg['custom']['reply_group'].append(tmp)
#micro cols - end
def precisionEval(goldColOrFilename, testColOrFilename, cachePath, simCoeff=0.3, extraParams=None):

    if( extraParams is None ):
        extraParams = {}

    if( isinstance(goldColOrFilename, str) ):
        goldstandard = getDictFromFile(goldColOrFilename)
    else:
        goldstandard = goldColOrFilename
    gs = PrecEval( goldstandard=goldstandard, cachePath=cachePath, simCoeff=simCoeff )
    
    if( isinstance(testColOrFilename, str) ):
        testCol = getDictFromFile(testColOrFilename)
    else:
        testCol = testColOrFilename
    PrecEval.getHTMLTextForURILst( col=testCol, cachePath=cachePath )

    testCol['timestamp'] = getISO8601Timestamp()
    testCol['predicted_precision'] = PrecEval.prlEvalCol( testCol, gs.goldstandard, cachePath, gs.simCoeff, extraParams=extraParams )
    testCol['sim_coeff'] = gs.simCoeff
    
    return {'goldstandard': gs.goldstandard, 'test_col': testCol}

class DocVect(object):

    @staticmethod
    def getStopwordsSet(frozenSetFlag=False):
        stopwords = DocVect.getStopwordsDict()
        
        if( frozenSetFlag ):
            return frozenset(stopwords.keys())
        else:
            return set(stopwords.keys())

    @staticmethod
    def getStopwordsDict():

        stopwordsDict = {
            "a": True,
            "about": True,
            "above": True,
            "across": True,
            "after": True,
            "afterwards": True,
            "again": True,
            "against": True,
            "all": True,
            "almost": True,
            "alone": True,
            "along": True,
            "already": True,
            "also": True,
            "although": True,
            "always": True,
            "am": True,
            "among": True,
            "amongst": True,
            "amoungst": True,
            "amount": True,
            "an": True,
            "and": True,
            "another": True,
            "any": True,
            "anyhow": True,
            "anyone": True,
            "anything": True,
            "anyway": True,
            "anywhere": True,
            "are": True,
            "around": True,
            "as": True,
            "at": True,
            "back": True,
            "be": True,
            "became": True,
            "because": True,
            "become": True,
            "becomes": True,
            "becoming": True,
            "been": True,
            "before": True,
            "beforehand": True,
            "behind": True,
            "being": True,
            "below": True,
            "beside": True,
            "besides": True,
            "between": True,
            "beyond": True,
            "both": True,
            "but": True,
            "by": True,
            "can": True,
            "can\'t": True,
            "cannot": True,
            "cant": True,
            "co": True,
            "could not": True,
            "could": True,
            "couldn\'t": True,
            "couldnt": True,
            "de": True,
            "describe": True,
            "detail": True,
            "did": True,
            "do": True,
            "does": True,
            "doing": True,
            "done": True,
            "due": True,
            "during": True,
            "e.g": True,
            "e.g.": True,
            "e.g.,": True,
            "each": True,
            "eg": True,
            "either": True,
            "else": True,
            "elsewhere": True,
            "enough": True,
            "etc": True,
            "etc.": True,
            "even though": True,
            "ever": True,
            "every": True,
            "everyone": True,
            "everything": True,
            "everywhere": True,
            "except": True,
            "for": True,
            "former": True,
            "formerly": True,
            "from": True,
            "further": True,
            "get": True,
            "go": True,
            "had": True,
            "has not": True,
            "has": True,
            "hasn\'t": True,
            "hasnt": True,
            "have": True,
            "having": True,
            "he": True,
            "hence": True,
            "her": True,
            "here": True,
            "hereafter": True,
            "hereby": True,
            "herein": True,
            "hereupon": True,
            "hers": True,
            "herself": True,
            "him": True,
            "himself": True,
            "his": True,
            "how": True,
            "however": True,
            "i": True,
            "ie": True,
            "i.e": True,
            "i.e.": True,
            "if": True,
            "in": True,
            "inc": True,
            "inc.": True,
            "indeed": True,
            "into": True,
            "is": True,
            "it": True,
            "its": True,
            "it's": True,
            "itself": True,
            "just": True,
            "keep": True,
            "latter": True,
            "latterly": True,
            "less": True,
            "made": True,
            "make": True,
            "may": True,
            "me": True,
            "meanwhile": True,
            "might": True,
            "mine": True,
            "more": True,
            "moreover": True,
            "most": True,
            "mostly": True,
            "move": True,
            "must": True,
            "my": True,
            "myself": True,
            "namely": True,
            "neither": True,
            "never": True,
            "nevertheless": True,
            "next": True,
            "no": True,
            "nobody": True,
            "none": True,
            "noone": True,
            "nor": True,
            "not": True,
            "nothing": True,
            "now": True,
            "nowhere": True,
            "of": True,
            "off": True,
            "often": True,
            "on": True,
            "once": True,
            "one": True,
            "only": True,
            "onto": True,
            "or": True,
            "other": True,
            "others": True,
            "otherwise": True,
            "our": True,
            "ours": True,
            "ourselves": True,
            "out": True,
            "over": True,
            "own": True,
            "part": True,
            "per": True,
            "perhaps": True,
            "please": True,
            "put": True,
            "rather": True,
            "re": True,
            "same": True,
            "see": True,
            "seem": True,
            "seemed": True,
            "seeming": True,
            "seems": True,
            "several": True,
            "she": True,
            "should": True,
            "show": True,
            "side": True,
            "since": True,
            "sincere": True,
            "so": True,
            "some": True,
            "somehow": True,
            "someone": True,
            "something": True,
            "sometime": True,
            "sometimes": True,
            "somewhere": True,
            "still": True,
            "such": True,
            "take": True,
            "than": True,
            "that": True,
            "the": True,
            "their": True,
            "theirs": True,
            "them": True,
            "themselves": True,
            "then": True,
            "thence": True,
            "there": True,
            "thereafter": True,
            "thereby": True,
            "therefore": True,
            "therein": True,
            "thereupon": True,
            "these": True,
            "they": True,
            "this": True,
            "those": True,
            "though": True,
            "through": True,
            "throughout": True,
            "thru": True,
            "thus": True,
            "to": True,
            "together": True,
            "too": True,
            "toward": True,
            "towards": True,
            "un": True,
            "until": True,
            "upon": True,
            "us": True,
            "very": True,
            "via": True,
            "was": True,
            "we": True,
            "well": True,
            "were": True,
            "what": True,
            "whatever": True,
            "when": True,
            "whence": True,
            "whenever": True,
            "where": True,
            "whereafter": True,
            "whereas": True,
            "whereby": True,
            "wherein": True,
            "whereupon": True,
            "wherever": True,
            "whether": True,
            "which": True,
            "while": True,
            "whither": True,
            "who": True,
            "whoever": True,
            "whole": True,
            "whom": True,
            "whose": True,
            "why": True,
            "will": True,
            "with": True,
            "within": True,
            "without": True,
            "would": True,
            "yet": True,
            "you": True,
            "your": True,
            "yours": True,
            "yourself": True,
            "yourselves": True
        }
        
        return stopwordsDict

    @staticmethod
    def getNgram(docList, ngramRange=(2, 2), tokenPattern=r'(?u)\b[a-zA-Z\'\’-]+[a-zA-Z]+\b|\d+[.,]?\d*', binaryTF=False, minDF=1):
        
        if( len(docList) == 0 ):
            return {}
        
        try:
            countVectorizer = CountVectorizer(stop_words=DocVect.getStopwordsSet(), ngram_range=ngramRange, token_pattern=tokenPattern, binary=binaryTF, min_df=minDF)
            countVectorizer.fit_transform(docList)
            return countVectorizer.vocabulary_
        except:
            genericErrorInfo()
            return {}

    @staticmethod
    def cosineSim(X, Y):
        try:
            X2Norm = np.linalg.norm(X, 2)
            Y2Norm = np.linalg.norm(Y, 2)
            
            if( X2Norm == 0 or Y2Norm == 0 ):
                return 0

            return round(np.dot(X, Y)/(X2Norm * Y2Norm), 10)
        except:
            genericErrorInfo()
            return 0

    @staticmethod
    def getTFMatrixFromDocList(oldDocList, params=None):

        if( len(oldDocList) == 0 ):
            return {}

        docList = [ d for d in oldDocList if len(d) != 0 ]
        if( len(docList) == 0 ):
            return {}

        if( params is None ):
            params = {}

        params.setdefault('idf', False)
        params.setdefault('norm', 'l2')#see TfidfTransformer for options

        params.setdefault('normalize', False)#normalize TF by vector norm (L2 norm)
        params.setdefault('ngram_range', (1, 1))#normalize TF by vector norm (L2 norm)
        params.setdefault('tokenizer', None)
        params.setdefault('verbose', False)
        params.setdefault('no_ngram_freqs', False)
        params.setdefault('token_pattern', r'(?u)\b[a-zA-Z\'\’-]+[a-zA-Z]+\b|\d+[.,]?\d*')
                

        count_vectorizer = CountVectorizer(token_pattern=params['token_pattern'], tokenizer=params['tokenizer'], stop_words=DocVect.getStopwordsSet(), ngram_range=params['ngram_range'])
        tf_mat = count_vectorizer.fit_transform(docList).toarray()
        payload = {}

        if( params['normalize'] is True  ):
            tf_mat = normalize(tf_mat, norm=params['norm'], axis=1)

        elif( params['idf'] is True ):
            tfidf = TfidfTransformer( norm=params['norm'] )
            tfidf.fit(tf_mat)
            tf_idf_matrix = tfidf.transform(tf_mat).todense()
            payload['tf_idf_matrix'] = tf_idf_matrix

        payload['tf_mat'] = tf_mat
        
        if( params['no_ngram_freqs'] is False ):

            top_freq_ngrams = []
            vocab = count_vectorizer.get_feature_names()
            all_col_sums_tf = np.sum(tf_mat, axis=0)
            
            for i in range( len(vocab) ):
                top_freq_ngrams.append( {'term': vocab[i], 'tf': int(all_col_sums_tf[i])} )
            
            payload['ngram_freqs'] = sorted(top_freq_ngrams, key=lambda x: x['tf'], reverse=True)
             
        
        if( params['verbose'] is True ):
            np.set_printoptions(threshold=sys.maxsize, linewidth=100)
            print('\nVOCABULARY')
            print( count_vectorizer.get_feature_names() )

            print('\nDENSE tf_mat matrix')
            print( payload['tf_mat'] )
            
            if( 'ngram_freqs' in payload ):
                print('\nngram_freqs')
                print( payload['ngram_freqs'] )
            
            if( 'tf_idf_matrix' in payload ):
                print('\nDENSE tf_idf_matrix matrix')
                print( payload['tf_idf_matrix'] )
        
        
        payload['tf_mat'] = payload['tf_mat'].tolist()
        if( 'tf_idf_matrix' in payload ):
            payload['tf_idf_matrix'] = payload['tf_idf_matrix'].tolist()

        return payload

class PrecEval(object):

    def __init__(self, goldstandard, cachePath, simCoeff=0.3):

        self.goldstandard = goldstandard
        self.simCoeff = simCoeff
        self.cachePath = cachePath

        if( self.cachePath.endswith('/') == False ):
            self.cachePath = self.cachePath + '/'

        try:
            os.makedirs( self.cachePath + 'CosineSim/', exist_ok=True )
            os.makedirs( self.cachePath + 'HTML/', exist_ok=True )
            os.makedirs( self.cachePath + 'Plaintext/', exist_ok=True )
        except:
            genericErrorInfo( '\tcachePath: ' + self.cachePath )

        if( 'uris' in self.goldstandard ):
            PrecEval.getHTMLTextForURILst( col=self.goldstandard, cachePath=self.cachePath )
            #self.setSimCoeff()
            #parallel version did not achieve decent speedup
            #self.prlSetSimCoeff()
        else:
            logger.warning('\tInvalid goldstandard supplied')
        
    @staticmethod
    def calcPairSim(matrix, noopFlag):
        
        if( len(matrix) != 2 or noopFlag ):
            return -1

        params = {}
        params['normalize'] = True
        matrix = DocVect.getTFMatrixFromDocList( matrix, params=params )

        if('tf_mat' not in matrix ):
            return -1

        matrix = matrix['tf_mat']
        if( len(matrix) != 2 ):
            return -1
        
        return DocVect.cosineSim(matrix[0], matrix[1])

    @staticmethod
    def uriDctHasBasics(uriDct):

        if( 'text' in uriDct and 'text_len' in uriDct and 'title' in uriDct ):
            return True
        else:
            return False

    @staticmethod
    def getHTMLTextForURILst_reviewForFreezing(col, cachePath, printSuffix='', extraParams=None):

        if( extraParams is None ):
            extraParams = {}

        extraParams.setdefault('sim_cache_lookup', True)
        extraParams.setdefault('uri_deref_q_size', 40)
        extraParams.setdefault('thread_count', 3)

        jobsLst = [[]]
        jobSize = len(col['uris'])

        for i in range(jobSize):

            uri = col['uris'][i]
            if( 'hash' not in uri ):
                uri['hash'] = getStrHash( uri['uri'] )


            if( PrecEval.uriDctHasBasics(uri) and extraParams['sim_cache_lookup'] ):
                #ignore already proc. files, usually already proc. segments
                #except cache lookup is off
                continue

            #attempt - cache - start
            cosineSimFile = cachePath + 'CosineSim/' + col['uris'][i]['hash'] + '.json.gz'
            if( os.path.exists(cosineSimFile) and extraParams['sim_cache_lookup'] ):
                
                cache = getDictFromJsonGZ(cosineSimFile)
                if( PrecEval.uriDctHasBasics(cache) ):
                    uri['text'] = cache['text']
                    uri['text_len'] = cache['text_len']
                    uri['title'] = cache['title']
                    continue


            if( 'custom' in uri ):
                if( 'mime' in uri['custom'] ):
                    if( uri['custom']['mime'] != 'text/html' ):
                        
                        logger.info( '\tskipping NoneHTML ' + uri['custom']['mime'] )
                        uri['text'] = 'NoneHTML'
                        uri['text_len'] = 8

                        uri.setdefault('title', '')
                        continue
            

            if( len(jobsLst[-1]) == extraParams['uri_deref_q_size'] ):
                jobsLst.append([])

            derefParams = {
                'html_cache_file': cachePath + 'HTML/' + uri['hash'] + '.html.gz',
                'return_blank': True
            }
            jobsLst[-1].append({
                'func': derefURI, 
                'args': {'uri': uri['uri'], 'extraParams': derefParams}, 
                'misc': {'i': i, 'hash': uri['hash']}, 
                'print': '\tgetHTMLTextForURILst -> derefURI(): ' + str(i) + ' of ' + str(jobSize) + printSuffix
            })
        
        
    
        for i in range( len(jobsLst) ):

            if( len(jobsLst[i]) == 0 ):
                continue

            logger.info( '\turi batch: ' + str(i+1) + ' of ' + str(len(jobsLst)) )
            logger.info( '\t' + str( len(jobsLst[i]) ) + ' jobs' )
            #for u in jobsLst[i]:
            #    logger.info('\t\tu: ' + u['args']['uri'])
            resLst = parallelTask( jobsLst[i], threadCount=extraParams['thread_count'] )
            logger.info( '\tdone uri batch, boilerplate rm next: ' + str(i+1) + ' of ' + str(len(jobsLst)) )

            continue
            for res in resLst:
                
                html = res['output']
                plaintext = clean_html(html, method='justext')
                indx = res['misc']['i']

                col['uris'][indx]['text'] = plaintext
                col['uris'][indx]['text_len'] = len(plaintext)
                col['uris'][indx]['title'] = extractPageTitleFromHTML(html)
                col['uris'][indx]['timestamp'] = getISO8601Timestamp()

                gzipTextFile( cachePath + 'HTML/' + res['misc']['hash'] + '.html.gz', html )
                gzipTextFile( cachePath + 'Plaintext/' + res['misc']['hash'] + '.txt.gz', plaintext )
                gzipTextFile( cachePath + 'CosineSim/' + res['misc']['hash'] + '.json.gz', json.dumps(col['uris'][indx], ensure_ascii=False) )

    
    @staticmethod
    def getHTMLTextForURILst(col, cachePath, printSuffix='', extraParams=None):

        if( extraParams is None ):
            extraParams = {}

        extraParams.setdefault('sim_cache_lookup', True)
        jobSize = len(col['uris'])

        for i in range(jobSize):

            uri = col['uris'][i]
            if( 'hash' not in uri ):
                uri['hash'] = getStrHash( uri['uri'] )


            if( PrecEval.uriDctHasBasics(uri) and extraParams['sim_cache_lookup'] ):
                #ignore already proc. files, usually already proc. segments
                #except cache lookup is off
                continue

            #attempt - cache - start
            cosineSimFile = cachePath + 'CosineSim/' + col['uris'][i]['hash'] + '.json.gz'
            if( os.path.exists(cosineSimFile) and extraParams['sim_cache_lookup'] ):
                
                cache = getDictFromJsonGZ(cosineSimFile)
                if( PrecEval.uriDctHasBasics(cache) ):
                    uri['text'] = cache['text']
                    uri['text_len'] = cache['text_len']
                    uri['title'] = cache['title']
                    continue


            if( 'custom' in uri ):
                if( 'mime' in uri['custom'] ):
                    if( uri['custom']['mime'] != 'text/html' ):
                        
                        logger.info( '\tskipping NoneHTML ' + uri['custom']['mime'] )
                        uri['text'] = 'NoneHTML'
                        uri['text_len'] = 8

                        uri.setdefault('title', '')
                        continue            

            logger.info( '\tgetHTMLTextForURILst -> derefURI(): ' + str(i) + ' of ' + str(jobSize) + printSuffix )
           
            htmlFile = cachePath + 'HTML/' + uri['hash'] + '.html.gz'
            plaintextFile = cachePath + 'Plaintext/' + uri['hash'] + '.txt.gz'

            if( os.path.exists(htmlFile) ):
                html = getTextFromGZ(htmlFile)
            else:
                html = derefURI( uri['uri'], sleepSec=0, timeout=10 )
                gzipTextFile( cachePath + 'HTML/' + uri['hash'] + '.html.gz', html )

            if( os.path.exists(plaintextFile) ):
                plaintext = getTextFromGZ(plaintextFile)
            else:
                plaintext = clean_html(html)
                gzipTextFile( cachePath + 'Plaintext/' + uri['hash'] + '.txt.gz', plaintext )
            
            col['uris'][i]['text'] = plaintext
            col['uris'][i]['text_len'] = len(plaintext)
            col['uris'][i]['title'] = extractPageTitleFromHTML(html)
            col['uris'][i]['timestamp'] = getISO8601Timestamp()

            gzipTextFile( cachePath + 'CosineSim/' + uri['hash'] + '.json.gz', json.dumps(col['uris'][i], ensure_ascii=False) )


    @staticmethod
    def combineDocsForIndices(uris, indices):

        combinedDoc = ''

        for indx in indices:
            combinedDoc += uris[indx]['text'] + '\n\n'

        return combinedDoc

    def updateGoldstandard(self):
        self.goldstandard['timestamp'] = getNowTime()
        dumpJsonToFile(self.goldFname, self.goldstandard)   


    @staticmethod
    def isRel(sim, goldSim):
        
        sim = round(sim, 1)
        goldSim = round(goldSim, 1)

        if( sim >= goldSim ):
            return True
        else:
            return False

    @staticmethod
    def prlEvalCol(col, goldstandard, cachePath, simCoeff, extraParams=None):
        
        if( extraParams is None ):
            extraParams = {}

        
        '''
            Important note:
            1. If min_text_size is changed, If gold standard text content is change, 
                set prec_sim_cache_lookup False avoid cache lookup in order to true to recalculate sim
            
            2. If gold standard sim-coeff is change, no need to do anything
        '''
        extraParams.setdefault('min_text_size', 300)
        extraParams.setdefault('prec_sim_cache_lookup', True)
        extraParams.setdefault('print_suffix', '')
        extraParams.setdefault('thread_count', 4)

        logger.info('\nprlEvalCol(), prec_sim_cache_lookup: ' + str(extraParams['prec_sim_cache_lookup']))

        colsize = len(col['uris'])

        if( colsize == 0 or len(goldstandard) == 0 ):
            logger.info('\tprlEvalCol(): colsize is 0 or goldstandard == 0, returning')
            return -1

        if( 'uris' not in goldstandard ):
            logger.info('\tprlEvalCol(): no uris in goldstandard, returning')
            return -1

        goldRange = list(range(len(goldstandard['uris'])))
        combinedGold = PrecEval.combineDocsForIndices(goldstandard['uris'], goldRange)
        
        precision = 0
        validColSize = 0
        jobsLst = []        
        for i in range(colsize):            

            #attempt getting sim from cache - start
            cosineSimFile = cachePath + 'CosineSim/' + col['uris'][i]['hash'] + '.json.gz'
            if( os.path.exists(cosineSimFile) and extraParams['prec_sim_cache_lookup'] ):
                
                cosSim = getDictFromJsonGZ(cosineSimFile)
                if( 'sim' in cosSim ):
                    
                    col['uris'][i]['sim'] = cosSim['sim']

                    if( cosSim['sim'] != -1 ):
                        validColSize += 1

                        if( PrecEval.isRel(cosSim['sim'], simCoeff) ):
                            col['uris'][i]['relevant'] = True
                            precision += 1
                        else:
                            col['uris'][i]['relevant'] = False

                    continue
            #attempt getting sim from cache - end

            noopFlag = False
            usingSubText = ''
            if( len(col['uris'][i]['text']) < extraParams['min_text_size'] ):
                if( 'post_details' in col['uris'][i] ):
                    #gold standards do not have post-details
                    if( 'substitute_text' in col['uris'][i]['post_details'] ):
                        
                        subText = col['uris'][i]['post_details']['substitute_text'].strip()
                        if( subText != '' ):
                            col['uris'][i]['text'] = subText
                            col['uris'][i]['custom']['substitute_text_active'] = True
                            usingSubText = '\n\t\tusing subtext: ' + col['uris'][i]['uri']
                        else:
                            noopFlag = True
                    
                    else:
                        #don't process uris with small text
                        #don't skip (continue) so cache can update
                        noopFlag = True

            matrix = [
                col['uris'][i]['text'], 
                combinedGold
            ]
            keywords = {'matrix': matrix, 'noopFlag': noopFlag}
            toPrint = '\tprlEvalCol():' + str(i) + ' of ' + str(colsize) + ' ' + extraParams['print_suffix'] + usingSubText

            cache = {
                'hash': col['uris'][i]['hash'],
                'self': cosineSimFile,
                'uri': col['uris'][i]['uri'],
                'title': col['uris'][i]['title'],
                'text': col['uris'][i]['text'],
                'text_len': len(col['uris'][i]['text'])
            }
            jobsLst.append({
                'func': PrecEval.calcPairSim, 
                'args': keywords, 
                'misc': {'i': i, 'cache': cache}, 
                'print': toPrint
            })


        resLst = []
        if( len(jobsLst) != 0 ):
            resLst = parallelTask(jobsLst, threadCount=extraParams['thread_count'])
        
        for res in resLst:
            
            indx = res['misc']['i']
            cache = res['misc']['cache']

            sim = res['output']
            col['uris'][indx]['sim'] = sim

            if( sim != -1 ):
                validColSize += 1

                if( PrecEval.isRel(sim, simCoeff) ):
                    col['uris'][indx]['relevant'] = True
                    precision += 1
                else:
                    col['uris'][indx]['relevant'] = False

            #write cache - start
            cache['sim'] = sim
            gzipTextFile(cache['self'], json.dumps(cache, ensure_ascii=False))
            #write cache - end
        
        
        for i in range( colsize ):
            if( 'text' in col['uris'][i] ):
                del col['uris'][i]['text']

        for i in range( len(goldstandard['uris']) ):
            if( 'text' in goldstandard['uris'][i] ):
                del goldstandard['uris'][i]['text']

        if( validColSize > 0 ):
            return precision/validColSize
        else:
            return -1


    @staticmethod
    def singleDocPrecCalc(docList):

        if( len(docList) != 2 ):
            return -1

        params = {}
        params['normalize'] = True
        locMatrix = DocVect.getTFMatrixFromDocList( docList, params=params )

        if( len(locMatrix) != 2 ):
            return -1

        return DocVect.cosineSim(locMatrix[0], locMatrix[1])
