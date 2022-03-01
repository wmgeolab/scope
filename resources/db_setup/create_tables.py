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
sql = """CREATE TABLE tUser (
           user_id INT PRIMARY KEY,
           first VARCHAR(30),
           last VARCHAR(30),
           username VARCHAR(30)
        );"""
curs.execute(sql)

# tQuery
sql = """CREATE TABLE tQuery (
           query_id INT PRIMARY KEY,
           name VARCHAR(150),
           user_id INT, FOREIGN KEY (user_id) REFERENCES tUser(user_id),
           keywords LONGTEXT
        );"""
curs.execute(sql)

# tSourceType
sql = """CREATE TABLE tSourceType (
           type_id INT PRIMARY KEY,
           description LONGTEXT,
           name VARCHAR(50)
        );"""
curs.execute(sql)

# tSource
sql = """CREATE TABLE tSource (
           source_id INT PRIMARY KEY,
           text LONGTEXT,
           url LONGTEXT,
           type_id INT, FOREIGN KEY (type_id) REFERENCES tSourceType(type_id),
           datetime DATETIME
        );"""
curs.execute(sql)

# tResult
sql = """CREATE TABLE tResult (
           result_id INT PRIMARY KEY,
           source_id INT, FOREIGN KEY (source_id) REFERENCES tSource(source_id)
        );"""
curs.execute(sql)

# tRun
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