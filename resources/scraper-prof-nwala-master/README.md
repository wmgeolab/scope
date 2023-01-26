# scraper

Scraper is a Python tool that scrapes the Google (All, and News) and Twitter SERPs (Search Engine Result Pages). Additionally, scaper provides a wrapper to the [Reddit API](https://www.reddit.com/dev/api/)

## Installation

```
$ git clone https://github.com/oduwsdl/scraper.git
$ cd scraper; pip install .; cd ..; rm -rf scraper;
```
Alternatively, build Docker image and run from inside Docker Python container:
```
$ git clone https://github.com/oduwsdl/scraper.git
$ cd scraper/
$ docker build -t wsdl/scraper .
$ cd ..; rm -rf scraper;
$ docker run --rm -it -v "$PWD":/data/ wsdl/scraper
```

## Usage
### Basic usage:
```
$ scraper google [options] query
OR
$ scraper google [options] path_to_serps...
OR
$ scraper reddit [options] query
OR
$ scraper twitter [options] query
OR
$ scraper batch [options] jobs_config_json_file
OR to run tests
$ scraper [test-google | test-reddit | test-twitter]

To see the complete list, run $ scraper [google | reddit | twitter] --help
Google options:
path_to_serps               Path to single and/or files and/or directories containing HTML of Google SERPs

-f, --files                 Read Google SERPs from files instead of searching with query
-n, --news                  Search Google News Vertical (default is False)
-o, --output                Output file
-p, --max-page=1            Maximum number of pages to visit
-s , --sleep-sec            For search throttling process: maximum number or seconds to sleep between adjacent searches

--chromedriver-path         Path to chromedriver, use this to avoid using curl to for search, but chromedriver (with selenium) instead. Enable extraction of links (e.g., links in Carousel) generated via running JavaScript
--delay-sec                 Delay by set value before extracting links
--directives                Directives to accompany search, e.g., "site:example.com")
--find-uri-key              Search for uri

--log-file                  Log output filename
--log-format                Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html
--log-level=info            Log level from OPTIONS: {critical, error, warning, info, debug, notset}
--no-interleave             Do not interleave search, override interleave logic
--pretty-print              Pretty print JSON output


Reddit options:
-h, --help                  show this help message and exit
-o, --output                Output file
-p, --max-page=1            Maximum number of pages to visit
-s, --sleep-sec             For search throttling process: maximum number or seconds to sleep between adjacent searches
--expand=False              Expand posts from SERP by extracting links from comment posts

--log-file                  Log output filename
--log-format                Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html
--log-level=info            Log level from OPTIONS: {critical, error, warning, info, debug, notset}

--max-posts                 Maximum number of Reddit posts to return
--sort=relevance            Sort criteria for posts from OPTIONS: {relevance, top, new, comments}
--subreddit=''              Search Reddit subreddit vertical
--thread-count              Maximum number of threads to use for parallel operations
--pretty-print              Pretty print JSON output


Twitter options:
-h, --help                  show this help message and exit
-o, --output                Output file
-l, --latest                Search Twitter Latest vertical (default is False)
-m, --max-tweets=20         Maximum number of tweets to collect
-s, --sleep-sec=1           For search throttling process: maximum number or seconds to sleep between adjacent searches

--access-token              Twitter API info needed for hydrating tweets
--access-token-secret       Twitter API info needed for hydrating tweets
--consumer-key              Twitter API info needed for hydrating tweets
--consumer-secret           Twitter API info needed for hydrating tweets

--cache-path=''             Path to save tweets (single and/or conversation)
--cache-read=False          Switch on reading cache for conversations
--cache-write=False         Switch on writing cache

--chromedriver-path='./chromedriver' Path to chromedriver
--delay-sec=0               Delay by set value before extracting tweets (for debugging)
--expand                    Expand tweets from SERP by extracting links from conversation tweets

--hydrate-files             Instead of searching, hydrate JSON files that have mininum of data_tweet_id
--no-hydrate-tweets         Do not hydrate tweets
--no-add-hydrated-tweet-json Do not add raw tweet (hydrated tweet) JSON to extracted tweets

--keep-dom-tweets=False     Do not remove tweets from DOM
--search-uri-key=''         Search with uri, NOT query.  Extract tweets with uri

--log-file                  Log output filename
--log-format                Log print format, see: https://docs.python.org/3/howto/logging-cookbook.html
--log-level=info            Log level from OPTIONS: {critical, error, warning, info, debug, notset}

--max-no-more-tweets-counter=4 Maximum number of times to retry getting tweets before declaring: no more tweets 
--max-reply-count           Maximum number of tweet replies to collect (for --expand)
--no-check-reply-count      Do not check if tweets have replies before attempting to expand
--no-redact-keys            Do not redact consumer-key/secret access-token/secret
--pretty-print=False        Pretty print JSON output
--stop-datetime=''          Collect tweets with datetime < local stop-datetime (format: YYYY-MM-DD HH:MM:SS)
--thread-count=5            Maximum number of threads to use for parallel operations


Batch options:
See "Scraper Batch" section
```
## Examples: Command-line usage
### Google Examples:
1. Scrape first page of [Google All](https://www.google.com/) with query: "norfolk weather":  `$ scraper google "norfolk weather"`
2. Search first 3 pages of Google All with query: "norfolk": `$ scraper google -p 3 norfolk`
3. Search first 3 pages of Google All with query: "norfolk," write result to file: 
`$ scraper google -p 3 -o serp_norfolk.json norfolk`
4. Scrape first page of [Google News](https://news.google.com) with query: "norfolk":  `$ scraper google --news norfolk`
5. Scrape first page of Google with query: "norfolk," restrict results to links from `cnn.com`:
`$ scraper google --directives="site:cnn.com" norfolk`
6. Scrape SERPs saved in HTML files (single HTML files may be compressed - html.gz, or multiple HTML files - tar.gz) in a directory (files are extracted recursively): 
    * Scrape HTML SERPs form single directory `scraper google -f path_to_html/`, e.g., scraper google -f [tests/sample_serps/](tests/sample_serps)
    * Scrape HTML SERPs form multiple files `scraper google -f path/to/serp1.html path/to/serp2.html`

### Google: A note on throttling and interleaving
Since Google search is meant for humans and not bots, scraper attempts to be courteously make requests by throttling requests. Specifically, scraper sleeps (controlled by `sleep_sec`) for 1 second for each request made to Google. If you plan to issue just a few queries (e.g., under 25), you could switch of throttling (`sleep_sec = 0`).

Scraper employs interleaving to avoid triggering Google's CAPTCHA test. Interleaving refers to the issuing of random queries in addition to the user-issued queries. Interleaving occurs when `maxPage > 2` and `directives` is set (e.g., `--directives="site:cnn.com"`). If you plan to issue just a few queries (e.g., under 25), you could switch of interleaving (`--no-interleave` - command-line or `interleave=False` - Python script).

### Reddit Examples:
1. Search first page of Reddit with query: "norfolk":  `$ scraper reddit norfolk`
2. Search first 3 pages of Reddit (sort by relevance - default) with query: "norfolk": `$ scraper reddit -p 3 norfolk`
3. Search first 3 pages of Reddit with query: "norfolk," write result to file:
`$ scraper reddit -p 3 -o reddit_serp_norfolk.json norfolk`
4. Search first page of Reddit with query: "norfolk":  `$ scraper reddit --sort=comments norfolk`
5. Search first page of Reddit with query: "norfolk," restrict results to links from subreddit `news`:
`$ scraper reddit --subreddit=news norfolk`

### Twitter Examples:
1. Extract 20 tweets (do not hydrate) for query: "norfolk":  `$ scraper twitter -m 20 norfolk`
2. Extract 20 tweets for query: "norfolk," write result to file: `$ scraper twitter -m 20 -o twitter_serp_norfolk.json norfolk`
3. Extract 5 replies from URI, e.g., `$ scraper twitter -m 5 https://twitter.com/acnwala/status/1214203046801969152`
4. Search and for each extracted tweet, extract replies, e.g, extract 5 "flint water crisis" tweets, and for each extract max 10 replies `$ scraper twitter -m 5 --expand --max-reply-count=10 "flint water crisis"`. This can be expensive, so consider hydrating files (Example No. 7)
5. Extract 20 latest tweets (hydrate) for query: "norfolk":  
    ```
    $ scraper twitter -m 20 -l \
    --consumer-key="XXX" --consumer-secret="XXX" \
    --access-toke="XXX" --access-token-secret="XXX" \
    norfolk
    ```
6. Extract 100 tweets for query: "norfolk," write result to file, cache individual tweets in "TweetsCache" folder:
    ```
    $ scraper twitter --cache-write --cache-path="./TweetsCache" \
    --cache-single-tweets -m 100 -o twitter_serp_norfolk.json norfolk
    ```
7. Hydrate tweets stored in `--cache-path`. Each JSON file has minimum of "data_tweet_id" key
    ```
    scraper twitter --cache-path=./tweets /
    --hydrate-files /
    --no-check-reply-count / #attempt to extract replies irrespective of the value of tweet.replies
    --consumer-key="XXX" /
    --consumer-secret="XXX" /
    --access-toke="XXX" / 
    --access-token-secret="XXX" / 
    ""
    ```
## Examples: Python usage
### Google Examples:
The following is a Python script example illustrating the use of scraper.Google done by calling the `googleSearch(query, maxPage=1, newsVertical=False, extraParams=None)` function.
In this example, the user intends to search for a URI (`'find_uri_key': 'https://www.visitnorfolk.com/'`) until page 3 (`maxPage = 3`). Note 
that the search stops once the URI is found (e.g., at page 1). If the URI is found, the position (in `links`) of the link would be stored in `uri_key_found_indx`.
```
import json
from scraper.Google import googleSearch

query = 'norfolk'
extra_params = {
    'find_uri_key': 'https://www.visitnorfolk.com/'
}

'''
    To process SERPs saved in HTML files stored in ./HTML_SERPS,
    replace query and extra_params as follows:

    query = './HTML_SERPS'
    extra_params = {
        'files': True
    }
'''

serp = googleSearch(query, maxPage=3, newsVertical=False, extraParams=extra_params)

with open('google_serp.json', 'w') as outfile:
    json.dump(serp, outfile, indent=4)
```
### Reddit Examples:
The following is a Python script example illustrating the use of scraper.Reddit done by calling the `redditSearch(query, subreddit='', maxPage=1, extraFieldsDict=None, extraParams=None)` function.
```
import json
from scraper.Reddit import redditSearch

query = 'norfolk'
serp = redditSearch(query)

with open('reddit_serp.json', 'w') as outfile:
    json.dump(serp, outfile, indent=4)
```
### Twitter Examples:
The following is a Python script example illustrating the use of scraper.Twitter done by calling the `twitterSearch(chromedriverPath, query='', maxTweetCount=100, latestVertical=False, extraParams=None)` function.
```
import json
from scraper.Twitter import twitterSearch

query = 'norfolk'
serp = twitterSearch(
    chromedriverPath='/usr/local/bin/chromedriver',
    query=query,
    maxTweetCount=20
)

with open('twitter_serp.json', 'w') as outfile:
    json.dump(serp, outfile, indent=4)
```
## Output Description
### Scraper Output: Google
Highlights of selected (not all) fields in the output generated from the following command:
```
$ scraper google --pretty-print -o output.json norfolk
```
- **source** (str = 'Google'): The service processed to produce output
- **query** (str): Query issued to Google
- **max_pages** (int): Maximum number of pages searched
- **gen_timestamp** (str): Timestamp (UTC) indicating when query was issued
- **self_uris** (array[objects]): List of Google SERP URIs
- **stats** (object): Collection of metrics
- **extra_params** (object):
    - **raw_request_params** (objects): User-defined parameters and default parameters used to generate output
    - **page_dets** (objects):
        - **result_count** (int): Total number of hits as reported by Google
        - **captcha_on** (bool): A flag indicating if the query was caught by Google's CAPTCHA's trap
        - **scaping_report** (objects): Information needed for debugging if scraper breaks
        - **related_queries** (array[str]): List of related queries extracted from the Google SERP
- **links** (array[objects]): SERP results
    - (object)
        - **link** (str): Link extracted from Google SERP
        - **title** (str): Link title
        - **snippet** (str): Link snippet
        - **page** (int): Page from which link was extracted
        - **rank** (int): Link rank
        - **date** (str): Date extracted from SERP. Note: if this value is not found, it is auto-generated (see `custom.date_auto_gen`)
        - **custom** (object): Additional details about link
### Scraper Output: Reddit
Highlights of selected fields (not all) in the output generated from the following command.
```
$ scraper reddit --pretty-print -o output.json norfolk
```
- **source** (str = 'Reddit'): The service processed to produce output
- **query** (str): Query issued to Reddit
- **max_page** (int): Maximum number of pages searched
- **gen_timestamp** (str): Timestamp (UTC) indicating when query was issued
- **self_uris** (array[str]): List of Reddit SERP URIs
- **stats** (object): Collection of metrics
- **posts** (array[objects]): SERP results
    - (object)
        - **link** (str): Link extracted from Reddit SERP. This could be an outlink or a Reddit comment link
        - **title** (str): Link title
        - **snippet** (str): Link snippet
        - **pub_datetime** (str): Publication datetime (UTC) of Reddit post
        - **outlinks** (array[objects]): List of external links extracted from post
        - **custom** (object): Additional details about post, e.g., `permalink`, `author`, and `subreddit`.
### Scraper Output: Twitter
Highlights of selected fields (not all) in the output generated from the following command.
```
$ scraper twitter -m 3 --pretty-print -o output.json norfolk
```
- **source** (str = 'Twitter'): The service processed to produce output
- **query** (str): Query issued to Twitter
- **max_tweets** (int): Maximum number of tweet requested to extract
- **gen_timestamp** (str): Timestamp (UTC) indicating when query was issued
- **self** (str): URI issued to Twitter to generate output
- **stats** (object): Coming soon
- **tweets** (array[objects]): SERP results
    - (object)
        - **tweet_text** (str): Tweet text
        - **tweet_time** (str): Tweet publication time (UTC)
        - **data_tweet_id** (str): Tweet ID
        - **data_conversation_id** (str): Tweet parent ID (same as tweet ID if tweet has no parent)
        - **data_name** (str): Name of tweet author
        - **data_screen_name** (str): Screen name (handle) of tweet author
        - **data_mentions** (array[str]): List of handles tweet mentions
        - **hashtags** (array[str]): List of hashtags in tweet
        - **tweet_links** (array[str]): List of links embedded in tweet
        - **user_verified** (bool): Flag indicating if the tweet author is a verified user
        - **tweet_stats** (object): Object containing counts of `reply`, `retweet`, and `favorite`

FOR replies or threads, here is documentation of the first tweet object in the **tweets** list
- **extra** (object)
    - (optional) **reply_group** (array[object]): List of tweet IDs that are part of a reply block. If a **reply_group** exists, the tweets would contain **tweet_replies** otherwise **tweet_thread**
    
## Scraper Batch
The batch option (`scraper batch jobs_config_json_file` OR from docker `docker run --rm -it -v "$PWD":/data/ wsdl/scraper /data/jobs_config_json_file`) of scraper is meant to issue multiple queries to scraper at once. 
Batch may also be invoked periodically (e.g., daily). The `jobs_config_json_file` instructs scraper on what combination of 
queries, sources (Google and/or Reddit and/or Twitter), and parameters to send to scraper.
Consider the following inline annotated (`# comment not part of JSON`) sample content for a hurricanes_batch.json `jobs_config_json_file`:
```
{
    # jobs list of object specifies the queries to be issued to scraper
    "jobs": [
        {
            # "query" and "repo" (mandatory): are mandatory keys. Without them, 
            # batch would not run. Every other key is optional
            
            # "query": query to be issued to services
            "query": "hurricane harvey",

            # "repo": directory to save payload
            "repo": "./repo/",
            
            # "output_max_lines" (mandatory): maximum number of lines a single output NDJSON file should contain. 2 means
            # each output file would contain a maximum of 2 lines, 
            # after which a new file would be created
            "output_max_lines": 2,

            # "output_max_files" (mandatory): maximum number of output NDJSON files to create. 2 means each output
            # directory containing output files would contain a maximum of 2 files,
            # after which a new directory would be created
            "output_max_files": 2,

            # "output_filename_max_len" (mandatory): output filenames are created from the queries. This field sets a limit 
            # for the length of the filename
            "output_filename_max_len": 50,
            
            # "params" (optional): Collection of parameters to send to the various sources.
            # Three sources (google, reddit, twitter) are specified here, this means scraper would issue
            # the "hurricane harvey" query to Google, Reddit, and Twitter. Since the parameters for each
            # source is left blank, the default parameters would be used.
            "params": {
                "google": {}, #see Basic Usage - Google options (e.g., news, max_page) - for parameter options
                "reddit": {}, #see Basic Usage - Reddit options (e.g., subreddit, max_posts) - for parameter options
                "twitter": {} #see Basic Usage - Twitter options (e.g., latest, max_tweets) - for parameter options
            }
        },
        {
            "query": "hurricane irma",
            "repo": "./repo/",
            
            "params": {
                "google": {"news": true, "max_page": 2}
            }
        }
    ]
}

```
The first time batch is invoked (with `scraper batch hurricanes_batch.json`) leads to the following actions: 
1. Two directories are created `./repo/hurricane_harvey/timestamp1/` and `./repo/hurricane_irma/timestamp1/`
2. One line of JSON output (from scraper) is written into `./repo/hurricane_harvey/timestamp1/timestamp1.txt.gz`
3. One line of JSON output (from scraper) is written into `./repo/hurricane_irma/timestamp1/timestamp1.txt.gz`

The second time batch is invoked (with `scraper batch hurricanes_batch.json`) leads to the following actions: 
1. One line of JSON output (from scraper) is written into `./repo/hurricane_harvey/timestamp1/timestamp1.txt.gz`
2. One line of JSON output (from scraper) is written into `./repo/hurricane_irma/timestamp1/timestamp1.txt.gz`

The third time batch is invoked (with `scraper batch hurricanes_batch.json`) leads to the following actions: 
1. One line of JSON output (from scraper) is written into a new file `./repo/hurricane_harvey/timestamp1/timestamp2.txt.gz` 
because the previous file (`timestamp1.txt.gz`) reached its maximum line count (`output_max_lines = 2`)
2. One line of JSON output (from scraper) is written into into a new file `./repo/hurricane_irma/timestamp1/timestamp2.txt.gz`

The fourth time batch is invoked (with `scraper batch hurricanes_batch.json`) leads to the following actions: 
1. One line of JSON output (from scraper) is written into `./repo/hurricane_harvey/timestamp1/timestamp2.txt.gz`
2. One line of JSON output (from scraper) is written into `./repo/hurricane_irma/timestamp1/timestamp2.txt.gz`

The fifth time batch is invoked (with `scraper batch hurricanes_batch.json`) leads to the following actions: 
1. Two directories are created `./repo/hurricane_harvey/timestamp2/` and `./repo/hurricane_irma/timestamp2/`
2. One line of JSON output (from scraper) is written into `./repo/hurricane_harvey/timestamp2/timestamp1.txt.gz`
3. One line of JSON output (from scraper) is written into `./repo/hurricane_irma/timestamp2/timestamp1.txt.gz`

etc.