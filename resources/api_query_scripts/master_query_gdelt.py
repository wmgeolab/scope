import logging
import os
import time

from mysql.connector import connect
from pydantic import BaseModel
from query_gdelt_api import GDELTQueryArgs, query_gdelt

QUERY_START_DATE = "20220915000000"
QUERY_END_DATE = "20240217000000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Configuration and data models
class DatabaseConfig(BaseModel):
    """
    Represents the configuration for connecting to a database.

    Attributes:
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        host (str): The host address for the database connection.
        database (str): The name of the database to connect to.
    """

    user: str
    password: str
    host: str
    database: str


class Keyword(BaseModel):
    """
    Represents a keyword with an ID and text.

    Attributes:
        id (int): The ID of the keyword.
        text (str): The text of the keyword.
    """

    id: int
    text: str


def fetch_and_store_queries(db_config: DatabaseConfig):
    """
    Fetch and store queries from the database.

    Args:
        db_config (DatabaseConfig): The configuration object for the database connection.

    Returns:
        None
    """
    conn = connect(**db_config.model_dump())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scopeBackend_query;")
    queries = cursor.fetchall()

    if not queries:
        logger.info("No queries found.")
        return

    for query in queries:
        process_query(conn, cursor, query)


def process_query(conn, cursor, query):
    """
    Process a query by executing it, retrieving keywords, initiating a run, querying GDELT, and storing the results.

    Args:
        conn (connection): The database connection.
        cursor (cursor): The database cursor.
        query (tuple): The query to be processed.

    Returns:
        None
    """
    # logger.info(query[0])
    cursor.execute(
        "SELECT id, word FROM scopeBackend_keyword WHERE query_id = %s;", (query[0],)
    )
    keywords = [Keyword(id=row[0], text=row[1]) for row in cursor.fetchall()]
    logger.info("Keywords: %s", keywords)

    current_run_id = initiate_run(conn, cursor, query[0])

    for keyword in keywords:
        if "," in keyword.text or len(keyword.text) <= 2:
            continue
        args = prepare_query_args(keyword.text)
        results = query_gdelt(args)
        logger.info("Found %d articles for keyword '%s'", len(results), keyword.text)
        # logger.info("Results: %s", results)
        store_articles(conn, cursor, current_run_id, results)


def initiate_run(conn, cursor, query_id) -> int:
    """
    Inserts a new entry into the 'scopeBackend_run' table with the current time and the given query ID.
    Returns the ID of the newly inserted row.

    Args:
        cursor: The database cursor object.
        query_id: The ID of the query.

    Returns:
        int: The ID of the newly inserted row.
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO scopeBackend_run (time, query_id) VALUES (%s, %s);",
        (current_time, query_id),
    )
    conn.commit()
    logger.info("New run at %s for query ID %s", current_time, query_id)
    cursor.execute(
        "SELECT id FROM scopeBackend_run WHERE time=%s AND query_id=%s;",
        (current_time, query_id),
    )
    return cursor.fetchone()[0]


def prepare_query_args(keyword: str) -> GDELTQueryArgs:
    """
    Prepares the query arguments for the GDELT API query.

    Args:
        keyword (str): The keyword to search for in the query.

    Returns:
        GDELTQueryArgs: The prepared query arguments.

    """
    return GDELTQueryArgs(
        query=keyword,
        startdatetime=QUERY_START_DATE,
        enddatetime=QUERY_END_DATE,
        maxrecords=5,
    )


def store_articles(conn, cursor, run_id, results):
    """
    Store articles in the database.

    Args:
        conn (connection): The database connection object.
        cursor (cursor): The database cursor object.
        run_id (int): The ID of the current run.
        results (dict): The results containing the articles.

    Returns:
        None
    """
    if results.get("articles"):
        for article in results["articles"]:
            source_id = insert_if_new_source(conn, cursor, article)
            if source_id:
                logger.info("Inserted new source with ID %s", source_id)
                cursor.execute(
                    "INSERT INTO scopeBackend_result (run_id, source_id) VALUES (%s, %s);",
                    (run_id, source_id),
                )
                conn.commit()


def insert_if_new_source(conn, cursor, article):
    """
    Inserts a new source into the 'scopeBackend_source' table if it doesn't already exist.

    Args:
        conn: The database connection object.
        cursor: The database cursor object.
        article: A dictionary containing the article information, including 'title', 'url', and 'sourceType_id'.

    Returns:
        The ID of the inserted source if it was inserted successfully, otherwise None.
    """
    # First, check if the source already exists in the database
    cursor.execute(
        "SELECT id FROM scopeBackend_source WHERE url = %s", (article["url"],)
    )
    result = cursor.fetchone()

    # If it exists, return None to indicate the source was already present
    if result:
        return None

    # If it does not exist, insert the new source
    cursor.execute(
        """INSERT INTO scopeBackend_source (text, url, sourceType_id)
           VALUES (%s, %s, %s)""",
        (article["title"], article["url"], article["sourceType_id"]),
    )
    conn.commit()

    # Retrieve and return the ID of the newly inserted source
    cursor.execute(
        "SELECT id FROM scopeBackend_source WHERE url = %s", (article["url"],)
    )
    new_result = cursor.fetchone()
    return new_result[0] if new_result else None


if __name__ == "__main__":
    db_config = DatabaseConfig(
        user=os.environ.get("SCOPE_USER", ""),
        password=os.environ.get("SCOPE_PASSWORD", ""),
        host=os.environ.get("SCOPE_HOST", ""),
        database=os.environ.get("SCOPE_DB", ""),
    )
    logger.info("Database configuration: %s", db_config)
    logger.info("Fetching and storing queries...")
    fetch_and_store_queries(db_config)
