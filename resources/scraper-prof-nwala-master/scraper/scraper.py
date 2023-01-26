#!/usr/bin/env python
import argparse
import os
import sys

from os.path import dirname, abspath
from subprocess import call

def cur_path():
    return dirname(abspath(__file__)) + '/'

def menu():

    scraper_art = '''
    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
    '''
    usage = '''
    basic usage: scraper [google | reddit | twitter | batch]\nadvanced: scraper [twitter-qp | twitter-mc]\ntests: scraper [test-google | test-reddit | test-twitter]
    '''
    usage = usage.strip()

    if( len(sys.argv) < 2 ):
        print(scraper_art)
        print(usage)
        return

    caller = sys.argv[1].lower().strip()
    filename_map = {
        'twitter-qp': 'TwitterQualityProxy.py',
        'twitter-mc': 'MicroCol.py',
        'test-google': '../tests/unit/test_google.py',
        'test-reddit': '../tests/unit/test_reddit.py',
        'test-twitter': '../tests/unit/test_twitter.py'
    }
    
    if( caller == 'batch' ):
        
        if( sys.argv[-1] == caller ):
            print('usage: scraper batch jobs_config_json_file')
            return

        scraper_client( sys.argv[2] )

    elif( caller in ['google', 'reddit', 'twitter'] ):
    
        f = cur_path() + sys.argv[1].capitalize() + '.py'
        call( ['python', f] + sys.argv[2:] )#check_output for unknown reasons could not invoke Google.py --help

    elif( caller in filename_map ):

        f = cur_path() + filename_map[caller]
        call( ['python', f] + sys.argv[2:] )#check_output for unknown reasons could not invoke Google.py --help

    elif( caller == '-v' or caller == '--version' ):

        if __name__ == 'scraper.scraper':
            from scraper.config import __appversion__
        else:
            from config import __appversion__
            
        print(__appversion__)
        return

    else:
        print('caller:', caller)        
        print(scraper_art)
        print(usage)

def main():
    menu()
    

if __name__ == 'scraper.scraper':
    from scraper.Batch import scraper_client
else:
    from Batch import scraper_client

if __name__ == '__main__':    
    main()
