import os

import psycopg2  # type: ignore


def connect():
    """
    Connect to the Post database
    """
    # Connect to the postgres server and return
    return psycopg2.connect(os.environ["DATABASE_URL"])
