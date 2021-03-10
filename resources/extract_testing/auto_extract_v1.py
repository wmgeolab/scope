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

sql = """SELECT source_id, source_text
			FROM sourcing_source;"""

x = pd.read_sql(sql,conn)

#kw = "arrest"

#def findWholeWord(w):
#    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#for row in x.values:
#	findWorldWord(kw)(row[1])

for row in x.values:
	tokens = word_tokenize(row[1])
	text = nltk.Text(tokens)
	if (text.find("arrest") > 0):
		sent_tokens = sent_tokenize(row[1])
		n = 0
		for sent in sent_tokens:
			e = n + 2
			if (sent.find("arrest") > 0):
				print(' '.join(sent_tokens[n:e]))
			n += 1


