import psycopg2  # type: ignore

from app.configs.postgres_config import config


def connect():
    """
    Connect to the Post database
    """
    # Read connection parameters
    params = config()

    # Connect to the postgres server and return
    return psycopg2.connect(**params)
