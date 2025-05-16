"""All functionality needed to load data into the database."""

# pylint: skip-file

from os import environ
import psycopg2


def get_db_connection():
    """Gets the connection to the database using .env data."""
    return psycopg2.connect(
        dbname=environ["DB_NAME"],
        user=environ["DB_USER"],
        password=environ["DB_PASSWORD"],
        host=environ["DB_HOST"],
        port=environ.get("DB_PORT", 5432)
    )


def insert_message(conn, message: dict):
    """Inserts data into database."""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO rating_interaction (rating_at, exhibition_id, rating_id, request_id)
            VALUES (%s, %s, %s, %s)
        """, (
            message.get("at"),
            message.get("site"),
            message.get("val"),
            message.get("type")
        ))
        conn.commit()
