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
curs.execute("DROP TABLE IF EXISTS tActivity")
curs.execute("DROP TABLE IF EXISTS tSource")
curs.execute("DROP TABLE IF EXISTS tActivityCode")
curs.execute("DROP TABLE IF EXISTS tStatusCode")
curs.execute("DROP TABLE IF EXISTS tActorCode")
curs.execute("DROP TABLE IF EXISTS tSourceCode")

print('Old tables dropped!')

# Turn foreign keys back on
#SET FOREIGN_KEY_CHECKS = 1;


#-----PART THREE: CREATE NEW TABLES-----

# tActivityCode
sql = """CREATE TABLE tActivityCode (
           activity_code VARCHAR(30) PRIMARY KEY,
           activity_desc VARCHAR(255) NOT NULL
        );"""
curs.execute(sql)

# tStatusCode
sql = """CREATE TABLE tStatusCode (
           status_code VARCHAR(10) PRIMARY KEY,
           status_desc VARCHAR(255) NOT NULL
        );"""
curs.execute(sql)

# tActorCode
sql = """CREATE TABLE tActorCode (
                actor_code VARCHAR(10) PRIMARY KEY,
                actor_desc VARCHAR(255) NOT NULL
            );"""
curs.execute(sql)

# tSourceCode
sql = """CREATE TABLE tSourceCode (
                source_code VARCHAR(10) PRIMARY KEY,
                source_desc VARCHAR(255) NOT NULL
            );"""
curs.execute(sql)

# tSource
sql = """CREATE TABLE tSource (
                source_id INT PRIMARY KEY,
                source_code VARCHAR(10), FOREIGN KEY (source_code) REFERENCES tSourceCode(source_code),
                source_text LONGTEXT,
                source_date INT(20),
                date_added INT(20),
                source_url VARCHAR(400) NOT NULL
            );"""
curs.execute(sql)

# tActivity
sql = """CREATE TABLE tActivity (
                activity_id INT PRIMARY KEY,
                actor_code VARCHAR(10), FOREIGN KEY (actor_code) REFERENCES tActorCode(actor_code),
                activity_code VARCHAR(30), FOREIGN KEY (activity_code) REFERENCES tActivityCode(activity_code),
                activity_date INT(20),
                fuzzy_date INT(20),
                status_code VARCHAR(10), FOREIGN KEY (status_code) REFERENCES tStatusCode(status_code),
                notes VARCHAR(10000),
                lat NUMERIC(11,8),
                lon NUMERIC(11,8),
                geom TEXT,
                source_id INT, FOREIGN KEY (source_id) REFERENCES tSource(source_id)
            );"""
curs.execute(sql)

print('New tables made!')


#-----PART THREE: CLOSE-----
# disconnect from server
conn.close()