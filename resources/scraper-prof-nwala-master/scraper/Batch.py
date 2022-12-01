import gzip
import json
import os
import re

from datetime import datetime

def validate_job(job):
    if( len(set(job.keys()) & {'query', 'repo'}) == 0 ):
        return False
    else:
        return True

def unify_args(user_params, default_params):
    
    for key, val in default_params.items():
        user_params[key] = val

    return user_params

def jobs_dispatcher(src, params):

    if( src == 'google' ):
        res = googleProcReq( params )
    elif( src == 'reddit' ):
        res = redditProcReq( params )
    elif( src == 'twitter' ):
        res = twitterProcReq( params )
    else:
        res = {'error': 'unexpected src: ' + src}

    return res

def write_payload(job, res_lst, debug=None):

    if( debug is None ):
        debug = {}

    debug.setdefault('echo_output_len', 0)
    try:
        repo = job['repo'].strip()
        if( repo.endswith('/') == False ):
            repo = repo + '/'

        job.setdefault('output_max_lines', 1000)
        job.setdefault('output_max_files', 100)
        job.setdefault('output_filename_max_len', 50)


        slug = re.sub('[^0-9a-zA-Z]+', '_', job['query'].strip())
        if( 'output_filename' in job ):
            #special case when query is blank, directives is usually set
            slug = re.sub('[^0-9a-zA-Z]+', '_', job['output_filename'].strip())


        slug = slug[: job['output_filename_max_len'] ]

        repo = repo + slug + '/'
        os.makedirs(repo, exist_ok=True)
        
        cur_date = re.sub( '[^0-9]+', '', datetime.utcnow().isoformat().split('.')[0] )
        last_date = os.listdir(repo)

        if( len(last_date) == 0 ):
            last_date = cur_date
        else:
            last_date.sort()
            last_date = last_date[-1]
    
        
        os.makedirs(repo + last_date + '/', exist_ok=True)
        last_file = os.listdir( repo + last_date + '/' )

        if( len(last_file) == 0 ):
            last_file = last_date
        else:
            last_file.sort()
            last_file = last_file[-1].split('_')[-1].replace('.txt.gz', '')

        
        cur_line_count = 0
        outfile_name = repo + last_date + '/' + last_file + '.txt.gz'
        if( os.path.exists(outfile_name) ):
            with gzip.open(outfile_name, 'rb') as f:

                cur_line_count = len(f.readlines())
        
        print('repo:', repo)
        print('cur_line_count of output_max_lines:', cur_line_count, 'of', job['output_max_lines'])
        new_outfile_flag = ''
        if( cur_line_count >= job['output_max_lines'] ):
            #new outfile_name
            
            outfile_name = repo + last_date + '/' + cur_date + '.txt.gz'
            cur_folder_count = len( os.listdir(repo + last_date + '/') )

            if( cur_folder_count >= job['output_max_files'] ):
                print('new folder:', last_date)
                #since previous folder max reached, create new folder and store new outfile_name there
                os.makedirs(repo + cur_date + '/', exist_ok=True)
                outfile_name = repo + cur_date + '/' + cur_date + '.txt.gz'
            
            new_outfile_flag = 'new '
        
        print(new_outfile_flag + 'outfile_name:', outfile_name)
        
        content = str.encode( json.dumps(res_lst, ensure_ascii=False) + '\n' )
        with gzip.open(outfile_name, 'ab') as f:
            f.write( content )
            print('\tsuccess: new line added to outfile_name')

        if( debug['echo_output_len'] > 0 ):

            print('\nInfo exclusively for debug:')
            print('outfile_name content:')

            with gzip.open(outfile_name, 'rb') as f:
                file_content = f.readlines()
                for fc in file_content:
                    print( fc[:debug['echo_output_len']] )
    except:
        genericErrorInfo()

def format_write_payload(res_lst):
    return {
        'source': 'ScraperBatch',
        'payload': res_lst
    }

def scraper_client(config_file):

    config_file = getDictFromFile(config_file)
    if( 'jobs' not in config_file ):
        print('Error: jobs not in config file, returning')
        return

    config_file.setdefault('debug', {})
    jobsize = len(config_file['jobs'])

    print('scraper_client issued jobs count:', jobsize, '\n')

    for i in range(jobsize):
        
        job = config_file['jobs'][i]
        if( validate_job(job) is False ):
            continue

        print('job', i, 'of', jobsize)

        job.setdefault('params', {})

        jobs_lst = []
        res_lst = []
        for src in ['google', 'reddit', 'twitter']:
            if( src in job['params'] ):
                
                src_params = eval(src + 'GetDefaultArgs("parseKnown")')
                src_params['query'] = job['query']
                src_params = unify_args( src_params, job['params'][src] )
                
                keywords = {
                    'src': src,
                    'params': src_params
                }

                jobs_lst.append({
                    'func': jobs_dispatcher,
                    'args': keywords,
                    'misc': False
                })
        
        if( len(jobs_lst) != 0 ):
            res_lst = parallelTask(jobs_lst, threadCount=3)
            res_lst = [res['output'] for res in res_lst]

        res_lst = format_write_payload(res_lst)
        write_payload(job, res_lst, config_file['debug'])
        print()

if __name__ == 'scraper.Batch':

    from scraper.ScraperUtil import getDictFromFile
    from scraper.ScraperUtil import parallelTask
    from scraper.ScraperUtil import genericErrorInfo

    from scraper.Google import getDefaultArgs as googleGetDefaultArgs#called by eval() - used with caution
    from scraper.Reddit import getDefaultArgs as redditGetDefaultArgs#called by eval() - used with caution
    from scraper.Twitter import getDefaultArgs as twitterGetDefaultArgs#called by eval() - used with caution
    from scraper.Google import procReq as googleProcReq
    from scraper.Reddit import procReq as redditProcReq
    from scraper.Twitter import procReq as twitterProcReq

else:
    from ScraperUtil import getDictFromFile
    from ScraperUtil import parallelTask
    from ScraperUtil import genericErrorInfo

    from Google import getDefaultArgs as googleGetDefaultArgs#called by eval() - used with caution
    from Reddit import getDefaultArgs as redditGetDefaultArgs#called by eval() - used with caution
    from Twitter import getDefaultArgs as twitterGetDefaultArgs#called by eval() - used with caution
    from Google import procReq as googleProcReq
    from Reddit import procReq as redditProcReq
    from Twitter import procReq as twitterProcReq