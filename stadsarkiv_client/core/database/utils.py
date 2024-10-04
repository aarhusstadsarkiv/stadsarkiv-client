from stadsarkiv_client.core.logging import get_log
import sqlite3
import os
from contextlib import asynccontextmanager


DATABASE_URL = str(os.getenv("DATABASE_URL"))


log = get_log()


async def _get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_URL)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL;")
    return connection


@asynccontextmanager
async def transaction_scope():
    connection = await _get_db_connection()
    try:

        connection.execute("BEGIN")
        yield connection

        connection.commit()
    except sqlite3.Error as e:
        log.error(f"Transaction error: {e}")
        connection.rollback()
        raise
    finally:
        connection.close()
