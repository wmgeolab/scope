# dumb dumb version of auto extraction

# Load packages
import pymysql
import pandas as pd
import re
import nltk
from nltk import word_tokenize, sent_tokenize

# Open database connection (host, username, password, database_name)
conn = pymysql.connect(host="mysql.scopedata.org", user="scopesql",
                     password="fY7Ukl52UI", db="scopesql")

# prepare a cursor object using cursor() method
#curs = conn.cursor()

#print('Connection opened!')

# query the db

sql = """SELECT id, source_text
			FROM sourcing_m_source;"""

x = pd.read_sql(sql,conn)

sql = """SELECT id, triggerword
			FROM domain_triggerword"""

y = pd.read_sql(sql,conn)
#kw = "arrest"

#def findWholeWord(w):
#    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#for row in x.values:
#	findWorldWord(kw)(row[1])

for xrow in x.values:
	for yrow in y.values:
		trigger = yrow[1]
		if (xrow[1].find(trigger) > 0):
			sent_tokens = sent_tokenize(xrow[1])
			n = 0
			for sent in sent_tokens:
				e = n + 3
				if (sent.find(trigger) > 0):
					print(trigger)
					print(' '.join(sent_tokens[n:e]))
				n += 1
	#else:
	#	print('No events found')

