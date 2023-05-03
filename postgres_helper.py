# pylint: disable=R0913
"""
Various utilities for working with a Postgres database.
"""
import psycopg2 # type: ignore


LOCAL_HOST = "127.0.0.1"
DEFAULT_PORT = 5432


def connect(
    *,
    host: str = LOCAL_HOST,
    port: int = DEFAULT_PORT,
    database: str,
    user: str,
    password: str,
) -> psycopg2.extensions.connection:
    """
    Connect to the Postgres server
    """
    return psycopg2.connect(
        database=database, user=user, password=password, host=host, port=port
    )


def create_fill_local_table_from_csv(
    database: str,
    user: str,
    password: str,
    table_name: str,
    create_sql: str,
    csv_path: str,
):
    """
    On the local Postgres server, create a table and fill it with data from
    a CSV file.
    """
    with connect(database=database, user=user, password=password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(create_sql)
            cursor.execute(
                f"""
            COPY {table_name}
            FROM '{csv_path}'
            DELIMITER ','
            CSV HEADER;
            """
            )
