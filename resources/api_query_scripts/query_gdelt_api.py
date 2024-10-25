# This program takes in arugments as keywords, the length of time they want to
# query their data from, and how many articles they want returned (further expansion
# for parameters possible.) It then returns a json of all articles found.

# Here are some examples of the url based queries
# https://api.gdeltproject.org/api/v2/doc/doc?format=html&timespan=2Y&query=ecuador&mode=artlist&maxrecords=250&format=json&sort=hybridrel
# https://api.gdeltproject.org/api/v2/summary/summary?d=web&t=summary
# https://api.gdeltproject.org/api/v2/doc/doc?format=html&startdatetime=20170103000000&enddatetime=20181011235959&query=ecuador%20china&mode=artlist&maxrecords=75&format=json&sort=hybridrel

import logging
from datetime import datetime

from gdeltdoc import Filters, GdeltDoc
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GDELTQueryArgs(BaseModel):
    """
    Represents the arguments for querying the GDELT API.

    Attributes:
        query (str): The query string.
        startdatetime (str): The start date and time for the query.
        enddatetime (str): The end date and time for the query.
        maxrecords (int): The maximum number of records to retrieve.
    """

    query: str
    startdatetime: str
    enddatetime: str
    maxrecords: int


def format_datetime(dt_str: str) -> str:
    """
    Format a datetime string from 'YYYYMMDDHHMMSS' to 'YYYY-MM-DD'.

    Args:
        dt_str (str): The datetime string in the format 'YYYYMMDDHHMMSS'.

    Returns:
        str: The formatted datetime string in the format 'YYYY-MM-DD'.
    """
    return datetime.strptime(dt_str, "%Y%m%d%H%M%S").strftime("%Y-%m-%d")


def query_gdelt(args: GDELTQueryArgs):
    """
    Query GDELT using validated and formatted arguments from a Pydantic model.

    Args:
        args (GDELTQueryArgs): The validated and formatted arguments from a Pydantic model.

    Returns:
        List[Article]: A list of articles retrieved from the GDELT API.
    """
    args.startdatetime = format_datetime(args.startdatetime)
    args.enddatetime = format_datetime(args.enddatetime)

    logger.info(
        f"Querying from {args.startdatetime} to {args.enddatetime} with keyword '{args.query}'"
    )

    filters = Filters(
        keyword=args.query.strip(),
        start_date=args.startdatetime,
        end_date=args.enddatetime,
    )
    gdelt = GdeltDoc()
    articles = gdelt.article_search(filters)
    return articles


if __name__ == "__main__":
    # Example usage
    test_args = GDELTQueryArgs(
        query="palestine",
        startdatetime="20210615000000",
        enddatetime="20240325000000",
        maxrecords=10,
    )
    print(query_gdelt(test_args))
