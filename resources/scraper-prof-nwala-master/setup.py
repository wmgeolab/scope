#!/usr/bin/env python

from setuptools import setup, find_packages

desc = """A utility for Scraping Google and a wrapper for the Reddit JSON API"""

__appversion__ = None

#__appversion__, defined here
exec(open('scraper/config.py').read())

setup(
    name='scraper',
    version=__appversion__,
    description=desc,
    long_description='A utility for Scraping Google and a wrapper for the Reddit JSON API',
    author='Alexander C. Nwala',
    author_email='anwala@cs.odu.edu',
    url='https://github.com/oduwsdl/scraper',
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_data={
        'scraper': [
            './RandQueries.txt',
            './TwitterUtil/*',
            './RedditUtil/*',
            './GoogleSampleSerps/*',
            './GoogleSampleSerps/c/*',
            './GoogleSampleSerps/c/g/*'
        ]
    },
    install_requires=[
        'beautifulsoup4==4.8.2',
        'boilerpy3==1.0.4',
        'dateparser==0.7.2',
        'googlemaps==4.1.0',
        'jusText==2.2.0',
        'networkx==2.4',
        'requests==2.22.0',
        'selenium==3.141.0',
        'tldextract==2.2.2',
        'tweepy==3.8.0',
        'sklearn==0.0'
    ],
    scripts=[
        'bin/sqm'
    ],
    entry_points={'console_scripts': ['scraper = scraper.scraper:main']}
)