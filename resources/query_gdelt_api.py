import requests
from bs4 import BeautifulSoup

# https://api.gdeltproject.org/api/v2/doc/doc?format=html&timespan=2Y&query=ecuador&mode=artlist&maxrecords=250&format=json&sort=hybridrel
# https://api.gdeltproject.org/api/v2/summary/summary?d=web&t=summary
# https://api.gdeltproject.org/api/v2/doc/doc?format=html&startdatetime=20170103000000&enddatetime=20181011235959&query=ecuador%20china&mode=artlist&maxrecords=75&format=json&sort=hybridrel

# This program uses the gdelt project apis to query for articles based on keywords and timespans
# It takes in arguments
#   "query" : A string of keywords separated by spaces
#   "startdatetime" : A string in the YYYYMMDDHHMMSS that marks the start date/time to look for sources
#   "enddatetime" : A string in the YYYYMMDDHHMMSS that marks the end date/time to look for sources
#   "maxrecords" : A string of the number of sources wanted, maxes out at 250 sources

def query_gdelt(args):

  url = "https://api.gdeltproject.org/api/v2/doc/doc?format=html&mode=artlist&format=json&sort=hybridrel"

  parameter_list = ['query', 'startdatetime', 'enddatetime', 'maxrecords']
  for i in parameter_list:
    if i not in args:
      continue

    if i == 'startdatetime' and 'enddatetime' not in args:
      url += '&timespan=' + args[i]
      continue

    url += '&' + i + '=' + args[i]

  headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

  req = requests.get(url, headers)
  return req.json()

if __name__ == "__main__":
  args = {}
  args["query"] = "china ecuador"
  args["startdatetime"] = "20140630235959"
  args["maxrecords"] = "10"
  args['enddatetime'] = '20150630235959'

  print(query_gdelt(args))
  #print(query_gdelt({"query":'china ecuador','startdatetime':'2y','maxrecords':'10'}))