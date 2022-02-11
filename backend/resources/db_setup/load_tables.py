#-----PART ONE: PACKAGES AND CONNECTION SET-UP-----

# Load packages
import pymysql
import pandas as pd
import datetime as dt

# Open database connection (host, username, password, database_name)
conn = pymysql.connect(host="mysql.scopedata.org", user="scopesql",
                     password="fY7Ukl52UI", db="scopesql")

# prepare a cursor object using cursor() method
curs = conn.cursor()

print('Connection opened!')


#-----PART TWO: IMPORT DATA-----

#import data to pandas
activitycode = pd.read_csv('./activitycode.csv')
statuscode = pd.read_csv('./statuscode.csv')
actorcode = pd.read_csv('./actorcode.csv')
sourcecode = pd.read_csv('./sourcecode.csv')
source = pd.read_csv('./test_sources.csv',
                     dtype={'source_id': 'int64'})
activity = pd.read_csv('./test_data.csv',
                       dtype={'activity_id': 'int64', 'fuzzy_date': 'float64',
                              'lat': 'float64', 'lon': 'float64', 'source_id': 'int64'})

print('Data files imported!')


#-----PART THREE: EDIT DATA TYPES-----

source['source_date'] = pd.to_datetime(source['source_date'], format="%m/%d/%Y")
source['source_date'] = (source['source_date'] - dt.datetime(1970,1,1)).dt.total_seconds()
source['date_added'] = pd.to_datetime(source['date_added'], format="%m/%d/%Y")
source['date_added'] = (source['date_added'] - dt.datetime(1970,1,1)).dt.total_seconds()
activity['activity_date'] = pd.to_datetime(activity['activity_date'], format="%m/%d/%Y")
activity['activity_date'] = (activity['activity_date'] - dt.datetime(1970,1,1)).dt.total_seconds()

#print(source)
print('Data types changed!')


#-----PART FOUR: LOAD DATA-----

# tActivityCode
sql = """INSERT INTO tActivityCode VALUES(%s,%s);"""
try:
    for row in activitycode.values:
        curs.execute(sql,tuple(row))
    conn.commit()
    print('ActivityCode data loaded!')
except pymysql.Error:
    conn.rollback()
    print('ActivityCode data not loaded...')

# tStatusCode
sql = """INSERT INTO tStatusCode VALUES(%s,%s);"""
try:
    for row in statuscode.values:
        curs.execute(sql,tuple(row))
    conn.commit()
    print('StatusCode data loaded!')
except pymysql.Error:
    conn.rollback()
    print('StatusCode data not loaded...')

# tActorCode
sql = """INSERT INTO tActorCode VALUES(%s,%s);"""
try:
    for row in actorcode.values:
        curs.execute(sql,tuple(row))
    conn.commit()
    print('ActorCode data loaded!')
except pymysql.Error:
    conn.rollback()
    print('ActorCode data not loaded...')

# tSourceCode
sql = """INSERT INTO tSourceCode VALUES(%s,%s);"""
try:
    for row in sourcecode.values:
        curs.execute(sql,tuple(row))
    conn.commit()
    print('SourceCode data loaded!')
except pymysql.Error:
    conn.rollback()
    print('SourceCode data not loaded...')

# tSource
sql = """INSERT INTO tSource VALUES(%s,%s,%s,%s,%s,%s);"""
try:
    for row in source.values:
        curs.execute(sql,tuple(row))
    conn.commit()
    print('Source data loaded!')
except pymysql.Error:
    conn.rollback()
    print('Source data not loaded...')

# tActivity
sql = """INSERT INTO tActivity VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
try:
    for row in activity.values:
        curs.execute(sql,tuple(row))
    conn.commit()
    print('Activity data loaded!')
except pymysql.Error:
    conn.rollback()
    print('Activity data not loaded...')    
    
    
#-----PART FIVE: CLOSE-----
# disconnect from server
conn.close()
