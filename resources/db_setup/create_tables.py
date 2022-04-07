#-----PART ONE: PACKAGES AND CONNECTION SET-UP-----

# Load packages
import pymysql
import pandas as pd

# Open database connection (host, username, password, database_name)
conn = pymysql.connect(host="mysql.scopedata.org", user="scopesql",
                     password="fY7Ukl52UI", db="scopesql")

# prepare a cursor object using cursor() method
curs = conn.cursor()

print('Connection opened!')


#-----PART TWO: DROP OLD TABLES-----

# Turn foreign keys off momentarily to delete
#SET FOREIGN_KEY_CHECKS = 0;

# Drop tables if they already exist using execute() method.
curs.execute("DROP TABLE IF EXISTS tRun")
curs.execute("DROP TABLE IF EXISTS tResult")
curs.execute("DROP TABLE IF EXISTS tSource")
curs.execute("DROP TABLE IF EXISTS tSourceType")
curs.execute("DROP TABLE IF EXISTS tQuery")
curs.execute("DROP TABLE IF EXISTS tUser")

print('Old tables dropped!')

# Turn foreign keys back on
#SET FOREIGN_KEY_CHECKS = 1;


#-----PART THREE: CREATE NEW TABLES-----

# tUser
# table that saves the information of the user
sql = """CREATE TABLE tUser (
           user_id INT PRIMARY KEY,
           first VARCHAR(30),
           last VARCHAR(30),
           username VARCHAR(30)
        );"""
curs.execute(sql)

# tQuery
# table that saves information about each query
sql = """CREATE TABLE tQuery (
           query_id INT PRIMARY KEY,
           name VARCHAR(150),
           user_id INT, FOREIGN KEY (user_id) REFERENCES tUser(user_id),
           keywords LONGTEXT
        );"""
curs.execute(sql)

# tSourceType
# table that has information about each source type i.e. GDELT, Twitter, etc.
sql = """CREATE TABLE tSourceType (
           type_id INT PRIMARY KEY,
           description LONGTEXT,
           name VARCHAR(50)
        );"""
curs.execute(sql)

# tSource
# table that has information about each source
sql = """CREATE TABLE tSource (
           source_id INT PRIMARY KEY,
           text LONGTEXT,
           url LONGTEXT,
           type_id INT, FOREIGN KEY (type_id) REFERENCES tSourceType(type_id),
           datetime DATETIME
        );"""
curs.execute(sql)

# tResult
# table that has infomation about which sources should be returned when the user calls the result for the query
sql = """CREATE TABLE tResult (
           result_id INT PRIMARY KEY,
           source_id INT, FOREIGN KEY (source_id) REFERENCES tSource(source_id)
        );"""
curs.execute(sql)

# tRun
# table that has information about each run for the query i.e. information pull from GDELT, Twitter
sql = """CREATE TABLE tRun (
           run_id INT PRIMARY KEY,
           result_id INT, FOREIGN KEY (result_id) REFERENCES tResult(result_id),
           query_id INT, FOREIGN KEY (query_id) REFERENCES tQuery(query_id),
           datetime DATETIME
        );"""
curs.execute(sql)

print('New tables made!')


#-----PART THREE: CLOSE-----
# disconnect from server
conn.close()