import mysql.connector
import csv

# Connect to the database
cnx = mysql.connector.connect(
    host="mysql.scopedata.org",
    user="scopesql",
    password="!vrQeSisAJ4f8jt",
    database="scopesql",
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Define the SQL query to fetch the id and text columns from the scopeBackend_source table
query = "SELECT id, text, url, sourceType_id FROM scopeBackend_source"

# Execute the SQL query and fetch the results
cursor.execute(query)
results = cursor.fetchall()

with open("./scopesql.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "text", "url", "sourceType_id"])

    for row in results:
        writer.writerow(row)

# Loop through the results and print the id and text columns
# for row in results:
#     print("id = ", row[0])
#     print("text = ", row[1])

# Close the cursor and database connections
cursor.close()
cnx.close()
